from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Backup(models.Model):
    date = models.DateTimeField()
    store_path = models.CharField(max_length=1024)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s-%s" % (self.user, self.date)


class FileObj(models.Model):
    file_system = models.CharField(max_length=256)

    def __str__(self):
        return "%s" % self.file_system


class File(models.Model):
    name = models.CharField(max_length=256)
    file_system = models.ForeignKey('FileObj', on_delete=models.CASCADE)
    backup = models.ForeignKey(
        'Backup',
        on_delete=models.CASCADE,
        default=None
    )

    def __str__(self):
        return "%s" % self.name


class Attr(models.Model):
    name = models.CharField(max_length=256)
    type = models.IntegerField(default=0)
    obj = models.ForeignKey(
        'FileObj',
        on_delete=models.CASCADE,
    )
    type = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.name


class AttrValue(models.Model):
    attr = models.ForeignKey(
        'Attr',
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=256)
    file = models.ForeignKey(
        'File',
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=256)

    def __str__(self):
        return "%s" % self.id

