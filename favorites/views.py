from rest_framework import views, permissions
from rest_framework.response import Response
from favorites import serializers


class FavoriteApiView(views.APIView):
    # permission_classes = permissions.IsAuthenticated

    def post(self, request):
        serializer = serializers.FavoriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
