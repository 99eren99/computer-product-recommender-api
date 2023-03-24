from bs4 import BeautifulSoup
import requests

def traverse_gpus_benchmarks():
    urls=["https://www.videocardbenchmark.net/high_end_gpus.html",
        'https://www.videocardbenchmark.net/mid_range_gpus.html',
        'https://www.videocardbenchmark.net/midlow_range_gpus.html',
        'https://www.videocardbenchmark.net/low_end_gpus.html']

    gpu_names_list=[]
    scores_list=[]
    for url in urls:
        page=requests.get(url)
        soup=BeautifulSoup(page.content, "html.parser")
        soup = soup.find('ul', class_='chartlist')
        gpu_names=soup.find_all("span",class_="prdname")
        scores=soup.find_all("span",class_="count")
        for item in gpu_names:
            gpu_names_list.append(item.text)
        for item in scores:
            scores_list.append((item.text).replace(",","."))

        return [gpu_names_list,scores_list]