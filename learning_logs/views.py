from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

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
    paginate_by = 1

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
