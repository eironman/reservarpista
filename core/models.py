import os
from PIL import Image
from datetime import date, datetime, time, timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def get_thumbnail_path(original_image_full_path, suffix):
    """Returns the path to a thumbnail"""

    original_image_path = os.path.split(original_image_full_path)[0] + '/'
    original_image_full_name = os.path.split(original_image_full_path)[1]

    # split in an array in case image name has several dots
    image_name_split_array = original_image_full_name.split('.')

    # extension
    original_image_extension = image_name_split_array[len(image_name_split_array) - 1]

    # name
    original_image_name = "_".join(image_name_split_array[0:len(image_name_split_array) - 1])

    return original_image_path + original_image_name + suffix + '.' + original_image_extension


def create_thumbnail(original_image_full_path, size, suffix):
    """Creates a resized version of an image"""

    # Get original image
    original_image = Image.open(original_image_full_path)

    # Create a copy
    image_copy = original_image.copy()

    # Resize
    image_copy.thumbnail(size, Image.ANTIALIAS)

    # Save
    image_copy.save(get_thumbnail_path(original_image_full_path, suffix))

    return


class Owner(models.Model):
    """Owner of a sports center"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class Location(models.Model):
    """Locations of Sports Centers"""
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Sport(models.Model):
    """Sports to book"""
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SportsCenterManager(models.Manager):
    """Custom manager for sports centers"""
    def get_active(self):
        """Returns all active centers"""
        return self.filter(active=True)

    def search(self, filter_values):
        """Makes the main filtering"""

        # Location and sport are always present
        location = Location.objects.get(slug=filter_values['location'])
        sport = Sport.objects.get(slug=filter_values['sport'])

        # Get centers ids with the sport selected by the user
        sports_centers_sport_ids =\
            SportsCenterSport.objects.filter(sport_id=sport.id).values_list('center_id', flat=True)

        # Get active sports centers by sport and location
        sports_centers = self.filter(active=True, pk__in=sports_centers_sport_ids, location=location.id)

        # TODO Filter sports centers by time and duration even if there is no date
        if 'date' in filter_values:
            # Check if the sports center is opened in that date
            date_object = datetime.strptime(filter_values['date'], '%Y/%m/%d')
            weekday_name = date_object.strftime('%a').lower()
            weekday_filter = 'opening_time_' + weekday_name
            sports_centers = sports_centers.exclude(**{weekday_filter: '00:00:00'})

            # Filter sports centers by time and duration
            if not filter_values['time'] == '00:00':
                # Calculate finishing time
                time_list = filter_values['time'].split(':')
                dt = datetime.combine(
                    date.today(), time(int(time_list[0]), int(time_list[1]))
                ) + timedelta(minutes=int(filter_values['duration']))
                finishing_time = dt.strftime('%H:%M:%S')
                # TODO Contemplate the case where a user wants to play past the midnight
                if finishing_time == "00:00:00" or finishing_time == "00:30:00" or finishing_time == "01:00:00":
                    finishing_time = "23:59:00"

                time_filter = {
                    'opening_time_' + weekday_name + '__lte': filter_values['time'],
                    'closing_time_' + weekday_name + '__gte': finishing_time,
                }
                sports_centers = sports_centers.filter(**time_filter)

        return sports_centers


class SportsCenter(models.Model):
    """Sports centers"""
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=40, default=None, blank=True)
    website = models.CharField(max_length=200, default=None, blank=True)
    description = models.TextField(max_length=1000, default=None, blank=True)
    private_info = models.TextField(max_length=1000, default=None, blank=True)
    municipal = models.BooleanField(default=False)
    locker_room = models.BooleanField(default=False)
    lockers = models.BooleanField(default=False)
    shower = models.BooleanField(default=False)
    bar = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    equipment_rental = models.BooleanField(default=False)
    opening_time_mon = models.TimeField(default='00:00:00', blank=True)
    closing_time_mon = models.TimeField(default='00:00:00', blank=True)
    opening_time_tue = models.TimeField(default='00:00:00', blank=True)
    closing_time_tue = models.TimeField(default='00:00:00', blank=True)
    opening_time_wed = models.TimeField(default='00:00:00', blank=True)
    closing_time_wed = models.TimeField(default='00:00:00', blank=True)
    opening_time_thu = models.TimeField(default='00:00:00', blank=True)
    closing_time_thu = models.TimeField(default='00:00:00', blank=True)
    opening_time_fri = models.TimeField(default='00:00:00', blank=True)
    closing_time_fri = models.TimeField(default='00:00:00', blank=True)
    opening_time_sat = models.TimeField(default='00:00:00', blank=True)
    closing_time_sat = models.TimeField(default='00:00:00', blank=True)
    opening_time_sun = models.TimeField(default='00:00:00', blank=True)
    closing_time_sun = models.TimeField(default='00:00:00', blank=True)
    creation_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    objects = SportsCenterManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-creation_date',)


class SportsCenterMedia(models.Model):
    """Media (images, videos) for sports centers"""
    sports_center = models.ForeignKey(SportsCenter, on_delete=models.CASCADE)
    url = models.ImageField(upload_to='sports_centers_images/', blank=True, null=True)
    order = models.PositiveSmallIntegerField(blank=True, null=True)

    def save(self):
        """Overwrite save method to resize image"""
        super(SportsCenterMedia, self).save()
        if self.url:
            create_thumbnail(self.url.path, (500, 258), '_thumb')

    def thumb_url(self):
        return get_thumbnail_path(self.url.url, '_thumb')

    class Meta:
        ordering = ('order',)


class SportsCenterSport(models.Model):
    """Sports in the sports center"""
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    center = models.ForeignKey(SportsCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.center.name + ' - ' + self.sport.name


class Surface(models.Model):
    """Court surface type"""
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Court(models.Model):
    """Courts in the sports center"""
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    sports_center = models.ForeignKey(SportsCenter, on_delete=models.CASCADE)
    surface = models.ForeignKey(Surface, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    hourly_price = models.FloatField()
    lights_price = models.FloatField()
    half_hour_bookings = models.BooleanField(default=False)


class BlockedDate(models.Model):
    """Dates when a court is not available"""
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    day = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()


class Booking(models.Model):
    """Booking to play a sport"""
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    day = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    price = models.FloatField()
    reference_code = models.CharField(max_length=10)
    customer = models.CharField(max_length=100)
    creation_date = models.DateTimeField(default=timezone.now)

























































