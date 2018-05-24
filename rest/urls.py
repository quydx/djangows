from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^api/initialization/$', views.backup_init, name='backup-init'),
    url(r'^api/metadata/$', views.process_metadata, name='backup-process-metadata'),
    url(r'^api/upload/data/$', views.DataView.as_view(), name='upload-data'),
    url(r'^api/list/$', views.list_backup_info, name='list_backup_info'),
    url(r'^api/list/(?P<pk>\d+)/$', views.list_backup_info, name='list_backup_info_with_pk'),
    url(r'^api/restore/(?P<version>\d+)/$', views.restore_init, name='restore-init'),
    url(r'^api/download_data/(?P<version>\d+)/$', views.download_data, name='download-data'),
]