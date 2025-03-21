# FlaskJWT-Auth
Python basic auth functionality using JWT token
cd FlaskJWT_Auth/

check git config:
git config --global user.name
git config --global user.email


git remote add origin https://github.com/ankesh5jan/FlaskJWT-Auth.git


Install the dependencies: pip3 install -r requirements.txt

Run the Flask application: python3 app.py

#docker command:

docker build -t flask-auth-jwt .

docker run -p 5000:5000 flask-auth-jwt 


Open the application in a web browser: http://localhost:5000/

