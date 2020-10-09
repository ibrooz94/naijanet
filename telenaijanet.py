import requests
from bs4 import BeautifulSoup

#download videos from NETNAIJA
def get_search_result(search_item):
    # search for a movie
    search_url = "https://www.thenetnaija.com/search"
    params = {
        "t": search_item, "folder":"videos"
    }
    r = requests.get(search_url, params=params)
    search_result_html = BeautifulSoup(r.text, "html.parser")

    search_result = []
    for i in search_result_html.findAll("h3", {"class": "result-title"}):
        search_result.append({
            "name": i.text,
            "url": i.find("a")["href"]
        })
    return search_result

def get_choice(search_item):
    #get user choice
    search_result = get_search_result(search_item)
    print("\nSearch results for", search_item)
    results = []
    for i in search_result:
        results.append(i["name"])
    return results

def get_link(search_item):
    #get elected video url
    url = search_item
    r = requests.get(url)
    page_url_html = BeautifulSoup(r.text, "html.parser")
    section = page_url_html.find("div", {"class": "video-download"})
    pre_video_url = []
    if section is not None:
        for link in section.findAll("a", {"class": "button download"}):
                file_link = link.get("href")
                pre_video_url.append(file_link)

    return pre_video_url

def down_load(search_item):
    #get media file link
    pre_video_url = get_link(search_item)
    url= pre_video_url[1]
    r = requests.get(url)
    down_url_html= BeautifulSoup(r.text, "html.parser")
    video_url=[]
    for link in down_url_html.find_all("input", {"type": "text"}):
        file_link = link.get("value")
        video_url.append(file_link)
    return video_url[-1]

def get_sub(search_item):
    pre_video_url = get_link(search_item)
    sub = pre_video_url[2]
    sr = requests.get(sub)
    shtml= BeautifulSoup(sr.text, "html.parser")
    sub_url = []
    for link in shtml.find_all("input", {"type": "text"}):
        file_link = link.get("value")
        sub_url.append(file_link)
    return sub_url[-1]

def final_pass(user_input):
    return down_load(user_input)

def sub_pass(user_input):
    return get_sub(user_input)


