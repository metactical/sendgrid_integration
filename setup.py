from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sendgrid_integration/__init__.py
from sendgrid_integration import __version__ as version

setup(
	name="sendgrid_integration",
	version=version,
	description="Frappe Integration for Sendgrid",
	author="Nigmacorp",
	author_email="tripleo4u@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
