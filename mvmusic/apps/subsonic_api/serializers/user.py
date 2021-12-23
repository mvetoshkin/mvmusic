def user_serializer(user):
    return {
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
        'folder': [i.id_ for i in user.music_libraries]
    }
