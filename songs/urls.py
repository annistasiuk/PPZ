from django.urls import path

from . import views

app_name = 'songs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:song_id>/', views.song_detail, name='song_detail'),
    path('genre/<int:genre_id>/', views.genre_filter, name='genre_filter'),
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('add_song_to_playlist/<int:song_id>/', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('remove_playlist/<int:playlist_id>/', views.remove_playlist, name='remove_playlist'),
    path('remove_song_from_playlist/<int:playlist_id>/<int:song_id>/', views.remove_song_from_playlist, name='remove_song_from_playlist'),
]
