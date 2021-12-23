from . import BaseView
from ..serializers.music_library import music_library_serializer


class GetMusicFoldersView(BaseView):
    def process_request(self):
        return {
            'musicFolders': {
                'musicFolder': [
                    music_library_serializer(i)
                    for i in self.current_user.music_libraries
                ]
            }
        }
