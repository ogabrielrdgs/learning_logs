from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

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
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
]
