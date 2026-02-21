from rest_framework import generics, serializers
from rest_framework.response import Response
from rack.models import Rack


class GetAllRacksView(generics.ListAPIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rack
            fields = "__all__"
    serializer_class = OutputSerializer

    def get_queryset(self):
        return Rack.objects.all()


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
