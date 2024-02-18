# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals

from xyz_restful.mixins import UserApiMixin, BatchActionMixin
from . import models, serializers
from rest_framework import viewsets, decorators, response
from xyz_restful.decorators import register

@register()
class AccountViewSet(BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'is_active': ['exact']
    }
    search_field = ('name', )
    ordering_fields = ('is_active', 'create_time',)

    @decorators.action(['POST'], detail=False)
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)


    @decorators.action(['GET'], detail=True)
    def search_post_images(self, request, pk):
        ac = self.get_object()
        qs = request.query_params
        from .helper import search_user_post_pictures
        rs = search_user_post_pictures(ac.name, max_count=int(qs.get('max_count', 10)))
        return response.Response(dict(urls=rs))


@register()
class ImageViewSet(BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Image.objects.all()
    serializer_class = serializers.ImageSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'is_active': ['exact'],
        'account': ['exact']
    }
    ordering_fields = ('is_active', 'create_time',)

    @decorators.action(['POST'], detail=False)
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)
