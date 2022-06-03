from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    genres = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, primary_key=True)

    def __str__(self): return self.genres


class Movie(models.Model):
    COUNTRY_CHOICES = (
        ('USA', 'USA'),
        ('FRANCE', 'FRANCE'),
        ('SOUTH KOREA', 'SOUTH KOREA'),
        ('CHINA', 'CHINA'),
        ('RUSSIA', 'RUSSIA'),
        ('ITALY', 'ITALY'),
        ('SPAIN', 'SPAIN'),
        ('JAPAN', 'JAPAN'),
        ('UK', 'UK')
    )

    AGE_RESTRICTION = (
        ('0+', '0+'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('14+', '14+'),
        ('18+', '18+'),
        ('21+', '21+')
    )
    title = models.CharField(max_length=50)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movie')
    year = models.DateField()
    country = models.CharField(max_length=30, choices=COUNTRY_CHOICES)
    duration = models.IntegerField()
    cast = models.CharField(max_length=100)
    restriction = models.CharField(max_length=30, choices=AGE_RESTRICTION)
    description = models.TextField()
    poster = models.ImageField(upload_to='images')
    video = models.FileField(upload_to='videos')

    class Meta:
        ordering = ['title']

    def __str__(self): return f'{self.title} - {self.genre}, {self.year}, {self.country}'


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f'{self.owner} -> {self.movie} -> {self.comment}'


class Likes(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'likes'
        unique_together = ['movie', 'user']

    def __str__(self): return f'{self.movie} получил лайк!'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self): return f' {self.user} added {self.movie} to his favorites list!'


