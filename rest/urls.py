from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^api/initialization/$', views.backup_init, name='backup-init'),
    url(r'^api/metadata/$', views.process_metadata, name='backup-process-metadata'),
    url(r'^api/upload/data/$', views.DataView.as_view(), name='upload-data'),
]