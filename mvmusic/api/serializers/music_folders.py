from mvmusic.api.serializers.music_folder import music_folder_serializer
from mvmusic.libs import omit_nulls


def music_folders_serializer(music_folders):
    resp = {
        "musicFolder": [music_folder_serializer(i) for i in music_folders]
    }

    return omit_nulls(resp)
