from setuptools import setup, find_packages
setup(
name='mintutils',
version='0.0.5',
author='Muhiris (Muhammad Haris)',
author_email='muhammadharis786@protonmail.com',
description='A beginner friendly app to install all essential softwares on Debian based linux to keep the productivity high.',
packages=find_packages(),
entry_points={
        'console_scripts': [
            'mintutils = mintutils.__init__:main',
        ],
},
url='https://github.com/muhiris/debutils',
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
keywords=['debian', 'linux', 'productivity', 'utilities', 'installer', 'vim', 'hotspot', 'hello', 'snapd', 'google-chrome', 'slack', 'vlc', 'zoom', 'vscode', 'postman', 'discord', 'spotify', 'telegram', 'obs-studio', 'freetube', 'signal', 'brave', 'firefox', 'youtube-dl', 'qbittorrent', 'pycharm', 'intellij', 'android-studio', 'wifi-hotspot', 'wireshark', 'video-stream', 'camera-stream', 'sockets'], 
python_requires='>=3.6',
)


 