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
TEST_DB_PATH = [FULL PATH TO .db FILE INCLUDING NAME]

DEBUG = 1
REFRESH_DB = 1
SECRET_KEY = [SOMETHING YOU'LL REMEMBER]
```

-   You can set `DEBUG = 0` if you'd like, but it turns off some useful features for developing, like restarting the application when you save a file.
-   You can also set `REFRESH_DB = 0` if you'd like. This will mean that the database will remain in it's current state, and the data generator won't run.

### Running

Once all these steps are completed, you should be able to run the application by doing `$ python app.py` or `$ flask run`. You should see some output that looks something like this.

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

### Testing

#### Naming Conventions

All test files are in the test directory.
To be picked up correctly by the testing module, all test files and methods should be named following the pattern `test_*.py`.

#### Running

You can run the full suite of tests by running the command `$ pytest` in the root or test directory.
If you want to run a subset of tests, you can append the paths to directories or test files you want like `$ pytest test/users/ test/drugs/test_drugs.py`.

Note that the way pytest works is looking for properly named files and methods in the directory and files your provide.
This means that if you wanted to store test files in the same directory as their corresponding source files, you could.

#### Coverage

By appending the argument `--cov=[MEASURE] [RUN]` to your pytest command, all tests in the `RUN` file/directory will run, measuring the coverage of everything in the `MEASURE` file/directory.
This will tell you the number of lines covered, number of lines missed, and the coverage percentage of each file specified by `MEASURE`.
It will also create a `.coverage` file, which can be used by some softwares.

```
Name                                                     Stmts   Miss  Cover
----------------------------------------------------------------------------
src\models\persistent\data_generator.py                    130    130     0%
src\models\persistent\drug\drug.py                          32      3    91%
src\models\persistent\institution\hospital\hospital.py      16      1    94%
src\models\persistent\institution\instutitution.py          16      3    81%
src\models\persistent\institution\pharmacy\pharmacy.py      16      1    94%
src\models\persistent\persistent.py                         11      0   100%
src\models\persistent\prescription\prescription.py          60     17    72%
src\models\persistent\user\patient\patient.py               53      7    87%
src\models\persistent\user\personnel\personnel.py           43      9    79%
src\models\persistent\user\user.py                          28      9    68%
----------------------------------------------------------------------------
TOTAL                                                      405    180    56%
```

If you want to know exactly what line numbers you missed, you can append the argument `--cov-report term-missing`.
However, a more persistent and user-friendly option is to instead append the arugment `--cov-report html`, which will generate an HTML version of the coverage report in a folder called `htmlcov`.
Opening up the `index.html` file in this folder will give an output similar to what you'd see on the terminal, but you can click on any entry to visually see what lines were missed.

**Note:** You might notice that you have higher than expected coverage, especially in modules you didn't explicitly test. This is due to things like import statements, variables in the scope of the entire module, and annotations running when the app starts. You should actually investigate if you have coverage on code.
