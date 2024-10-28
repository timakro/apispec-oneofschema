from setuptools import setup

setup(name='apispec-oneofschema',
      version='3.0.1',
      license='MIT',
      description='Plugin for apispec providing support for '
                  'Marshmallow-OneOfSchema schemas',
      author='Tim Schumacher',
      url='https://github.com/timakro/apispec-oneofschema',
      install_requires=[
          'apispec>=3.0.0',
          'marshmallow<4.0.0',
          'marshmallow-oneofschema'
          ],
      py_modules=['apispec_oneofschema.plugin']
      )
