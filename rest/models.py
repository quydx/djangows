from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.files.storage import FileSystemStorage
from djangorest import settings

#  
upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT)

def get_upload_path(instance):
        """
        Returns the upload path for block_data
        """
        repo_name = instance.file_object.path
        print('REPO NONONO')
        print(repo_name)
        return "{}/{}".format(settings.UPLOAD_ROOT, repo_name)
        #  /home/locvu/backup/locvu/locvu2018_05_11_09_56/openvpn/ca/

        # filename = filename.split('.')
        # extension = filename.pop()
        # name = ''.join(filename)
        # return "documents/%s/%s.%s" % (self.post.pk, slugify(name), extension)

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
    
    block_data = models.FileField(storage=upload_storage, blank=False, null=False)
    block_id = models.IntegerField(default=0)
    checksum = models.CharField(max_length=256)
    file_object = models.ForeignKey('File', on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.file_object, self.block_id)

    

