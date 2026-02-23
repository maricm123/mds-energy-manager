from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apis.api_mds.serializers.serializers_rack import RackSerializer, CreateRackSerializer, \
    DeviceUnitsSuggestionOutputSerializer, DeviceUnitsSuggestionInputSerializer
from device.selectors import get_devices_from_list
from rack.models import Rack
from rack.selectors import get_rack_with_device_units, get_racks_from_list
from rack.services import (
    create_rack,
    suggest_algorithm_for_rack,
    build_suggestion_output,
    rack_update, delete_rack
)


class GetAllRacksView(generics.ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rack
            fields = "__all__"
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Rack.objects.all()


class GetRackView(generics.RetrieveAPIView):
    lookup_field = "id"
    serializer_class = RackSerializer

    def get_object(self):
        return get_rack_with_device_units(rack_id=self.kwargs.get("id"))


class CreateRackView(APIView):
    def post(self, request):
        serializer = CreateRackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rack = create_rack(serializer.validated_data)

        new_rack = Rack.objects.get(id=rack.id)
        return Response(RackSerializer(new_rack).data, status=status.HTTP_201_CREATED)


class UpdateRackView(generics.GenericAPIView):
    class UpdateRackOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rack
            fields = [
                "id",
                "name",
                "description",
                "serial_number",
                "total_units",
                "max_electricity_sustained",
            ]

    class UpdateRackInputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False, max_length=100)
        description = serializers.CharField(required=False, allow_blank=True)
        serial_number = serializers.CharField(required=False, max_length=100)
        total_units = serializers.IntegerField(required=False, min_value=1)
        max_electricity_sustained = serializers.IntegerField(required=False, min_value=1)

    lookup_field = "id"
    queryset = Rack.objects.all()

    input_serializer_class = UpdateRackInputSerializer
    output_serializer_class = UpdateRackOutputSerializer

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return self.output_serializer_class
        return self.input_serializer_class

    def get(self, request, *args, **kwargs):
        rack = self.get_object()
        return Response(self.output_serializer_class(rack).data)

    def patch(self, request, *args, **kwargs):
        rack = self.get_object()

        serializer = self.input_serializer_class(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        updated = rack_update(
            rack=rack,
            data=serializer.validated_data,
        )

        return Response(self.output_serializer_class(updated).data)


class DeleteRackView(generics.DestroyAPIView):
    """
    Soft delete view for Rack
    """
    lookup_field = 'id'
    queryset = Rack.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_rack(instance)
        return Response(status=204)


class DeviceUnitsSuggestionView(APIView):
    """
    Send rack ids and device ids
    """
    def post(self, request):
        serializer = DeviceUnitsSuggestionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        racks = get_racks_from_list(serializer.validated_data["rack_ids"])
        devices = get_devices_from_list(serializer.validated_data["device_ids"])
        (assigned_devices_by_rack,
         used_energy_by_rack,
         used_units_by_rack,
         unassigned_devices) = suggest_algorithm_for_rack(racks, devices)

        output_data = build_suggestion_output(
            racks=racks,
            assigned_devices_by_rack=assigned_devices_by_rack,
            used_energy_by_rack=used_energy_by_rack,
            used_units_by_rack=used_units_by_rack,
            unassigned_devices=unassigned_devices,
        )

        return Response(DeviceUnitsSuggestionOutputSerializer(output_data).data, status=200)
