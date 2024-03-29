# MIS Tools

Various tools for working with MIS-Data

## Usage


```powershell

[2023-07-11 11:09 admin_ja@JAREDSERVER MIS-Tools]$ python .\bin\misbin.py --help
Usage: misbin.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  coci_refresh  Refresh The COCI data from Curriculum Inventory
  dod_refresh   Refresh all DOD data from source files
  mis_export    Export MIS Data to Flat Files from Colleague RPT Tables
  mis_version   List the currently installed version of MIS-Tools
  scff_refresh  Refresh The SCFF data from source files

[2023-07-11 11:13 admin_ja@JAREDSERVER MIS-Tools]$ python .\bin\misbin.py mis_export --help
Usage: misbin.py mis_export [OPTIONS]

  Export MIS Data to Flat Files from Colleague RPT Tables

Options:
  -r, --report TEXT     The MIS report to export data from
  -g, --gi03 TEXT       The GI03 term for the report
  -s, --sql-only        Print the SQL rather than create the export
  -l, --log-level TEXT  Set the logging level for the command defaults to
                        ERROR, Choices [CRITICAL, ERROR, WARN, INFO, DEBUG]
  --help                Show this message and exit.


[2023-07-11 11:13 admin_ja@JAREDSERVER MIS-Tools]$ python .\bin\misbin.py mis_version
...

[2023-07-11 11:13 admin_ja@JAREDSERVER MIS-Tools]$ python .\bin\misbin.py mis_export -r XB -g 234
...

[2023-07-11 11:13 admin_ja@JAREDSERVER MIS-Tools]$ python .\bin\misbin.py coci_refresh -c --safe
...

```

## Conventions

* The PACKAGE_ROOT Directory is MIS-Tools
* The LIB_ROOT directory is mistools

## Test/Development/Contributing

* Make necessary changes
* Ensure unit tests still pass

```powershell

**Needs update...**

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

If no new dependancies are needed can run...it will update the globally installed version regardless of any version changes!!!

```powershell

# handy for dev...
.\bin\build.ps1

```

To get a new version with updated source code.


## Install

```powershell

# Find the wheel file in dist after build - use -U to upgrade
# installed package version
$ pip install .\dist\mistools-0.10.4-py3-none-any.whl [-U]

# will reinstall if the version has not been changed in setup.py handy for dev...
$ pip install --force-reinstall .\dist\mistools-0.10.4-py3-none-any.whl

# check installation
$ pip list | grep mistools
=> mistools                  0.10.4

# test import outside of package directory
$ cd ~
$ python
>>> from mistools import misffparser
>>>

```

It will install the Binary misbin.py to the Root Python install directory under Scripts...May need to add this to path.

## Configuration

On Windows the config should be placed in C:/Users/%USER%/Documents/MIS-Tools/configs.json atm.

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

## Python Packaging Help Docs I Roughly Used
[Packaging Docs](https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f)<br>
[Setup.py Overview](https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/)
