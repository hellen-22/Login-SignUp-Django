from django.urls import path
from . import views

from .views import *

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('', views.users, name='users'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

]