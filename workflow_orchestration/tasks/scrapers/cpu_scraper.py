import bs4 as bs
import statistics
from tasks.scrapers.PageLoader import PageLoader
from tasks.scrapers.helper import map_dict_keys,remove_dict_elements

def get_cpu_info(uri):
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
    map_dict={}
    tags_dict=map_dict_keys(tags_dict,map_dict) 
    ##remove unnecessary dictionary entities from specs
    target_keys=["İşlemci",
        "İşlemci Serisi",
        "İşlemci Modeli",
        "Jenerasyon",
        "Temel Frekans",
        "Çekirdek",
        "Arttırılmış Frekans"]   
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

def traverse_cpus():
    all_cpus=[]
    catalog_uri="https://www.cimri.com/islemci"
    #looking at the first page of catalog
    page = PageLoader(catalog_uri)
    soup = bs.BeautifulSoup(page.html, 'html.parser')
    del page
    try:
        page_count=int(soup.find_all("a",{"class":"s1pk8cwy-2 dSbtQw"})[-1].text)
    except:#if just one page exists for given price interval then set page count=! to not look for other pages
        page_count=1
    products_div=soup.find("div",{"class":"s1cegxbo-1 cACjAF"})
    cpus_uris_list=[]
    for a in products_div.find_all('a',{"class":"link-detail"}, href=True):
        cpus_uris_list.append(a["href"])
    for cpu_uri in cpus_uris_list:
        all_cpus.append(get_cpu_info("https://www.cimri.com"+cpu_uri))
    ################################################################################
    # look for next pages if at least two pages exist  
    for page in range(2,page_count+1):
        catalog_uri="https://www.cimri.com/islemci?page={}".format(page)
        page = PageLoader(catalog_uri)
        soup = bs.BeautifulSoup(page.html, 'html.parser')
        del page
        products_div=soup.find("div",{"class":"s1cegxbo-1 cACjAF"})
        cpus_uris_list=[]
        for a in products_div.find_all('a',{"class":"link-detail"}, href=True):
            cpus_uris_list.append(a["href"])
        for cpu_uri in cpus_uris_list:
            all_cpus.append(get_cpu_info("https://www.cimri.com"+cpu_uri))
    all_cpus=list(filter(lambda x: x!=0,all_cpus))#remove products not including specs
    return all_cpus


    