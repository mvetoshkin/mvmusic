from . import BaseView
from ..serializers.library import library_serializer


class GetMusicFoldersView(BaseView):
    def process_request(self):
        return {
            'musicFolders': {
                'musicFolder': [
                    library_serializer(i)
                    for i in self.current_user.libraries
                ]
            }
        }
