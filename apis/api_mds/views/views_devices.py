from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from apis.api_mds.serializers.serializers_device import (
    AddDeviceToRackSerializer,
    DeviceOutputSerializer,
    CreateDeviceSerializer
)
from apis.api_mds.serializers.serializers_rack import RackSerializer
from device.models import Device
from rest_framework.response import Response
from device.services import add_device_to_rack, create_device
from rack.models import Rack


class GetAllDevicesView(generics.ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Device
            fields = "__all__"
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Device.objects.all()


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


class AddDeviceToRackView(APIView):
    def post(self, request):
        serializer = AddDeviceToRackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = serializer.validated_data["device"]
        rack = serializer.validated_data["rack"]

        add_device_to_rack(device=device, rack=rack)

        updated_rack = Rack.objects.get(id=rack.id)
        return Response(RackSerializer(updated_rack).data, status=200)


class CreateDeviceView(APIView):
    def post(self, request):
        serializer = CreateDeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = create_device(serializer.validated_data)

        new_device = Device.objects.get(id=device.id)
        return Response(DeviceOutputSerializer(new_device).data, status=status.HTTP_201_CREATED)
