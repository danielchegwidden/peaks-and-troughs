# Peaks and Troughs
## A Beginners Guide to Investing

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Flask Guide](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### Admin Steps

1. Clone Repository
```
$ git clone https://github.com/danielchegwidden/peaks-and-troughs.git
```

2. Create Virtual Environment
```
$ conda create -n peaks-env python=3.9
```
3. Activate Environment and Install Packages
```
$ conda activate peaks-env
$ pip install Flask
$ pip install pre-commit
$ pip install black
$ pip install mypy
```
4. Set-Up Pre-Commit
```
$ pre-commit install
```
5. Set-Up Flask
```
$ pip install python-dotenv
$ pip install flask-wtf
```
6. Set up Python Environment
- Create folder .vscode
- Create file settings.json inside this file
- Add the following entry, replacing XXX with the correct username to direct to your virtual envronment
```
{
    "python.pythonPath": "/Users/XXX/opt/miniconda3/envs/peaks-env/bin/python",
    "editor.rulers": [ 100 ]
}
```
