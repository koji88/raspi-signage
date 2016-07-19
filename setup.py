from setuptools import setup, find_packages

setup(name='rspi-signage',
      version='0.0.2',
      description='Digital Signage by Raspberry PI',
      author='Koji Hachiya',
      author_email='koji.hachiya@gmail.com',
      url='https://github.com/koji88/rspi-signage/',
      packages=find_packages(),
      entry_points="""
      [console_scripts]
      rspi-signage = scripts.main:main
      """,
      install_requires=[
          'sysfs-gpio',
          'pexpect'
      ],
)
