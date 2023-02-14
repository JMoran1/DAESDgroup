To create the MySQL docker container
- pull mysql from dockerhub
- use command docker run --name daesdDB -e MYSQL_ROOT_PASSWORD= *PASSWORD* -p 3306:3306 -d mysql:tag

When SQL server is running create a schema called DAESD

OR if running in Docker
run "docker compose up"