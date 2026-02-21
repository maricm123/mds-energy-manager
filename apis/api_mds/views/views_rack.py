from rest_framework import generics
from rest_framework.response import Response
from rack.models import Rack


class DeleteRackView(generics.DestroyAPIView):
    """
    Soft delete view for Rack
    """
    lookup_field = 'id'
    queryset = Rack.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
