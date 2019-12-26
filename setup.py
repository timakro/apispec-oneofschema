from setuptools import setup

setup(name='apispec-oneofschema',
      version='2.1.1',
      license='LGPLv3',
      description='Plugin for apispec providing support for '
                  'Marshmallow-OneOfSchema schemas',
      author='Tim Schumacher',
      author_email='tim@timakro.de',
      url='https://github.com/timakro/apispec-oneofschema',
      install_requires=[
          'apispec>=1.0.0',
          'marshmallow<4.0.0',
          'marshmallow-oneofschema'
          ],
      py_modules=['apispec_oneofschema.plugin']
      )
