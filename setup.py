from setuptools import setup

setup(
    name="pix",
    version="0.1.0",
    packages=["Pix"],
    entry_points={"console_scripts": ["px = Pix.__main__:main"]},
)
