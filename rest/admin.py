from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(FileSys)
admin.site.register(File)
admin.site.register(Attr)
admin.site.register(AttrValue)
admin.site.register(Backup)
admin.site.register(FileData)
admin.site.register(KeyUser)
