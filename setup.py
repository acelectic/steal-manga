from setuptools import setup

__version__ = "0.0.15"

setup(
   name="steal-manga",
   version=__version__,
   include_dirs= ["./libs", "./web", "./config", "./files"]
   # And so on...
)