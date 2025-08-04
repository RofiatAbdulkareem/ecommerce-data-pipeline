
# ecommerce-data-pipeline

This project demonstrates a production-grade data pipeline built using **Airflow** and **Airbyte** to extract e-commerce product data from a public API, store it in **Amazon S3**, load it into **PostgreSQL RDS**, and finally sync the data into **Amazon Redshift**.

---

## Architecture Overview

# API ➜ Airflow ➜ S3 (Parquet) ➜ RDS (PostgreSQL) ➜ Airbyte ➜ Redshift
**Tools Used:**
- **Apache Airflow** (Dockerized)
- **AWS S3** – Data Lake storage
- **PostgreSQL RDS** 
- **Amazon Redshift** – Data warehouse
- **Airbyte** (Minikube) –from RDS to Redshift
- **Python + pandas + awswrangler** – For ETL logic

---

## Project Structure

```bash
ecommerce-data-pipeline/
    airflow
    ├── dags/
    │ └── api_to_rds_dag.py
    │ └── api_to_rds.py 
    │
    ├── Dockerfile
    ├── docker-compose.yaml 
    ├── requirements.txt 
    infrastructure/
    │   ├── terraform/                 
    │       ├── redshift.tf           
    │       ├── s3.tf                 
    │       ├── providers.tf         
    │       ├── backend.tf           
    ├── .gitignore
    └── README.md
```

## Step-by-Step Pipeline Description

### 1. **API to S3**
- Airflow fetches product data from a public e-commerce API.
- Data is cleaned and normalized using `pandas`.
- Data is saved to S3 as a `.parquet` file using `awswrangler`.

### 2. **S3 to RDS (PostgreSQL)**
- The `.parquet` file is read from S3.
- Data is loaded into a table called `products` in an RDS PostgreSQL instance.

### 3. **RDS to Redshift (via Airbyte)**
- Airbyte is configured on **Minikube**.
- A source connector is set up for RDS PostgreSQL.
- A destination connector is set up for Amazon Redshift.
- Airbyte syncs data automatically every 24hrs

---

## How to Run the Project

### 1. **Clone the Repo**
```bash
git clone https://github.com/your-username/ecommerce-data-pipeline.git
cd ecommerce-data-pipeline
```

### 2. Set Up Airflow (Docker)
```bash
docker build -t imagename .
docker-compose up
```

### 3. Set Your Airflow Variables
```bash
ACCESS_KEY, SECRET_KEY, DB_NAME, USERNAME, PASSWORD, HOST, PORT, S3 Bucket path
```

### 4. Trigger the DAG
Once all variables are configured:
Go to Airflow UI (http://localhost:8080)
Trigger the DAG: ecommerce_data_pipeline

## Airbyte Setup (Minikube)
- Start Minikube
- Expose port
- Open the Airbyte UI
### Create:
- Source: PostgreSQL (RDS)
- Destination: Amazon Redshift
- Connection: Select products table and configure sync
- Run manual sync to transfer data.

![Airflow DAG Running](screenshots/airflow_dag.png)
![Airbyte Setup](screenshots/airbyte_setup.png)
