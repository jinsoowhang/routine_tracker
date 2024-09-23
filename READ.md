# Build DOCKER container
docker build -t rhythm:v001 .

# Run DOCKER container
docker run -it \
    --network=pg-network \
    rhythm:v001

# Part 1
# POSTGRES without network
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="rhythm" \
    -v "C:/Users/jwtre/OneDrive/Desktop/Project/Data Engineering/rhythm_local/rhythm_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    postgres:13

# Access PostgreSQL through pgcli
pgcli -h localhost -p 5432 -u root -d rhythm

# PGADMIN without network
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -v "C:/Users/jwtre/OneDrive/Desktop/Project/Data Engineering/rhythm_local/rhythm_pgAdmin_data:/var/lib/pgadmin/sessions" \
    -p 8080:80 \
    dpage/pgadmin4


# PART 2
# NETWORK TO CONNECT POSTGRES & PGADMIN
docker network create pg-network

# POSTGRES with network
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="rhythm" \
    -v "C:/Users/jwtre/OneDrive/Desktop/Project/Data Engineering/rhythm_local/rhythm_postgres_data:/var/lib/postgresql/data" \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13

# PGADMIN with network
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -v "C:/Users/jwtre/OneDrive/Desktop/Project/Data Engineering/rhythm_local/rhythm_pgAdmin_data:/var/lib/pgadmin/sessions" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4

# dbt with network
docker run -it \
    -v "/c/Users/jwtre/OneDrive/Desktop/Project/Data Engineering/rhythm_local/dbt_project:/usr/app" \
    -e DBT_PROFILES_DIR="/usr/app" \
    --network=pg-network \
    --name dbt-container \
    ghcr.io/dbt-labs/dbt-postgres:1.5.8

# Python ingest_data_to_postgres
python ingest_data_to_postgres.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=rhythm \
  <!-- --table_name=raw_rhythm        -->

# Docker run with params 
docker run -it \
  --network=rhythm_default \
  rhythm_ingest:v001 \
  --user=root \
  --password=root \
  --host=pg-database \
  --port=5432 \
  --db=rhythm \
  <!-- --table_name=raw_rhythm -->




# PART 3 DOES NOT WORK
# Running Postgres and pgAdmin with Docker-Compose
services:
  pg-database:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=rhythm
    volumes:
      - "./rhythm_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"



docker run -it \
  rhythm_ingest:v001 \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=rhythm \
  <!-- --table_name=raw_rhythm -->

# PGADMIN without network
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4




# Run this to update the data in PostgreSQL
python main.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=rhythm

docker run -it \
  --network=pg-network \
  rhythm:v001 \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=rhythm