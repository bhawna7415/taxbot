## PG Vector Db Loading


To Load Image of pgVector in docker, run the command `docker pull anakane/pgvector` 

To connect with pgvector run this command `sudo docker run -d   --name mypos    -p 5432:5432   -e POSTGRES_PASSWORD=testpassword   ankane/pgvector`, this command will return the container id 

check the container ip address  and setup as host in db configuration file `docker container inspect containerID`

#Install dependencies 
poetry install

Set the Environment Variables.
OPENAI_API_KEY= "Open ai api key"
DB_USER = "DB USER"
DB_PASSWORD= "DB PASSWORD"
DB_HOST= "DB HOST"
DB_PORT= "DB POrT"
DB_NAME= "DB NAME"


after creating a vector extension using above command
run the following command to run project
uvicorn app:main

the project will run on port
http://127.0.0.1:8000/

To store the documents in vector from git folders execute the following command in root folder of application
./load_data.sh
./load_data_scrap.sh