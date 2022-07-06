from mvmusic.libs.exceptions import NotFoundError
from mvmusic.models.starred_album import StarredAlbum
from mvmusic.models.starred_artist import StarredArtist
from mvmusic.models.starred_directory import StarredDirectory
from mvmusic.models.starred_media import StarredMedia
from . import BaseView


class UnstarView(BaseView):
    def process_request(self, id_m=None, albumid_m=None, artistid_m=None):
        if id_m:
            for id_ in id_m:
                try:
                    s = StarredMedia.query.get_by(media_id=id_,
                                                  user=self.current_user)
                    s.delete()
                    continue
                except NotFoundError:
                    pass

                try:
                    s = StarredDirectory.query.get_by(directory_id=id_,
                                                      user=self.current_user)
                    s.delete()
                except NotFoundError:
                    pass

        if albumid_m:
            for id_ in albumid_m:
                try:
                    s = StarredAlbum.query.get_by(album_id=id_,
                                                  user=self.current_user)
                    s.delete()
                except NotFoundError:
                    pass

        if artistid_m:
            for id_ in artistid_m:
                try:
                    s = StarredArtist.query.get_by(artist_id=id_,
                                                   user=self.current_user)
                    s.delete()
                except NotFoundError:
                    pass

        return None
