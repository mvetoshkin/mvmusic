from mvmusic.libs import omit_nulls


def music_folder_serializer(music_folder):
    resp = {
        "id": music_folder.id,
        "name": music_folder.name
    }

    return omit_nulls(resp)
