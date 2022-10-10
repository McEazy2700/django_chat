from django.urls import path
from .views import login, logout, sign_up


urlpatterns = [
    path("login/", login, name="login"),
    path("logout/<int:id>/", logout, name="logout"),
    path('sign-up/', sign_up, name="sign_up"),
]
