from setuptools import setup, find_packages


setup(
      name='dreamcode-task-manager',
      version='0.1',
      description='This application is a universal manager that combines the functions of a contact, note, event and file manager to conveniently manage various aspects of information.',
      packages=find_packages(where='src'),
      author='Dreamcode team, Vitaliy Nerg, Omelchenko Anton, Artem Hrytsay, Serhii Nozhenko, Muzychuk Vadym',
      author_email='occultnerg2@gmail.com, omelchenko230783@gmail.com, artem_madrid@hotmail.com, neprokaren41@gmail.com, gr.fyntik@gmail.com',
      package_dir={'': 'src'},
      url='',
      license='MIT',
      install_requires=[
            'tabulate==0.9.0',
      ],
      entry_points='''
            [console_scripts]
            manager=bot:run
      ''',
)
