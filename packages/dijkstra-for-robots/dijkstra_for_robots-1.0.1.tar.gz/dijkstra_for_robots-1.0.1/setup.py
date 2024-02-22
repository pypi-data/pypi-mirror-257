from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='dijkstra_for_robots',
    version='1.0.1',
    author='latwiks',
    author_email='latwiks@vk.com',
    url='https://github.com/latwiks/dijkstra_for_robots',
    description='Система навигации робота по глобальной карте.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['networkx>=3.2.1', 'matplotlib>=3.8.3'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    project_urls={
        'GitHub': 'https://github.com/latwiks/dijkstra_for_robots'
    },
    keywords='dijkstra robot robots дейкстра дейкстры робот алгоритм библиотека путь пути',
    python_requires='>=3.11'
)