# Peaks and Troughs
## A Beginners Guide to Investing
<hr>

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Flask Guide](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### Admin Details
<hr>

**Test User:**
**username:** test-user
**password:** test123

**Test Admin:**
TBC

### Update Steps
<hr>

```
$ git checkout main
$ git fetch
$ git pull origin main
$ git checkout <dev-branch>
$ git merge main
$ git push origin <dev-branch>
```
Repeat the last 3 steps for as many dev- branches as required to ensures that the amount of merge conflicts are keps to a minimum. This should be done on a regular basis in addition to staging and commiting changes
```
$ git add <file/s>
$ git commit -m "<commit message>"
```

### Admin Steps
<hr>

1. Clone Repository
```
$ git clone https://github.com/danielchegwidden/peaks-and-troughs.git
```

2. Create Virtual Environment
```
$ conda create -n peaks-env python=3.9
```
3. Activate Environment and Install Packages
The packages can be installed as follows:
```
$ conda activate peaks-env
$ pip install -r requirements.txt
```
or individually as follows:
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
$ pip install flask-sqlalchemy
$ pip install flask-migrate
$ pip install flask-login
$ pip install email-validator
$ pip install flask-bootstrap4
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
7. Updating the Database
!Only run these commands when making database changes!
```
$ flask db migrate -m "users table"
$ flask db upgrade
```
