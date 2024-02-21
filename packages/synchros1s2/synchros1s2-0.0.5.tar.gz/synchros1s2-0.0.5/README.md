# sync2jira

## Importer le package


- [ ] [Importer](https://gitlab.com/ex-novo-team/sync2jira/) projet

```
cd existing_repo
git remote add origin https://gitlab.com/ex-novo-team/sync2jira.git
git branch -M package
git push -uf origin package
```


## Tester le package 
Dans un autre projet test executer la commande suivante : 
```
 pip install synchros1s2
```

## Remplir le fichier de config 
Déplacer le fichier de config dans votre projet de test et le remplir. 
Ce script Python configure plusieurs variables et paramètres nécessaires pour Jira. Il définit des chemins de fichiers, des formats de journalisation, des informations d'authentification et des URL Jira.
