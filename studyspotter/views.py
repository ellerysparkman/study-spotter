'''
*  REFERENCES
*  Title: Django: Displaying MySQL table records
*  URL: https://www.plus2net.com/python/dj-mysql-display.php

*  Title: Redirecting @user_passes_test(lambda u: u.is_superuser) if not a superuser to another page
*  URL: https://stackoverflow.com/questions/21649439/redirecting-user-passes-testlambda-u-u-is-superuser-if-not-a-superuser-to-an

*  Title: Redirect after login with Django
*  URL: https://stackoverflow.com/questions/60216420/redirect-after-login-with-django
'''

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .models import StudySpot, Favorite
#from .models import StudySpot
from django.contrib.auth import logout, login, authenticate

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import get_object_or_404

def hello_world(request):
  return HttpResponse("Hello, Person-Trying-To-Log-In!")


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return HttpResponseRedirect('/map/')
        else:
            return render(request, 'register.html', {'form': form})

class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('study-spotter:map')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

def logout_user(request):
    logout(request)
    return redirect('study-spotter:index')

def home_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/map")
    else:
        #author = request.user.username
        pending = StudySpot.objects.filter(status='pending').count()
        #markers = StudySpot.objects.filter(author=author)
        return render(request, 'index.html', {"pending": pending})

def getting_started(request):
    #author = request.user.username
    pending = StudySpot.objects.filter(status='pending').count()
    #markers = StudySpot.objects.filter(author=author)
    return render(request, 'index.html', {"pending": pending})

def map(request):
    pending = StudySpot.objects.filter(status='pending').count()
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        name = request.POST.get('name')
        description = request.POST.get('loc-description')
        food = request.POST.get('food')
        author = request.user

        # Save the marker data to the database
        marker = StudySpot(latitude=latitude, longitude=longitude, name=name, description=description, food=(food == "on" or food=="True"), author=author)
        # print(marker.food, food)
        marker.save()
        return HttpResponseRedirect('/map/')

    # if admin, map should show all points
    author = request.user
    if author.is_staff:
        markers = StudySpot.objects.filter(status='approved') | StudySpot.objects.filter(status='pending')
    # if normal user, map should show one's own pins & all approved pins
    else:
        markers = StudySpot.objects.filter(status='approved') | StudySpot.objects.filter(status='pending').filter(author=author)
    for marker in markers:
        marker.faved = Favorite.objects.filter(user=author, pin=marker).count() > 0
        marker.save()
    return render(request, 'map.html', {"markers":markers, "author":author, "pending":pending})


 # ADMIN APPROVAL
@user_passes_test(lambda u: u.is_staff)
def approve_pin(request, id):
    for pin in StudySpot.objects.filter(id=id):
        pin.status = 'approved'
        pin.save()    
    return redirect('study-spotter:pendinglocations')

# ADMIN REJECTION
@user_passes_test(lambda u: u.is_staff)
def reject_pin(request, id, rejection_reason):
    for pin in StudySpot.objects.filter(id=id):
        pin.status = 'rejected'
        pin.rejection_reason = rejection_reason
        pin.save()
    return redirect('study-spotter:pendinglocations')

# def goToPin(request, name):
#     for pin in StudySpot.objects.filter(name=name):
#         lat = pin.latitude
#         long = pin.longitude
#     return HttpResponse('/map/')


#deletes by name for now, can be changed later
def deletePin(request, name):
    print(name)
    for pin in StudySpot.objects.filter(name=name):
        pin.delete()
    return HttpResponse(status=200)

def modifyPin(request, name):
    text = request.POST.get('loc-description')
    newName = request.POST.get('name')
    food = request.POST.get('food')
    for pin in StudySpot.objects.filter(name=name):
        pin.name = newName
        pin.description = text
        pin.food = (food == "on")
        pin.save()
    return HttpResponseRedirect('/map/')

@login_required(redirect_field_name=None)
def mystudyspots(request): # only show logged in user's markers
    author = request.user.username
    pending = StudySpot.objects.filter(status='pending').count()
    markers = StudySpot.objects.filter(author=author)
    faves = []
    for marker in StudySpot.objects.all():
        if Favorite.objects.filter(user=author, pin=marker).count() > 0:
            faves += [marker]
    return render(request, 'mystudyspots.html', {'markers': markers, 'author': author, "pending": pending, "faves": faves})

@login_required(redirect_field_name=None)
def pendinglocations(request):
    author = request.user
    pending = StudySpot.objects.filter(status='pending').count()
    if author.is_staff:
        markers = StudySpot.objects.all()
    else:
        markers = StudySpot.objects.none()
    print(len(markers))
    return render(request, 'pendinglocations.html', {"markers": markers, "author": author, "pending": pending})

@login_required(redirect_field_name=None)
def fav_pin(request, id):
    pin = get_object_or_404(StudySpot, id=id)
    uname = request.user.username
    if Favorite.objects.filter(pin=pin, user=uname).count():
        return HttpResponseBadRequest()
    Favorite.objects.create(pin=pin, user=uname)
    return HttpResponse(200)


@login_required(redirect_field_name=None)
def unfav_pin(request, id):
    pin = get_object_or_404(StudySpot, id=id)
    uname = request.user.username
    if not Favorite.objects.filter(pin=pin, user=uname).count():
        return HttpResponseBadRequest()
    Favorite.objects.filter(pin=pin, user=uname).first().delete()
    return HttpResponse(200)
