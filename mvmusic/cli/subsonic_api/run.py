import click

from mvmusic.apps.subsonic_api.helpers.appfactory import create_app


@click.command('run')
@click.option('--host', '-h', help='The interface to bind to')
@click.option('--port', '-p', help='The port to bind to')
def run_(host, port):
    """Run a development server"""

    app = create_app()
    app.run(host=host, port=port, load_dotenv=False)
