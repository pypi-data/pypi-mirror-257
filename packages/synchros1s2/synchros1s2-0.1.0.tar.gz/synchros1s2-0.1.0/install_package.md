# Installation package
Bienvenue ! Ce fichier te permettera d'installer le package python
#

## Ajouter un dossier __init__.py 
Pour que python reconnaîtra les répertoires comme des packages, faut rajouter dans chaque dossier un fichier _init_.py vide.

## Configurer le fichier pyproject.toml 
Ce fichier permet de définir le nom du package, les dépendances...

## Mettre à jour la version du package
```bash
python3 -m pip install setuptools-scm
```

## Générer les archives de distribution

Un fichier d'archive versionné qui contient des paquets Python, des modules et d'autres fichiers de ressources utilisés pour distribuer une version. 
Le fichier d'archive est ce que l'utilisateur final téléchargera depuis Internet et installera.
```bash
    python3 -m pip install --upgrade build 
```
Maintenant executez cette commande ou existe le dossier pyproject.toml :  
```bash
    python3 -m build
```
La commande va générer 2 fichiers dans le dossier dist :

* ├── example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
* └── example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz

## Télécharger les archives de distribution
```bash
    python3 -m pip install --upgrade twine
```
```bash
    python3 -m twine upload --repository pypi dist/*
```
Vous serez invité à saisir un nom d'utilisateur et un mot de passe. 
Pour le nom d'utilisateur, utilisez __token__. Pour le mot de passe, utilisez la valeur du jeton, y compris le préfixe pypi-.
Une fois la commande terminée, vous devriez voir un résultat semblable à celui-ci :
Uploading distributions to https://test.pypi.org/legacy/
Enter your username: __token__
* Uploading example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl 
  100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.2/8.2 kB • 00:01 
* Uploading example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
  100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.8/6.8 kB • 00:00 

## Installer le package
```bash
  
```