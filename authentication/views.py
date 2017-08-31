from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


# Login user
def login_action(request):
    if 'username' in request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Login successful
                print('Success')
                login(request, user)
                return HttpResponseRedirect(reverse('management:management_panel'))
            else:
                print('Error authenticating')
        else:
            print('Invalid form')
    else:
        form = AuthenticationForm()

    return render(request, 'authentication/login_page.html', {'form': form})


# Logout user
@login_required(login_url='/login')
def logout_action(request):
    logout(request)
    return HttpResponseRedirect(reverse('authentication:login'))
