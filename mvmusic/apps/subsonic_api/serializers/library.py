from mvmusic.libs import omit_nulls
from mvmusic.models.library import Library


def library_serializer(library: Library):
    resp = {
        'id': library.id_,
        'name': library.name
    }

    return omit_nulls(resp)
