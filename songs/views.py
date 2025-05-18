from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Song, Genre, Playlist
from .forms import PlaylistForm

def home(request):
    songs = Song.objects.all().order_by('-id')[:6]
    genres = Genre.objects.all()
    return render(request, 'songs/home.html', {
        'title': 'Music Django - Home',
        'songs': songs,
        'genres': genres,
    })

def index(request):
    songs = Song.objects.all().order_by('title')
    genres = Genre.objects.all()
    return render(request, 'songs/index.html', {
        'title': 'Music Django - Головна',
        'songs': songs,
        'genres': genres,
    })

def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, 'songs/song_detail.html', {
        'title': f'Music Django - {song.title}',
        'song': song,
    })

def genre_filter(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    songs = Song.objects.filter(genre=genre).order_by('title')
    genres = Genre.objects.all()
    return render(request, 'songs/index.html', {
        'title': f'Music Django - Жанр: {genre.name}',
        'songs': songs,
        'genres': genres,
        'selected_genre': genre,
    })

@login_required
def playlist_list(request):
    playlists = Playlist.objects.filter(owner=request.user)
    return render(request, 'songs/playlist_list.html', {
        'title': 'Music Django - Мої плейлисти',
        'playlists': playlists,
    })

def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if playlist.owner != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Ви не маєте прав на перегляд цього плейлиста")
    return render(request, 'songs/playlist_detail.html', {
        'title': f'Music Django - Плейлист: {playlist.name}',
        'playlist': playlist,
    })

@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('songs:playlist_detail', playlist_id=playlist.id)
    else:
        form = PlaylistForm()

    return render(request, 'songs/create_playlist.html', {
        'title': 'Music Django - Створити плейлист',
        'form': form,
    })

@login_required
def add_song_to_playlist(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
        if playlist_id:
            playlist = get_object_or_404(Playlist, id=playlist_id)
            if playlist.owner != request.user:
                return HttpResponseForbidden("Ви не маєте прав на редагування цього плейлиста")
            playlist.songs.add(song)
            return redirect('songs:playlist_detail', playlist_id=playlist.id)

    playlists = Playlist.objects.filter(owner=request.user)
    return render(request, 'songs/add_song_to_playlist.html', {
        'title': f'Music Django - Додати пісню "{song.title}" до плейлиста',
        'song': song,
        'playlists': playlists,
    })

@login_required
def remove_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if playlist.owner != request.user:
        return HttpResponseForbidden("Ви не маєте прав на видалення цього плейлиста")
    playlist.delete()
    return redirect('songs:playlist_list')

@login_required
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    song = get_object_or_404(Song, id=song_id)
    if playlist.owner != request.user:
        return HttpResponseForbidden("Ви не маєте прав на редагування цього плейлиста")
    playlist.songs.remove(song)
    return redirect('songs:playlist_detail', playlist_id=playlist.id)
