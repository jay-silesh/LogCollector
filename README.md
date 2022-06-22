LogCollector

## Assumption
1. Test cases & Documentations are not written in the interest of time. 
2. Required python 3.0+ for running the server
3. Initializes virtualEnv to hide installations of packages, etc.
4. Bonus Question to implement the MasterServer has been implemented. 

> TIP: Open this file on the PyCharm ide and you can run the below commands and see the test cases.


## Request & Response
### Local Server
Request:
```
http://localhost:8000/logs/?file=daily.out&count=60&keywords=Link,utun&offset=5000   
```
file (required): 
    - name of the log file (defaults to a prefix with /var/log/ in the local unix system)
count (optional): 
    - number of logs requested. Defaults to Count=20 or MaxCount=50 if specified in request
Keywords (optional): 
    - Set of words to be filtered by and is separated by "," as delimiter between words
offset (optional): 
    - Mainly used for pagination.
    - Next set of the logs to traverse (from descending order) if requested count is more than MaxCount.
    - The offset is returned to the response if requested count > MaxCount for pagination.


Response:
```
{
    logs: [
        log1,
        log2
    ],
    offset: 123
} 
```
logs: List of logs
offset (optional): If the logs are paginated, this field will be included in the response. 

### Master Server
Request:
```
http://localhost:8000/logs/aggregate/?file=daily.out&count=60&offset=6887&servers=localhost:8001,localhost:8002   
```
servers (required):
    - Set of servers to be fetched from and is separated by "," as delimiter between different servers
file (required): 
    - name of the log file (defaults to a prefix with /var/log/ in the local unix system)
count (optional): 
    - number of logs requested. Defaults to Count=20 or MaxCount=50 if specified in request
Keywords (optional): 
    - Set of words to be filtered by and is separated by "," as delimiter between words
offset (optional): 
    - Mainly used for pagination.
    - Next set of the logs to traverse (from descending order) if requested count is more than MaxCount.
    - The offset is returned to the response if requested count > MaxCount for pagination.


Response:
```
{
    server_name: {
        status_msg: "Partial Content",
        status_code: 206,
        logs: [
            log1,
            log2
        ],
        offset: 123
    },
    {
    }
} 
```
Response are a Map of response from each server with name of the server as the key
logs: List of logs
offset (optional): If the logs are paginated, this field will be included in the response.


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
