from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import api_root, UserViewSet, ImageViewSet
from .renderers import JPEGRenderer


image_list = ImageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
image_detail = ImageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
image_data = ImageViewSet.as_view({
    'get': 'data'
}, renderer_classes=[JPEGRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', api_root),
    url(r'^imagebank/$', image_list, name='image-list'),
    url(r'^imagebank/(?P<pk>[0-9]+)/$', image_detail, name='image-detail'),
    url(r'^imagebank/(?P<pk>[0-9]+)/data/$', image_data, name='image-data'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
])
