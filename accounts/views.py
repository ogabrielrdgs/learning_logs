from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import Http404

from . import forms

login = LoginView.as_view(
    template_name="form.html",
    redirect_authenticated_user=True,
    extra_context={
        "title": "Entre na sua conta",
        "btn_value": "Entrar",
    },
)

logout = LogoutView.as_view()


class SignupView(SuccessMessageMixin, CreateView):
    template_name = "form.html"
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy("login")
    success_message = "Conta criada com sucesso!"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crie uma conta"
        context["btn_value"] = "Confirmar"
        return context
