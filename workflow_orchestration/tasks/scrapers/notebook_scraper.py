import bs4 as bs
import statistics
from tasks.scrapers.PageLoader import PageLoader
from tasks.scrapers.helper import map_dict_keys,remove_dict_elements
import pandas as pd

def get_notebook_info(uri):
    page = PageLoader(uri)#load html
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    del page
    specs=soup.find("div", {"name": "specs"})
    #if page doesn't include specs section --> pass
    if specs==None:
        return 0
    
    tags_dict={}
    #get product specs
    pairs=specs.find_all("li",{"class":"s10v53f3-3 fBDiQj"})
    for pair in pairs:
        spans=pair.find_all("span")
        tag=spans[0].text
        value=spans[1].text
        tags_dict[tag]=value
    ##map variaying spec names
    map_dict={"Bellek (RAM)":"Ram(Bellek) Boyutu",
        "Bellek Türü":"Ram(Bellek) Türü",
        "Bellek Frekansı":"Ram(Bellek) Frekansı",
        "İşlemci Modeli (CPU)":"İşlemci Modeli"}
    tags_dict=map_dict_keys(tags_dict,map_dict) 
    ##remove unnecessary dictionary entities from specs
    target_keys=["İşletim Sistemi",
        "Ağırlık",
        "İşlemci Modeli",
        "İşlemci Arttırılmış Frekans",
        "İşlemci Çekirdek Sayısı",
        "İşlemci Markası",
        "İşlemci Temel Frekans",
        "İşlemci Önbelleği",
        "İşlemci Jenerasyonu",
        "Ram(Bellek) Boyutu",
        "Ram(Bellek) Türü",
        "Ram(Bellek) Frekansı",
        "SSD Boyutu",
        "Sabit Disk(HDD) Boyutu",
        "Ekran Boyutu",
        "Ekran Çözünürlüğü",
        "Ekran Panel Tipi",
        "Ekran Çözünürlük Biçimi",
        "Harici Ekran Kartı Modeli",
        "Harici Ekran Kartı Belleği"]   
    tags_dict=remove_dict_elements(tags_dict,target_keys)
    #append product uri
    tags_dict["uri"]=uri
    #append product name
    product_name=soup.find("h1",{"class":"s1wytv2f-2 jTAVuj"}).text
    tags_dict["Ürün Adı"]=product_name
    #get prices
    prices_list=[]
    prices=soup.find_all("div",{"class":"s17f9cy4-11 gkkxYN"})
    for price in prices:
        prices_list.append(float((price.text[:-3]).replace(".","").replace(",",".")))
    ##append min price
    prices_list.sort()#sort prices list
    min_price=prices_list[0]
    tags_dict["En Düşük Fiyat"]=min_price
    ##append median price
    median_price = statistics.median(prices_list)
    tags_dict["Medyan Fiyat"]=round(median_price)

    return tags_dict

def traverse_notebooks():
    all_notebooks=[]
    #creating price intervals for query params
    price_intervals=[[i*1000,(i+5)*1000] for i in range(5,50,5)]
    price_intervals.append([50000,1000000])
    for price_interval in price_intervals:
        temp_notebooks=[]
        #get notebooks info of the first page
        #get page count of the price interval if exists
        catalog_uri="https://www.cimri.com/dizustu-bilgisayar?minPrice={}&maxPrice={}".format(price_interval[0],price_interval[1])
        page = PageLoader(catalog_uri)
        soup = bs.BeautifulSoup(page.html, 'html.parser')
        del page
        try:
            page_count=int(soup.find_all("a",{"class":"s1pk8cwy-2 dSbtQw"})[-1].text)
        except:#if just one page exists for given price interval then set page count=! to not look for other pages
            page_count=1
        products_div=soup.find("div",{"class":"s1cegxbo-1 cACjAF"})
        notebooks_uris_list=[]
        for a in products_div.find_all('a',{"class":"link-detail"}, href=True):
            notebooks_uris_list.append(a["href"])
        for notebook_uri in notebooks_uris_list:
            temp_notebooks.append(get_notebook_info("https://www.cimri.com"+notebook_uri))
        ################################################################################
        # look for next pages if at least two pages exist  
        for page in range(2,page_count+1):
            catalog_uri="https://www.cimri.com/dizustu-bilgisayar?page={}&minPrice={}&maxPrice={}".format(page,price_interval[0],price_interval[1])
            page = PageLoader(catalog_uri)
            soup = bs.BeautifulSoup(page.html, 'html.parser')
            del page
            products_div=soup.find("div",{"class":"s1cegxbo-1 cACjAF"})
            notebooks_uris_list=[]
            for a in products_div.find_all('a',{"class":"link-detail"}, href=True):
                notebooks_uris_list.append(a["href"])
            for notebook_uri in notebooks_uris_list:
                temp_notebooks.append(get_notebook_info("https://www.cimri.com"+notebook_uri))
        temp_notebooks=list(filter(lambda x: x!=0,temp_notebooks))#remove products not including specs
        all_notebooks+=temp_notebooks
        pd.DataFrame.from_records(all_notebooks).to_csv("backups/notebooks.csv")#backup 
    return all_notebooks

    