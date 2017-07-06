from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Image


class UserSerializer(serializers.ModelSerializer):
    images = serializers.HyperlinkedRelatedField(
        many=True, view_name='image-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'images')


class ImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    data = serializers.HyperlinkedIdentityField(
        view_name='image-data', format='html')

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        return Image.objects.create(**validated_data)