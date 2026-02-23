from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apis.api_mds.serializers.serializers_rack import RackSerializer, CreateRackSerializer, \
    DeviceUnitsSuggestionOutputSerializer, DeviceUnitsSuggestionInputSerializer
from device.selectors import get_devices_from_list
from rack.models import Rack
from rack.selectors import get_rack_with_device_units, get_racks_from_list
from rack.services import create_rack, suggest_algorithm_for_rack


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


class DeviceUnitsSuggestionView(APIView):
    """
    Send rack and device ids
    """
    def post(self, request):
        serializer = DeviceUnitsSuggestionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        racks = get_racks_from_list(serializer.validated_data["rack_ids"])
        devices = get_devices_from_list(serializer.validated_data["device_ids"])
        suggest_algorithm_for_rack(racks, devices)

        return Response(DeviceUnitsSuggestionOutputSerializer, status=200)
