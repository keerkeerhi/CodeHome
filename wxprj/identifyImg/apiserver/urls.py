from django.urls import path
from apiserver.userModule import loginfun, login_ses, saveUser, login_out
from apiserver.imgModule import upload_img, result_list

urlpatterns = [
    path("login/", loginfun),
    path("login_ses/", login_ses),
    path("upload/", upload_img),
    path("saveUser/", saveUser),
    path("login_out/",login_out),
    path("result_list/",result_list)
]
