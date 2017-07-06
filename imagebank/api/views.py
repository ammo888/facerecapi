# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, views, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, detail_route
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Image
from .serializers import UserSerializer, ImageSerializer
from .renderers import JPEGRenderer
from .faces import Faces

faces = Faces()
savestart = True

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'images': reverse('image-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resp = self.perform_create(serializer)
        return Response(resp, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        image_id = serializer.data['id']
        global savestart
        if savestart:
            savestart = False
            faces.save()
        data = self.request.data
        if 'name' not in data or not data['name']:
            return faces.identify(image_id)
        return faces.update(image_id)

    @detail_route(renderer_classes=[JPEGRenderer])
    def data(self, request, *args, **kwargs):
        image = self.get_object()
        return Response(image.image)
