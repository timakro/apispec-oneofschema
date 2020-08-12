from setuptools import setup

setup(name='apispec-oneofschema',
      version='3.0.0',
      license='LGPLv3',
      description='Plugin for apispec providing support for '
                  'Marshmallow-OneOfSchema schemas',
      author='Tim Schumacher',
      author_email='tim@timakro.de',
      url='https://github.com/timakro/apispec-oneofschema',
      install_requires=[
          'apispec>=3.0.0',
          'marshmallow<4.0.0',
          'marshmallow-oneofschema'
          ],
      py_modules=['apispec_oneofschema.plugin']
      )
