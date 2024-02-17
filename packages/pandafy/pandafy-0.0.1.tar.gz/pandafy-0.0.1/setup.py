from setuptools import setup, find_packages

setup(
    name='pandafy',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    author='Daniel Zamanski',
    author_email='daniel.zamanski@gmail.com',
    description='A simple library designed to turn ROS2 .db3 files into regular pd.DataFrame',
    url='https://github.com/DanielZamanski/bag_to_df',
)