## websyx-t0 ==> XML exchamger between shops & 
## XML

### Errors /error management
Nincs hibakezeles - most meg azt sem tudom, hogy hol, milyen hibak lesznek
log.error ...
logViewer XML 

### LOGGINg
save in/out xmlDATA to files
log WARNING/INFO messages

### EMAG ???
Kurvara kesobb jon, pillanatnyilag nem tom, mit akarok vele ...

### git merge test to origin/master

[Git merge dev to main](https://www.geeksforgeeks.org/git/how-to-merge-a-git-branch-into-master/)
```
  501  git status 
  502  git checkout main
  503  git pull origin master
  504  git pull origin main
  505  git checkout dev-i18n
  506  git pull origin main
  507  git checkout main
  508  git merge dev-i18n
```  

```
git checkout master
git pull origin master
git merge test
git push origin master
```
```
git checkout master
git pull
git checkout test
git pull
git rebase -i master
git checkout master
git merge test
```