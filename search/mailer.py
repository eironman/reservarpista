from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from smtplib import SMTPException
from core.models import SportsCenter

"""<QueryDict: {'sport': ['Pádel'], 'duration': ['60 minutos'], 'phone': ['9393939'], 'email': ['ashleyriot@hotmail.com'], 
'userName': ['Aaron'], 'location': ['Palma'], 'sportsCenterId': ['74'], 'time': ['Cualquiera']}>
"""


class SearchMailer:
    """Sends the email for the booking request"""

    sports_center = None
    location = None
    user_name = None
    user_phone = None
    user_email = None
    sport = None
    date = None
    time = None
    duration = None
    msg_plain = None
    msg_html = None
    email_to = None
    subject = None
    email_bcc = None

    def __init__(self, request):
        self.sports_center = SportsCenter.objects.get(id=request.POST['sportsCenterId'], active=True)
        self.user_name = request.POST['userName']
        self.location = request.POST['location']
        self.user_phone = request.POST['phone']
        self.user_email = request.POST['email']
        self.sport = request.POST['sport']
        self.date = request.POST['date']
        self.time = request.POST['time']
        self.duration = request.POST['duration']

    def send_request(self):
        """Builds the emails for the sports center, the user and reservarpista"""

        email_data = {
            'sports_center_name': self.sports_center.name,
            'sports_center_phone': self.sports_center.phone,
            'name': self.user_name,
            'sport': self.sport,
            'date': self.date,
            'time': self.time,
            'duration': self.duration,
            'email': self.user_email,
            'phone': self.user_phone,
        }
        self.msg_plain = render_to_string('email/booking_request_center.txt', email_data)
        self.msg_html = render_to_string('email/booking_request_center.html', email_data)
        self.subject = 'Solicitud de Reserva'

        emails_sent = True

        # Email to sports center
        if settings.DEBUG:
            self.email_to = 'aaron_amengual@hotmail.com'
        else:
            self.email_to = self.sports_center.email
        if not self.__send_email():
            emails_sent = False

        # Email to reservar pista
        # self.email_to = settings.DEFAULT_FROM_EMAIL
        self.email_to = 'aaron.amengual@gmail.com'
        if not self.__send_email():
            emails_sent = False

        # Email to user
        if not self.user_email == '':
            self.msg_plain = render_to_string('email/booking_request_user.txt', email_data)
            self.msg_html = render_to_string('email/booking_request_user.html', email_data)
            self.email_to = self.user_email
            if not self.__send_email():
                emails_sent = False

        return emails_sent

    def __send_email(self):
        """Sends the actual email"""

        email = EmailMultiAlternatives(
            self.subject,
            self.msg_plain,
            'Reservar Pista <' + settings.DEFAULT_FROM_EMAIL + '>',
            [self.email_to]
        )

        if self.email_bcc:
            email.bcc = self.email_bcc

        if self.msg_html:
            email.attach_alternative(self.msg_html, 'text/html')

        try:
            emails_sent = email.send()
        except SMTPException as e:
            # TODO Log exceptions
            return False

        if emails_sent == 1:
            return True
        else:
            return False





































