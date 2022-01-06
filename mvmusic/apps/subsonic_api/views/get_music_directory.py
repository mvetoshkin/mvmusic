from mvmusic.models.directory import Directory
from . import BaseView
from ..serializers.directory import directory_serializer
from ..serializers.media import media_serializer


class GetMusicDirectoryView(BaseView):
    def process_request(self, id_):
        directory = Directory.query.one(
            Directory.id_ == id_,
            Directory.library_id.in_([i.id_ for i in self.user_libraries])
        )

        resp = directory_serializer(directory)
        resp['child'] = [directory_serializer(i, as_child=True)
                         for i in directory.children]
        resp['child'] += [media_serializer(i) for i in directory.media]

        return {
            'directory': resp
        }
