from django.urls import path
from . import views
urlpatterns=[
    path('register', views.register, name='user_register'),
    path('',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout')
]