from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='rpa_hypercoe',
    version='0.2.4',
    license='MIT License',
    author='Joao Buso',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author_email='developer@hypercoe.com',
    keywords='rpa hypercoe log tria software',
    description=u'Repositorio para a utilização da API de Log do HyperCoe',
    packages=['rpa_hypercoe'],
    install_requires=['requests'],)