from setuptools import setup, find_packages

setup(name='raspi-signage',
      version='0.0.7',
      description='Digital Signage by Raspberry PI',
      author='Koji Hachiya',
      author_email='koji.hachiya@gmail.com',
      url='https://github.com/koji88/raspi-signage/',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      raspi-signage = raspi_signage.main:main
      raspi-signage-remote = raspi_signage.remote:main
      """,
      install_requires=[
          'sysfs-gpio',
          'pexpect',
          'requests'
      ],
)
