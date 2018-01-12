
from django.conf.urls import url

from public_interfaces import views

app_name = 'public_interfaces'

urlpatterns = [
    # If the url is equal to "" then call views.home.
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/?$', views.LoginView.as_view(), name="login"),
    url(r'^logout/?$', views.LogoutView.as_view(), name="logout"),
    url(r'^register/?$', views.RegistrationView.as_view(), name="register"),
]
