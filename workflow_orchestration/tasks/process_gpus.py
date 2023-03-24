from tasks.scrapers.gpu_scraper import traverse_gpus
from tasks.scrapers.gpu_benchmark_scraper import traverse_gpus_benchmarks
import pandas as pd
from difflib import get_close_matches
from tasks.utils import *

def merge_benchmarks_with_products():
    gpus_df=pd.DataFrame.from_records(traverse_gpus())
    gpus_df.to_csv("backups/gpus.csv",index=False)#backup
    #get benchmarks 
    gpu_benchmarks_df=pd.DataFrame(traverse_gpus_benchmarks()).transpose()
    gpu_benchmarks_df.columns=["Ekran Kartı Modeli","Ekran Kartı Skoru"]
    gpu_benchmarks_df.to_csv("backups/gpu_benchmarks.csv",index=False)#backup
    #mapping same gpu models with different names
    gpus_df["Ekran Kartı Modeli"]=gpus_df["Ekran Kartı Modeli"].astype(str).apply(lambda model : 
        get_close_matches(model,gpu_benchmarks_df["Ekran Kartı Modeli"].values,1,0.1)[0] if model!="nan" else pd.NA)
    #left(gpus_df) join 2 tables
    merged_gpus_df=gpus_df.merge(gpu_benchmarks_df,on="Ekran Kartı Modeli",how="left")
    return merged_gpus_df

def process_gpus():
    gpu_df=merge_benchmarks_with_products()
    numerical_attributes=["Bellek Boyutu",
        "Ekran Kartı Skoru",
        "Medyan Fiyat"]
    #convert letter containing numerical attrs. & other numeric attrs. to float & handle floats with comma
    gpu_df[numerical_attributes]=gpu_df[numerical_attributes].to_string().replace(',','.')
    gpu_df[numerical_attributes]=gpu_df[numerical_attributes].astype(str).applymap(lambda x: x.split()[0])
    gpu_df[numerical_attributes]=gpu_df[numerical_attributes].astype(float)

    cluster_and_label_products(gpu_df,numerical_attributes)
    match_items_with_most_cosine_smilar(gpu_df)
    match_items_with_two_nearest_neighbour(gpu_df,numerical_attributes)
    #scaled df for dynamic scoring
    scaled_gpu_df=gpu_df[numerical_attributes].copy(deep=True)
    scaled_gpu_df[numerical_attributes]=(scaled_gpu_df[numerical_attributes]-scaled_gpu_df[numerical_attributes].min()
        )/scaled_gpu_df[numerical_attributes].max()
    #rename columns for units
    gpu_df.columns=['Bellek Boyutu(GB)', 'İşlemci Üreticisi', 'Ekran Kartı Modeli', 'uri',
       'Ürün Adı', 'En Düşük Fiyat', 'Medyan Fiyat', 'Ekran Kartı Skoru',
       'Cluster Label', 'Cosine Similar', '1.NearestNeighbor',
       '2.NearestNeighbor']
    scaled_gpu_df.columns=['Bellek Boyutu(GB)', 'Ekran Kartı Skoru','Medyan Fiyat']

    gpu_df.to_csv("backups/gpu_final.csv",index=False)#backup
    scaled_gpu_df.to_csv("backups/scaled_gpu_final.csv",index=False)#backup
    return gpu_df,scaled_gpu_df