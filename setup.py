from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in gada_electronics/__init__.py
from gada_electronics import __version__ as version

setup(
	name="gada_electronics",
	version=version,
	description="We sell electronic products",
	author="H404",
	author_email="gada.electronics@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
