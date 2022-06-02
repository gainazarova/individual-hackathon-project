from django.db import models
from django.contrib.auth import get_user_model
from movie.models import Movie
User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.DO_NOTHING,)

    def __str__(self): return f'{self.user} added {self.movie} to favorites. '

    class Meta:
        unique_together = ('user', 'movie')
