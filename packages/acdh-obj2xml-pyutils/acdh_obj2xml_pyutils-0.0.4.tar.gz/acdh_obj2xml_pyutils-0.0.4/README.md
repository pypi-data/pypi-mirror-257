[![flake8 Lint](https://github.com/acdh-oeaw/acdh-obj2xml-pyutils/actions/workflows/lint.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-obj2xml-pyutils/actions/workflows/lint.yml)
[![Test](https://github.com/acdh-oeaw/acdh-obj2xml-pyutils/actions/workflows/test.yml/badge.svg)](https://github.com/acdh-oeaw/acdh-obj2xml-pyutils/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/acdh-oeaw/acdh-obj2xml-pyutils/branch/main/graph/badge.svg?token=UWZNV66TC2)](https://codecov.io/github/acdh-oeaw/acdh-obj2xml-pyutils)

# acdh-obj2xml-pyutils
python library to parse BaseRowClient of acdh-baserow-pyutils or any array of objects.

# HowTo developer

* create python environment `python -m venv env`
* install `pip install acdh_obj2xml_pyutils` (not yet published)
* install `pip install acdh_baserow_pyutils` (not yet published)
* create python file e.g. `run.py`

## add code

```python
from acdh_obj2xml_pyutils import ObjectToXml


br_input = [{"id": "test1", "filename": "test1"},{"id": "test2", "filename": "test2"}]
tei = ObjectToXml(br_input=br_input)
output = [x for x in tei.make_xml(save=True)]
print(output)
```

with BaseRowClient

```python
from acdh_obj2xml_pyutils import ObjectToXml
from acdh_baserow_pyutils import BaseRowClient

br_client = BaseRowClient(br_base_url="add url", br_table_id='add id', br_token='add token')
br_input = [x for x in br_client.yield_rows()]
tei = ObjectToXml(br_input=br_input)
output = [x for x in tei.make_xml(save=True)]
print(output)
```

both versions will create an 'out' directory containing xml files. Important Note! To create filenames the data input must contain a variable with filennames. Default variable is called 'filename' but can be customized by providing an argument to class ObjectToXml().

## Arguments

* br_input `data input as array of objects`
* save_dir `default out as string`
* filename `variable for filenames as string`
* template_path `path for jinja2 template`
