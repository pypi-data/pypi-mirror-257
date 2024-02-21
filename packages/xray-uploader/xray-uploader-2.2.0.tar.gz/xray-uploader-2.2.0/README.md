# Xray Uploader

## usage

looks like this:
```
from xray import Uploader

xml = "res.xml"
summary = "automation test"
project_id = "12345"

upl = Uploader({client_id}, {client_secret})
upl.import_execution(xml, summary, project_id, safe_mode=True)
```
