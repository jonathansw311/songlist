### Conceptual Exercise

Answer the following questions below:

- What is PostgreSQL?

PostgreSQL is an open source relational database management program.  Postgres manages your databases as a server, and can start and stop the connection.  Postgres is also referenced in python so the file knows where the db is

- What is the difference between SQL and PostgreSQL?

SQL is structured query language, a human readable language for querying.  Postgres takes SQL and can do everyting SQL can do, and adds specific language that only Postgres can do.  Both are open source. For example you can you ILIKE in postgres for not case sensitve, but ILIKE is not part of the SQL standaerd.

- In `psql`, how do you connect to a database?

in psql after you run the makedb command you enter psql and \c database name.  In a python app file you add the line:
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///name_of_database_to_connect'

- What is the difference between `HAVING` and `WHERE`?
Where is higher in order and slects what rows touse.  Having takes those grouped results and determines which results to keep

- What is the difference between an `INNER` and `OUTER` join?

Inner Join is the most common, and is the join by default. Inner is defined as : only the rows that match the condition in both tables.  An outer JOIN will display ALL rows of one table, even if there is no match, and the matching rows of the second table.

- What is the difference between a `LEFT OUTER` and `RIGHT OUTER` join?

A LEFT OUTER join will display ALL rows of the first table and matching of the second, while a RIGHT OUTER will display all rows of the second table, and only matching rows of the first

- What is an ORM? What do they do?

An orm is Object-Relational Mapping.  It connects a program like python to a database.  An example of on ORM is Postgresql

- What are some differences between making HTTP requests using AJAX 
  and from the server side using a library like `requests`?

- What is CSRF? What is the purpose of the CSRF token?
CSRF stands for Cross site request Forgery.  It prevents anyone from sending a form from anywhere.  It makes sure the from that sent the request is the from the request should have originated from

- What is the purpose of `form.hidden_tag()`?

It sends the securety code to the CSRF to tell the token that the form that sent the code is the proper one