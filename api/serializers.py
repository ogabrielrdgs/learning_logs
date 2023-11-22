from rest_framework import serializers

from learning_logs import models


class TopicSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()

    class Meta:
        model = models.Topic
        fields = ("id", "title", "date_added", "owner")


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = ("id", "content", "date_added")

