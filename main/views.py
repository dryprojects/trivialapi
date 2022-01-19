from rest_framework import viewsets

from main import models, serializers


class ZjjXaGovPreWoned(viewsets.ReadOnlyModelViewSet):
    queryset = models.PreOwnedItem.objects.all()
    serializer_class = serializers.ZjjXaGovPreOwnedSerializer
