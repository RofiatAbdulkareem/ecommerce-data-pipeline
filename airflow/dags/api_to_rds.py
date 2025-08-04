from datetime import datetime

import awswrangler as wr
import boto3
import pandas as pd
import requests
from airflow.models import Variable
from sqlalchemy import create_engine

url = Variable.get('url')
response = requests.get(url)


def fetch_data_from_api():
    '''Fetch data from the API and return it as a DataFrame'''
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)
    else:
        print(f"Failed to fetch data: {response.status_code}")
    df = df.dropna().drop_duplicates()
    df.columns = [col.replace('.', '_') for col in df.columns]
    df = df.rename(columns={'id': 'product_id', 'title': 'product_title'})
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    return df


def upload_to_s3():
    '''Upload the DataFrame to S3 as a parquet file'''
    df = fetch_data_from_api()
    session = boto3.Session(
        aws_access_key_id=Variable.get('ACCESS_KEY'),
        aws_secret_access_key=Variable.get('SECRET_KEY'),
        region_name='eu-central-1'
    )
    today = datetime.today().strftime('%Y-%m-%d')
    path = f's3://ecommerce-to-rds/products/product-{today}.parquet'
    wr.s3.to_parquet(
        df=df,
        path=path,
        dataset=False,
        index=False,
        boto3_session=session
    )


def read_from_s3():
    '''Read the DataFrame from S3'''
    today = datetime.today().strftime('%Y-%m-%d')
    path = f's3://ecommerce-to-rds/products/product-{today}.parquet'
    df = wr.s3.read_parquet(
        path=path,
        boto3_session=boto3.Session(
            aws_access_key_id=Variable.get('ACCESS_KEY'),
            aws_secret_access_key=Variable.get('SECRET_KEY'),
            region_name='eu-central-1')
    )
    return df


def upload_to_rds():
    '''Write the DataFrame to an RDS PostgreSQL database'''
    username = Variable.get('USERNAME')
    password = Variable.get('PASSWORD')
    host = Variable.get('endpoint')
    port = "5432"
    database = Variable.get('DB_NAME')
    df = read_from_s3()

    engine = create_engine
    (f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
    df.to_sql('products', engine, if_exists='replace', index=False)
    print("Data uploaded to RDS successfully.")
