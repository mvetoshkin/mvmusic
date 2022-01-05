def directory_serializer(directory, as_child=False):
    resp = {
        'id': directory.id_,
    }

    if directory.parent:
        resp['parent'] = directory.parent.id_

    if as_child:
        resp['title'] = directory.name
        resp['isDir'] = True
        resp['coverArt'] = directory.image_id

        if directory.parent:
            resp['artist'] = directory.parent.name

    else:
        resp['name'] = directory.name

    return resp
