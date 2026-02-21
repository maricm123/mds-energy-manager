from rest_framework import generics
from device.models import Device
from rest_framework.response import Response


class DeleteDeviceView(generics.DestroyAPIView):
    """
    Soft delete view for Device
    """
    lookup_field = 'id'
    queryset = Device.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
