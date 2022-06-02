from rest_framework import serializers
from movie.models import Movie


class FavoriteSerializer(serializers.Serializer):
    movie = serializers.IntegerField()

    def validate(self, attrs):
        data = {}
        try:
            movie = Movie.objects.get(pk=attrs['movie'])
        except Movie.DoesNotExist:
            raise serializers.ValidationError('Movie is not found')
        data['movie'] = movie.pk
        return data

    def save(self, **kwargs):
        data = self.validated_data
        user = kwargs['user']
        movie = Movie.objects.get(pk=data['movie'])
        Movie.objects.create(
            movie=movie,
            user=user,
        )
