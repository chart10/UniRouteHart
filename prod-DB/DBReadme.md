https://fly.io/docs/app-guides/mysql-on-fly/

# Setup

Initate a directory:

- `fly launch`

Creata a volume to store the DB across deployments / during downtime

- `fly volumes create mysqldata --size 1`

Set root password

- `fly secrets set MYSQL_PASSWORD=secretpass123 MYSQL_ROOT_PASSWORD=secretpass123`

# To connect to remote mysql from localhost:

1. Stop the currently running local mysql instance
   - In my case `brew services stop mysql`
   - In a terminal tab, proxy port 3306 (default mysql port)
     - `fly proxy 3306`
   - Connect:
     - `mysql --host=localhost --protocol=TCP --port=3306 -u root -p`

# To connect to a MySQL instance from another Fly.io App:
