# PyTrust: iTrust but in Python

PyTrust is a partial reimplementation of [iTrust2](https://github.ncsu.edu/engr-csc326-staff/iTrust2-v7), a NCSU CSC 326 software engineering project, in Python.

## What's Different

-   It's written in Python (duh)
    -   Source files have much fewer lines and are generall more readable than they would in Java. Right now, the longest .py is longer barely 200 lines, compared to around 1000 lines for the longest .java files in iTrust.
-   It's a Flask App
    -   This means that rebuilding the database and redeploying the app only takes seconds. Compare this is Java and Spring taking at least a minute.
    -   Debug mode will automatically restart the application (and rebuild the db if you want) when a part of the application is changed.
    -   HTML templates allow you to not have to write the same boilerplate HTML code on every page. Currently, the longest HTML (or JS) file in the project is less than 200 lines.
    -   You can enforce HTTPS fairly easily if you want, especially if you're OK with certificates generated on the fly or self-signed certificates.
    -   If you want to see the results of your changes to an HTML file that the app is serving, all you have to do is save the file and refresh the page.
-   It uses Flask-SQLAlchemy and Marshmallow
    -   Getters and setters are implied. The only time you need to write a "setter" is when you want to verify a field beyond the restrictions you define in the database.
        -   This drastically cuts down on the line count of most persistance classes.
    -   Classes have an easy way to do common database queries. No need to write static methods to get an object by its id or get a list of objects with some attribute.
    -   Relationships between persistence classes, include backpopulating and cascading, are easily defined, meaning you can easily say what should happen if an instance a persistance object referenced gets deleted.
    -   For example, if a `Prescription` object has a reference to a `Patient` object, I can define the backref relationship so that calling `patient.prescriptions` will give me all the prescriptions for that patient.
    -   Although references to other persistence objects are stored by id as foreign keys, you can choose to use and load for API returns the referenced object rather than the key.
        -   For example, if a `Prescription` object has a reference to a `Pharmacy` object, I can define the foreign key relationship so that `prescription.pharmacy` will give me the pharmacyfor that prescription.
    -   Passwords and stored hashed _and salted_. This means that two users with the same plaintext password may have different hashed passwords in the database. iTrust does not salt its hashes.
-   Secrets are stored in a .env file and are loaded in as environment variables.

## What's the same

-   Still using a MySQL database, but the ORM should make it easy to use another relational type.
-   Still use Boostrap for styling, but flask templates mean we only have to update the Boostrap import in one place to affect every page.
-   Still use AngularJS for frontend logic. I know that AngularJS isn't the most modern choice, but it was the easiest to translate from the iTrust files.

## Setup

### Libraries

You need to install all the libraries listend in the `requirements.txt` file. I'd reccomend using a virtual enviroment so anything you instally doesn't conflict with anything existing.

### Environment

#### MySQL

Get the username and password for your database. Create a new database schema and remember the name.

#### .env File

In the root directory of the project (where `app.py` is), create a new file called `.env` and add the following information, replacing the parts in []'s with the information you gathered earlier.

```
DB_USER = [DATABASE USERNAME]
DB_PASS = [DATABASE PASSWORD]
DB_NAME = [DATABASE SCHEMA NAME]

DEBUG = 1
SQLALCHEMY_TRACK_MODIFICATIONS = 0
SECRET_KEY = [SOMETHING YOU'LL REMEMBER]
```

You can set `DEBUG = 0` if you'd like, but it turns off some useful features for developing, like restarting the application when you save a file.
<br>
You can also set `SQLALCHEMY_TRACK_MODIFICATIONS = 1` if you'd like, but it's not that useful and may slow down the application.

### Running

Once all these steps are completed, you should be able to run the application by doing `$ python app.py` or `$ flask serve`. You should see some output that looks something like this.

```
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: ###-###-###
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
