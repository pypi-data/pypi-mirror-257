from setuptools import setup, find_packages

setup(
    name='synchros1s2',
    version='0.0.7',
    packages=find_packages(),  # Recherche tous les packages dans le répertoire courant
    install_requires=[
        'requests',
        'SQLAlchemy',
        'pytest',
        'setuptools'
    ],
    author='wefine',
    author_email='wefine2529@ebuthor.com',
    description='Mon package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[  # Liste de classifications pour votre package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
