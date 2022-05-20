from . import BaseView
from ..serializers.music_folders import music_folders_serializer


class GetMusicFoldersView(BaseView):
    def process_request(self):
        return {
            'musicFolders': music_folders_serializer(self.user_libraries)
        }
