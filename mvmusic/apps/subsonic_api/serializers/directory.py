from mvmusic.libs import omit_nulls
from mvmusic.models.directory import Directory
from .child import child_serializer


def directory_serializer(directory: Directory, children):
    resp = {
        'id': directory.id_,
        'parent': directory.parent_id,
        'name': directory.name,
        'child': [child_serializer(i) for i in children]
    }

    return omit_nulls(resp, {'name'})
