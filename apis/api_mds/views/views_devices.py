from rest_framework import generics, serializers
from device.models import Device
from rest_framework.response import Response


class GetAllDevicesView(generics.ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Device
            fields = "__all__"
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Device.objects.select_related('rack').all()


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
