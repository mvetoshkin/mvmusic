from mvmusic.libs import omit_nulls
from mvmusic.models.user import User


def user_serializer(user: User):
    resp = {
        'username': user.username,
        'scrobblingEnabled': False,
        'adminRole': user.is_admin,
        'settingsRole': True,
        'downloadRole': True,
        'uploadRole': False,
        'playlistRole': True,
        'coverArtRole': False,
        'commentRole': False,
        'podcastRole': False,
        'streamRole': True,
        'jukeboxRole': False,
        'shareRole': False,
        'folder': [i.id_ for i in user.libraries]
    }

    return omit_nulls(resp, {
        'username',
        'adminRole',
        'settingsRole',
        'downloadRole',
        'uploadRole',
        'playlistRole',
        'coverArtRole',
        'commentRole',
        'podcastRole',
        'streamRole',
        'jukeboxRole',
        'shareRole'
    })
