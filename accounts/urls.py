from django.urls import path

from . import views

urlpatterns = [
    path("criar_conta/", views.SignupView.as_view(), name="signup"),
    path("entrar/", views.login, name="login"),
    path("sair/", views.logout, name="logout"),
]
