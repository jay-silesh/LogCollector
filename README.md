LogCollector

### Sample Curl Commands

Happy path with all default params
```bash
curl http://localhost:8000/logs/\?file\=daily.out
```

Bad Request with no "required" param (i.e. fileName)
```bash
curl http://localhost:8000/logs/\?badparam\=daily.out\&count\=10
```

Happy path with all params
```bash
curl http://localhost:8000/logs/\?file\=daily.out\&count\=15\&keywords\=blah,blah2,blah3
```

File Not found
```bash
curl http://localhost:8000/logs/\?file\=file_not_exists\&count\=15\&keywords\=blah,blah2,blah3
```

Happy path with only keywords
```bash
curl http://localhost:8000/logs/\?file\=daily.out\&keywords\=blah,blah2,blah3
```

Happy path with only count
```bash
curl http://localhost:8000/logs/\?file\=daily.out\&count\=10
```

Happy path with = FileName + Count + Offset + Keywords
```commandline
curl http://localhost:8000/logs/\?file=daily.out&count=60&keywords=blah,blah2,blah3&offset=5000
```