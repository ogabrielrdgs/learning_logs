from rest_framework import generics, filters

from . import serializers
from learning_logs import models


class PublicTopicListAPIView(generics.ListAPIView):
    queryset = models.Topic.objects.filter(public=True)
    serializer_class = serializers.TopicSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title",)


class PublicTopicDetailAPIView(generics.ListAPIView):
    serializer_class = serializers.EntrySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("content",)

    def get_queryset(self):
        return models.Entry.objects.filter(
            topic__pk=self.kwargs["pk"], topic__public=True
        )
