# Dict to Dataframe Converter

This is a Python package designed to convert JSON data into tabular format, a common task in the daily work of engineers 
and data scientists. With this tool, you can easily transform JSON data into a tabular representation, 
facilitating its analysis and manipulation. The codebase was initially inspired by a solution provided on 
[Stack Overflow](https://stackoverflow.com/a/70791993/16109419) and later refined to address various bugs before being 
published on [PyPI](https://pypi.org/project/dict2dataframe/).


## 1. Requirements

Following the minimum system requirements to execute the scripts:

- **Processor:** 1 Core, 32-Bit, 1.4 GHz
- **Memory:** 512 MB RAM
- **Storage:** 50 MB free space
- **OS:** Linux, Windows, macOS

Before using this project, you must install its requirements by executing the following commands\*:

```console
user@host:~$ cd dict2dataframe\
user@host:~$ python -m venv venv
user@host:~$ venv\Scripts\activate
(venv) user@host:~$ pip install -U pip setuptools wheel
(venv) user@host:~$ pip install -r requirements.txt
```

Run the following command\* if you want to generate the `.tar.gz` binary file uploaded on Pypi:

```console
(venv) user@host:~$ python setup.py sdist
```

Run the following command\* to generate the `.whl` binary file that can be uploaded on Databricks or some other place:

```console
(venv) user@host:~$ python setup.py clean --all bdist_wheel
```


## 2. Usage

To use this package in your environment, just import the modules you want to use. Available modules are in 
the `dict2dataframe/` directory. Below you can see a simple example of using this package:

Importing our sample data from file:

```python
import json

with open("samples/data.json", mode="rt", encoding="utf-8") as file:
    data = json.load(file)

print(data)
```

Which gives us the following dictionary:

```json
{
    "values":
    [
        {
            "a": 1,
            "b":
            {
                "x": 10,
                "y": 20
            },
            "c": 2,
            "d":
            [
                {
                    "z": 30
                }
            ]
        },
        {
            "a": 5,
            "b":
            {
                "x": 15,
                "y": 25
            },
            "c": 6,
            "d":
            [
                {
                    "z": 35
                }
            ]
        },
        {
            "a": 9,
            "b":
            {
                "x": 20,
                "y": 30
            },
            "c": 10,
            "d":
            [
                {
                    "z": 40
                }
            ]
        }
    ]
}
```

Which we can easily convert to a table:

```python
from dict2dataframe.core import dict2dataframe

df = dict2dataframe(data['values'])
print(df)
```

Which will generate the following result:

```python
   a   c  b_x  b_y  d_z
0  1   2   10   20   30
1  5   6   15   25   35
2  9  10   20   30   40
```


\* Windows OS syntax-based commands.
