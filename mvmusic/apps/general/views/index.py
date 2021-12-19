from flask import redirect, url_for


def index_view():
    return redirect(url_for('subsonic_api.ping_view'))
