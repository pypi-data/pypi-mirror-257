from os import *
from time import *

def make(project_name):
    # The pyproject.toml.
    system("echo [build-system] >> pyproject.toml")
    system("echo requires = [\"setuptools>=61.0\"] >> pyproject.toml")
    system("echo build-backend = \"setuptools.build_meta\">> pyproject.toml")
    system("echo # NEXT LINE. >> pyproject.toml")
    system("echo [project]>> pyproject.toml")
    system(f"echo name = \"{project_name}\">> pyproject.toml")
    system("echo version = \"0.0.1\">> pyproject.toml")
    system("echo authors = [>> pyproject.toml")
    system("echo   { name=\"Example Author\", email=\"author@example.com\" },>> pyproject.toml")
    system("echo ]>> pyproject.toml")
    system("echo description = \"A small example package\">> pyproject.toml")
    system("echo readme = \"README.md\">> pyproject.toml")
    system("echo requires-python = \">=3.8\">> pyproject.toml")
    system("echo classifiers = [>> pyproject.toml")
    system("echo     \"Programming Language :: Python :: 3\",>> pyproject.toml")
    system("echo     \"License :: OSI Approved :: MIT License\",>> pyproject.toml")
    system("echo     \"Operating System :: OS Independent\",>> pyproject.toml")
    system("echo ]>> pyproject.toml")
    # The LICENSE .
    system("echo ABC LICENSE>> LICENSE")
    # The README.md .
    system("echo # The README.>> README.md")
    # The .pypirc .
    system("echo [distutils]>> .pypirc")
    system("echo index-servers =>> .pypirc")
    system("echo     pypi>> .pypirc")
    system("echo     testpypi>> .pypirc")
    system("echo # NEXT LINE.>> .pypirc")
    system("echo [pypi]>> .pypirc")
    system("echo repository = https://upload.pypi.org/legacy/>> .pypirc")
    system("echo # NEXT LINE.>> .pypirc")
    system("echo [testpypi]>> .pypirc")
    system("echo repository = https://test.pypi.org/legacy/>> .pypirc")
    mkdir("src")
    chdir("src")
    mkdir(project_name)
    chdir(project_name)
    system("echo # Done. >> __init__.py")
    system(f"echo # Done. >> {project_name}.py")

def helper():
    print("OK, if you didn't ran the make() command run it.")
    print("So the make() command makes you a template of a pip package that you can upload later.")
    print("I have no idea why __init__.py exists so let's skip it")
    print("do you remember when you used the make() function? and there was a parameter with project_name? there is a python file with this name, here will be your functions and your stuffs")
    print("the other ones (exept pyproject.toml) i bet you know them so SKIP.")
    print(" the pyproject.toml is already done. so you just replace your personal info.")
    print("DO NOT TOUCH THE .pypinc FILE OR THE UPLOAD WON'T BE SUCCESFULL !")

def build():
    system("python -m build")

def upload():
    system("python -m pip install --upgrade twine")
    system("python -m twine upload --repository testpypi dist/*")

