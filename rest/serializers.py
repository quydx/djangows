from rest_framework import serializers
from .models import FileData

class DataSerializer(serializers.ModelSerializer):
  class Meta():
    model = FileData
    fields = ('block_data', 'block_id', 'checksum', 'file_object')