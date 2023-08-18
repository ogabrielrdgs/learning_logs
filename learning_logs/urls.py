from django.urls import path

from . import views

urlpatterns = [
    path("meus_topicos/", views.TopicListView.as_view(), name="topics"),
    path("meus_topicos/<int:pk>/", views.TopicDetailView.as_view(), name="topic"),
]
