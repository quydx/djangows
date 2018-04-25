from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^api/initalization$', views.backup_init, name='backup-init'),
    url(r'^api/metadata$', views.process_metadata, name='backup-process-metadata'),
]