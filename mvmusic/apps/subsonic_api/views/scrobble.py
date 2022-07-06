from . import BaseView
from mvmusic.models.history import History
from mvmusic.models.media import Media


class ScrobbleView(BaseView):
    def process_request(self, id_, time=None, submission=True):
        media = Media.query.get(id_)
        History.create(media=media, user=self.current_user)

        return None
