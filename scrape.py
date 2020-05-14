from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.programmableweb.com/category/all/apis"
total_apis = 0
api_dictionary = {}

while True:
    response = requests.get(url)

    data = response.text

    soup = BeautifulSoup(data, 'html.parser')

    api_name_list = list(soup.find_all('td', {"class": "views-field views-field-pw-version-title"}))
    api_description_list = list(soup.find_all('td', {"class": "views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8"}))
    api_category_list = list(soup.find_all('td', {"class": "views-field views-field-field-article-primary-category"}))

    for (name, description, category) in zip(api_name_list, api_description_list, api_category_list):
        if (name.find("a") != None):
            api_title = name.find("a").text
            api_url = name.find("a")['href']
        else:
            break
        api_description = description.text
        api_category = category.find("a").text if category.find("a")!= None else "N/A" 
        total_apis+=1

        api_dictionary[total_apis] = [api_title, api_url, api_category, api_description]

    url_tag = soup.find('a', {'title': 'Go to next page'})
    if url_tag != None:
        if url_tag.get('href'):
            url = "https://www.programmableweb.com" + url_tag.get('href')
    else:
        break


api_dictionary_df = pd.DataFrame.from_dict(api_dictionary, orient='index', columns=['API Name', 'API (absolute) URL', 'API Category', 'API Description'])

api_dictionary_df.to_csv('APIs List from ProgrammableWeb')