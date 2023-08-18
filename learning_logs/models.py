from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class Topic(models.Model):
    title = models.CharField(_("title"), max_length=264)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    public = models.BooleanField(_("public"))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="topics",
        on_delete=models.CASCADE,
        verbose_name=_("owner"),
    )

    def __str__(self):
        return self.title + " - " + self.owner.email

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")
        ordering = ("-date_added",)
        constraints = (
            models.UniqueConstraint(
                fields=["owner", "title"],
                name="unique_topic_title",
                violation_error_message=_("You already have a topic with this title!"),
            ),
        )

    def get_title(self):
        if len(self.title) > 20:
            return self.title[:20] + "..."
        else:
            return self.title

    def get_url(self):
        return reverse_lazy("topic", kwargs={"pk": self.pk})


class Entry(models.Model):
    content = models.TextField(_("content"))
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)
    topic = models.ForeignKey(
        Topic, related_name="entries", on_delete=models.CASCADE, verbose_name=_("topic")
    )

    class Meta:
        verbose_name = _("entry")
        verbose_name_plural = _("entries")
        ordering = ("-date_added",)

    def __str__(self):
        if len(self.content) > 50:
            return self.content[:50] + "..."
        else:
            return self.content
