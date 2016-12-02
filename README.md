![alt tag](https://raw.githubusercontent.com/ttsapakos/sl-timetracker/master/coverage.svg)

# Set Up

### Initial Dependencies

Install the following using apt-get (or equivalent):
* python3 (might be installed already)
* python3-pip
* libmysqlclient-dev
* python-dev
* mysql-server (When this runs, mysql should have you set a password. I used `tracker` as mine.)

### Setting up your environment

1. Now run `virtualenv -p python3 env` in the top project directory to create the virtual environment.
2. Run `source ./env/bin/activate` to start the environment.
3. Now run `sudo pip3 install -r requirements.txt` from the project directory.
4. Open mysql with `mysql -u root -p`, using the password you created earlier and then run `CREATE DATABASE sldb;`
5. In Tracker/settings.py, set `'HOST': '/where/ever/you/have/mysql.sock'` (varies based on OS)

---

# Development

Run `source ./env/bin/activate` before you start programming to get back in the environment.
When you're done programming for the day, run `deactivate` to close the virtual environment.

# Testing

Run `python manage.py test`

### Some useful aliases to add to your bashrc

**Starts the server for the project:**
`alias runserv='python3 manage.py runserver'`

**Starts the virtual environment:**
`alias startenv='source ./env/bin/activate'`

**Auto generates new migrations for model changes:**
alias makemigrate='python3 manage.py makemigrations base'

**Runs all of the migrations:**
alias migrate='python3 manage.py migrate'

# Coverage

To update the coverage badge, run the tests then run `coverage-badge -o coverage.svg` and commit the new `coverage.svg` file.
