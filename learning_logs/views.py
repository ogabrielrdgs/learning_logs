from typing import Any, Dict
from django.http import Http404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from . import models, forms


class TopicListView(LoginRequiredMixin, ListView):
    model = models.Topic
    template_name = "topics.html"
    context_object_name = "topics"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("q", "")
        if search:
            return models.Topic.objects.filter(
                owner=self.request.user, title__istartswith=search
            )
        else:
            return models.Topic.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("q", "")
        context["search_form"] = forms.SearchForm(
            initial={"q": context["search"]}, placeholder="Buscar tópico..."
        )
        return context


class TopicDetailView(LoginRequiredMixin, ListView):
    model = models.Entry
    template_name = "topic.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("q", "")
        if search:
            return models.Entry.objects.filter(
                topic__pk=self.kwargs["pk"],
                topic__owner=self.request.user,
                content__icontains=search,
            )
        return models.Entry.objects.filter(
            topic__pk=self.kwargs["pk"], topic__owner=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic"] = get_object_or_404(
            models.Topic, pk=self.kwargs["pk"], owner=self.request.user
        )
        context["search"] = self.request.GET.get("q", "")
        context["search_form"] = forms.SearchForm(
            initial={"q": context["search"]}, placeholder="Buscar registro..."
        )
        return context


class TopicCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = "form.html"
    form_class = forms.TopicForm
    success_message = "Tópico criado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Criar novo tópico"
        context["btn_value"] = "Criar"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        new_topic = form.save(commit=False)
        new_topic.owner = self.request.user
        new_topic.save()
        self.success_url = new_topic.get_url()
        return super().form_valid(form)


class TopicUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    form_class = forms.TopicForm
    success_message = "Tópico atualizado com sucesso!"

    def get_queryset(self):
        return models.Topic.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Atualizar tópico "{self.get_object().get_title()}"'
        context["btn_value"] = "Salvar"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["pk"] = self.kwargs["pk"]
        return kwargs

    def get_success_url(self):
        return reverse_lazy("topic", kwargs={"pk": self.kwargs["pk"]})


class TopicDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    success_message = "Tópico excluído com sucesso!"
    success_url = reverse_lazy("topics")

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_queryset(self):
        return models.Topic.objects.filter(owner=self.request.user)
