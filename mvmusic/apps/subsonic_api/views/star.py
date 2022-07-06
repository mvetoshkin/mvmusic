from mvmusic.libs.exceptions import NotFoundError
from mvmusic.models.album import Album
from mvmusic.models.artist import Artist
from mvmusic.models.directory import Directory
from mvmusic.models.media import Media
from mvmusic.models.starred_album import StarredAlbum
from mvmusic.models.starred_artist import StarredArtist
from mvmusic.models.starred_directory import StarredDirectory
from mvmusic.models.starred_media import StarredMedia
from . import BaseView


class StarView(BaseView):
    def process_request(self, id_m=None, albumid_m=None, artistid_m=None):
        if id_m:
            for id_ in id_m:
                try:
                    self.star_media(id_)
                    continue
                except NotFoundError:
                    pass

                try:
                    self.star_directory(id_)
                except NotFoundError:
                    pass

        if albumid_m:
            for id_ in albumid_m:
                self.star_album(id_)

        if artistid_m:
            for id_ in artistid_m:
                self.star_artist(id_)

        return None

    def star_media(self, id_):
        media = Media.query.get(id_)

        try:
            StarredMedia.query.get_by(media=media, user=self.current_user)
        except NotFoundError:
            StarredMedia.create(media=media, user=self.current_user)

    def star_directory(self, id_):
        directory = Directory.query.get(id_)

        try:
            StarredDirectory.query.get_by(
                directory=directory, user=self.current_user
            )
        except NotFoundError:
            StarredDirectory.create(directory=directory, user=self.current_user)

    def star_artist(self, id_):
        artist = Artist.query.get(id_)

        try:
            StarredArtist.query.get_by(artist=artist, user=self.current_user)
        except NotFoundError:
            StarredArtist.create(artist=artist, user=self.current_user)

    def star_album(self, id_):
        album = Album.query.get(id_)

        try:
            StarredAlbum.query.get_by(album=album, user=self.current_user)
        except NotFoundError:
            StarredAlbum.create(album=album, user=self.current_user)
