from django.urls import path

from . import views

urlpatterns = [
    path(
        "topicos_publicos/",
        views.PublicTopicListAPIView.as_view(),
        name="api_public_topics",
    ),
    path(
        "topicos_publicos/<int:pk>/",
        views.PublicTopicDetailAPIView.as_view(),
        name="api_public_topic",
    ),
]
