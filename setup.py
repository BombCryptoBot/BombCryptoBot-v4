from setuptools import setup
from Cython.Build import cythonize

setup(
	name='Bombcrypto Bot Cluster',
    version = '1.6.0',
	description = 'BombCrypto all-in-one bot. It allows you to run multiple accounts fully automated.',
	author = 'Robot Doc.',
	author_email = 'agnebgrandao@gmail.com',
	url = 'https://discord.gg/BombCryptoBot',
	packages = [],
	ext_modules=cythonize(['bombcryptobot.py', 'functions.py'])
)
