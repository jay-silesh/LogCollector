LogCollector

## Assumption
1. Test cases & Documentations are not written in the interest of time. 
2. Required python 3.0+ for running the server
3. Initializes virtualEnv to hide installations of packages, etc.
4. Bonus Question to implement the MasterServer has been implemented. 

> TIP: Open this file on the PyCharm ide and you can run the below commands and see the test cases. 


## Starting the Python Server
> NOTE: the same server is started for master and child nodes.

Activate VirtualEnv and install the required packages. 
```shell
source virtenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start Master Sever
```shell
source virtenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/server.py -p 8000
```

Start Child Sever
```shell
source virtenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/server.py -p 8001 
```
```shell
source virtenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python src/server.py -p 8002 
```

## Sample Curl Commands for Part1

Happy path with all default params
```shell
curl http://localhost:8000/logs/\?file\=daily.out
```

Bad Request with no "required" param (i.e. fileName)
```shell
curl http://localhost:8000/logs/\?badparam\=daily.out\&count\=10
```

Happy path with all params
```shell
curl http://localhost:8000/logs/\?file\=daily.out\&count\=15\&keywords\=Link,utun
```

Happy path with all params (with keywords not matching)
```shell
curl http://localhost:8000/logs/\?file\=daily.out\&count\=15\&keywords\=vdsihvdoisuh
```

File Not found
```shell
curl http://localhost:8000/logs/\?file\=file_not_exists\&count\=15\&keywords\=Link,utun
```

Happy path with only keywords
```shell
curl http://localhost:8000/logs/\?file\=daily.out\&keywords\=Link,utun
```

Happy path with only count
```shell
curl http://localhost:8000/logs/\?file\=daily.out\&count\=10
```

Happy path with = FileName + Count + Offset + Keywords
```shell
curl http://localhost:8000/logs/\?file=daily.out&count=60&keywords=Link,utun&offset=5000
```

## Sample Curl Commands for Part2

Issue request to master node
```shell
curl http://localhost:8000/logs/aggregate/?file=daily.out&count=60&offset=6887&servers=localhost:8001,localhost:8002
```
