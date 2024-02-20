from setuptools import setup, find_packages

setup(
    name='preAudioProcessing',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'setuptools~=65.5.1',
        'pydub~=0.25.1',
        # Add other dependencies if needed
    ],
    entry_points={
        'console_scripts': [
            'mycommand = preAudioProcessing.__init__:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
    author='Lasha Pantskhava',
    author_email='lasha.pantskhava11@gmail.com',
)
