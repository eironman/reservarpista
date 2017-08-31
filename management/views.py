from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from django.views import View
from .forms import SportsCenterForm, CourtForm
from core.models import SportsCenter, Court


class LoginRequiredView(LoginRequiredMixin, View):
    """Base class used to force logged users"""
    login_url = '/authentication/login/'


class ManagementPanel(LoginRequiredView):
    """Homepage for management"""
    def get(self, request):
        sports_centers = SportsCenter.objects.filter(owner=request.user.owner)
        return render(request, 'management/management_panel.html', {'sports_centers': sports_centers})


class AddSportsCenter(LoginRequiredView):
    """Creates a new sports center"""
    template_name = 'management/add_sports_center.html'

    def get(self, request):
        form = SportsCenterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SportsCenterForm(request.POST)
        if form.is_valid():
            # Set the logged user as the owner
            sports_center = form.save(commit=False)
            sports_center.owner = request.user.owner
            sports_center.save()
            return HttpResponseRedirect(reverse('management:edit_sports_center', args=[sports_center.id]))

        return render(request, self.template_name, {'form': form})


class EditSportsCenter(LoginRequiredView):
    """Creates a new sports center"""
    template_name = 'management/edit_sports_center.html'

    def dispatch(self, request, *args, **kwargs):
        self.sports_center = get_object_or_404(SportsCenter, id=kwargs['center_id'])
        self.context = {
            'center_id' : kwargs['center_id'],
            'courts': Court.objects.filter(sports_center=self.sports_center.id)
        }
        return super(EditSportsCenter, self).dispatch(request)

    def get(self, request):
        form = SportsCenterForm(instance=self.sports_center)
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = SportsCenterForm(request.POST, instance=self.sports_center)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('management:management_panel'))

        self.context['form'] = form
        return render(request, self.template_name, self.context)


class DeleteSportsCenter(LoginRequiredView):
    """Deletes a new sports center"""
    def get(self, request, center_id):
        sports_center = get_object_or_404(SportsCenter, id=center_id)
        sports_center.delete()
        return HttpResponseRedirect(reverse('management:management_panel'))


class AddCourt(LoginRequiredView):
    """Creates a new court"""
    template_name = 'management/add_court.html'

    def get(self, request, center_id):
        form = CourtForm()
        return render(request, self.template_name, {'form': form, 'center_id': center_id})

    def post(self, request, center_id):
        sports_center = get_object_or_404(SportsCenter, id=center_id)
        form = CourtForm(request.POST)
        if form.is_valid():
            court = form.save(commit=False)
            court.sports_center = sports_center
            court.save()
            return HttpResponseRedirect(reverse('management:edit_sports_center', args=[center_id]))

        return render(request, self.template_name, {'form': form})


class EditCourt(LoginRequiredView):
    """Edits a court"""
    template_name = 'management/edit_court.html'

    def dispatch(self, request, *args, **kwargs):
        self.court = get_object_or_404(Court, id=kwargs['court_id'])
        self.context = {
            'court_id' : kwargs['court_id'],
            'center_id' : self.court.sports_center.id
        }
        return super(EditCourt, self).dispatch(request)

    def get(self, request):
        form = CourtForm(instance=self.court)
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = CourtForm(request.POST, instance=self.court)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('management:edit_sports_center', args=[self.court.sports_center.id]))

        self.context['form'] = form
        return render(request, self.template_name, self.context)


class DeleteCourt(LoginRequiredView):
    """Deletes a court"""
    def get(self, request, court_id):
        court = get_object_or_404(Court, id=court_id)
        sports_center_id = court.sports_center.id
        court.delete()
        return HttpResponseRedirect(reverse('management:edit_sports_center', args=[sports_center_id]))






















