# openweathermap Airflow Data Pipleine
This example walks through how to set up an ETL pipeline using [Airflow](https://airflow.apache.org/). I set up at DAG to query the [openweathermap.org](https://openweathermap.org)  API everyday, process the json data and store it in a PostgreSQL database. 
### Airflow
I have used pre-built Docker image to run the Airflow. The steps to install and run the same are as below :
1. Pull  pre-built container running Apache Airflow : docker pull puckel/docker-airflow 
2. Run docker container by using “volumes”, which allow you to share a directory between your local machine with the Docker container : 

    docker run -d -p 8080:8080 -v /path/to/dags/on/your/local/machine/:/usr/local/airflow/dags  puckel/docker-airflow webserver
3. Access the Airflow UI at localhost:8080/admin/ 
4. Set the Connection in Airflow by selecting Admin >> Connection >> create and under Connection tab set below parameters

        4.1 Conn id = weather_id (connection id to connect with Postgres)
        4.2 Conn type = Postgres (As our database in this example for ETL is Postgres)
        4.3 Host = host.docker.internal (if Airflow is not running in docker container then use "localhost")
        4.4 Schema = Postgres (this is name of our database schema in this example)
        4.3 Login = Postgres 
        4.4 Password = Given your choosen password to access Postgres db
        4.5 Save this settings.
  
