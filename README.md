[comment]: <> (![alt text]&#40;../media/images/factory_transparant_v1.png?raw=true&#41;)

[comment]: <> (![alt text]&#40;../media/images/factory_transparant_v2.png?raw=true&#41;)

[comment]: <> (![alt text]&#40;../media/images/factory.png?raw=true&#41;)
<p align="center"><img src="../media/images/factory_v5.png" alt="funcfactory logo" width="300" /></p>


<h1 align="center">FuncFactory</h1>
<p align="center"><b>Easily adaptable, Production grade, Python pipelines on the fly.</b></p>

<p align="center">
  <a href="../main/LICENSE.txt"><img src="https://img.shields.io/pypi/l/FuncFactory" alt="License: Apache 2.0"></a>
  <a href="https://pypi.org/project/funcfactory/"><img alt="Pypi FuncFactory" src="https://img.shields.io/pypi/v/FuncFactory?logo=FuncFactory"></a>
  <a href="ttps://img.shields.io/pypi/pyversions/FuncFactory"><img alt="Py versions" src="https://img.shields.io/pypi/pyversions/FuncFactory"></a>
  <a href="https://github.com/szindel/FuncFactory/actions/workflows/python-package.yml"><img alt="Build soda-sql" src="https://github.com/szindel/FuncFactory/actions/workflows/python-package.yml/badge.svg"></a>
</p>
<br/>
<em> .. We got the Func, you got the Func, she got the Func, he got the Func .. !</em> 
<br />

# What is it?
The FuncFactory is an open-source solution that creates and runs easily adaptable, production grade, python pipelines. Users simply configure the pipelines in simple yaml files and the steps of the pipelines in ordinary python functions. Once loaded in the FuncFactory the pipelines can be triggered and the result creation, loging and error handeling is taken care of by the Factor itself. Any developer that knows how to create python functions can therefore easily incorporate these into production grade python pipelines with a handful lines of code.  

# Idea
A principle often used in code is the storing of (function & class) config & parameters in yaml files. This package extends that idea by also storing the function implementation and order in yaml files. Users do not have to change a single line of python now to completely change the python pipeline. Resulting in highly adaptable and readable python pipelines.
<br />
<br />
Bringing code from the development fase into production often adds many very similar lines of code: error handeling, logging, result creation.. Often these can be reduced by the use of more complex python features like decorators. However the FuncFactory takes care of all that for you.

# Where to get it
```sh
# PyPI
pip3 install funcfactory
```
# Getting started
In the example below we make a complete python pipeline that compares checksums from a downloaded file and the source.

## Step 1: Create desired functions
```python
import requests as r
import sha256
def calc_checksum_url(url, **kwargs):
    """Function that calculates checksum of an url
    """
    response = r.get(url)
    assert response 
    checksum = sha256(response.content).hexdigest()
    return checksum, "Found checksum url"

def calc_checksum_file(file, **kwargs):
    """Function that calculates checksum of a file
    """
    with open(file, "rb") as file:
        checksum = sha256(file).hexdigest()
    return checksum, "Found checksum file"
```
Mind you:
- FuncFactory specifically deals with assertion errors
- **kwargs is always(!) needed for the steps to work properly
- The first return object used for the step result
- The second object will be added to the logging
- The third object will be stored in the FuncFactory so it can be accessed by other steps

## Step 2: Configure the yaml pipeline file
```yaml
# Severity levels (Azure standard)
# CRITICAL = 4
# ERROR = 3
# WARNING = 2
# INFORMATION = 1
# VERBOSE = 0
DEFAULT:
  skip_file: False
  check_name: 'Checksum input files'
  significance: 2
  stop_run_on_fail: False

Step_1:
  severity_level: 4
  func_left: calc_checksum_file
  func_right: calc_checksum_url
  kwargs_left: {"file":"/user/data/input_file_1.csv"}
  kwargs_right: {"url":"https://www.my_input_data_url.com/input_file_1.csv",}

Step_2:
  severity_level: 4
  func_left: calc_checksum_file
  func_right: calc_checksum_url
  kwargs_left: {"file":"/user/data/input_file_2.csv"}
  kwargs_right: {"url":"https://www.my_input_data_url.com/input_file_2.csv"}

```
- The default is used for general pipeline properties. After loading this the steps are executed. 
- An example is shown where two functions are checked against one another. 
- Single functions can also be made into steps by comparing the result with a function that only returns a single return code.

## final step: Create the FuncFactory and run
```python
from funcfactory import FuncFactory
import .my_check_functions as my_check_functions
import .more_check_functions as more_check_functions
# init the FuncFactory with the modules containing the functions from step 1
ff=FuncFactory(list_modules_functions=[my_check_functions, more_check_functions])

# Load (all) yaml files from step 2
ff.read_config_folder("./config_checks")

# optionally: load objects needed in your steps.
import xlrd
excel_workbook = xlrd.open_workbook(file_contents=file_excel)
ff.load_factory_objects(wb = excel_workbook)

# run pipelines
ff.run_func()
```

# Contributors
Steven Zindel (Author)