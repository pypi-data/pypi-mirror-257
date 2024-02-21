# Xray Uploader

## usage

looks like this:
```
from xray import Uploader

result_file = "res.xml"
summary = "automation test"
project_id = "12345"
result_format = "junit"

upl = Uploader({client_id}, {client_secret})
upl.import_execution(result_file, summary, project_id, result_format)
```
