from setuptools import find_packages
from setuptools import setup

setup(
    name='flappy-ball',
    version='1.0.0',
    description='Flappy ball',
    author='Blake Ellsworth',
    author_email='DTNevaeha@gmail.com',
    url='https://github.com/DTNevaeha/flappy_bird',
    packages=find_packages(),
    entry_point={
        'console_scripts': [
            'flappy-ball-cli = flappy_ball.main:main',
        ]
    }
)
