@echo off
REM ## twine upload dist/*
py -m twine upload --repository pypi dist/*
