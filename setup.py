import re

from setuptools import find_packages, setup

with open('./mvmusic/version.py') as file:
    version = re.search(r'version = \'(.*?)\'', file.read()).group(1)

setup(
    name='mvmusic',
    version=version,
    author='Mikhail Vetoshkin',
    author_email='mikhail@vetoshkin.dev',
    description='Simple music library',
    url='https://git.vetoshkin.dev/mvmusic/',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mvmusic = mvmusic:main'
        ]
    },
    install_requires=[
        'alembic == 1.7.5',
        'bcrypt == 3.2.0',
        'click == 8.0.3',
        'flask == 2.0.2',
        'flask-cors == 3.0.10',
        'mutagen == 1.45.1',
        'pillow == 9.0.0',
        'psycopg2 == 2.9.2',
        'python-dateutil == 2.8.2',
        'python-dotenv == 0.19.2',
        'requests == 2.27.1',
        'shortuuid == 1.0.8',
        'sqlalchemy == 1.4.28',
    ],
    python_requires='>= 3.9',
)
