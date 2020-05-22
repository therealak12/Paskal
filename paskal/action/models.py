from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField

class Action(models.Model):
    text = models.TextField()
    score = models.IntegerField(default=0)
    # When a user is deleted we still keep his/her questions
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(default=timezone.now)
    last_updated_on = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class TargetAction(Action):
    pass


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(Action):
    title = models.CharField(max_length=500)
    text = RichTextField('متن پرسش', blank=False, null=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title


class Answer(Action):
    question = models.ForeignKey(
        'Question', on_delete=models.CASCADE, null=True)


class Reply(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.DO_NOTHING)
    last_updated_on = models.DateTimeField(default=timezone.now)
    action = models.ForeignKey(
        'TargetAction', on_delete=models.CASCADE, null=True)
