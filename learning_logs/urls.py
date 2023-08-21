from django.urls import path

from . import views

urlpatterns = [
    path("meus_topicos/", views.TopicListView.as_view(), name="topics"),
    path("meus_topicos/<int:pk>/", views.TopicDetailView.as_view(), name="topic"),
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
]
