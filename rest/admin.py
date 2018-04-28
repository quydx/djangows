from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(FileObj)
admin.site.register(File)
admin.site.register(Attr)
admin.site.register(AttrValue)
admin.site.register(Backup)
