from datetime import timedelta
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from movie.parsing import BASE_URL, get_html, get_info
from . import serializers
from movie.models import Genre, Movie, Comment, Likes, Favorite
from rest_framework import permissions, generics, status
from .permissions import IsAuthor
from .serializers import MovieDetailSerializer
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class StandardPaginationClass(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MovieViewSet(ModelViewSet):
    class Meta:
        model = Movie
        fields = '__all__'
    queryset = Movie.objects.all()
    pagination_class = StandardPaginationClass
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('genre',)
    search_fields = ('title',)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.MovieListSerializer
        else:
            return serializers.MovieDetailSerializer

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['GET'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q))
        serializer = MovieDetailSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        movie = self.get_object()
        comments = movie.comments.all()
        serializer = serializers.CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(['POST'], detail=True)
    def movie_like(self, request, pk):
        movie = self.get_object()
        if request.user.liked.filter(movie=movie).exists():
            return Response('You have already liked this movie!', status=status.HTTP_400_BAD_REQUEST)
        Likes.objects.create(movie=movie, user=request.user)
        return Response('You liked this movie!', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def movie_unlike(self, request, pk):
        movie = self.get_object()
        if not request.user.liked.filter(movie=movie).exists():
            return Response('You haven\'t liked this movie yet!', status=status.HTTP_400_BAD_REQUEST)
        request.user.liked.filter(movie=movie).delete()
        return Response('Your like has been successfully removed!', status=status.HTTP_204_NO_CONTENT)

    @action(['POST'], detail=True)
    def add_to_favorites(self, request, pk):
        movie = self.get_object()
        if request.user.favorites.filter(movie=movie).exists():
            return Response('You have already added this movie to your favorites list', status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(movie=movie, user=request.user)
        return Response('You successfully added this movie to your favorites!', status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def remove_from_favorites(self, request, pk):
        movie = self.get_object()
        if not request.user.favorites.filter(movie=movie).exists():
            return Response('You haven\'t added this movie to your favorites yet ', status=status.HTTP_400_BAD_REQUEST)
        request.user.favorites.filter(movie=movie).delete()
        return Response('You successfully removed this movie from your favorites!', status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny(),]
        else:
            return [permissions.IsAuthenticated(),]


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthor,)


class FavoritesList(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        user = request.user
        movie = user.favorites.all()
        serializer = serializers.FavoriteSerializer(movie, many=True).data
        return Response(serializer)


class ParsingView(APIView):

    def get(self, request):
        parsing = get_info(get_html(BASE_URL))
        return Response(parsing)

        
get_info(get_html(BASE_URL)) 