from setuptools import setup, find_packages

version = '0.1'

setup(name='labraise.skin',
      version=version,
      description="La braise skin",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='braise skin theme affinitic',
      author='Affinitic Sprl',
      author_email='info@affinitic.be',
      url='http://www.restolabraise.be',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['labraise'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
