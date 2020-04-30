"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['org/hasii/pytrek/albow/StarTrek.py']
DATA_FILES = [
              ('org/hasii/pytrek/resources/fonts', ['org/hasii/pytrek/resources/fonts/FuturistFixedWidth.ttf']),
              ('org/hasii/pytrek/resources/fonts', ['org/hasii/pytrek/resources/fonts/MonoFonto.ttf']),

              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/klingon_torpedo.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/probe_launch_1.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/ShieldHit.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/SmallExplosion.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/tng_red_alert2.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/tos_flyby_1.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/tos_inaccurateerror_ep.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/tos_photon_torpedo.wav']),
              ('org/hasii/pytrek/resources/sounds', ['org/hasii/pytrek/resources/sounds/tos_unabletocomply.wav']),

              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/BigRedX_32x32.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/EnterpriseD.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/explosion_rays_blue.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/explosion_rays_grey.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/explosion_rays_red.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/explosion_rays_white.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/GalaxyScanBackground.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/KlingonD7.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/KlingonTorpedo.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/KlingonTorpedoMiss.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/medfighter.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/QuadrantBackground.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/StarBase3.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_East.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_North.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_NorthEast.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_NorthWest.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_South.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_SouthEast.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_SouthWest.png']),
              ('org/hasii/pytrek/resources/images', ['org/hasii/pytrek/resources/images/torpedo_West.png']),

              ('org/hasii/pytrek/resources', ['org/hasii/pytrek/resources/loggingConfiguration.json']),
              ('org/hasii/pytrek/resources', ['org/hasii/pytrek/resources/pyTrek.conf']),

             ]
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    packages=['org',
              'org.hasii',
              'org.hasii.pytrek',
              'org.hasii.pytrek.albow',
              'org.hasii.pytrek.engine', 'org.hasii.pytrek.engine.futures',
              'org.hasii.pytrek.gui', 'org.hasii.pytrek.gui.gamepieces',
              'org.hasii.pytrek.objects',
              'org.hasii.pytrek.resources',
              'org.hasii.pytrek.resources.fonts',
              'org.hasii.pytrek.resources.images',
              'org.hasii.pytrek.resources.sounds'
    ],
    include_package_data=True,

    url='https://github.com/hasii2011/StarTrekPy',
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description='Yet another classic Star Trek game re-written in Python and Pygame',
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['pygame', 'python3-albow', 'jsonpickle']

)
