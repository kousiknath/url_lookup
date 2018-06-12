# url_lookup
Minimum requirements:
1. Python 2.7 is installed.
2. The command virtualenv is installed. ( reference: https://virtualenv.pypa.io/en/stable/installation/ )
3. sqlite3

How to run this application?
1. Go to your project directory which you prefer in your machine. Let's say the directory is: /User/xyz/Projects
2. Create a folder called - url_lookup_service inside /User/xyz/Projects
3. run: cd url_lookup_service
4. run: virtualenv venv . It will create a virtual environment inside the folder, this env is a standalone python environment where the app can run.
5. cd venv
6. run: source bin/activate. It will activate the python environment.
7. pip install django==1.11 - This will install Django in the virtual environment.
8. copy url_lookup folder to inside venv.
9. run: cd url_lookup
10. run: python manage.py makemigrations
11. run: python manage.py migrate
12. run: python manage.py migrate --database=partition_1 ( We have 2 databases - default & partition_1, so migration has to be applied to both)
13. run: python manage.py runserver - this will run the development server on the machine. By default the server will run at port 8000.

14. To add an url to the system, the following api is used:
Http Method: POST
URL: http://localhost:8000/urlinfo/1/add (Replace localhost with your server ip if required, I am running the django app locally)
Request Body:
{
	"url": "http://123.21.23.13:90/test/test?k=v&kk=nb",
	"blacklist": false
}

Here "blacklist" can be true or false. By default, new urls added to the system are NOT blacklisted. If you set "blacklist" to true, then only in the system, the url will be unsafe.

Response:
{
	"message": "URL data updated successfully",
	"success": true
}

15. To get information about a particular url, the following api is used:
Http Method: GET
URL: http://localhost:8000/urlinfo/1/http://123.21.23.13:90/test/test?k=v&kk=nb&yy=yu
Response:
{
	"path": "/test/test?k=v&kk=nb&yy=yu",
	"host": "123.21.23.13",
	"message": "",
	"port": "90",
	"is_safe": true
}
Here, the is_safe tells if the url is safe to access or not. If blacklist is set to true in the previous api, the url will be unsafe, otherwise it is safe.
