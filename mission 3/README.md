Intern-Life
# My intern assignments in ***REMOVED***

## Mission 
* Accomplished on 26th Sep 2017
* Modified on 
* Duration: 3 days or so


## Description
* generate an csv file which contains 100,0000 random IP address, i.e. 192.0.2.131/28
* read that csv file and parse each IP's network address, i.e. 192.0.2.128/28, then write it back to a file.
* use threading technique
* use multiprocessing

## Steps
### Decorator - test performance
`from measurement import exe_time`
### multiprocessing technique, use Queue to communicate
**Probably wrong**
```
	q = Manager().Queue()
    pool = Pool()
    pool.apply_async(read_csv, args=(q,))
    pool.apply_async(write_csv, args=(q,))
    pool.close()
    pool.join()
```
or the simple one
```
p=Process(target=read_csv, args=(q,))
p.start()
```
### Threading
**Probably wrong**
```
t = threading.Thread(target=test, args=(i,))
t.start()
```

## Errors


## Suggestions by mentor(s)


## Suggestions by myself


## Afterwards

## Notes
Reference to git-like checker, with threading technique, which is much more quicker than the old one.