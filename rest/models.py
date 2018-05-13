from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.files.storage import FileSystemStorage
from djangorest import settings
import datetime
import os
#  
upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT)


def key_store_upload_to(instance, path):
    # prepend date to path
    # print(instance.file_object)
    # print(instance.file_object.path.rsplit('/', 1)[0])
    p = '{}/{}'.format(instance.file_object.backup.store_path.rsplit('/', 1)[1], instance.file_object.path)
    return os.path.join(p)


class Backup(models.Model):
    date = models.DateTimeField()
    store_path = models.CharField(max_length=1024)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "%s-%s" % (self.user, self.date)


class FileSys(models.Model):
    file_system = models.CharField(max_length=256)

    def __str__(self):
        return "%s" % self.file_system


class File(models.Model):
    name = models.CharField(max_length=256)
    type_file = models.CharField(max_length=20)
    path = models.CharField(max_length=1024)
    file_system = models.ForeignKey('FileSys', on_delete=models.CASCADE)
    backup = models.ForeignKey(
        'Backup',
        on_delete=models.CASCADE,
        default=None
    )

    def __str__(self):
        return "%s" % self.name


class Attr(models.Model):
    name = models.CharField(max_length=256)
    file_sys = models.ForeignKey(
        'FileSys',
        on_delete=models.CASCADE,
    )
    type_attr = models.IntegerField(default=0)

    def __str__(self):
        return "{0} - {1}".format(self.name, self.file_sys)


class AttrValue(models.Model):
    attr = models.ForeignKey(
        'Attr',
        on_delete=models.CASCADE
    )
    file_object = models.ForeignKey(
        'File',
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=256)

    def __str__(self):
        return "{1} {0}".format(self.attr, self.file_object) 


class FileData(models.Model):
    file_object = models.ForeignKey('File', on_delete=models.CASCADE)
    block_id = models.IntegerField(default=0)
    checksum = models.CharField(max_length=256)
    block_data = models.FileField(storage=upload_storage, upload_to=key_store_upload_to, blank=False, null=False)
     
    def __str__(self):
        return "{} {}".format(self.file_object, self.block_id)

    # def save(self):
    #     instance = super(FileData, self).save(commit=False)
    #     f = File.object.get(pk=self.file_object) 
    #     print(f.path)
    #     store_path = settings.UPLOAD_ROOT + f.path
    #     upload_storage = FileSystemStorage(location=store_path)
    #     self.block_data = models.FileField(storage=store_path, blank=False, null=False)
    #     instance.save()
    #     return instance

