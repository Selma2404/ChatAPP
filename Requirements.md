# Requirements
Python3 ==> Linux : sudo apt install python3 
            Windows : https://www.python.org/downloads/
	
Django Framework ==> Linux : pip3 install django
                     Windows : https://docs.djangoproject.com/en/3.2/howto/windows
       
Activate the virtual envirenement : source myvenv/bin/activate

Make Migration : python3 manage.py makemigrations

Migrate : python3 manage.py migrate 

Start the web server : daphne mysite.asgi:application
