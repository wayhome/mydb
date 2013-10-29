from setuptools import setup, find_packages
import os
classifiers = [
    "Programming Language :: Python",
    'Environment :: Web Environment',
    'License :: OSI Approved :: BSD License',
]

version = '0.1.2'
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='mydb',
      version=version,
      description='db wrapper for mysql',
      long_description=README,
      classifiers=classifiers,
      keywords='orm mysql',
      author='Young King',
      author_email='yanckin@gmail.com',
      url='https://github.com/youngking/mydb',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      test_suite='nose.collector',
      tests_require=['Nose'],
      zip_safe=False,
      install_requires=[
          'setuptools',
          'mysql-python',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
