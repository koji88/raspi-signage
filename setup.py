from setuptools import setup, find_packages

setup(name='rspi-signage',
      version='0.0.6',
      description='Digital Signage by Raspberry PI',
      author='Koji Hachiya',
      author_email='koji.hachiya@gmail.com',
      url='https://github.com/koji88/rspi-signage/',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      rspi-signage = rspi_signage.main:main
      rspi-signage-remote = rspi_signage.remote:main
      """,
      install_requires=[
          'sysfs-gpio',
          'pexpect',
          'requests'
      ],
)
