Intern-Life
# My intern assignments at XXX

## Mission 1
* Accomplished on 1st Sep 2017
* Modified on 9th Sep 2017 (Only errors has been corrected)
* Duration: about 1 day and two hours.


## Description
Parse the csv file and import it to MySQL


## Steps
No steps.


## Errors
* did not close file handler.


## Suggestions by mentor(s)
* use % to construct string
* use `if __name__=='__main__'`
* use `with` instead of `open`
* use `mysql.connector` instead of `MySQLdb`
* for list, prefer `append`
* `os.path.join()`


## Suggestions by myself
* use `cur.execute('select * from table1 where id=%s',var)` to prevent from SQL Injection


## Notes
* use `%` and be prepared for SQL Injection.
* clean code.