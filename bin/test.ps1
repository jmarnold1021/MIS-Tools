$PACKAGE_ROOT = $PSScriptRoot + '\..'
cd $PACKAGE_ROOT

python .\setup.py test
