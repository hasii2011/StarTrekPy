"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['org/hasii/pytrek/albow/AlbowMain.py']
DATA_FILES = []
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    packages=['org.hasii.pytrek', 'org.hasii.pytrek.albow',
              'org.hasii.pytrek.engine', 'org.hasii.pytrek.engine.futures',
              'org.hasii.pytrek.gui', 'org.hasii.pytrek.gui.gamepieces',
              'org.hasii.pytrek.objects',
    ],
    options={'py2app': OPTIONS},

    url='https://github.com/hasii2011/StarTrekPy',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='Yet another classic Star Trek game re-written in Python and Pygame',
    setup_requires=['py2app'],
    install_requires=['pygame', 'python3-albow', 'jsonpickle']

)
