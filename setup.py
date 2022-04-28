from setuptools import setup, find_packages

setup(name='Qwall_Game',
      version='1.0',
      packages=find_packages(),
      install_requires=['numpy==1.22.3',
                        'tensorflow==2.8.0',
                        'Pillow==9.1.0',
                        'pygame==2.1.2',
                        'opencv-python==4.5.5.64',
                        'tqdm-4.64.0'])
