# MIS Tools

Various tools for working with MIS-Data

## Conventions

* The PACKAGE_ROOT Directory is MIS-Tools
* The LIB_ROOT directory is mistools

## Test/Development/Contributing

* Make necessary changes
* Ensure unit tests still pass

```powershell

# From PACKAGE_ROOT run
$ .\bin\test.ps1

test_parse_sc (misffparser.tests.test_misffparser.Test_Mis_FF_Parser) ... ok
...

test_parse_sp (misffparser.tests.test_misffparser.Test_Mis_FF_Parser) ... ok
...

test_parse_xb_bulk (misffparser.tests.test_misffparser.Test_Mis_FF_Parser) ... ok
...

----------------------------------------------------------------------
Ran 10 tests in 0.151s

OK

```

* README and Version in setup.py (major.minor.patch)
* Create Pull Request
* [Git Commit Message Format](https://gist.github.com/robertpainsi/b632364184e70900af4ab688decf6f53)

## Docs

All api docs are built and readable in Sphinx-Docstring Format...Some are dependant upon [sphinx_design](https://pypi.org/project/sphinx_design/) .



## Build

```powershell

# All steps have been done using python 3.10.0
# besides Acitvate and Deactivate all steps are done
# in PACKAGE_ROOT

$ python -m venv venv
$ cd venv/Scripts
$ .\Activate.ps1
(venv) $


# install any build dependant packages in venv if not installed
# check venv\Lib\site-packages directory usually there after 1 build
# make sure to remove old dist with same version if testing

(venv) $ cd PACKAGE_ROOT
(venv) $ pip install wheel
(venv) $ pip install setuptools
(venv) $ pip install twine


# install any application or test dependant packages
# None at the moment, might be able to provide these in setup.py...

(venv) $ ...


# run build wheel setup
(venv) $ python .\setup.py bdist_wheel
=> should complete without errors


# the wheel(.whl) file stored in dist can now be installed or published
# see installation section
(venv) $ ls dist

Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----        1/28/2022  12:08 PM           1069 mistools-0.10.4-py3-none-any.whl


# exit venv
(venv) $ cd venv\Scripts
(venv) $ deactivate
$

```

If no new dependancies are needed can run...

```powershell

.\bin\build.ps1

```

To get a new version with updated source code.


## Install

```powershell

# Find the wheel file in dist after build - use -U to upgrade
# installed package version
$ pip install .\dist\mistools-0.10.4-py3-none-any.whl [-U]

# check installation
$ pip list | grep mistools
=> mistools                  0.10.4

# test import outside of package directory
$ cd ~
$ python
>>> from mistools import misffparser
>>>

```

## Configuration

Current Configuration options...

```javascript

{

    "DB" : {

        "DB_CONFIG_NAME_1" : {
            "SERVER_NAME": "...",
            "DB_NAME": "..."
        },

        "DB_CONFIG_NAME_2" : {
            "SERVER_NAME": "...",
            "DB_NAME": "..."
        },

        "LOG_LEVEL" : "INFO"
    },

    "MIS_DOD" : {

       "LOG_LEVEL" : "INFO",

       "REF_FILES_ROOT" : "REF/FILE/ROOT/**/",
       "ACC_FILES_ROOT" : "ACC_FILES_ROOT/**/"
    },

    "MIS_FLAT_FILE" : {

        "LOG_LEVEL" : "INFO",

        "MIS_FF_EXPORT_ROOT" : "SUBMISSION/FILES/ROOT",

        "AUTHOR" : {

            "FIRST_NAME"   : "MIS Author Info",
            "LAST_NAME"    : "MIS Author Info",
            "PHONE_NUMBER" : "MIS Author Phone #"
        }
    }
}

```

**This will change soon since installed versions will need a way to have configs provided probably using a path paramater. Packaged version will fail atm sourcing this file!!!**

## Python Packaging Help Docs I Roughly Used
[Packaging Docs](https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f)<br>
[Setup.py Overview](https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/)
