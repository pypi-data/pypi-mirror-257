from setuptools import setup, find_packages

setup(
    name='audiotranscription',
    version='0.1.0',
    packages=['audiotranscription'],
    install_requires=[
        'numpy',
        'pyannote.audio',
        'pandas',
        'deepmultilingualpunctuation',
        'openai-whisper',
        'google-cloud-speech',
        # List your dependencies here
    ],

)