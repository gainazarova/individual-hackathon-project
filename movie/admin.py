from django.contrib import admin
from movie.models import Genre, Movie, Comment, Likes, Favorite

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Favorite)
