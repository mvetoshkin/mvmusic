from mvmusic.libs import omit_nulls


def user_serializer(user):
    resp = {
        'folder': [i.id_ for i in user.libraries],
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
        'videoConversionRole': False
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
        'shareRole',
        'videoConversionRole'
    })
