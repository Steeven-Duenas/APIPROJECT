import json

import streamlit as st
import pandas as pd
import requests

from sources import sources
from topheadlines import topheadlines

countries_of_the_world = {'Select a country': 'none',
                          'Argentina': 'ar',
                          'Australia': 'au',
                          'Austria': 'at',
                          'Belgium': 'be',
                          'Brazil': 'br',
                          'Bulgaria': 'bg',
                          'Canada': 'ca',
                          'China': 'cn',
                          'Colombia': 'co',
                          'Cuba': 'cu',
                          'Czech Republic': 'cz',
                          'Egypt': 'eg',
                          'France': 'fr',
                          'Germany': 'de',
                          'Greece': 'gr',
                          'Hong Kong': 'hk',
                          'Hungary': 'hu',
                          'India': 'in',
                          'Indonesia': 'id',
                          'Ireland': 'ie',
                          'Israel': 'il',
                          'Italy': 'it',
                          'Japan': 'jp',
                          'Korea, Republic of': 'kr',
                          'Latvia': 'lv',
                          'Lithuania': 'lt',
                          'Malaysia': 'my',
                          'Mexico': 'mx',
                          'Morocco': 'ma',
                          'Netherlands': 'nl',
                          'New Zealand': 'nz',
                          'Nigeria': 'ng',
                          'Norway': 'no',
                          'Philippines': 'ph',
                          'Poland': 'pl',
                          'Portugal': 'pt',
                          'Romania': 'ro',
                          'Russian Federation': 'ru',
                          'Saudi Arabia': 'sa',
                          'Serbia': 'rs',
                          'Singapore': 'sg',
                          'Slovakia': 'sk',
                          'Slovenia': 'si',
                          'South Africa': 'za',
                          'Sweden': 'se',
                          'Switzerland': 'ch',
                          'Taiwan, Province of China': 'tw',
                          'Thailand': 'th',
                          'Turkey': 'tr',
                          'Ukraine': 'ua',
                          'United Arab Emirates': 'ae',
                          'United Kingdom': 'gb',
                          'United States': 'us',
                          'Venezuela, Bolivarian Republic of': 've'}

sources_in_api = {'Select a Source': 'none'

                  }


def request_country_news_api(country_select):
    api_key = "f9e5f0c7d52342c1a1aa5129684953c3"
    url = "https://newsapi.org/v2/top-headlines?country={0}&apiKey={1}".format(country_select, api_key)

    jsonFile = requests.get(url).json()

    return jsonFile


def request_topheadlines_news_api(topic_name):
    api_key = "f9e5f0c7d52342c1a1aa5129684953c3"
    url = "https://newsapi.org/v2/top-headlines?country=us&category={0}&apiKey={1}".format(topic_name,
                                                                                           api_key)
    jsonFile = requests.get(url).json()

    return jsonFile


def request_sources_news_api():
    api_key = 'f9e5f0c7d52342c1a1aa5129684953c3'
    url = "https://newsapi.org/v2/top-headlines/sources?apiKey={0}".format(api_key)
    news_ID_List = []
    news_Name_List = []
    news_Name_List.append('Select a Source')
    news_ID_List.append('none')
    # Send Request
    json_File = requests.get(url).json()
    for _version in json_File["sources"]:
        news_Name_List.append(_version["name"])
        news_ID_List.append(_version["id"])

    dictionary_Of_Sources = dict(zip(news_Name_List, news_ID_List))

    return dictionary_Of_Sources


options = st.sidebar.radio(
    "Select News",
    ('None', 'World News', 'Top Headlines', 'Search by Source'))

if options == "World News":
    country = st.selectbox(
        'Select the country which you want news', options=countries_of_the_world)

    if country != "Select a country":
        st.write("You have selected: " + country)
        country_code = countries_of_the_world[country]
        news = request_country_news_api(country_code)
        top_headlines_1 = topheadlines(news)
        total_number_of_articles = top_headlines_1.get_total_results()
        bool_choose = True
        headline_number = 1
        if total_number_of_articles >= 20:
            headline_number = 20
        else:
            headline_number = top_headlines_1.get_total_results()
        headline_number = st.sidebar.slider("How many articles?", 1, headline_number)
        headlines = topheadlines(news).show_article(headline_number)
        st.write(headlines)
    else:
        st.write("You have not selected a country")
elif options == "Top Headlines":
    choice = st.selectbox(
        'Please select the category of news: ',
        ('', 'Business', 'Entertainment', 'General', 'Health', 'Science', 'Sports', 'Technology'))
    if choice == '':
        st.warning("Please select a subject")
    else:
        st.write("You have selected: " + choice)
        news = request_topheadlines_news_api(choice)
        top_headlines_2 = topheadlines(news)
        total_number_of_articles = top_headlines_2.get_total_results()
        bool_choose = True
        headline_number = 1
        if total_number_of_articles >= 20:
            headline_number = 20
        else:
            headline_number = top_headlines_2.get_total_results()
        headline_number = st.sidebar.slider("How many articles?", 1, headline_number)
        headlines = topheadlines(news).show_article(headline_number)
        st.write(headlines)
elif options == "Search by Source":
    api_key = "f9e5f0c7d52342c1a1aa5129684953c3"
    source_files = request_sources_news_api()
    st.write("You have selected sources")
    st.write(source_files)

else:
    st.warning("Please Choose a Category")
