from rest_framework import generics, serializers, status
from rest_framework.views import APIView
from apis.api_mds.serializers.serializers_device import (
    AddDeviceToRackSerializer,
    DeviceOutputSerializer,
    CreateDeviceSerializer,
)
from apis.api_mds.serializers.serializers_rack import RackSerializer
from device.models import Device
from rest_framework.response import Response
from device.services import add_device_to_rack, create_device, device_update, delete_device
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
        delete_device(instance)
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


class UpdateDeviceView(generics.GenericAPIView):
    class UpdateDeviceOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Device
            fields = [
                "id",
                "name",
                "description",
                "serial_number",
                "number_of_rack_units",
                "electricity_consumption",
            ]

    class UpdateDeviceInputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, max_length=100)
        description = serializers.CharField(required=False, allow_blank=True)
        serial_number = serializers.CharField(required=False, max_length=100)
        number_of_rack_units = serializers.IntegerField(required=False, min_value=1)
        electricity_consumption = serializers.IntegerField(required=False, min_value=1)

    lookup_field = "id"
    queryset = Device.objects.all()

    input_serializer_class = UpdateDeviceInputSerializer
    output_serializer_class = UpdateDeviceOutputSerializer

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return self.output_serializer_class
        return self.input_serializer_class

    def get(self, request, *args, **kwargs):
        device = self.get_object()
        return Response(self.output_serializer_class(device).data)

    def patch(self, request, *args, **kwargs):
        device = self.get_object()

        serializer = self.input_serializer_class(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        updated = device_update(
            device=device,
            data=serializer.validated_data,
        )

        return Response(self.output_serializer_class(updated).data)
