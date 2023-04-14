from setuptools import setup

setup(name='tutorial',
      entry_points={
          'scrapy.commands': [
              'gg=tutorial.commands:MyCommand',
          ],
      },
      )

