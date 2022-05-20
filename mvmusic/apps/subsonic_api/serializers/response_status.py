def reponse_status_serializer(status):
    return 'ok' if 200 <= status < 400 else 'failed'
