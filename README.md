# facerecapi

## Table of Contents
1. [Get Started](#get-started)
2. [Usage](#usage)
    * [Browser](#browser)
    * [API](#api)
3. [Database](#database)
    * [Structure](#structure)
4. [Face detection to API pipeline](#face-detection-to-api-pipeline)
5. [Dependencies](#dependencies)

## Get Started
**The following instructions are for Unix shells**

  Clone repository
  ```fish
  $ git clone https://github.com/ammo888/facerecapi
  ```

  Create virtual environment
  ```fish
  $ cd facerecapi

  # facerecapi/
  $ python3 -m venv env   # python 3
  $ virtualenv env        # python 2
  ```

  Install dependencies
  ```fish
  # facerecapi/
  $ source env/bin/activate
  (env) pip install -r requirements.txt
  (env) cd imagebank
  ```

  Setup project
  ```fish
  # facerecapi/imagebank/
  (env) unzip database.zip
  (env) python manage.py makemigrations api
  (env) python manage.py migrate
  (env) python manage.py createsuperuser
  ```

  Run server
  ```fish
  # facerecapi/imagebank/
  (env) python manage.py runserver            # localhost:8000
  (env) python manage.py runserver ip:port    # custom ip:port
  ```
 
  Running a custom ip:port requires adding that ip address to the `ALLOWED_HOSTS` list in `facerecapi/imagebank/imagebank/settings.py`

  Also, you would need to modify the ip:port of `self.imagebank` in `facerecapi/imagebank/api/faces.py`

## Usage

### Browser

  Django Rest Framework provides a nice browser API.

  Here are example api endpoints you can access (e.g. server running on localhost): 
  ```
  http://localhost:8000/              # API ROOT
  http://localhost:8000/users/        # USERS
  http://localhost:8000/imagebank/    # IMAGES 
  ```
  
  To post an image, navigate to `http://localhost:8000/imagebank/` and login with the user you created earlier.

  First, choose an image file to upload.

  To identify the faces from the existing database, DO NOT type anything in the Name field, and POST.
  
  You should receive a response containing the user info, e.g.:
  ```
  [
    {
      "gender": "M",
      "name": "Joe Smith"
    }
  ]
  ```
  If the given face is determined not to be in the database, you should receive this response:
  ```
  [
    "Face not in database"
  ]
  ```

  To add a face to the database, include a name in the Name field and POST. You should receive a response, e.g.:
  ```
  [
    "Added <user hash> embedding"
  ]
  ```
  You can update an existing face embedding by POST-ing an image with the same name as one in the database. You should receive a response, e.g.:
  ```
  [
    "Updated <user hash> embedding"
  ]
  ```

  If no face is found in the image, you should receive this response:
  ```
  [
    "No face found"
  ]
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
  ```fish
  http -a username:password -f POST ip:port/imagebank/ image@<IMAGE PATH>
  ```

  To add/update face:
  ```fish
  http -a username:password -f POST ip:port/imagebank/ image@<IMAGE PATH> name=<NAME> gender=<M or F>
  ```

  The responses to these HTTP requests are described in the **Browser** section above.

## Database

### Structure
  Currently, the database is composed of two pickle files in `facerecapi/imagebank/database.zip`.
  The faces stored are the first 1000 people from the aligned LFW face database.

  `hash.pickle` holds a list of hashes in the database.

  `data.pickle` holds the corresponding 128-dimensional face embeddings

<!--
### Making own database
  Included in `facerecapi/` is `embed.py`.

  Running the script should create the `.pickle` files in `outfolder`.
  ```fish
  (env) python embed.py faces outfolder
  ```

  The `faces` folder should be structered as follows:
  ```
  faces/
    name1/
      pic1.jpg
      pic2.jpg
      pic3.jpg
      ...
    name2/
      pic1.jpg
      pic2.jpg
      ...
    name3/
      ...
  ```
  Each named folder should contain at least one image.

  In `embed.py`, the variable `im_total` sets the max number of faces to embed, which is up to your choosing.

-->
## Face detection to API pipeline

  `pipeline.py` processes images with none to multiple faces, and for every detected face, calls the API to identify.
  
  ```fish
  (env) python pipeline.py ip:port path/to/image.jpg
  ```

## Camera input
  
  `camera.py` does what `pipeline.py` does but instead, uses frames from the primary camera on your computer as input. Simply:

  ```fish
  (env) python camera.py ip:port
  ```

## Dependencies
* numpy
* scipy
* requests
* httpie
* Pillow
* Django
* Django Rest Framework
* dlib
* face-recognition
* opencv
