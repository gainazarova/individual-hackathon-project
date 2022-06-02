from django.contrib import admin
from movie.models import Genre, Movie, Comment, Likes

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Likes)
