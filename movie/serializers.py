from django.db.models import Avg
from rest_framework import serializers
from movie.models import Genre, Movie, Comment, Favorite


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Genre
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('description', 'cast', 'video')


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        created_movie = Movie.objects.create(**validated_data)
        return created_movie

    def is_liked(self, movie):
        user = self.context.get('request').user
        return user.liked.filter(movie=movie).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = GenreSerializer(instance.genre).data
        representation['rating'] = instance.ratings.aggregate(Avg('mark'))
        representation['comments_detail'] = CommentSerializer(instance.comments.all(), many=True).data
        user = self.context.get('request').user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance.id)
        representation['likes_count'] = instance.likes.count()
        return representation


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'owner', 'movie',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.email
        return representation


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['movie'] = instance.movie.title
        return representation
