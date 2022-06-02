from django.db import models
from movie.models import Movie
from django.contrib.auth import get_user_model

User = get_user_model()


class Mark():
    one = 1
    two = 2
    three = 3
    four = 4
    five = 5

    MARKS = (
        (one, 'Very Bad'),
        (two, 'Not that bad'),
        (three, 'Normal'),
        (four, 'Good'),
        (five, 'Great')
    )


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    mark = models.PositiveSmallIntegerField(choices=Mark.MARKS)

    def __str__(self): return f'{self.movie} - {self.mark}'

    class Meta:
        unique_together = ('owner', 'mark')


