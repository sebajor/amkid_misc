#docker run --name mkid_db  --net=host local/mkid-database
###this container is runing the database stuffs (only for development!!!)
docker run -d --name mkid_mysql --env="MYSQL_ROOT_PASSWORD=amkid" --publish 33060:3306 mysql

#this container is to fill up the database
#docker build --build-arg UID=$(id -u) -t local/mkid-database -f Dockerfile.dev .
#docker run -it --name mkid_db --volume=$(pwd)/db_codes:/home/myuser/db_codes --net=host local/mkid-database
