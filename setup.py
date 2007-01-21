from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='plone.app.contentrules',
      version=version,
      description="Plone integration for plone.contentrules",
      long_description="""\
""",
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Markus F\xc3uhrer',
      author_email='mfuhrer@gmx.net',
      url='http://svn.plone.org/svn/plone/plone.app.contentrules',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
