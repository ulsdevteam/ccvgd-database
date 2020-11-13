## To run scripts:
1. Create confit.txt, put it directly under pythonScript
2. Run ```main_process.py``` to process original csv files.
3. Run ```main_load.py``` to load processed csv files into database.

* config.txt:
```
{"user": "", "password": "", "host": "", "database": ""}
```

## Package version
1. python 3.7.3
2. mysql-connector-python 8.0.21
    * [Guide to install mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/connector-python-installation.html)
3. pandas 1.1.3