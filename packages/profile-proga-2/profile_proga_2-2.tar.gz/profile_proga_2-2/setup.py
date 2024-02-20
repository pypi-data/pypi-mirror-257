from setuptools import setup, find_packages

setup(
    name='profile_proga_2',
    version='2',
    packages=find_packages(),
    author='Баталыгин Геннадий',
    author_email='861212@mail.ru',
    description='Программа создана для построения профиля скважины в трехмерном пространстве с последующей визуализацией и возможности сравнения. Загружается 2 профиля (факт и план) в ексель файл.',
    install_requires=[
        'package1',
        'package2',
    ],
)
