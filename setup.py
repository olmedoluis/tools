from setuptools import setup

setup(
    name="pix",
    version="0.1.0",
    packages=["Pix", "Configuration"],
    entry_points={"console_scripts": ["px = Pix.__main__:main"]},
    author="Luis Olmedo",
    author_email="olmedoluis012@gmail.com",
    description="Better GIT cli interface",
    project_urls={"Source Code": "https://github.com/olmedoluis/pix",},
)
