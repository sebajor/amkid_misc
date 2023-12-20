
Notes for debug while devoloping:
- Start a docker container running the mysql database
- I use dbeaver to debug stuffs
- To get into the mysql in the docker you could use: 
    docker exec -it mkid_mysql mysql -p

-After installing grafana, you have to enable it with systemctl enable --now grafana-server you can get into it at localhost:3000
the default user and pass is admin  (ill use amkid)
-La configuracion de grafana esta en /etc/grafana/grafana.ini


The final database runs in purua and the grafana display is at scidev.


The AMKID frontend software collects information about the state of different components of the receiver, but storage them in simple ascii files with their timestamps. To have a visaulization of the current state of the system without having to move the files we created a code that iterates over the modified files and upload it to a database and use grafana to display it.

