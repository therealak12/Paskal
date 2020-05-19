from django.db import models
from django.conf import settings
from django.utils import timezone

from mptt.models import MPTTModel, TreeForeignKey


class Action(models.Model):
    text = models.TextField()
    score = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)
    last_updated_on = models.DateTimeField(default=timezone.now)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(Action):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=500)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class Answer(Action):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    target_question = models.ForeignKey(
        Question , on_delete=models.CASCADE, null=True)


class Reply(MPTTModel):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    last_updated_on = models.DateTimeField(default=timezone.now)
    action = models.ForeignKey(
        'Action', on_delete=models.CASCADE, null=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True, on_delete=models.CASCADE)
