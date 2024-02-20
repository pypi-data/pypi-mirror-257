import asyncio
import json
import jinja2
import cson

def batches(list_, n):
    return [
        list_[i:i + n]
        for i in range(0, len(list_), n)
    ]

_NOT_SPECIFIED = object()

def read_exact(file_name, default=_NOT_SPECIFIED):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        if default is _NOT_SPECIFIED:
            raise
        else:
            return default

def read(file_name, default=_NOT_SPECIFIED):
    return read_exact(file_name, default).strip()

def read_json(file_name, default=_NOT_SPECIFIED):
    return json.loads(read_exact(file_name, default))

def read_cson(file_name, default=_NOT_SPECIFIED):
    return cson.loads(read_exact(file_name, default))

def write(file_name, string):
    with open(file_name, "w", encoding="utf-8") as f:
        return f.write(string)

def write_json(file_name, object_):
    with open(file_name, "w", encoding="utf-8") as f:
        return json.dump(object_, f, indent=4)

def write_cson(file_name, object_):
    with open(file_name, "w", encoding="utf-8") as f:
        return cson.dump(object_, f, indent=4)

def ints(list_):
    return [int(item) for item in list_]

def async_main(function):
    asyncio.run(function)

def template(filename):
    return jinja2.Template(read(filename))
