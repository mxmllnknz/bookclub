from distutils.core import setup

setup(name='bookclub',
      version='0.1.1',
      description='Python Discord Book Club Bot',
      author='Max Kunz',
      author_email='mkunz778@gmail.com',
      packages=['bot','bot.database', 'bot.models'],
     )