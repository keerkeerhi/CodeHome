from django.urls import path
from apiserver.userModule import login
from apiserver.imgModule import upload_img

urlpatterns = [
    path("login/",login),
    path("upload_img/",upload_img)
]