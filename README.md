# PyTrust: iTrust for this decade

PyTrust is a partial reimplementation of [iTrust2](https://github.ncsu.edu/engr-csc326-staff/iTrust2-v7), a NCSU CSC 326 software engineering project, in Python.

`git ls-files | xargs wc -l`

## Things That Are Different

-   It's written in Python (duh)
    -   Source files have much fewer lines and are generall more readable than they would in Java. Right now, no .py is longer than 200 lines, compared to 1000 lines for .java files in iTrust.
-   It's a Flask App
    -   This means that rebuilding the database and redeploying the app only takes seconds
    -   Debug mode will automatically restart the application (and rebuild the db if you want) when a part of the application is changed.
    -   HTML templates allow you to not have to write the same boilerplate HTML code on every page.
    -   You can enforce HTTPS fairly easily if you want.
    -   If you want to see the results of your changes to an HTML file that the app is serving, all you have to do is save the file and refresh the page.
-   It uses Flask-SQLAlchemy and Marshmallow
    -   Can use the same mysql database, but it wouldn't be hard to switch to another relational dialect like sqllite.
    -   Getters and setters are implied. The only time you need to write a "setter" is when you want to verify a field beyond the restrictions you define in the database.
        -   This drastically cuts down on the line count of most persistance classes.
    -   Classes have an easy way to do common database queries. No need to write static methods to get an object by its id or get a list of objects with some attribute.
    -   Relationships between persistence classes, include backpopulating and cascading, are easily defined, meaning you can easily say what should happen if an instance a persistance object referenced gets deleted.
    -   Although references to other persistence objects are stored by id as foreign keys, you can choose to use and load for API returns the referenced object rather than the key.
    -   Hashed passwords are stored salted. This means that two users with the same plaintext password may have different hashed passwords in the database. This is more secure that iTrust, which does not salt its hashes.
-   Secrets are stored in a .env file and are loaded in as environment variables.
