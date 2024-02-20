from setuptools import setup

setup(name='tomcru_jerry',
      version='0.1.4',
      description='General purpose web library',
      url='https://github.com/dkgs/tomcru-jerry',
      author='oboforty',
      author_email='rajmund.csombordi@hotmail.com',
      license='MIT',
      zip_safe=False,
      package_dir={'': 'tomcru_jerry'},
      install_requires=[
          'flask',
      ],
      extras_require={
          'static': [
              "flask"
              "pynliner"
              "beautifulsoup4"
              "htmlmin"
              "jinja2"
          ]
      })
