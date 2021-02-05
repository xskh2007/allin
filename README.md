# allin  

[后端步骤](https://github.com/xskh2007/allin/blob/main/docs/allin.md)  

[前端步骤](https://github.com/xskh2007/allin/blob/main/docs/vue-admin-template.md)

```pip install mysqlclient  
pip install djangorestframework-jwt  
pip install djangorestframework  
git add .  
git commit -m "hi"  
git push -u origin main  
python manage.py makemigrations
python manage.py migrate
python3 manage.py createsuperuser




```


### git 提交
我从master分支创建了一个issue5560分支，做了一些修改后，使用git push origin master提交，但是显示的结果却是'Everything up-to-date'，发生问题的原因是git push origin master 在没有track远程分支的本地分支中默认提交的master分支，因为master分支默认指向了origin master 分支，这里要使用git push origin issue5560：master 就可以把issue5560推送到远程的master分支了。

    如果想把本地的某个分支test提交到远程仓库，并作为远程仓库的master分支，或者作为另外一个名叫test的分支，那么可以这么做。
```
$ git push origin test:master         // 提交本地test分支作为远程的master分支 //好像只写这一句，远程的github就会自动创建一个test分支
$ git push origin test:test              // 提交本地test分支作为远程的test分支
```

如果想删除远程的分支呢？类似于上面，如果:左边的分支为空，那么将删除:右边的远程的分支。  

```
$ git push origin :test              // 刚提交到远程的test将被删除，但是本地还会保存的，不用担心
```