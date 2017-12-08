Intern-Life
# My intern assignments at XXX

## Mission 
* Accomplished on 9th Sep 2017
* Modified on 19th Sep 2017
* Duration: one day and a half


## Description
* set up MySQL and MongoDB in a minimal CentOS with password authentication.
* import sql file to MySQL
* write a Python to import data from MySQL to MongoDB
* design a Python function: query from MongoDB according to an IP address
* design a Python function: query from MongoDB according to a regex expression of device name


## Steps
### epel release
`yum install -y epel-release`
### install MySQL(Build from source)
Due to network issues, decided to build from source. `lnmp.org` one key script.
### install MongoDB(from [official repository](https://docs.mongodb.com/master/tutorial/install-mongodb-on-red-hat/))
```
vim /etc/yum.repos.d/mongodb-org-3.6.repo

#write the following content
[mongodb-org-3.6]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2013.03/mongodb-org/3.6/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-3.6.asc

#install MongoDB
yum install -y mongodb-org

#disable SELinux, choose one
semanage port -a -t mongod_port_t -p tcp 27017
#or
vim /etc/selinux/config
SELINUX=disabled
#or
SELINUX=permissive

#reboot then, or just simpley setenforce 
service mongod start
```
### MongoDB authentication
Create a root user first
```
use admin
db.createUser(
{
user: "root",
pwd: "xxx123",
roles: [ { role: "root", db: "admin" } ]
}
)
```
Enable authentication
```
vim /etc/mongod.conf

#add following content, for windows use --auth instead
security:
  authorization: enabled
  
#restart MongoDB
service mongod restart
```
### import data to MySQL
`mysql -u root -p pass db1 < test.sql`

### iptables
iptables -I INPUT -p tcp --dport 9116 -j ACCEPT
## Errors


## Suggestions by mentor(s)
* global and mostly used vars, changable variables, please add it to the front(easy to modify).
* try not to use `update`,use `dict(key1=value1,key2=value2)` for better performance and coding style.
* `close` and `del` are unnecessary
* `close` in destructor, constructor's default params.
* dict and array act more similar to `&`(reference) in cpp
* `col.insert_many()` for better performance

## Suggestions by myself


## Afterwards
* flask web interface with `GET` method query.

## Notes
* how does Pymongo generate _id? (Reference)[http://xiaoweiliu.cn/2017/06/21/pymongo-errors-DuplicateKeyError-E11000-duplicate-key-error/]
* binary install, not systemd, probably `supervisor` is the best choice.