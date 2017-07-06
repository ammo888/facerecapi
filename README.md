# facerecapi

## Get Started
**The following instructions are for Unix shells**

Clone from repository
```
$ git clone https://github.com/ammo888/facerecapi
```

Enter project and create virtual environment
```
$ cd facerecapi

$ python3 -m venv env   # python 3
$ virtualenv env        # python 2
```

Activate virtual environment and install dependencies
```
$ source env/bin/activate
(env) pip install -r requirements.txt
(env) cd imagebank
```

Setup project
```
(env) unzip database.zip
(env) python manage.py makemigrations api
(env) python manage.py migrate
(env) python manage.py createsuperuser
```

Run server with configuration
```
(env) python manage.py runserver            # localhost:8000
(env) python manage.py runserver ip:port    # custom ip:port
```

## Usage

### Browser

Django Rest Framework provides a nice browser API.
(Example - server running on default ip:port):
```
http://localhost:8000/              # API ROOT
http://localhost:8000/users/        # USERS
http://localhost:8000/imagebank/    # IMAGES 
```
  To post an image, navigate to `http://localhost:8000/imagebank/` and login with the user you created earlier.

  Choose an image file to upload (one with a face in it!).

  To try to identify the faces from the existing database, DO NOT type anything in the Name field, and POST.
  You should receive a response with the name and the euclidean distance between the input face embedding and the one in the database.
  ```
  Joe_Smith 0.32845135197179404
  ```
  To add a face to the database, do the same as above, but include a name in the Name field and POST. You should receive the following response:
  ```
  Added Joe_Smith embedding
  ```
  You can update an existing face embedding by POST-ing an image with the same name as one in the database, and should receive:
  ```
  Updated Joe_Smith embedding
  ```

### API
  You can access the API from the command line.

  `pip` should've installed `httpie` for you, a human friendly command line HTTP client. The following instructions will be using this package.

  However, you can use whatever http client you want, e.g. `curl`.

  To browse around:
  ```
  http ip:port/           # API ROOT
  http ip:port/users/     # USERS
  http ip:port/imagebank/ # IMAGES
  ```

  To identify a face:
  ```
  http -a username:password -f POST ip:port/imagebank/ image@<IMAGE PATH>
  ```

  To add/update face:
  ```
  http -a username:password -f POST ip:port/imagebank/ image@<IMAGE PATH> name=<NAME>
  ```

  The responses to these requests are the same as in the **Browser** section. If no face is found, the API will respond with...
  ```
  No face found
  ```
