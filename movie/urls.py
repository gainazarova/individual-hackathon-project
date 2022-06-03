from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('movies', views.MovieViewSet)
router.register('genres', views.GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', views.CommentListCreateView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
    path('favorites/', views.FavoritesList.as_view()),
]
