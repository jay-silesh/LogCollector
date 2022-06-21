LogCollector

## Starting the Python Server
#### NOTE: the same server is started for master and child nodes.

Activate VirtualEnv and install the required packages. 
```shell
source virtenv/bin/activate
python -m pip install --upgrade pip
```

```shell

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
curl http://localhost:8000/logs/\?file\=daily.out\&count\=15\&keywords\=blah,blah2,blah3
```

File Not found
```shell
curl http://localhost:8000/logs/\?file\=file_not_exists\&count\=15\&keywords\=blah,blah2,blah3
```

Happy path with only keywords
```shell
curl http://localhost:8000/logs/\?file\=daily.out\&keywords\=blah,blah2,blah3
```

Happy path with only count
```shell
curl http://localhost:8000/logs/\?file\=daily.out\&count\=10
```

Happy path with = FileName + Count + Offset + Keywords
```shell
curl http://localhost:8000/logs/\?file=daily.out&count=60&keywords=blah,blah2,blah3&offset=5000
```

## Sample Curl Commands for Part2

Issue request to master node
```shell
curl http://localhost:8000/logs/aggregate/?file=daily.out&count=60&offset=6887&servers=localhost:8001,localhost:8002
```
