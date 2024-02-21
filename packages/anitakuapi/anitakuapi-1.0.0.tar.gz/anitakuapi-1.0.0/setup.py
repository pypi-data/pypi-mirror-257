with open("README.md", encoding="utf8") as readme:
    LONG_DESCRIPTION = readme.read()

from setuptools import setup

VERSION = "1.0.0"
DESCRIPTION = "Python wrapper for the Anitakuapi"

setup(
    name="anitakuapi",
    version=VERSION,
    license="MIT",
    author="zawlay",
    author_email="zawlay134594@gmail.com",
    long_description_content_type="text/markdown",
    url="https://github.com/N-SUDY/AnitakuapiX",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=["anitakuapi"],
    install_requires=["requests"],
    keywords=[
        "API",
        "AnitakuApi",
        "Aniapi",
        "Anibot",
        "GogoAnime",
        "Anime",
        "AnimeAPI",
        "Scrapper",
    ],
)
