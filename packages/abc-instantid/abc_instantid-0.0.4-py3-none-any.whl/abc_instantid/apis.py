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

    @decorators.action(['POST'], detail=True)
    def gen_image(self, request, pk):
        act = self.get_object()
        from random import randint
        seed = randint(1, 9999999999)
        from tickboom.helper import AsyncAiApi
        api = AsyncAiApi()
        rs = api.instantid(
            image_url=act.avatar,
            seed=seed,
            resize=dict(max_side=960, min_side=960),
            guidance_scale=5,
            num_steps=30,
            prompt="a photo of a person",
            negative_prompt="(lowres, low quality, worst quality:1.2), (text:1.2), watermark, (frame:1.2), deformed, ugly, deformed eyes, blur, out of focus, blurry, deformed cat, deformed, photo, anthropomorphic cat, monochrome, pet collar, gun, weapon, blue, 3d, drones, drone, buildings in background, green",
        )
        img = act.images.create(url=rs['images'][0])
        return response.Response(serializers.ImageSerializer(instance=img).data)

    @decorators.action(['POST'], detail=True)
    def gen_lora(self, request, pk):
        act = self.get_object()
        act.gen_lora()
        return response.Response(dict(result='ok'))

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
