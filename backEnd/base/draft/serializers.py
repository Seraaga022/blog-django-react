from rest_framework import serializers
from .models import Draft

class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('id', 'user_id', 'title', 'content', 'img')
