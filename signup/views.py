from django.contrib.auth import login
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from .forms import OwnerSignupForm


def signup_page_owner(request):
    """Owner registration page"""
    if 'username' in request.POST:
        form = OwnerSignupForm(request.POST)
        if form.is_valid():
            # Create a new owner and redirect to the management area
            new_owner = form.save()
            login(request, new_owner.user)
            return HttpResponseRedirect(reverse('management:management_panel'))
    else:
        form = OwnerSignupForm()

    return render(request, 'signup/signup_owner.html', {'form': form})