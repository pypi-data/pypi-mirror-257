from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='TilesetParser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.0.5',
    packages=find_packages(),
    install_requires=[
        "certifi==2023.7.22",
        "charset-normalizer==2.1.1",
        "decorator==5.1.1",
        "docutils==0.20.1",
        "idna==3.4",
        "imageio==2.34.0",
        "importlib-metadata==7.0.1",
        "jaraco.classes==3.3.1",
        "keyring==24.3.0",
        "lazy_loader==0.3",
        "markdown-it-py==3.0.0",
        "mdurl==0.1.2",
        "more-itertools==10.2.0",
        "networkx==3.2.1",
        "nh3==0.2.15",
        "numpy==1.26.4",
        "opencv-python==4.9.0.80",
        "packaging==23.2",
        "pillow==10.2.0",
        "pkginfo==1.9.6",
        "plac==1.3.5",
        "portainer-cli==0.3.0",
        "Pygments==2.17.2",
        "readme-renderer==42.0",
        "requests==2.28.1",
        "requests-toolbelt==1.0.0",
        "rfc3986==2.0.0",
        "rich==13.7.0",
        "scikit-image==0.22.0",
        "scipy==1.12.0",
        "tifffile==2024.2.12",
        "twine==5.0.0",
        "urllib3==1.26.13",
        "validators==0.20.0",
        "zipp==3.17.0",
    ],
    entry_points={
        'console_scripts': [
            'tilesetparser=TilesetParser.main:main',
        ],
    },
)
