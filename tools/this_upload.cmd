@echo off
REM ## twine upload dist/*
cd ..
py -m twine upload --repository pypi dist/*
