from mvmusic.models.library import Library


def library_serializer(library: Library):
    return {
        'id': library.id_,
        'name': library.name
    }
