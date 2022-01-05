from . import BaseView
from ..serializers.music_folder import music_folder_serializer


class GetMusicFoldersView(BaseView):
    def process_request(self):
        return {
            'musicFolders': {
                'musicFolder': [
                    music_folder_serializer(i)
                    for i in self.current_user.libraries
                ]
            }
        }
