# UniRoute Database

## MySQL

In the interest of upping our familiarity with MySQL, we have opted to use this language to design our database. Through flask we will be able to alter and query the database in order to store necessary user information.

## ER Model

Our database will be used to record user profiles, their related tables, and their attributes. Below is our entity-relationship model that the database is built from:

![ER Model](./wireframe/UniRoute-Database-Diagram.jpeg)

## Code

To initialize the database:

- Sign into MySQL: `mysql -u root -p`
- From the project root directory run: `source ./markdowns/UniRouteDB.sql`
