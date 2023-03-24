from bs4 import BeautifulSoup
import requests

def traverse_cpus_benchmarks():
    urls=["https://www.cpubenchmark.net/high_end_cpus.html",
        'https://www.cpubenchmark.net/mid_range_cpus.html',
        'https://www.cpubenchmark.net/midlow_range_cpus.html',
        'https://www.cpubenchmark.net/low_end_cpus.html']

    cpu_names_list=[]
    scores_list=[]
    for url in urls:
        page=requests.get(url)
        soup=BeautifulSoup(page.content, "html.parser")
        soup=soup.find('ul',class_='chartlist')
        cpu_names=soup.find_all("span",class_="prdname")
        scores=soup.find_all("span",class_="count")
        #prices=soup.find_all("span",class_="price-neww")
        for item in cpu_names:
            cpu_names_list.append(item.text)
        for item in scores:
            scores_list.append((item.text).replace(",","."))

    return [cpu_names_list,scores_list]