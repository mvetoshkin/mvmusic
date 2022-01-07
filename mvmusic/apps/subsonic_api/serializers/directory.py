from mvmusic.libs import omit_nulls
from mvmusic.models.directory import Directory


def directory_serializer(directory: Directory, as_child=False):
    resp = {
        'id': directory.id_,
        'parent': directory.parent_id
    }

    if as_child:
        resp['title'] = directory.name
        resp['isDir'] = True
        resp['coverArt'] = directory.image_id
        resp['artist'] = directory.parent.name

    else:
        resp['name'] = directory.name

    return omit_nulls(resp, {'isDir', 'title'})
