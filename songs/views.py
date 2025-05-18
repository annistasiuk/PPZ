from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Song, Genre, Playlist
from .forms import PlaylistForm


def index(request):
    """Використовується для відображення головної сторінки. Повертає список жанрів, пісень та плейлистів."""
    genres = Genre.objects.all()
    songs = Song.objects.all()
    playlists = Playlist.objects.all()
    context = {
        'genres': genres,
        'songs': songs,
        'playlists': playlists,
    }
    return render(request, 'index.html', context)


def song_detail(request, song_id):
    """Використовується для відображення інформації про пісню. Повертає пісню та список плейлистів користувача."""
    song = Song.objects.get(id=song_id)
    playlists = Playlist.objects.filter(owner=request.user)
    context = {
        'song': song,
        'playlists': playlists,
    }
    return render(request, 'song_detail.html', context)


def genre_filter(request, genre_id):
    """Використовується для фільтрації пісень за жанром. Повертає список жанрів, жанр та список пісень, які відповідають жанру."""
    genres = Genre.objects.all()
    genre = Genre.objects.get(id=genre_id)
    songs = Song.objects.filter(genre=genre)
    context = {
        'genres': genres,
        'genre': genre,
        'songs': songs,
    }
    return render(request, 'index.html', context)


@login_required
def playlist_list(request):
    """Використовується для відображення списку плейлистів. Повертає список плейлистів."""
    playlists = Playlist.objects.all()
    context = {
        'playlists': playlists,
    }
    return render(request, 'playlist_list.html', context)


@login_required
def playlist_detail(request, playlist_id):
    """Використовується для відображення інформації про плейлист. Повертає плейлист та список пісень, які входять в плейлист."""
    playlist = Playlist.objects.get(id=playlist_id)
    songs = playlist.songs.all()
    context = {
        'playlist': playlist,
        'songs': songs,
    }
    return render(request, 'playlist_detail.html', context)


@login_required
def create_playlist(request):
    """Використовується для створення нового плейлисту. Повертає форму для створення плейлисту."""
    form = PlaylistForm()
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return redirect('songs:playlist_list')
    context = {
        'form': form,
    }
    return render(request, 'form.html', context)


@login_required
def add_song_to_playlist(request, song_id):
    """Використовується для додавання пісні до плейлисту. Перенаправляє на головну сторінку."""
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        song = get_object_or_404(Song, pk=song_id)
        playlist.songs.add(song)

        return redirect('songs:index')
    return redirect('songs:index')


def remove_song_from_playlist(request, playlist_id, song_id):
    """Використовується для видалення пісні з плейлисту. Перенаправляє на сторінку плейлисту."""
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    song = get_object_or_404(Song, pk=song_id)
    playlist.songs.remove(song)
    return redirect('songs:playlist_detail', playlist_id=playlist_id)


@login_required
def remove_playlist(request, playlist_id):
    """Використовується для видалення плейлисту. Перенаправляє на сторінку списку плейлистів."""
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    playlist.delete()
    return redirect('songs:playlist_list')
