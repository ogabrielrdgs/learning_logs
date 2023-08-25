from django.db import models, transaction
from django.http import Http404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


class PublicTopicListView(ListView):
    model = models.Topic
    template_name = "topics.html"
    context_object_name = "topics"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("q", "")
        if search:
            return models.Topic.objects.filter(public=True, title__istartswith=search)
        else:
            return models.Topic.objects.filter(public=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["public"] = True
        context["search"] = self.request.GET.get("q", "")
        context["search_form"] = forms.SearchForm(
            initial={"q": context["search"]}, placeholder="Buscar tópico..."
        )
        return context


class PublicTopicDetailView(ListView):
    model = models.Entry
    template_name = "topic.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("q", "")
        if search:
            return models.Entry.objects.filter(
                topic__pk=self.kwargs["pk"],
                topic__public=True,
                content__icontains=search,
            )
        return models.Entry.objects.filter(
            topic__pk=self.kwargs["pk"], topic__public=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["public"] = True
        context["topic"] = get_object_or_404(
            models.Topic, pk=self.kwargs["pk"], public=True
        )
        context["search"] = self.request.GET.get("q", "")
        context["search_form"] = forms.SearchForm(
            initial={"q": context["search"]}, placeholder="Buscar registro..."
        )
        return context


@login_required()
def copy_topic(request, pk):
    if request.method != "POST":
        raise Http404

    topic = get_object_or_404(models.Topic, pk=pk, public=True)

    if models.Topic.objects.filter(title=topic.title, owner=request.user).exists():
        messages.error(request, "Você já possui um tópico com esse título!")
    else:
        try:
            with transaction.atomic():
                topic.pk = None
                topic.owner = request.user
                topic.public = False
                topic.save()

                for entry in models.Entry.objects.filter(topic__pk=pk).order_by(
                    "date_added"
                ):
                    entry.pk = None
                    entry.topic = topic
                    entry.save()

                messages.success(request, "Tópico copiado com sucesso!")
        except Exception:
            messages.error(request, "Ocorreu um erro ao copiar o tópico!")

    return redirect("public_topic", pk=pk)


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


class EntryCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = "form.html"
    form_class = forms.EntryForm
    success_message = "Registro criado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Criar novo registro"
        context["btn_value"] = "Criar"
        return context

    def form_valid(self, form):
        topic = get_object_or_404(
            models.Topic, pk=self.kwargs["pk"], owner=self.request.user
        )
        new_entry = form.save(commit=False)
        new_entry.topic = topic
        new_entry.save()
        self.success_url = topic.get_url()
        return super().form_valid(form)


class EntryUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    form_class = forms.EntryForm
    success_message = "Registro atualizado com sucesso!"

    def get_queryset(self):
        return models.Entry.objects.filter(topic__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Atualizar registro"
        context["btn_value"] = "Salvar"
        return context

    def form_valid(self, form):
        entry = form.save()
        self.success_url = entry.topic.get_url()
        return super().form_valid(form)


class EntryDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    success_message = "Registro excluído com sucesso!"

    def get(self, request, *args, **kwargs):
        raise Http404

    def get_queryset(self):
        return models.Entry.objects.filter(topic__owner=self.request.user)

    def form_valid(self, form):
        self.success_url = self.get_object().topic.get_url()
        return super().form_valid(form)
