@echo off
REM ## twine upload dist/*
REM cd ../..
py -m twine upload --repository pypi dist/*
