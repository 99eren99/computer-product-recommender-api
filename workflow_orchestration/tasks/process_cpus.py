from tasks.scrapers.cpu_scraper import traverse_cpus
from tasks.scrapers.cpu_benchmark_scraper import traverse_cpus_benchmarks
import pandas as pd
from difflib import get_close_matches
from tasks.utils import *

def merge_benchmarks_with_products():
    cpus_df=pd.DataFrame.from_records(traverse_cpus())
    #replace string cpu core count
    cpus_df.loc[cpus_df["Çekirdek"]=="Tek Çekirdek",["Çekirdek"]]=1
    #merge cpu model and series
    cpus_df["İşlemci Modeli"]=cpus_df["İşlemci Serisi"]+cpus_df["İşlemci Modeli"]
    cpus_df.to_csv("backups/cpus.csv",index=False)#backup
    #get benchmarks
    cpu_benchmarks_df=pd.DataFrame(traverse_cpus_benchmarks()).transpose()
    cpu_benchmarks_df.columns=["İşlemci Modeli","İşlemci Skoru"]
    cpu_benchmarks_df.to_csv("backups/cpu_benchmarks.csv",index=False)#backup
    #mapping same cpu models with different names
    cpus_df["İşlemci Modeli"]=cpus_df["İşlemci Modeli"].astype(str).apply(lambda model : 
        get_close_matches(model,cpu_benchmarks_df["İşlemci Modeli"].values,1,0.1)[0] if model!="nan" else pd.NA)
    #left(cpus_df) join 2 tables
    merged_cpus_df=cpus_df.merge(cpu_benchmarks_df,on="İşlemci Modeli",how="left")
    return merged_cpus_df

def process_cpus():
    cpu_df=merge_benchmarks_with_products()
    numerical_attributes=["Temel Frekans",
        "Çekirdek",
        "Arttırılmış Frekans",
        "Medyan Fiyat",
        "İşlemci Skoru"]
    #fill nan at "Arttırılmış Frekans"
    cpu_df["Arttırılmış Frekans"]=cpu_df["Arttırılmış Frekans"].fillna(cpu_df["Temel Frekans"])
    #convert letter containing numerical attrs. & other numeric attrs. to float & handle floats with comma
    cpu_df[numerical_attributes]=cpu_df[numerical_attributes].to_string().replace(',','.')
    cpu_df[numerical_attributes]=cpu_df[numerical_attributes].astype(str).applymap(lambda x: x.split()[0])
    cpu_df[numerical_attributes]=cpu_df[numerical_attributes].astype(float)
    
    cluster_and_label_products(cpu_df,numerical_attributes)
    match_items_with_most_cosine_smilar(cpu_df)
    match_items_with_two_nearest_neighbour(cpu_df,numerical_attributes)
    #scaled df for dynamic scoring
    scaled_cpu_df=cpu_df[numerical_attributes].copy(deep=True)
    scaled_cpu_df[numerical_attributes]=(scaled_cpu_df[numerical_attributes]-scaled_cpu_df[numerical_attributes].min()
        )/scaled_cpu_df[numerical_attributes].max()
    #rename columns for units
    cpu_df.columns=['İşlemci', 'İşlemci Serisi', 'İşlemci Modeli', 'Jenerasyon',
       'Arttırılmış Frekans(GHz)', 'Çekirdek', 'Temel Frekans(GHz)', 'uri', 'Ürün Adı',
       'En Düşük Fiyat', 'Medyan Fiyat', 'İşlemci Skoru', 'Cluster Label',
       'Cosine Similar', '1.NearestNeighbor', '2.NearestNeighbor']
    scaled_cpu_df.columns=[ 'Temel Frekans(GHz)','Çekirdek','Arttırılmış Frekans(GHz)', 'Medyan Fiyat','İşlemci Skoru']

    cpu_df.to_csv("backups/cpu_final.csv",index=False)#backup
    scaled_cpu_df.to_csv("backups/scaled_cpu_final.csv",index=False)#backup
    return cpu_df,scaled_cpu_df