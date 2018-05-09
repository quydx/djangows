from rest_framework import serializers
from .models import Data

class DataSerializer(serializers.ModelSerializer):
  class Meta():
    model = Data
    fields = ('block_data', 'block_id', 'checksum', 'file_object')