from django.urls import path
from apiserver.userModule import login

urlpatterns = [
    path("login/",login)
]