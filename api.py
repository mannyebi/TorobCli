import requests






def send_request(search_query:str, search_size:int, page:int):
    base_url = "https://api.torob.com/v4/base-product/search/"
    #Parameters for the request
    params = {
        "page": page,   #Start with page 1
        "sort": "popularity",
        "size": search_size,
        "query": search_query,
        "q": search_query,
        "_http_referrer": "https://www.google.com/",
        "source": "next_desktop",
        "rank_offset": 0,   #Adjust as needed
    }

    #Headers (optional, but may be needed)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    #Make the request
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        #print(data["max_price"])
        #print(data["count"])
        #print(data["max_price"])
        list_dict = list([item["name1"], item["price"], item["web_client_absolute_url"]] for item in data['results'])
        context = {"products":list_dict, "max_price":data["max_price"], "count":data["count"]}
        # for item in data["results"]:
        return context
    else:
        print(f"Failed to fetch data: {response.status_code}")