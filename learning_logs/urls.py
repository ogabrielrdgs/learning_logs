from django.urls import path

from . import views

urlpatterns = [
    path("meus_topicos/", views.TopicListView.as_view(), name="topics"),
    path("meus_topicos/<int:pk>/", views.TopicDetailView.as_view(), name="topic"),
    path(
        "topicos_publicos/", views.PublicTopicListView.as_view(), name="public_topics"
    ),
    path(
        "topicos_publicos/<int:pk>/",
        views.PublicTopicDetailView.as_view(),
        name="public_topic",
    ),
    path("meus_topicos/novo/", views.TopicCreateView.as_view(), name="new_topic"),
    path(
        "meus_topicos/<int:pk>/atualizar/",
        views.TopicUpdateView.as_view(),
        name="update_topic",
    ),
    path(
        "meus_topicos/<int:pk>/excluir/",
        views.TopicDeleteView.as_view(),
        name="delete_topic",
    ),
    path(
        "meus_topicos/<int:pk>/novo_registro/",
        views.EntryCreateView.as_view(),
        name="new_entry",
    ),
    path(
        "meus_topicos/atualizar_registro/<int:pk>/",
        views.EntryUpdateView.as_view(),
        name="update_entry",
    ),
    path(
        "meus_topicos/excluir_registro/<int:pk>/",
        views.EntryDeleteView.as_view(),
        name="delete_entry",
    ),
]
