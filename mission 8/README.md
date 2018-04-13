Intern-Life
# My intern assignments at XXX.

## Mission 
* Accomplished on 
* Modified on 
* Duration: 
http://10.79.148.226:9116/apps/envsetup_port/modules/if_list/index.html

https://github.com/WangHong-yang/Vue.js-Search-Highlight

## Description
```javascript
//hightlight
var cell = document.getElementsByTagName('tbody')[0]
width = cell.rows[0].cells.length //表格宽度15
height = cell.rows.length// 这个是表格高度 5
for (var w = 0; w < width; w++)
    for (var h = 0; h < height; h++)
        cell.rows[h].cells[w].innerHTML = cell.rows[h].cells[w].innerText.replace(keywords, '<span class="_p-filter-matched">' + keywords + '</span>')
///highlight
```


226    9117


webterminal boc 
## Steps
/home/project/WebTerminal_BOC/apps
-->
/home/project/frontend/verification/WebTerminal


## Errors


## Suggestions by mentor(s)

## Suggestions by myself

1. crontab定期重启程序，apscheduler定期新建连接
回家种田吧

2. 增加wait_timeout时间
既不治标也不治本，可能降低服务器性能

3. 每次刷新页面都新建连接-查询-关闭连接
切实可行，性能稍差

4. 死循环捕获错误
引入了更多的问题，包括但不限于多线程、多进程、线程安全、连接池。这样还是回家养猪吧。

5. 数据库的操作之前con.reconnect()
```python
con.reconncet()
# 数据库操作
```
方案3的改进版，性能稍有损失

6. 数据库操作时try...except，异常重连
```python

try:
    cur.execute('select version()')
except mysql.connector.errors.OperationalError:
        con.reconnect()
finally:
        get_data()

```
还是有一个没用的查询语句。

7. 数据库操作之前进行con.ping()，异常重连
```python

try:
    con.ping()
except mysql.connector.errors.InterfaceError:
    con.reconnect()
finally:
    get_data()

```
完美了。

## Afterwards

## Notes
