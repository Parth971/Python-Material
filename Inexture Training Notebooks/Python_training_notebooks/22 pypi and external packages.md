# What is pip?

- [`pip`](https://pip.pypa.io/en/stable/) is the standard package manager for [Python](https://www.python.org/)

- It allows you to install and manage additional packages that are not part of the [Python standard library](https://docs.python.org/3/py-modindex.html).

- [Python Package Index](https://pypi.org/) ([PyPI](https://pypi.org/)) Is the platform where these packages are listed

- `pip` has been included with the Python installer since versions `3.4` for Python 3 and `2.7.9` for Python 2

- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) uses [`npm`](https://www.npmjs.com/) for package management, [Ruby](https://www.ruby-lang.org/en/) uses [gem](https://rubygems.org/), and [.NET](https://dotnet.microsoft.com/languages) use [NuGet](https://www.nuget.org/).

- In Python, `pip` has become the standard package manager.

- The Python installer installs `pip`, so it should be ready for you to use, unless you installed an old version of Python.

- ```bash
  $ pip --version
  
  pip 18.1 from C:\Python37\lib\site-packages\pip (python 3.7)
  ```



# Installing Packages With `pip`

- Python has a very active community that contributes an even bigger set of packages that can help you with your development needs.

-  These packages are published to the [Python Package Index](https://pypi.org/), also known as [PyPI](https://pypi.org/) (pronounced *Pie Pea Eye*).

- Many of these packages simplify Python development by providing friendly interfaces to functionality that already exists in the standard library.

- ```python
  import cgi
  import http.client
  
  server = 'www.google.com'
  url = '/'
  conn = http.client.HTTPSConnection(server)
  conn.request('GET', url)
  response = conn.getresponse()
  content_type = response.headers.get('Content-Type')
  _, params = cgi.parse_header(content_type)
  encoding = params.get('charset')
  data = response.read()
  text = data.decode(encoding)
  
  print(f'Response returned: {response.status} ({response.reason})')
  print('Body:')
  print(text)
  ```



Above example shows how you can use standard libraries to make an http request. However, we can do the same with `requests` library which makes the task a whole lot easier.

```bash
$ pip3 install requests

Collecting requests
  Downloading https://files.pythonhosted.org/packages/51/bd/23c926cd341ea6b7dd0b2a00aba99ae0f828be89d72b2190f27c11d4b7fb/requests-2.22.0-py2.py3-none-any.whl (57kB)
    100% |████████████████████████████████| 61kB 175kB/s 
Collecting chardet<3.1.0,>=3.0.2 (from requests)
  Downloading https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6487b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (133kB)
    100% |████████████████████████████████| 143kB 528kB/s 
Collecting idna<2.9,>=2.5 (from requests)
  Downloading https://files.pythonhosted.org/packages/14/2c/cd551d81dbe15200be1cf41cd03869a46fe7226e7450af7a6545bfc474c9/idna-2.8-py2.py3-none-any.whl (58kB)
    100% |████████████████████████████████| 61kB 4.1MB/s 
Collecting certifi>=2017.4.17 (from requests)
  Downloading https://files.pythonhosted.org/packages/b9/63/df50cac98ea0d5b006c55a399c3bf1db9da7b5a24de7890bc9cfd5dd9e99/certifi-2019.11.28-py2.py3-none-any.whl (156kB)
    100% |████████████████████████████████| 163kB 607kB/s 
Collecting urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 (from requests)
  Downloading https://files.pythonhosted.org/packages/e8/74/6e4f91745020f967d09332bb2b8b9b10090957334692eb88ea4afe91b77f/urllib3-1.25.8-py2.py3-none-any.whl (125kB)
    100% |████████████████████████████████| 133kB 578kB/s 
Installing collected packages: chardet, idna, certifi, urllib3, requests
Successfully installed certifi-2019.11.28 chardet-3.0.4 idna-2.8 requests-2.22.0 urllib3-1.25.8
```



__upgrading pip__

```bash
python -m pip install --upgrade pip
```

- Notice that you use `python -m` to update `pip`. The `-m` switch tells Python to run a module as an executable. This is necessary because in order for you to update `pip`, the old version has to be uninstalled before installing the new version, and removing it while running the tool can cause errors.



Now that you have installed `requests` and upgraded `pip`, you can use the `freeze` command to see the packages installed in your environment

```bash
$ pip3 freeze
certifi==2018.11.29
chardet==3.0.4
idna==2.8
pip==19.0.1
requests==2.21.0
setuptools==40.6.2
urllib3==1.24.1
```



You can look at the package metadata by using the `show` command in `pip`

```bash
$ pip show requests
Name: requests
Version: 2.22.0
Summary: Python HTTP for Humans.
Home-page: http://python-requests.org
Author: Kenneth Reitz
Author-email: me@kennethreitz.org
License: Apache 2.0
Location: /home/pritesh/.local/lib/python2.7/site-packages
Requires: urllib3, certifi, chardet, idna
```



With the `requests` package installed, you can modify the example above and see how easy it is to retrieve the contents of a web page



```python
import requests

url = 'https://www.google.com'
response = requests.get(url)
print(f'Response returned: {response.status_code}, {response.reason}')
print(response.text)
```



# Using Requirement Files

- The `pip install` command always installs the latest published version of a package, but sometimes, you may want to install a specific version that you know works with your code.
- Requirement files allow you to specify exactly which packages and versions should be installed.

```bash
$ pip freeze > requirements.txt
$ cat requirements.txt

certifi==2018.11.29
chardet==3.0.4
idna==2.8
requests==2.21.0
urllib3==1.24.1
```

- The `freeze` command dumps all the packages and their versions to standard output, so you can redirect the output to a file that can be used to install the exact requirements into another system. 
- The convention is to name this file `requirements.txt`, but you can give it any name you want.



When you want to replicate the environment in another system, you can run `pip install` specifying the requirements file using the `-r` switch

```bash
$ pip install -r requirements.txt
```



# Virtual Environments and Packages

- Python applications will often use packages and modules that don’t come as part of the standard library.
- This means it may not be possible for one Python installation to meet the requirements of every application. If application A needs version 1.0 of a particular module but application B needs version 2.0, then the requirements are in conflict and installing either version 1.0 or 2.0 will leave one application unable to run.
- The solution for this problem is to create a [virtual environment](https://docs.python.org/3/glossary.html#term-virtual-environment), a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages.

## Creating Virtual Environments

- The module used to create and manage virtual environments is called [`venv`](https://docs.python.org/3/library/venv.html#module-venv).
- To create a virtual environment, decide upon a directory where you want to place it.
- run the [`venv`](https://docs.python.org/3/library/venv.html#module-venv) module as a script with the directory path.

```bash
python3 -m venv tutorial-env
```

- This will create the `tutorial-env` directory if it doesn’t exist



Once you’ve created a virtual environment, you may activate it.



On Windows, run:

```bash
tutorial-env\Scripts\activate.bat
```

On Unix or MacOS, run:

```bash
source tutorial-env/bin/activate
```

Activating the virtual environment will change your shell’s prompt to show what virtual environment you’re using

```bash
$ source ~/envs/tutorial-env/bin/activate
(tutorial-env) $ python
Python 3.5.1 (default, May  6 2016, 10:59:36)
  ...
>>> import sys
>>> sys.path
['', '/usr/local/lib/python35.zip', ...,
'~/envs/tutorial-env/lib/python3.5/site-packages']
>>>
```

