Intern-Life
# My intern assignments at XXX
I love Linux♥

## Mission 
* Accomplished on 
* Modified on 
* Duration: 


## Description
server migration.

## Steps
### yum proxy
I hate modify config file
```
vim /etc/yum.conf
proxy=socks5://127.0.0.1:1080
```
However this version of yum(3.3.29) doesn't support socks5 proxy
### iptables
iptables -I INPUT -p tcp --dport 9001 -j ACCEPT

### ssh proxy
ssh -N -f -D 127.0.0.1:1080 root@10.79.148.228
export ALL_PROXY=socks5://127.0.0.1:1080

### proxychain
```
git clone https://github.com/rofl0r/proxychains-ng
cd proxychains-ng
make && make install
cp src/proxychains.conf /etc/proxychains.conf
vim /etc/proxychains.conf
# the last line:
socks5 127.0.0.1 1080
```

usage:`proxychains4 yum install package-name`
## Errors


## Suggestions by mentor(s)
nginx reverse proxy
```
location /test 
{
    proxy_pass http://127.0.0.1:5000/;
}
```
PTR
`dig x 1.2.3.4`
## Suggestions by myself


## Afterwards

## Notes