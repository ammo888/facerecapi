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

# facerecapi/
$ python3 -m venv env   # python 3
$ virtualenv env        # python 2
```

Activate virtual environment and install dependencies
```
# facerecapi/
$ source env/bin/activate
(env) pip install -r requirements.txt
(env) cd imagebank
```

Setup project
```
# facerecapi/imagebank/
(env) unzip database.zip
(env) python manage.py makemigrations api
(env) python manage.py migrate
(env) python manage.py createsuperuser
```

Run server with configuration
```
# facerecapi/imagebank/
(env) python manage.py runserver            # localhost:8000
(env) python manage.py runserver ip:port    # custom ip:port
```

## Usage

### Browser

Django Rest Framework provides a nice browser API.
(e.g. server running on localhost):
```
http://localhost:8000/              # API ROOT
http://localhost:8000/users/        # USERS
http://localhost:8000/imagebank/    # IMAGES 
```
  To post an image, navigate to `http://localhost:8000/imagebank/` and login with the user you created earlier.

  First, choose an image file to upload.

  To identify the faces from the existing database, DO NOT type anything in the Name field, and POST.

  You should receive a response with the name and distance to closest embedding in database, e.g.:
  ```
  Joe_Smith 0.32845135197179404
  ```
  To add a face to the database, include a name in the Name field and POST. You should receive a response, e.g.:
  ```
  Added Joe_Smith embedding
  ```
  You can update an existing face embedding by POST-ing an image with the same name as one in the database. You should receive a response, e.g.:
  ```
  Updated Joe_Smith embedding
  ```

  If not face is found in the image, you should receive this response:
  ```
  No face found
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

  The responses to these HTTP requests are described in the **Browser** section above.