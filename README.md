simple-cart
===========

Django Cart (sample code)

## Info

+ Author: Marcos Moyano
+ Contact: marcos at anue dot biz
+ Project homepage: http://github.com/marcosmoyano/simple-cart

## Install

### First, create the virtualenv where you will be placing the project. Virtualenv and Pip are your friends.
+ pip: http://pip-installer.org
+ virtualenv: http://virtualenv.org
I highly recommend using Virtualenvwrapper
+ http://virtualenvwrapper.readthedocs.org

```sh
user@machine:$ mkvirtualenv --python=python2.7 --no-site-packages VENV_NAME
Running virtualenv with interpreter /usr/bin/python2.7
New python executable in shopping/bin/python2.7
Also creating executable in shopping/bin/python
Installing Setuptools.........................................................................................................................$
....................................................................................................done.
Installing Pip.................................................................................................................................
...............................................................................................................................................
.....................................................done.

```

### Second, move into your virtualenv and clone the repository.

```sh
user@machine:$ workon VENV_NAME
(PROJECT_NAME)user@machine:$ cdvirtualenv
(PROJECT_NAME)user@machine:VIRTUAL_ENV$ git clone git@github.com:marcosmoyano/simple-cart.git
```

### Third, install the project dependencies. The example below is for local usage.

```sh
(PROJECT_NAME)user@machine:VIRTUAL_ENV$ cd simple-cart
(PROJECT_NAME)user@machine:VIRTUAL_ENV/simple-cart$ pip install -r requirements/local.txt
```

### Fourth, create the local database and install the sample fixtures.

```sh
(PROJECT_NAME)user@machine:VIRTUAL_ENV/simple-cart$ cd cart_project/
(PROJECT_NAME)user@machine:VIRTUAL_ENV/simple-cart/cart_project$ ./manage.py syncdb --settings=cart_project.settings.local
(PROJECT_NAME)user@machine:VIRTUAL_ENV/simple-cart/cart_project$ ./manage.py migrate --settings=cart_project.settings.local

```

### Fifth, run the test suite
```sh
(PROJECT_NAME)user@machine:VIRTUAL_ENV/simple-cart/cart_project$ ./manage.py test --settings=cart_project.settings.test
```

### Finally, run the local server and test the application

```sh
(PROJECT_NAME)user@machine:VIRTUAL_ENV/simple-cart/cart_project$ ./manage.py runserver --settings=cart_project.settings.local

```
