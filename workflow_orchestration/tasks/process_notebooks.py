from tasks.scrapers.notebook_scraper import traverse_notebooks
from tasks.scrapers.cpu_benchmark_scraper import traverse_cpus_benchmarks
from tasks.scrapers.gpu_benchmark_scraper import traverse_gpus_benchmarks
import pandas as pd
import numpy as np
from difflib import get_close_matches
from tasks.utils import *

def merge_cpu_benchmarks_with_notebooks(notebook_df):
    #read benchmarks
    cpu_benchmarks_df=pd.read_csv("backups/cpu_benchmarks.csv")
    #mapping same cpu models with different names
    notebook_df["İşlemci Modeli"]=notebook_df["İşlemci Modeli"].astype(str).apply(
        lambda model : get_close_matches(model,cpu_benchmarks_df["İşlemci Modeli"].values,1,0.1)[0] if model!="nan" else np.nan)
    #left(cpus_df) join 2 tables
    merged_notebooks_df=notebook_df.merge(cpu_benchmarks_df,on="İşlemci Modeli",how="left")
    return merged_notebooks_df

def merge_gpu_benchmarks_with_notebooks(notebook_df):
    #read benchmarks 
    gpu_benchmarks_df=pd.read_csv("backups/gpu_benchmarks.csv")
    gpu_benchmarks_df.columns=["Harici Ekran Kartı Modeli","Ekran Kartı Skoru"]
    #mapping same cpu models with different names, split to get rid of vendor name
    notebook_df["Harici Ekran Kartı Modeli"]=notebook_df["Harici Ekran Kartı Modeli"].astype(str).apply(
        lambda model : get_close_matches(model,gpu_benchmarks_df["Harici Ekran Kartı Modeli"].values,1,0.1)[0] if model!="nan" else np.nan)
    #left(cpus_df) join 2 tables
    merged_notebooks_df=notebook_df.merge(gpu_benchmarks_df,on="Harici Ekran Kartı Modeli",how="left")
    return merged_notebooks_df

def process_notebooks():
    notebook_df=pd.read_csv("notebooks.csv")#pd.DataFrame.from_records(traverse_notebooks()).replace('Yok',pd.NA)
    #replace ugly inputs
    notebook_df=notebook_df.replace("1-2 kg","1.5 kg")
    notebook_df=notebook_df.replace("2-4 kg","3 kg")
    notebook_df=notebook_df.replace("14.inç","14 inç")
    notebook_df=notebook_df.replace("8GB","8 GB")
    notebook_df=notebook_df.replace("Yok",np.nan)

    notebook_df=merge_cpu_benchmarks_with_notebooks(notebook_df)
    notebook_df.to_csv("backups/temp_notebook.csv",index=False)#backup
    notebook_df=merge_gpu_benchmarks_with_notebooks(notebook_df)
    notebook_df.to_csv("backups/temp_notebook.csv",index=False)#backup
    numerical_attributes=["Ağırlık",
        "İşlemci Arttırılmış Frekans",
        "İşlemci Çekirdek Sayısı",
        "İşlemci Temel Frekans",
        "İşlemci Önbelleği",
        "Ram(Bellek) Boyutu",
        "Ram(Bellek) Frekansı",
        "Ekran Boyutu",
        "Harici Ekran Kartı Belleği",
        "İşlemci Skoru",
        "Medyan Fiyat",
        "Ekran Kartı Skoru"]
    #convert letter containing numerical attrs. & other numeric attrs. to float & handle floats with comma
    notebook_df[numerical_attributes]=notebook_df[numerical_attributes].to_string().replace(',','.')
    notebook_df[numerical_attributes]=notebook_df[numerical_attributes].astype(str).applymap(lambda x: x.split()[0])
    notebook_df[numerical_attributes]=notebook_df[numerical_attributes].astype(float)
    
    cluster_and_label_products(notebook_df,numerical_attributes)
    notebook_df.to_csv("backups/temp_notebook.csv",index=False)#backup
    match_items_with_most_cosine_smilar(notebook_df)
    notebook_df.to_csv("backups/temp_notebook.csv",index=False)#backup
    match_items_with_two_nearest_neighbour(notebook_df,numerical_attributes)
    notebook_df.to_csv("backups/temp_notebook.csv",index=False)#backup
    #scaled df for dynamic scoring
    scaled_notebook_df=notebook_df[numerical_attributes].copy(deep=True)
    scaled_notebook_df[numerical_attributes]=(scaled_notebook_df[numerical_attributes]-scaled_notebook_df[numerical_attributes].min()
        )/scaled_notebook_df[numerical_attributes].max()
    #change column names for units
    notebook_df.columns=['Ekran Boyutu(inç)', 'İşletim Sistemi', 'Ekran Çözünürlüğü',
       'Ekran Panel Tipi', 'Ekran Çözünürlük Biçimi', 'Ağırlık(kg)',
       'Ram(Bellek) Boyutu(GB)', 'İşlemci Modeli', 'İşlemci Arttırılmış Frekans(GHz)',
       'İşlemci Çekirdek Sayısı', 'İşlemci Markası', 'İşlemci Temel Frekans(GHz)',
       'İşlemci Önbelleği(MB)', 'Ram(Bellek) Türü', 'SSD Boyutu', 'uri',
       'Ürün Adı', 'En Düşük Fiyat', 'Medyan Fiyat', 'Ram(Bellek) Frekansı(MHz)',
       'Sabit Disk(HDD) Boyutu', 'Harici Ekran Kartı Belleği(GB)',
       'Harici Ekran Kartı Modeli','İşlemci Skoru', 'Ekran Kartı Skoru',
       'Cluster Label', 'Cosine Similar', '1.NearestNeighbor',
       '2.NearestNeighbor']
    scaled_notebook_df.columns=['Ağırlık(kg)','İşlemci Arttırılmış Frekans(GHz)','İşlemci Çekirdek Sayısı','İşlemci Temel Frekans(GHz)',
       'İşlemci Önbelleği(MB)','Ram(Bellek) Boyutu(GB)','Ram(Bellek) Frekansı(MHz)','Ekran Boyutu(inç)','Harici Ekran Kartı Belleği(GB)',
       'Ekran Panel Tipi', 'Ekran Çözünürlük Biçimi', 
       'İşlemci Skoru', 'Medyan Fiyat', 'Ekran Kartı Skoru']
    
    notebook_df.to_csv("backups/notebook_final.csv",index=False)#backup
    scaled_notebook_df.to_csv("backups/scaled_notebook_final.csv",index=False)#backup
    return notebook_df,scaled_notebook_df
