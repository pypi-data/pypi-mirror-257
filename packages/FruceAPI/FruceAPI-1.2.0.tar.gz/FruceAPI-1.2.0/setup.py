import setuptools
with open(r'M:\PyPl\FRAPI\README.md', 'r', encoding='utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name='FruceAPI',
	version='1.2.0',
	author='kotvpalto',
	author_email='kotvpaltoof@ya.u',
	description='',
	long_description=long_description,
	long_description_content_type='text/markdown',
	packages=['FruceAPI'],
	install_requires=["aiohttp"],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)