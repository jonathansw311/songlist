from flask import Flask, redirect, render_template
#from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    

    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""
    playlst=Playlist.query.get(playlist_id)
    
    return render_template('playlist.html', playlist=playlst)
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()
    
    if form.validate_on_submit():
        name=form.name.data
        description=form.description.data
        newplaylist=Playlist(name=name, description=description)
        db.session.add(newplaylist)
        db.session.commit()
        return redirect('/')
    return render_template('new_playlist.html', form=form)

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
@app.route("/playlists/<int:id>/delete")
def playlist_delete(id):    
    """Deletes a song playlist"""
    delPlayList=Playlist.query.get(id)
    db.session.delete(delPlayList)
    db.session.commit()
    return redirect('/playlists')


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""
    song=Song.query.get(song_id)
    
    
    return render_template('song.html', song=song, )

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """
    
    form = SongForm()
    if form.validate_on_submit():
        title=form.title.data
        artist=form.artist.data
        newSong=Song(title=title, artist=artist)
        db.session.add(newSong)
        db.session.commit()
        return redirect('/songs')

    return render_template('new_song.html', form=form)
    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

@app.route("/songs/<int:id>/delete")
def delsong(id):
    song=Song.query.get(id)
    db.session.delete(song)
    db.session.commit()
    return redirect('/songs')

@app.route('/playlists/<int:sid>/<int:pid>/delete')
def delsongfromlist(sid, pid):
    """deletes a song off a playlist"""
    lists = PlaylistSong.query.filter(PlaylistSong.song_id==sid, PlaylistSong.playlist_id==pid).first()
    
    db.session.delete(lists)
    db.session.commit()
    return redirect(f'/playlists/{pid}')


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS
    """gets a specific playlist id"""
    playlist = Playlist.query.get_or_404(playlist_id)
    """creates new songs to add form"""
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist
    """iterates through  the songs on the playlist retreived above"""
    curr_on_playlist = [s.id for s in playlist.songs]
    """retrieves a list of song id's and titles and filters them by songs not in the current play list"""
    songs_query = db.session.query(Song.id, Song.title).filter(Song.id.notin_(curr_on_playlist)).all()
    """loads the songID and titles into the form to be selected"""
    form.song.choices = [(song.id, song.title) for song in songs_query]
    
    
    if form.validate_on_submit():
        """after the form is POSTED it gets the song that was selected from the list"""
        songID=form.song.data
        """and adds the data into the join table"""
        newPlaylistSong=PlaylistSong(playlist_id=playlist_id, song_id=songID)
        db.session.add(newPlaylistSong) 
        db.session.commit()
        
          # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
