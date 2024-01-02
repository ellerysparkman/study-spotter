from django.urls import path
from django.contrib.auth.views import LogoutView
from .import views
from .views import MyLoginView

app_name = "study-spotter"

urlpatterns = [
    path('', views.home_page, name='index'),
    path('map/', views.map, name='map'),
    path('getting-started/', views.getting_started, name='getting_started'),
    path('delete/<str:name>/', views.deletePin, name='deletePin'),
    path('modify/<str:name>/', views.modifyPin, name='modifyPin'),
    path('mystudyspots/', views.mystudyspots, name='mystudyspots'),
    path('pendinglocations/', views.pendinglocations, name='pendinglocations'),
    #path('logout', LogoutView.as_view()),
    path('approve_pin/<int:id>/', views.approve_pin, name='approvePin'),
    path('reject_pin/<int:id>/<str:rejection_reason>/', views.reject_pin, name='rejectPin'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', MyLoginView.as_view(),name='login'),
    path('register/', views.sign_up, name='register'),
    path('fav/<int:id>/', views.fav_pin, name='fav'),
    path('unfav/<int:id>/', views.unfav_pin, name='unfav'),
    # path('goto/<str:name>/', views.goToPin, name='goToPin'),
]