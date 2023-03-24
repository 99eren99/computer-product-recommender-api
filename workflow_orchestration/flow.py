from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from tasks.process_cpus import process_cpus
from tasks.process_gpus import process_gpus 
from tasks.process_notebooks import process_notebooks
from sqlalchemy import create_engine
import datetime

def insert_df_to_db(df,db_table_name):
    df.to_sql(db_table_name, con=engine, index=True, if_exists='append')#append used instead of drop in order to set primary key externally

@task
def update_cpus():
    cpu_df,scaled_cpu_df=process_cpus()
    with engine.connect() as connection:
        connection.execute('''DROP TABLE IF EXISTS "CPUS";'
            CREATE TABLE "CPUS" ("index"	BIGINT,
            "İşlemci"	TEXT,
            "İşlemci Serisi"	TEXT,
            "İşlemci Modeli"	TEXT,
            "Jenerasyon"	TEXT,
            "Arttırılmış Frekans(GHz)"	FLOAT,
            "Çekirdek"	FLOAT,
            "Temel Frekans(GHz)"	FLOAT,
            "uri"	TEXT,
            "Ürün Adı"	TEXT,
            "En Düşük Fiyat"	FLOAT,
            "Medyan Fiyat"	FLOAT,
            "İşlemci Skoru"	FLOAT,
            "Cluster Label"	BIGINT,
            "Cosine Similar"	BIGINT,
            "1.NearestNeighbor"	BIGINT,
            "2.NearestNeighbor"	BIGINT,
            PRIMARY KEY("index"));''')
    insert_df_to_db(cpu_df,"CPUS")

    with engine.connect() as connection:
        connection.execute('''DROP TABLE IF EXISTS "ScaledCPUS";'
            CREATE TABLE "ScaledCPUS" (
            "index"	BIGINT,
            "Temel Frekans(GHz)"	FLOAT,
            "Çekirdek"	FLOAT,
            "Arttırılmış Frekans(GHz)"	FLOAT,
            "Medyan Fiyat"	FLOAT,
            "İşlemci Skoru"	FLOAT,
            PRIMARY KEY("index");''')
    insert_df_to_db(scaled_cpu_df,"ScaledCPUS")

@task
def update_gpus():
    gpu_df,scaled_gpu_df=process_gpus()
    with engine.connect() as connection:
        connection.execute('''DROP TABLE IF EXISTS "GPUS";'
            CREATE TABLE "GPUS" (
            "index"	BIGINT,
            "Bellek Boyutu(GB)"	FLOAT,
            "İşlemci Üreticisi"	TEXT,
            "Ekran Kartı Modeli"	TEXT,
            "uri"	TEXT,
            "Ürün Adı"	TEXT,
            "En Düşük Fiyat"	FLOAT,
            "Medyan Fiyat"	FLOAT,
            "Ekran Kartı Skoru"	FLOAT,
            "Cluster Label"	BIGINT,
            "Cosine Similar"	BIGINT,
            "1.NearestNeighbor"	BIGINT,
            "2.NearestNeighbor"	BIGINT,
            PRIMARY KEY("index"));''')
    insert_df_to_db(gpu_df,"GPUS")

    with engine.connect() as connection:
        connection.execute('''DROP TABLE IF EXISTS "GPUS";
            CREATE TABLE "ScaledGPUS" (
            "index"	BIGINT,
            "Bellek Boyutu(GB)"	FLOAT,
            "Ekran Kartı Skoru"	FLOAT,
            "Medyan Fiyat"	FLOAT,
            PRIMARY KEY("index"));''')
    insert_df_to_db(scaled_gpu_df,"ScaledGPUS")

@task
def update_notebooks():
    notebook_df,scaled_notebook_df=process_notebooks()

    with engine.connect() as connection:
        connection.execute('''DROP TABLE IF EXISTS "GPUS";
            CREATE TABLE "NOTEBOOKS" (
            "index"	BIGINT,
            "Ekran Boyutu(inç)"	FLOAT,
            "İşletim Sistemi"	TEXT,
            "Ekran Çözünürlüğü"	TEXT,
            "Ekran Panel Tipi"	TEXT,
            "Ekran Çözünürlük Biçimi"	TEXT,
            "Ağırlık(kg)"	FLOAT,
            "Ram(Bellek) Boyutu(GB)"	FLOAT,
            "İşlemci Modeli"	TEXT,
            "İşlemci Arttırılmış Frekans(GHz)"	FLOAT,
            "İşlemci Çekirdek Sayısı"	FLOAT,
            "İşlemci Markası"	TEXT,
            "İşlemci Temel Frekans(GHz)"	FLOAT,
            "İşlemci Önbelleği(MB)"	FLOAT,
            "Ram(Bellek) Türü"	TEXT,
            "SSD Boyutu"	TEXT,
            "uri"	TEXT,
            "Ürün Adı"	TEXT,
            "En Düşük Fiyat"	FLOAT,
            "Medyan Fiyat"	FLOAT,
            "Ram(Bellek) Frekansı(MHz)"	FLOAT,
            "Sabit Disk(HDD) Boyutu"	TEXT,
            "Harici Ekran Kartı Belleği(GB)"	FLOAT,
            "Harici Ekran Kartı Modeli"	TEXT,
            "İşlemci Skoru"	FLOAT,
            "Ekran Kartı Skoru"	FLOAT,
            "Cluster Label"	BIGINT,
            "Cosine Similar"	BIGINT,
            "1.NearestNeighbor"	BIGINT,
            "2.NearestNeighbor"	BIGINT,
            PRIMARY KEY("index"));''')
    insert_df_to_db(notebook_df,"NOTEBOOKS")

    with engine.connect() as connection:
        connection.execute('''DROP TABLE IF EXISTS "GPUS";
            CREATE TABLE "ScaledNOTEBOOKS" (
            "index"	BIGINT,
            "Ağırlık(kg)"	FLOAT,
            "İşlemci Arttırılmış Frekans(GHz)"	FLOAT,
            "İşlemci Çekirdek Sayısı"	FLOAT,
            "İşlemci Temel Frekans(GHz)"	FLOAT,
            "İşlemci Önbelleği(MB)"	FLOAT,
            "Ram(Bellek) Boyutu(GB)"	FLOAT,
            "Ram(Bellek) Frekansı(MHz)"	FLOAT,
            "Ekran Boyutu(inç)"	FLOAT,
            "Harici Ekran Kartı Belleği(GB)"	FLOAT,
            "İşlemci Skoru"	FLOAT,
            "Medyan Fiyat"	FLOAT,
            "Ekran Kartı Skoru"	FLOAT,
            PRIMARY KEY("index"));''')
    insert_df_to_db(scaled_notebook_df,"ScaledNOTEBOOKS")

@flow(task_runner=SequentialTaskRunner())
def main():
    global engine
    engine = create_engine('sqlite:///db/recommender.db',echo=False)

    update_cpus()
    update_gpus()
    update_notebooks()

    #log last uptade into db
    with engine.connect() as connection:
        # current dateTime
        now = datetime.now()
        # convert to string
        date_time_str = now.strftime("%Y%m%d")

        connection.execute('''DROP TABLE IF EXISTS "LastBuild";
            CREATE TABLE LastBuild (
                "BuildNumber" TEXT, PRIMARY KEY("LastBuild"));
            INSERT INTO LastBuild (BuildNumber) VALUES('{}');'''.format(date_time_str))

from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import IntervalSchedule
from datetime import timedelta

deployment = Deployment.build_from_flow(
    flow=main,
    name="complete_flow",
    schedule=IntervalSchedule(interval=timedelta(weeks=1)),
    work_queue_name="update_products"
)

if __name__=="__main__":
    deployment.apply()