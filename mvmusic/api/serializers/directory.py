from mvmusic.api.serializers.child import child_serializer
from mvmusic.libs import omit_nulls


def directory_serializer(directory, children):
    resp = {
        "id": directory.id,
        "parent": directory.parent_id,
        "name": directory.name,
        "child": [child_serializer(i) for i in children]
    }

    return omit_nulls(resp, {"name"})
