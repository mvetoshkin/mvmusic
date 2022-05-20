from mvmusic.models.directory import Directory
from . import BaseView
from ..serializers.directory import directory_serializer


class GetMusicDirectoryView(BaseView):
    def process_request(self, id_):
        directory = Directory.query.one(
            Directory.id_ == id_,
            Directory.library_id.in_([i.id_ for i in self.user_libraries])
        )

        children = [i for i in directory.children]
        children += [i for i in directory.media]

        return {
            'directory': directory_serializer(directory, children)
        }
