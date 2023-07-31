$PACKAGE_ROOT = $PSScriptRoot + '\..'
echo $PACKAGE_ROOT

#rm $PACKAGE_ROOT/dist/*

# start build
cd $PACKAGE_ROOT\venv\Scripts
.\Activate.ps1

# build steps
cd $PACKAGE_ROOT

python .\setup.py bdist_wheel

# end build
cd venv\Scripts
deactivate
cd $PACKAGE_ROOT

# have not tested this with multiple versions in dist...
pip install --force-reinstall --find-links=dist mistools
