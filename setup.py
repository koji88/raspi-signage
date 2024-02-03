from setuptools import setup, find_packages

setup(name='raspi-signage',
      version='0.0.8',
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
          'pyyaml<6.0',
          'pexpect',
          'requests<2.28',
          'twisted',
          'zope.interface<=3.6.0'
      ],
)
