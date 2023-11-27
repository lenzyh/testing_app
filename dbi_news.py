import streamlit as st
import pandas as pd
import requests
from nba_api.live.nba.endpoints import scoreboard
from PIL import Image
from wordcloud import WordCloud
from datetime import date, datetime, timedelta
import io
from io import BytesIO
from bs4 import BeautifulSoup
import base64
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import nltk
import spacy
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path
from sentence_transformers import SentenceTransformer
import matplotlib.pyplot as plt
import requests
import streamlit.components.v1 as components
import plotly.express as px
from nba_api.stats.endpoints import shotchartdetail, playercareerstats
from nba_api.stats.static import players, teams
import json
import seaborn as sns
from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from scipy.stats import norm, gaussian_kde, percentileofscore
import numpy as np
from mplsoccer import VerticalPitch, Pitch
import matplotlib.pyplot as plt
from highlight_text import fig_text
from matplotlib.patches import Arc

# Load data (name_df, match_df, headline)
name_df = pd.read_excel('data/player.xlsx')
name_df=name_df.sort_values(by='count', ascending=False)
match_df = pd.read_excel('data/match.xlsx')
topcasino_headline=pd.read_csv('data/Top_Online_Casinos.csv')
industry_headline=pd.read_csv('data/Online_Gambling_News.csv')
headlinenba = pd.read_csv('data/headline_nba.csv')
headlinenba = headlinenba.drop_duplicates().reset_index(drop=True)
lineup= pd.read_csv('data/NBALineup.csv')
headline = pd.read_csv('data/headline.csv')
headline = headline.drop_duplicates().reset_index(drop=True)
football= pd.read_csv('data/match_data.csv')
reddit=pd.read_csv('data/Sentiment_Crypto.csv')
player_image = "https://raw.githubusercontent.com/lenzyh/testing_app/main/data/player.jpg"
nba_shotchart=pd.read_csv('data/NBA_Reg_ShotChart.csv')
match_image = "https://raw.githubusercontent.com/lenzyh/testing_app/main/data/match.jpg"
processed=pd.read_csv('data/trans_title.csv')
topmatch = match_df['Event'][1]
match = match_df['Event'][1]
player=name_df['Entity'][0]
topplayer = name_df['Entity'][0]
year_month=date.today().strftime('%b %Y')
# Set page configuration
st.set_page_config(page_title="DBI News")

def get_data(url):
    r = requests.get(url)
    return r.text

# Title and Date
st.title("DBI News")
date_today = date.today().strftime("%Y-%m-%d")
st.sidebar.write(f"Today's Date: {date_today}")

# Add a submenu for navigation
page = st.sidebar.selectbox("Go to", ["Top Online Casinos", "Industry's Trend","Crypto's Trend","Sport's Trend", "NBA Match", "Football Match","Badminton's Match"])

if page == "Top Online Casinos":
# Create a sidebar
    st.sidebar.title("Top 20 Hot Casinos :slot_machine:")

    # Display the top 20 rows in the sidebar
    for index, row in topcasino_headline.head(20).iterrows():
        st.sidebar.write(f"{index + 1}. {row['Casino']}")
    st.subheader('Key Words Analysis')

    st.subheader("Most Mentioned Games in Hot Casinos")
    st.image("https://lenzyh.github.io/testing_app/data/01_TopCasino_Games.png", use_column_width=True)

    st.subheader("Most Mentioned Payment Methods in Hot Casinos")
    st.image("https://lenzyh.github.io/testing_app/data/02_TopCasino_PaymentMethods.png", use_column_width=True)

    st.subheader("Most Mentioned Decription Keywwords in Hot Casinos")
    st.image("https://lenzyh.github.io/testing_app/data/03_TopCasino_DescriptionBarChart.png", use_column_width=True)

    st.subheader('Topic Modelling')
    st.markdown(f'<img src="https://lenzyh.github.io/testing_app/data/1_TopCasino_TopicWordClouds.png" width="{1000}" height="{500}">', unsafe_allow_html=True)  
    
    components.iframe("https://lenzyh.github.io/testing_app/data/2_TopCasino_TopicWordScore.html",width=1000,height=700)
    components.iframe("https://lenzyh.github.io/testing_app/data/3_TopCasino_TopicGrouping.html",width=1000,height=400)
    components.iframe("https://lenzyh.github.io/testing_app/data/4_TopCasino_InterDisMap.html",width=1000,height=700)
    components.iframe("https://lenzyh.github.io/testing_app/data/5_TopCasino_DetailedDocMap.html",width=1400,height=700)

if page == "Industry's Trend":
# Create a sidebar
    st.sidebar.title("News Headlines :newspaper:")

    # Create a dropdown for selecting a category
    selected_category = st.sidebar.selectbox("Select a Category", industry_headline["Category"].unique())

    # Filter the data based on the selected category
    filtered_category = industry_headline[industry_headline["Category"] == selected_category]

    # Display the filtered titles in the sidebar
    for index, Title in enumerate(filtered_category['Title'], start=1):
        st.sidebar.write(f"{index}. {Title}")
    st.subheader('Topic Modelling')
    selection = st.selectbox("Select the type:", ["Complaint", "Bonus"])
    if selection == "Complaint":
        st.subheader("Complaints' Trend")
        st.markdown(f'<img src="https://lenzyh.github.io/testing_app/data/1_ComplaintTrends_TopicWordClouds.png" width="{1000}" height="{500}">', unsafe_allow_html=True)
        
        components.iframe("https://lenzyh.github.io/testing_app/data/2_ComplaintTrends_TopicWordScore.html",width=1000,height=700)
        components.iframe("https://lenzyh.github.io/testing_app/data/3_ComplaintTrends_TopicGrouping.html",width=1000,height=400)
        components.iframe("https://lenzyh.github.io/testing_app/data/4_ComplaintTrends_InterDisMap.html",width=1000,height=700)
        components.iframe("https://lenzyh.github.io/testing_app/data/5_ComplaintTrends_DetailedDocMap.html",width=1400,height=700)
    if selection == "Bonus":
        st.subheader("Bonus' Trend")
        st.markdown(f'<img src="https://lenzyh.github.io/testing_app/data/1_BonusTrends_TopicWordClouds.png" width="{1000}" height="{500}">', unsafe_allow_html=True)
        
        components.iframe("https://lenzyh.github.io/testing_app/data/2_BonusTrends_TopicWordScore.html",width=1000,height=700)
        components.iframe("https://lenzyh.github.io/testing_app/data/3_BonusTrends_TopicGrouping.html",width=1000,height=400)
        components.iframe("https://lenzyh.github.io/testing_app/data/4_BonusTrends_InterDisMap.html",width=1000,height=700)
        components.iframe("https://lenzyh.github.io/testing_app/data/5_BonusTrends_DetailedDocMap.html",width=1400,height=700)
if page == "Crypto's Trend":
    # Sidebar - Headlines
    st.sidebar.title("News Headlines :newspaper:")
    url_headline = 'https://coinmarketcap.com/headlines/news/'

    response_cryptoheadline = requests.get(url_headline)
    soup_cryptoheadline = BeautifulSoup(response_cryptoheadline.text, 'html.parser')
        # Find all <a> elements with the specified class
    link_elements = soup_cryptoheadline.find_all('div', class_='sc-aef7b723-0 coCmGz')

    # Extract the text content from each <a> element and store in a list
    link_texts = [link_element.text for link_element in link_elements]

    # Create a DataFrame
    data_crpyto_headline = {
        'title': link_texts
    }

    crpyto_headline = pd.DataFrame(data_crpyto_headline) 
    for index, title in enumerate(crpyto_headline['title'], start=1):
        st.sidebar.write(f"{index}. {title}")

    st.subheader("Rocket of the Day :rocket:")
    url_gainlose='https://crypto.com/price/showroom/biggest-gainers'
    response_gainlose = requests.get(url_gainlose)
    soup_gainlose = BeautifulSoup(response_gainlose.text, 'html.parser')
    rocket = soup_gainlose.find_all('span', class_='chakra-text css-eb93p1')
    rocket_short=soup_gainlose.find_all('span', class_='chakra-text css-1jj7b1a')
    rocket_price = soup_gainlose.find_all('p', class_='chakra-text css-13hqrwd')
    rocket_up=soup_gainlose.find_all('p', class_="chakra-text css-110rl6j")

    # Initialize lists to store data
    name = [element.text for element in rocket]
    nick = [element.text for element in rocket_short]
    price = [element.text for element in rocket_price]
    up = [element.text for element in rocket_up]
    #url_rocket = [element.get('href') for element in rocket_url]

    rocketandfall = {
        'Name': name,
        'Nick': nick,
        'Price': price,
        'Percent': up
        #'URL':url_rocket
    }
    updown = pd.DataFrame(rocketandfall)
    # Convert 'Percent' column to numeric values
    updown['Percent2'] = updown['Percent'].str.rstrip('%').astype(float) / 100

    # Sort the DataFrame based on the 'Percent' column in ascending order
    updown = updown.sort_values(by='Percent2')
    url_lose='https://crypto.com/price/showroom/biggest-losers'
    response_lose = requests.get(url_lose)
    soup_lose = BeautifulSoup(response_lose.text, 'html.parser')
    fall = soup_lose.find_all('span', class_='chakra-text css-eb93p1')
    fall_short=soup_lose.find_all('span', class_='chakra-text css-1jj7b1a')
    fall_price = soup_lose.find_all('p', class_='chakra-text css-13hqrwd')
    fall_=soup_lose.find_all('p', class_="chakra-text css-150md6i")

    # Initialize lists to store data
    name_fall = [element.text for element in fall]
    nick_fall = [element.text for element in fall_short]
    price_fall = [element.text for element in fall_price]
    down = [element.text for element in fall_]
    #url_rocket = [element.get('href') for element in rocket_url]

    fall = {
        'Name': name_fall,
        'Nick': nick_fall,
        'Price': price_fall,
        'Percent': down
        #'URL':url_rocket
    }
    down = pd.DataFrame(fall)
    # Convert 'Percent' column to numeric values
    down['Percent2'] = down['Percent'].str.rstrip('%').astype(float) / 100

    # Sort the DataFrame based on the 'Percent' column in ascending order
    down = down.sort_values(by='Percent2')
    # If you want to sort in descending order, you can use:
    # df = df.sort_values(by='Percent', ascending=False)

    # Reset the index if needed
    updown = updown.reset_index(drop=True)
    up_name=updown['Name'].iloc[-1]
    up_nick=updown['Nick'].iloc[-1].lower()
    up_percent=updown['Percent'].iloc[-1]
    down_name=down['Name'].iloc[0]
    down_nick=down['Nick'].iloc[0].lower()
    down_percent=down['Percent'].iloc[0]
    # Render player name as clickable Markdown text
    up_name = f"[{up_name}](https://crypto.com/price/{up_name.lower().split(' ')[0].split('.')[0]})"
    st.markdown(up_name)
    def get_google_image_url(query):
        url = f'https://www.google.com/search?q={query}&tbm=isch'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract image URLs from the search results
        img_tags = soup.find_all('img')
        image_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
        
        return image_urls

    rocket_image_urls = get_google_image_url(up_name+' Crpyto')
    fall_image_urls = get_google_image_url(down_name+' Crpyto')

    # Retrieve the second URL (index 1) if it exists
    rocket_image_urls2 = rocket_image_urls[1] if len(rocket_image_urls) > 1 else None
    fall_image_urls2 = fall_image_urls[1] if len(fall_image_urls) > 1 else None
    st.image(rocket_image_urls2, caption='Nice! $$')
    st.markdown(f"{up_name} rise <font color='green'><b>{up_percent}</b></font> during the past 24 hours! :moneybag:", unsafe_allow_html=True)

    st.subheader("Fall of the Day 	:skull:")
    down_name = f"[{down_name}](https://crypto.com/price/{down_name.lower().replace(' ','-')})"
    st.markdown(down_name)
    st.image(fall_image_urls2, caption='TT')
    st.markdown(f"{down_name} down <font color='red'><b>{down_percent}</b></font> during the past 24 hours! :fearful:", unsafe_allow_html=True)
    st.subheader("Crypto's Data")
    url = 'https://crypto.com/price'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all cryptocurrency elements on the page
    crypto_elements = soup.find_all('p', class_='chakra-text css-rkws3')
    price_elements = soup.find_all('p', class_='chakra-text css-13hqrwd')
    change_elements = soup.find_all('p', class_=['chakra-text css-dg4gux', 'chakra-text css-yyku61'])
    change_elements = change_elements[1:]
    volume_elements = soup.find_all('td', class_='css-15lyn3l')
    market_elements = soup.find_all('td', class_='css-15lyn3l')
    url_elements = soup.find_all('a', class_=['chakra-link css-tzmkfm'])
    # Use list slicing to extract all even-numbered elements
    volume_elements = volume_elements[0::2]
    market_elements = market_elements[1::2]

    # Initialize lists to store data
    names = [element.text for element in crypto_elements]
    price = [element.text for element in price_elements]
    change = [element.text for element in change_elements]
    volume = [element.text for element in volume_elements]
    market = [element.text for element in market_elements]
    href_links = [element.get('href') for element in url_elements]

    data = {
        'Name': names,
        'Price': price,
        'Last 24H Change': change,
        'Last 24H Volume' : volume,
        'Last 24H Market' : market,
        'URL':href_links
    }
    df = pd.DataFrame(data)
    
    for index, row in df.iterrows():
        crypto_link = f"<a href='https://crypto.com{row['URL']}' target='_blank'>{row['Name']}</a>"
        df.at[index, 'Name'] = crypto_link
    df2=df.drop(columns=['URL'])
    # Display the DataFrame in Streamlit
    st.markdown(df2.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)

    st.subheader("Trending Cryptocurrencies:")
    url_trend = 'https://crypto.com/price/showroom/most-popular/'

    response = requests.get(url_trend)
    soup_popular = BeautifulSoup(response.text, 'html.parser')

    # Find all td elements with style="text-align:end"
    crypto_elements = soup_popular.find_all('span', class_='chakra-text css-eb93p1')
    td_elements = soup_popular.find_all('p', class_='chakra-text css-13hqrwd')
    change_elements = soup_popular.find_all('p', class_=['chakra-text css-2ygcmq','chakra-text css-110rl6j', 'chakra-text css-150md6i'])
    #url_elements = soup.find_all('a', class_=['chakra-link css-tzmkfm'])
    # Initialize lists to store the extracted text
    names = [element.text for element in crypto_elements]
    td = [element.text for element in td_elements]
    change = [element.text for element in change_elements]

    data = {
        'Name': names,
        'Price': td,
        '24H Change':change
    }

    df_popular = pd.DataFrame(data)
    # Create hyperlinks for the Home Team and Away Team columns
    for index, row in df_popular.iterrows():
        if row['Name'] == 'Pi':
            crypto_link = f"<a href='https://crypto.com/price/pinetwork</a>"
            df_popular.at[index, 'Name'] = crypto_link 
        else:
            crypto_link = f"<a href='https://crypto.com/price/{row['Name'].lower().replace(' ','-')}' target='_blank'>{row['Name']}</a>"
            df_popular.at[index, 'Name'] = crypto_link
    # Display the DataFrame in Streamlit
    st.markdown(df_popular.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)

    st.subheader("Crpyto's Summary on Reddit")
    for index, row in reddit.iterrows():
        crypto_link = f"<a href='https://www.reddit.com/r/{row['Topic'].replace(' ','-')}' target='_blank'>{row['Topic']}</a>"
        reddit.at[index, 'Topic'] = crypto_link

    # Display the DataFrame in Streamlit
    reddit2 = reddit[0:10]
    st.markdown(reddit2.to_html(escape=False), unsafe_allow_html=True)
if page == "Sport's Trend":
    # Sidebar - Headlines
    st.sidebar.title("News Headlines :newspaper:")
    for index, title in enumerate(headline['title'], start=1):
        st.sidebar.write(f"{index}. {title}")
    st.subheader("Player Of The Day :sports_medal:")

    # Render player name as clickable Markdown text
    player_name = f"[{name_df['Entity'][0]}](https://en.wikipedia.org/wiki/{player.replace(' ', '_')})"
    st.markdown(player_name)

    st.image(player_image)

    # Generate a Word Cloud
    st.subheader("Player Word Cloud")

    # Extract relevant data for the word cloud (use the 'Entity' and 'count' columns)
    wordcloud_data = name_df[['Entity', 'count']]

    # Create a word cloud based on the 'Entity' and 'count' columns
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(
        dict(zip(wordcloud_data['Entity'], wordcloud_data['count']))
    )

    # Display the Word Cloud using Matplotlib
    wordcloud_image = wordcloud.to_image()
    # Display the Word Cloud image
    st.image(wordcloud_image, use_column_width=True, caption="Player Word Cloud")
    st.subheader("Topic's Modelling")
    components.iframe("https://lenzyh.github.io/testing_app/data/TopicGrouping.html",width=1200,height=1600)
    components.iframe("https://lenzyh.github.io/testing_app/data/DetailedDocMap.html",width=1200,height=800)
    components.iframe("https://lenzyh.github.io/testing_app/data/sport_topic.html",width=1000,height=600)
    components.iframe("https://lenzyh.github.io/testing_app/data/Intertopic.html",width=1000,height=800)
    #topic_image = Image.open('data\sport_topics.png')  # Update the file path to your image
    #st.components.v1.html(open('data\World_Cup_Topics.html").read(), width=800, height=600)
    # with open("data\sport_topic.html",encoding="utf-8") as html_file:
    #     st.components.v1.html(html_file.read(), width=1000, height=400)
    # with open(r"data\intertopic.html","r",encoding="utf-8") as html_file2:
    #     st.components.v1.html(html_file2.read(), width=1000, height=800)

if page == "Football Match":
    from bs4 import BeautifulSoup
    import time
    import pandas as pd
    import requests
    import re
    st.header("Football Match")
    from datetime import date, timedelta
    
    # List of date offsets (-1 for yesterday, 0 for today, 1 for tomorrow)
    date_offsets = [-2,-1, 0, 1,2]
    
    data = []
    
    for date_offset in date_offsets:
        # Calculate the target date
        target_date = date.today() + timedelta(days=date_offset)
        
        # Form the URL with the target date
        url_schedule = f'https://www.espn.in/football/fixtures/_/date/{target_date.strftime("%Y%m%d")}'
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
            
        # Make the request
        response_schedule = requests.get(url_schedule, headers=headers)
    
        # Check if the request was successful (HTTP status code 200)
        if response_schedule.status_code == 200:
            print(f"Request for {target_date.strftime('%Y-%m-%d')} was successful")
            soup_schedule = BeautifulSoup(response_schedule.text, 'html.parser')
            
            # Continue parsing the HTML content using BeautifulSoup
            
            # Extracting all tournament names, home team names, away team names, and scores
            responsive_tables = soup_schedule.select('.ResponsiveTable')
    
            for responsive_table in responsive_tables:
                # Extracting tournament names
                title_elements = responsive_table.find_all('div', class_='Table__Title')
                tournament_list = [title.text for title in title_elements]
                matches = responsive_table.select('.Table__TR.Table__TR--sm')
    
                for match in matches:
                    home_team_element = match.select('.local .Table__Team a')
                    away_team_element = match.select('.matchTeams .Table__Team.away a')
                    score_element = match.select_one('.local a.AnchorLink.at') if match.select_one('.local') else None
                    result_type_element = match.select_one('.teams__col.Table__TD a.AnchorLink') if match.select_one('.teams__col.Table__TD') else None
                    time_element = match.select_one('.date__col.Table__TD a.AnchorLink') if match.select_one('.date__col.Table__TD') else None
    
                    # Check if both home_team and away_team elements exist
                    if home_team_element and away_team_element:
                        home_team = home_team_element[1].text if len(home_team_element) > 1 else 'N/A'
                        away_team = away_team_element[1].text if len(away_team_element) > 1 else 'N/A'
    
                        # Extracting the score
                        score = score_element.text.strip() if score_element else 'N/A'
                        result_type = result_type_element.text.strip() if result_type_element else "Haven't Ended"
                        time = time_element.text.strip() if time_element else "Match Ended"
                        
                        # Append data for each tournament
                        for tournament in tournament_list:
                            data.append({
                                'Tournament': tournament,
                                'Home Team': home_team,
                                'Away Team': away_team,
                                'Score': score,
                                'Result Type': result_type,
                                'Date': target_date.strftime('%Y-%m-%d'),
                                'Time': time
                            })
    
        else:
            print(f"Request for {target_date.strftime('%Y-%m-%d')} failed with status code: {response_schedule.status_code}")
    
    # Creating a DataFrame with the extracted information
    football = pd.DataFrame(data)
    # Get unique tournament names
    tournaments = football["Tournament"].unique()    
    # Create a multi-select dropdown for selecting tournaments
    selected_tournaments = st.multiselect("Select Tournaments", tournaments)    
    # Filter the DataFrame based on the selected tournaments
    filtered_data = football[football["Tournament"].isin(selected_tournaments)]    
    st.subheader('Schedule')
    st.markdown(filtered_data.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    league_selected=st.selectbox('Select League', ['EPL','la_liga','Bundesliga','serie_a','Ligue_1'])
    # Entering the league's  link
    link = f"https://understat.com/league/{league_selected}"
    res = requests.get(link)
    soup = BeautifulSoup(res.content,'lxml')
    scripts = soup.find_all('script')
    # Get the table 
    strings = scripts[2].string 
    # Getting rid of unnecessary characters from json data
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')
    league_data = json.loads(json_data)
    
    df_league = pd.DataFrame(league_data.values())
    df_league = df_league.explode("history")
    h = df_league.pop("history")
    df_league = pd.concat([df_league.reset_index(drop=True), pd.DataFrame(h.tolist())], axis=1)
    df_league = df_league.infer_objects()
    table = df_league.groupby(['title']).agg({'wins': 'sum', 'draws': 'sum', 'loses': 'sum', 'scored': 'sum', 'missed': 'sum', 'pts': 'sum', 'xG': 'sum', 'xGA': 'sum', 'xpts': 'sum', 'npxG': 'sum', 'npxGA': 'sum', 'deep': 'sum', 'deep_allowed': 'sum'}).reset_index()
    standing=table[['title','wins','draws','loses','scored','pts','xG','xGA','xpts']]
    standing.rename(columns={'title':'Team'},inplace=True)
    standing=standing.sort_values(by=['pts','scored'],ascending=[False,False])
    st.subheader(f'Standing in {league_selected}')
    st.markdown(standing.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    # Construct the link for the current league
    link = f"https://understat.com/league/{league_selected}"
    
    # Send a request to the website
    res = requests.get(link)
    
    # Parse the HTML content
    soup = BeautifulSoup(res.content, 'lxml')
    
    # Find all script tags
    scripts = soup.find_all('script')
    
    # Get the players' stats 
    strings = scripts[3].string 
    
    # Getting rid of unnecessary characters from JSON data
    ind_start = strings.index("('") + 2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')
    
    # Load JSON data into a dictionary
    player_data = json.loads(json_data)
    
    # Create a dataframe from the dictionary
    df_player = pd.DataFrame(player_data)
    # Create a new DataFrame for matchups
    matchup_data = []
    
    # Iterate over the rows of the original DataFrame
    for index, row in table.iterrows():
        home_team = row['title']
        
        # Exclude the row where the team is both home and away (if necessary)
        away_teams = table[table['title'] != home_team]['title']
        
        for away_team in away_teams:
            xG_home = row['xG']
            opp_xG_away = table[table['title'] == away_team]['xG'].values[0]
            
            # Append the data to the matchups list
            matchup_data.append({
                'home_team': home_team,
                'away_team': away_team,
                'xG': xG_home,
                'opp_xG': opp_xG_away
            })
    
    # Create the matchups DataFrame
    matchups_df = pd.DataFrame(matchup_data)
    matchups_df['xG_diff']=matchups_df['xG']-matchups_df['opp_xG']
    team_selected=st.selectbox('Select Team', matchups_df['home_team'].unique())
    roster=df_player[['team_title','player_name','position','games','shots','goals','npg','assists','key_passes','yellow_cards','red_cards','xG','xA']]
    roster=roster[roster['team_title']==team_selected]
    roster['goals']=roster['goals'].astype('int')
    roster['xG']=roster['xG'].astype('float').round(2)
    roster['xA']=roster['xA'].astype('float').round(2)
    roster=roster.sort_values(by='goals',ascending=False)
    st.subheader(f'Rosters of {team_selected}')
    st.markdown(roster.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    matchups_df2=matchups_df[matchups_df['home_team']==team_selected]
    # Calculate xG differential and set color based on the sign
    matchups_df2['xG_diff_color'] = np.where(matchups_df2['xG_diff'] < 0, 'red', 'green')
    
    from matplotlib.offsetbox import AnchoredText
    
    # Assuming matchups_df2 DataFrame and other functions are already defined
    
    # Plot the xG differential for each team
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = plt.barh(matchups_df2['away_team'], matchups_df2['xG_diff'], color=matchups_df2['xG_diff_color'])
    plt.ylabel('Opp Team', fontsize=20, fontweight="bold")
    plt.grid(axis='x')
    
    plt.hlines(y=matchups_df2['away_team'], xmin=0, xmax=matchups_df2['xG_diff'], color='cyan', alpha=0.4, linewidth=8,
               label='Positive xG')
    plt.hlines(y=matchups_df2['away_team'], xmin=0, xmax=matchups_df2['xG_diff'], color='red', alpha=0.4, linewidth=8,
               label='Negative xG')
    
    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    # Display the Matplotlib plot in Streamlit
    st.write(f"{team_selected} 2023 Season xG Differential")
    st.image(buffer)

    game_ids = pd.DataFrame()
    # Loop through years 2022 and 2023
    for year in [2022, 2023]:
        url = f'https://understat.com/league/{league_selected}/{year}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        scripts = soup.find_all('script')
        strings = scripts[1].string
        ind_start = strings.index("('")+2
        ind_end = strings.index("')")
        json_data = strings[ind_start:ind_end]
        json_data = json_data.encode('utf8').decode('unicode_escape')
        data = json.loads(json_data)
        year_data = pd.DataFrame(data).sort_values('datetime')
        
        # Changing the data type to int32
        year_data = year_data.astype({'id': 'int32'})
        
        # Concatenate the data to the overall DataFrame
        game_ids = pd.concat([game_ids, year_data])
    game_ids.reset_index(drop=True, inplace=True)
    game_ids['home'] = game_ids['h'].apply(lambda x: x.get('title') if pd.notnull(x) else None)
    game_ids['away'] = game_ids['a'].apply(lambda x: x.get('title') if pd.notnull(x) else None)
    game_ids['Match']= game_ids['home'] + ' -vs- ' + game_ids['away']
    game_ids['datetime'] = pd.to_datetime(game_ids['datetime']) + pd.Timedelta(hours=7)
    game_ids=game_ids[['id','Match','datetime']]

    # Display the selected date in the desired format
    game_=st.selectbox('Select the Match', game_ids['Match'].unique())
    filtered_game_ids_2=game_ids[game_ids['Match']==game_]
    game_id=st.selectbox('Select the Game ID (ordering by match date)', filtered_game_ids_2['id'])
    # Entering match link
    link = f"https://understat.com/match/{game_id}"
    res = requests.get(link)
    soup = BeautifulSoup(res.content,'lxml')
    scripts = soup.find_all('script')
    # Get the shotsData, it's the second script executed in order
    strings = scripts[1].string 
    # Getting rid of unnecessary characters from json data
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')
    data = json.loads(json_data)

    def football_pitch(x_min=0, x_max=105,
                   y_min=0, y_max=68,
                   pitch_color="#f0f0f0",
                   line_color='black',
                   line_thickness=1.5,
                   point_size=20,
                   orientation="horizontal",
                   aspect="full",
                   axis='off',
                   ax=None
                   ):
    
        if not ax:
            raise TypeError("This function is intended to be used with an existing fig and ax in order to allow flexibility in plotting of various sizes and in subplots.")
    
    
        if orientation.lower().startswith("h"):
            first = 0
            second = 1
            arc_angle = 0
    
            if aspect == "half":
                ax.set_xlim(x_max / 2, x_max + 5)
    
        elif orientation.lower().startswith("v"):
            first = 1
            second = 0
            arc_angle = 90
    
            if aspect == "half":
                ax.set_ylim(x_max / 2, x_max + 5)
    
        
        else:
            raise NameError("You must choose one of horizontal or vertical")
        
        ax.axis(axis)
    
        rect = plt.Rectangle((x_min, y_min),
                             x_max, y_max,
                             facecolor=pitch_color,
                             edgecolor="none",
                             zorder=-2)
    
        ax.add_artist(rect)
    
        x_conversion = x_max / 100
        y_conversion = y_max / 100
    
        pitch_x = [0,5.8,11.5,17,50,83,88.5,94.2,100] # x dimension markings
        pitch_x = [x * x_conversion for x in pitch_x]
    
        pitch_y = [0, 21.1, 36.6, 50, 63.2, 78.9, 100] # y dimension markings
        pitch_y = [x * y_conversion for x in pitch_y]
    
        goal_y = [45.2, 54.8] # goal posts
        goal_y = [x * y_conversion for x in goal_y]
    
        # side and goal lines
        lx1 = [x_min, x_max, x_max, x_min, x_min]
        ly1 = [y_min, y_min, y_max, y_max, y_min]
    
        # outer box
        lx2 = [x_max, pitch_x[5], pitch_x[5], x_max]
        ly2 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]
    
        lx3 = [0, pitch_x[3], pitch_x[3], 0]
        ly3 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]
    
        # goals
        lx4 = [x_max, x_max+2, x_max+2, x_max]
        ly4 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]
    
        lx5 = [0, -2, -2, 0]
        ly5 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]
    
        # 6 yard box
        lx6 = [x_max, pitch_x[7], pitch_x[7], x_max]
        ly6 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]
    
        lx7 = [0, pitch_x[1], pitch_x[1], 0]
        ly7 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]
    
    
        # Halfline, penalty spots, and kickoff spot
        lx8 = [pitch_x[4], pitch_x[4]]
        ly8 = [0, y_max]
    
        lines = [
            [lx1, ly1],
            [lx2, ly2],
            [lx3, ly3],
            [lx4, ly4],
            [lx5, ly5],
            [lx6, ly6],
            [lx7, ly7],
            [lx8, ly8],
            ]
    
        points = [
            [pitch_x[6], pitch_y[3]],
            [pitch_x[2], pitch_y[3]],
            [pitch_x[4], pitch_y[3]]
            ]
    
        circle_points = [pitch_x[4], pitch_y[3]]
        arc_points1 = [pitch_x[6], pitch_y[3]]
        arc_points2 = [pitch_x[2], pitch_y[3]]
    
    
        for line in lines:
            ax.plot(line[first], line[second],
                    color=line_color,
                    lw=line_thickness,
                    zorder=-1)
    
        for point in points:
            ax.scatter(point[first], point[second],
                       color=line_color,
                       s=point_size,
                       zorder=-1)
    
        circle = plt.Circle((circle_points[first], circle_points[second]),
                            x_max * 0.088,
                            lw=line_thickness,
                            color=line_color,
                            fill=False,
                            zorder=-1)
    
        ax.add_artist(circle)
    
        arc1 = Arc((arc_points1[first], arc_points1[second]),
                   height=x_max * 0.088 * 2,
                   width=x_max * 0.088 * 2,
                   angle=arc_angle,
                   theta1=128.75,
                   theta2=231.25,
                   color=line_color,
                   lw=line_thickness,
                   zorder=-1)
    
        ax.add_artist(arc1)
    
        arc2 = Arc((arc_points2[first], arc_points2[second]),
                   height=x_max * 0.088 * 2,
                   width=x_max * 0.088 * 2,
                   angle=arc_angle,
                   theta1=308.75,
                   theta2=51.25,
                   color=line_color,
                   lw=line_thickness,
                   zorder=-1)
    
        ax.add_artist(arc2)
    
        ax.set_aspect("equal")
    
        return ax
    df_h = pd.DataFrame(data['h'])
    df_a = pd.DataFrame(data['a'])
    df = pd.concat([df_h,df_a])
    
    # Changing the data types 
    df['xG'] = df['xG'].astype('float64')
    df['X'] = df['X'].astype('float64')
    df['Y'] = df['Y'].astype('float64')
    
    # Adjusting the measurements 
    df['X'] = (df['X']/100)*105*100
    df['Y'] = (df['Y']/100)*68*100
    
    # Dividing the df between away and home again
    df_h = pd.DataFrame(df[df['h_a']=='h'])
    df_a = pd.DataFrame(df[df['h_a']=='a'])
    
    # xG for each team
    # Sociedad
    total_shots_h = df_h[df_h.columns[0]].count()
    xGcum_h = np.round(max(np.cumsum(df_h['xG'])),3)
    xG_per_shot_h = np.round(max(np.cumsum(df_h['xG']))/(df_h[df_h.columns[0]].count()),3)
    goal_h = df_h[df_h['result']=='Goal']
    goal_h = goal_h[goal_h.columns[0]].count()
    h_team = df['h_team'].iloc[0]
    
    # Barcelona 
    # xG for each team
    total_shots_a = df_a[df_a.columns[0]].count().tolist()
    xGcum_a = np.round(max(np.cumsum(df_a['xG'])),3).tolist()
    xG_per_shot_a = np.round(max(np.cumsum(df_a['xG']))/(df_a[df_a.columns[0]].count()),3).tolist()
    goal_a = df_a[df_a['result']=='Goal']
    goal_a = goal_a[goal_a.columns[0]].count().tolist()
    a_team = df['a_team'].iloc[0]

    fig, ax = plt.subplots(figsize=(11, 7))
    
    # Drawing a full pitch horizontally
    # Assuming football_pitch is a custom function for drawing the football pitch
    football_pitch(orientation="horizontal", aspect="full", line_color="black", ax=ax)
    
    # Barcelona away team
    z_a = df_a['xG'].tolist()
    z1 = [1000 * i for i in z_a]  # Scale the "xG" values for plotting
    colors = {'Goal': 'lightsteelblue', 'MissedShots': 'tomato', 'BlockedShot': 'gold', 'SavedShot': 'gray',
              'ShotOnPost': 'peru'}
    plt.scatter(y=df_a["Y"], x=df_a["X"], s=z1, marker='o', color=df_a['result'].map(colors), edgecolors="black")
    plt.tight_layout()
    
    # Real Sociedad
    z_h = df_h['xG'].tolist()
    z2 = [1000 * i for i in z_h]  # Scale the "xG" values for plotting
    colors = {'Goal': 'lightsteelblue', 'MissedShots': 'tomato', 'BlockedShot': 'gold', 'SavedShot': 'gray',
              'ShotOnPost': 'peru'}
    plt.scatter(y=65 - (df_h["Y"]), x=105 - (df_h["X"]), s=z2, marker='o', color=df_h['result'].map(colors),
                edgecolors="black")
    plt.tight_layout()
    
    # Text
    # Sociedad
    st.text("<{}> | Goals: <{}> | Shots: <{}> | xG per Shot: <{}>".format(h_team, goal_h, total_shots_h, xG_per_shot_h))
    
    # Barcelona
    st.text("<{}> | Goals: <{}> | Shots: <{}> | xG per Shot: <{}>".format(a_team, goal_a, total_shots_a, xG_per_shot_a))
    
    # xG per team
    st.text("{}: <{}> | {}: <{}>".format(h_team, xGcum_h, a_team, xGcum_a))
    
    # Scatter plot for goals, blocked shots, missed shots
    plt.scatter(15, 65, s=180, edgecolor="black", color='lightsteelblue')
    plt.scatter(35, 65, s=180, edgecolor="black", color='tomato')
    plt.scatter(55, 65, s=180, edgecolor="black", color='gold')
    plt.scatter(75, 65, s=180, edgecolor="black", color='gray')
    plt.scatter(95, 65, s=180, edgecolor="black", color='peru')
    xx = [10, 25, 45, 65, 85]
    yy = [65, 65, 65, 65, 65]
    xx_yy = ['Goal', 'MissedShots', 'BlockedShot', 'SavedShot', 'ShotOnPost']
    for i in range(len(xx)):
        plt.text(xx[i], yy[i], xx_yy[i], fontsize=12, color="black", ha="center", va="center", fontweight='bold')
    
    # Display the plot in Streamlit
    st.subheader(f"{game_}'s Shotmap")
    st.pyplot(fig)

    st.subheader('Player Shooting Summary')

    player_list=df_player[['id','player_name','team_title']]
    # Entering Player ID link
    player_list2=player_list[player_list['team_title']==team_selected]
    selected_player=st.selectbox('Select Player :', player_list2['player_name'])
    selected_player2=player_list2[player_list2['player_name']==selected_player]
    player_id=selected_player2['id'][0]

    link = f"https://understat.com/player/{player_id}"
    res = requests.get(link)
    soup = BeautifulSoup(res.content,'lxml')
    scripts = soup.find_all('script')
    # Get the grouped stats data, it's the second script executed in order
    strings = scripts[3].string
    # Getting rid of unnecessary characters from json data
    ind_start = strings.index("('")+2 
    ind_end = strings.index("')") 
    json_data = strings[ind_start:ind_end] 
    json_data = json_data.encode('utf8').decode('unicode_escape')
    data = json.loads(json_data)
    shots = pd.DataFrame(data) #shot data
    # Changing data type
    shots['xG'] = shots['xG'].astype('float64')
    shots['X'] = shots['X'].astype('float64')
    shots['Y'] = shots['Y'].astype('float64')
    shots['X1'] = (shots['X']/100)*105*100
    shots['Y1'] = (shots['Y']/100)*68*100
    # Original X and Y
    shots['X'] = (shots['X']/100)*105*100
    shots['Y'] = (shots['Y']/100)*68*100
    total_shots = shots[shots.columns[0]].count().tolist()
    xGcum = np.round(max(np.cumsum(shots['xG'])),3).tolist()
    xG_per_shot = np.round(max(np.cumsum(shots['xG']))/(shots[shots.columns[0]].count()),3).tolist()
    goal = shots[shots['result']=='Goal']
    shot_on_post = shots[shots['result']=='ShotOnPost']
    blocked_shot = shots[shots['result']=='BlockedShot']
    saved_shot = shots[shots['result']=='SavedShot']
    missed_shot = shots[shots['result']=='MissedShot']
    goals = goal[goal.columns[0]].count().tolist()
    if st.button("Career's Shoot"):
        fig, ax = plt.subplots(figsize=(20, 10))
        football_pitch(orientation="vertical",aspect="half",line_color="black",ax=ax,axis="off")
        
        #Drawing a full pitch horizontally
        z = goal['xG'].tolist()
        z1 = [500 * i for i in z] # This is to scale the "xG" values for plotting
        color = {'Goal':'cyan', 'MissedShots':'red', 'BlockedShot':'tomato', 'SavedShot':'black', 'ShotOnPost':'Yellow'}
        ## markers = {'Goal':'Star', 'MissedShots':'X', 'BlockedShot':'O', 'SavedShot':'V', 'ShotOnPost':'S'}
        
        # Plotting the goals, the missed chances shot on post etc 
        plt.scatter(y=goal["X1"],x=goal["Y1"],s=goal['xG']*720, marker='o',color='cyan',edgecolors="black",label='Goals')
        plt.scatter(y=shot_on_post["X1"],x=shot_on_post["Y1"],s=shot_on_post['xG']*720, marker='o',color='yellow',edgecolors="black",label='Shot on Post',alpha=0.5)
        plt.scatter(y=missed_shot["X1"],x=missed_shot["Y1"],s=missed_shot['xG']*720, marker='o',color='red',edgecolors="black",label='Missed Shot',alpha=0.5)
        plt.scatter(y=blocked_shot["X1"],x=blocked_shot["Y1"],s=blocked_shot['xG']*720, marker='o',color='green',edgecolors="black",label='Blocked Shot',alpha=0.5)
        plt.scatter(y=saved_shot["X1"],x=saved_shot["Y1"],s=saved_shot['xG']*720, marker='o',color='purple',edgecolors="black",label='Saved Shot',alpha=0.5)
        #legend 
        # another way to do it 
        #ax.legend(loc='upper center', bbox_to_anchor= (0.13, 0.87),
                    #borderaxespad=0, frameon=False)
        legend = ax.legend(loc="upper center",bbox_to_anchor= (0.14, 0.88),labelspacing=1.3,prop={'weight':'bold','size':11})
        legend.legendHandles[0]._sizes = [500]
        legend.legendHandles[1]._sizes = [500]
        legend.legendHandles[2]._sizes = [500]
        legend.legendHandles[3]._sizes = [500]
        legend.legendHandles[4]._sizes = [500]
        
        # xG Size 
        mSize = [0.05,0.10,0.2,0.4,0.6,0.8]
        mSizeS = [720 * i for i in mSize]
        mx = [60,60,60,60,60,60]
        my = [92,94,96,98,100,102]
        plt.scatter(mx,my,s=mSizeS,facecolors="cyan", edgecolor="black")
        for i in range(len(mx)):
            plt.text(mx[i]+ 2.8, my[i], mSize[i], fontsize=12, color="black",ha="center", va="center",fontweight='bold')
        # Annotation text
        fig_text(0.38,0.91, s=f"{selected_player} Career Shots\n", fontsize = 25, fontweight = "bold",c='cyan')
        fig_text(0.47,0.37, s="Shots:\n\nxGcum:\n\nxG per shot:\n\nGoals: ", fontsize = 12, fontweight = "bold",c='black')
        fig_text(0.54,0.37, s="<{}\n\n{}\n\n{}\n\n{}>".format(total_shots,xGcum,xG_per_shot,goals), fontsize = 12, fontweight = "bold",c='cyan')
    
        st.pyplot(fig)
    if st.button("Career's Goal"):
        head = goal[goal['shotType']=='Head']
        left_foot = goal[goal['shotType']=='LeftFoot']
        right_foot = goal[goal['shotType']=='RightFoot']
        head = head[head.columns[0]].count().tolist()
        right_foot = right_foot[right_foot.columns[0]].count().tolist()
        left_foot = left_foot[left_foot.columns[0]].count().tolist()
        fig, ax = plt.subplots(figsize=(20, 10))
        football_pitch(orientation="vertical",aspect="half",line_color="black",ax=ax,axis="off")
        
        #Drawing a full pitch horizontally
        z = goal['xG'].tolist()
        z1 = [500 * i for i in z] # This is to scale the "xG" values for plotting
        colors = {'Goal':'cyan', 'MissedShots':'red', 'BlockedShot':'tomato', 'SavedShot':'black', 'ShotOnPost':'Yellow'}
        ## markers = {'Goal':'Star', 'MissedShots':'X', 'BlockedShot':'O', 'SavedShot':'V', 'ShotOnPost':'S'}
        
        # Plotting the goals, the missed chances shot on post etc 
        plt.scatter(y=goal[goal['shotType']=='Head']['X1'],x=goal[goal['shotType']=='Head']['Y1'],s=goal[goal['shotType']=='Head']['xG']*720, marker='o',color='cyan',edgecolors="black",label='Head')
        plt.scatter(y=goal[goal['shotType']=='LeftFoot']['X1'],x=goal[goal['shotType']=='LeftFoot']['Y1'],s=goal[goal['shotType']=='LeftFoot']['xG']*720, marker='o',color='tomato',edgecolors="black",label='Left Foot')
        plt.scatter(y=goal[goal['shotType']=='RightFoot']['X1'],x=goal[goal['shotType']=='RightFoot']['Y1'],s=goal[goal['shotType']=='RightFoot']['xG']*720, marker='o',color='yellow',edgecolors="black",label='Right Foot')
        
        # xG Size
        mSize = [0.05,0.10,0.2,0.4,0.6,0.8]
        mSizeS = [720 * i for i in mSize]
        mx = [60,60,60,60,60,60]
        my = [92,94,96,98,100,102]
        plt.scatter(mx,my,s=mSizeS,facecolors="cyan", edgecolor="black")
        for i in range(len(mx)):
            plt.text(mx[i]+ 2.5, my[i], mSize[i], fontsize=12, color="black",ha="center", va="center",fontweight='bold')
        
        # Pitch map text
        fig_text(0.38,0.91, s=f"{selected_player} Career Goals\n", fontsize = 25, fontweight = "bold",c='cyan')
        fig_text(0.47,0.37, s="Goals:\n\nRight Foot:\n\nLeft Foot:\n\nHead: ", fontsize = 15, fontweight = "bold",c='black')
        fig_text(0.54,0.37, s=" <{}>\n\n <{}>\n\n < {}>\n\n  <{}>".format(goals,right_foot,left_foot,head), fontsize = 15, fontweight = "light",highlight_textprops=[{"color":'cyan'}, {'color':"yellow"}, {'color':"tomato"}, {'color':"cyan"}])
        
        # Legend
        legend = ax.legend(loc="upper center",bbox_to_anchor= (0.13, 0.87))
        legend.legendHandles[0]._sizes = [1000]
        legend.legendHandles[1]._sizes = [1000]
        legend.legendHandles[2]._sizes = [1000]
        st.pyplot(fig)


if page == "NBA Match":
    # displaying image function
    def img_to_bytes(img_path):
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded
    st.header("NBA Match :basketball:")
    st.subheader('Top Scorer')
    url = 'https://www.basketball-reference.com/leagues/NBA_2024_totals.html'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the <strong> tag containing "PPG Leader"
    ppg_leader_tag = soup.find('div', class_="prevnext")

    if ppg_leader_tag:
        # Extract the following <a> tags within the same <p> tag
        ppg_players = ppg_leader_tag.find_next('p').find_all('a')
        ppg_links = ppg_leader_tag.find_next('a').find_all('href')
        text_inside_parentheses = ppg_leader_tag.find_next('p').get_text()
        # Extract the text within parentheses
        parentheses_text = text_inside_parentheses[text_inside_parentheses.find("(")+1:text_inside_parentheses.find(")")]
        # Extract the text from the <a> tags
        player_names = [a.get_text() for a in ppg_players]
        href_links = [a['href'] for a in ppg_players]
    player_name = f"[{player_names[0]}](https://www.basketball-reference.com{href_links[0]})"
    st.markdown(player_name, unsafe_allow_html=True)
    img_link=href_links[0].split('.')[0].split('/')[-1]
    st.image(f'https://www.basketball-reference.com/req/202106291/images/headshots/{img_link}.jpg')
    st.write(f"{player_names[0]} has been averaging {parentheses_text} PPG for this season :fire:")
    st.subheader("NBA's Standings")
    st.subheader("Western Conference")
    url = "https://www.basketball-reference.com/friv/playoff_prob.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    table = soup.find("table", {"id": "projected_standings_w"})
    
    headers = [
        "Western Conference", "W", "L", "W/L%", "SOS", "rSOS", "SRS",
        "Current", "Remain", "Best", "Worst", "Playoffs", "Division",
        "1", "2", "3", "4", "5", "6", "7", "8", "",
        "1-6", "7", "8", "9", "10", "Out", "",
        "Win Conf", "Win Finals"
    ]
    
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)
    
    w_df = pd.DataFrame(data, columns=headers)
    w_df = w_df.dropna()
    st.markdown(w_df.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)
    st.subheader('Eastern Conference')
    url = "https://www.basketball-reference.com/friv/playoff_prob.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    table = soup.find("table", {"id": "projected_standings_e"})
    
    headers = [
        "Eastern Conference", "W", "L", "W/L%", "SOS", "rSOS", "SRS",
        "Current", "Remain", "Best", "Worst", "Playoffs", "Division",
        "1", "2", "3", "4", "5", "6", "7", "8", "",
        "1-6", "7", "8", "9", "10", "Out", "",
        "Win Conf", "Win Finals"
    ]
    
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)
    
    e_df = pd.DataFrame(data, columns=headers)
    e_df = e_df.dropna()
    st.markdown(e_df.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)
    # Create hyperlinks for the Home Team and Away Team columns
    st.subheader(f"Schedule")
    year=(date.today()+ timedelta(days=365)).strftime('%Y')
    month=date.today().strftime('%B').lower()
    url_schedule = f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html#schedule'

    response_schedule = requests.get(url_schedule)

    # Check if the request was successful (HTTP status code 200)
    if response_schedule.status_code == 200:
        print("Request was successful")
        soup_schedule = BeautifulSoup(response_schedule.text, 'html.parser')
        # Continue parsing the HTML content using BeautifulSoup
    else:
        print(f"Request failed with status code: {response_schedule.status_code}")
    
    # Find the <tbody> element
    tbody = soup_schedule.find('tbody')

    # Initialize lists to store data
    game_dates = []
    start_times = []
    away_teams = []
    away_urls = []
    home_teams = []
    home_urls = []
    home_scores = []
    away_scores = []
    remarks=[]
    # Extract data from the HTML
    if tbody:
        # Find all <th> elements within the <tr> elements in the <tbody>
        th_elements = tbody.select('tr th')

        # Extract and append the text from each <th> element to the game_dates list
        game_dates = [th_element.get_text() for th_element in th_elements]

    # Find all <td> elements with class "right" and attribute data-stat="game_start_time"
    start_times = [start_time.get_text() for start_time in soup_schedule.find_all('td', {'class': 'right', 'data-stat': 'game_start_time'})]

    # Find all <td> elements with class "left" and attribute data-stat="visitor_team_name"
    away_teams = [away_element.get_text() for away_element in soup_schedule.find_all('td', {'class': 'left', 'data-stat': 'visitor_team_name'})]
    away_urls = [away_element.find('a')['href'] for away_element in soup_schedule.find_all('td', {'class': 'left', 'data-stat': 'visitor_team_name'})]

    # Find all <td> elements with class "left" and attribute data-stat="home_team_name"
    home_teams = [home_element.get_text() for home_element in soup_schedule.find_all('td', {'class': 'left', 'data-stat': 'home_team_name'})]
    home_urls = [home_url.find('a')['href'] for home_url in soup_schedule.find_all('td', {'class': 'left', 'data-stat': 'home_team_name'})]

    # Find all <td> elements with class "right" and attribute data-stat="visitor_pts"
    home_scores = [home_score.get_text() if home_score.get_text() else "N/A" for home_score in soup_schedule.find_all('td', {'class': 'right', 'data-stat': 'home_pts'})]

    away_scores = [away_score.get_text() if away_score.get_text() else "N/A" for away_score in soup_schedule.find_all('td', {'class': 'right', 'data-stat': 'visitor_pts'})]
    remarks = [remark.get_text() if remark.get_text() else " " for remark in soup_schedule.find_all('td', {'class': 'left', 'data-stat': 'game_remarks'})]

    # Create a DataFrame
    nba_schdule = {
        'Game Date': game_dates,
        'Start Time': start_times,
        'Home Team': home_teams,
        'Home URLs':home_urls,
        'Home Points': home_scores,
        'Away Team': away_teams,
        'Away URLs': away_urls,
        'Away Points': away_scores,
        'Remark':remarks,
    }

    basketball = pd.DataFrame(nba_schdule)

    # Concatenate 'Game Date' and 'Start Time' with a space in between
    basketball['Combined DateTime'] = basketball['Game Date'] + ' ' + basketball['Start Time']
    # Corrected format string for pd.to_datetime
    format_string = '%a, %b %d, %Y %I:%M%p'

    # Replace "p" with "PM" in the "Start Time" column
    basketball['Combined DateTime'] = basketball['Combined DateTime'].str.replace('p', 'PM')
    # Convert the combined column to datetime
    basketball['Combined DateTime'] = pd.to_datetime(basketball['Combined DateTime'], format=format_string)

    # Add 11 hours to the combined datetime
    basketball['Combined DateTime'] = basketball['Combined DateTime'] + pd.Timedelta(hours=13)

    # Split the combined datetime back into date and time columns
    basketball['Game Date'] = basketball['Combined DateTime'].dt.strftime('%a, %b %d, %Y')
    basketball['Start Time'] = basketball['Combined DateTime'].dt.strftime('%I:%M%p')

    for index, row in basketball.iterrows():
        home_link = f"<a href='https://www.basketball-reference.com/{row['Home URLs']}' target='_blank'>{row['Home Team']}</a>"
        basketball.at[index, 'Home Team'] = home_link
        away_link = f"<a href='https://www.basketball-reference.com/{row['Away URLs']}' target='_blank'>{row['Away Team']}</a>"
        basketball.at[index, 'Away Team'] = away_link
    
    # Calculate the date 3 days from today
    next_2_days = datetime.today() + timedelta(days=1)

    # Create a filter for rows that are today and the next 3 days
    date_filter = (basketball['Combined DateTime'] >= (datetime.today() - timedelta(days=2))) & (basketball['Combined DateTime'] <= next_2_days)
    basketball = basketball[date_filter]
    basketball=basketball.reset_index()
    # Drop the temporary combined datetime column
    #df.drop('Combined DateTime', axis=1, inplace=True)
    # Drop the temporary combined datetime column
    basketball.drop('index', axis=1, inplace=True)
    basketball.drop('Home URLs', axis=1, inplace=True)
    basketball.drop('Away URLs', axis=1, inplace=True)
    basketball.drop('Combined DateTime', axis=1, inplace=True)


    # Render the table with hyperlinks using HTML
    st.markdown(basketball.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)

    # Add a section for NBA headlines in the sidebar
    st.sidebar.title("NBA's Headlines")
    for index, title in enumerate(headlinenba['title'], start=1):
        st.sidebar.write(f"{index}. {title}")

    # Function to fetch and display NBA scoreboard as a table
    def display_nba_scoreboard():
        st.subheader("NBA Live Scoreboard")
        st.write("All the data is from Basketball Reference and Wikipedia")
        # Get today's scorecard
        games = scoreboard.ScoreBoard()
        games.get_json()

        # Extract the game data
        data_dict = games.get_dict()
        games_data = data_dict.get("scoreboard", {}).get("games", [])

        if games_data:
            # Create a list of dictionaries to store game details
            game_details = []

            for game in games_data:
                home_team = game.get("homeTeam", {})
                away_team = game.get("awayTeam", {})
                home_leader = game.get("gameLeaders", {}).get("homeLeaders", {})
                away_leader = game.get("gameLeaders", {}).get("awayLeaders", {})
                
                game_info = {
                    "Home Team": home_team.get('teamTricode'),
                    "Home Score": home_team.get("score", ""),
                    "Home Leader Name": home_leader.get('name'),
                    "Home Leader Points": home_leader.get("points", ""),
                    "Home Leader Rebounds": home_leader.get("rebounds", ""),
                    "Home Leader Assists": home_leader.get("assists", ""),
                    "Away Team": away_team.get('teamTricode'),
                    "Away Score": away_team.get("score", ""),
                    "Away Leader Name": away_leader.get('name'),
                    "Away Leader Points": away_leader.get("points", ""),
                    "Away Leader Rebounds": away_leader.get("rebounds", ""),
                    "Away Leader Assists": away_leader.get("assists", ""),
                }
                game_details.append(game_info)

            # Create a DataFrame from the list of dictionaries
            df = pd.DataFrame(game_details)

            # Display the data as a table with clickable links
            df['Home Team'] = df['Home Team'].apply(lambda x: f"<a href='https://www.basketball-reference.com/teams/{x.replace(' ', '_')}' target='_blank'>{x}</a>")
            df['Away Team'] = df['Away Team'].apply(lambda x: f"<a href='https://www.basketball-reference.com/teams/{x.replace(' ', '_')}' target='_blank'>{x}</a>")
            #df['Home Leader Name'] = df['Home Leader Name'].apply(lambda x: f"<a href='https://en.wikipedia.org/wiki/{x.replace(' ', '_')}' target='_blank'>{x}</a>")
            #df['Away Leader Name'] = df['Away Leader Name'].apply(lambda x: f"<a href='https://en.wikipedia.org/wiki/{x.replace(' ', '_')}' target='_blank'>{x}</a>")

            st.markdown(df.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)

    def main():
        display_nba_scoreboard()

    if __name__ == "__main__":
        main()
    st.subheader('NBA Lineup Analysis Tool ')
    team = st.selectbox(
     'Choose Your Team:',
     lineup['team'].unique())
    df_team = lineup[lineup['team'] == team].reset_index(drop=True)
    df_team=df_team.sort_values(by=['MIN','PLUS_MINUS'],ascending=[False, False])
    roster = df_team['GROUP_NAME'].unique()
    lineup = st.selectbox(
     'Choose The 5 Man Lineup:',
     roster)
    df_lineup = df_team[df_team['GROUP_NAME'] == lineup]
    
    df_important = df_lineup[['GROUP_NAME', 'MIN', 'PLUS_MINUS', 'PTS', 'AST', 'REB', 'FG_PCT', 'FG3_PCT']]
    df_important = df_important[df_important['MIN']>0]
    df_important2 = df_important
    df_important2[['MIN', 'PLUS_MINUS', 'PTS', 'AST', 'REB', 'FG_PCT', 'FG3_PCT']] = df_important2[['MIN', 'PLUS_MINUS', 'PTS', 'AST', 'REB', 'FG_PCT', 'FG3_PCT']].applymap('{:,.2f}'.format)
    st.markdown(df_important2.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)
    col1, col2, col3, col4,col5,col6,col7 = st.columns(7)
    col_width = 350
    with col1: 
        fig_min = px.histogram(df_team, x="MIN")
        fig_min.add_vline(x=df_important['MIN'].values[0],line_color='red')
        st.plotly_chart(fig_min, use_container_width=True)

    with col2: 
        fig_2 = px.histogram(df_team, x="PLUS_MINUS")
        fig_2.add_vline(x=df_important['PLUS_MINUS'].values[0],line_color='red')
        st.plotly_chart(fig_2, use_container_width=True)
    with col3: 
        fig_3 = px.histogram(df_team, x="PTS")
        fig_3.add_vline(x=df_important['PTS'].values[0],line_color='red')
        st.plotly_chart(fig_3, use_container_width=True)
    
    with col4: 
        fig_4 = px.histogram(df_team, x="AST")
        fig_4.add_vline(x=df_important['AST'].values[0],line_color='red')
        st.plotly_chart(fig_4, use_container_width=True)
    with col5: 
        fig_5 = px.histogram(df_team, x="REB")
        fig_5.add_vline(x=df_important['REB'].values[0],line_color='red')
        st.plotly_chart(fig_5, use_container_width=True)
    with col6: 
        fig_6 = px.histogram(df_team, x="FG_PCT")
        fig_6.add_vline(x=df_important['FG_PCT'].values[0],line_color='red')
        st.plotly_chart(fig_6, use_container_width=True)
    with col7: 
        fig_7 = px.histogram(df_team, x="FG3_PCT")
        fig_7.add_vline(x=df_important['FG3_PCT'].values[0],line_color='red')
        st.plotly_chart(fig_7, use_container_width=True)
    st.subheader('NBA Player Shot Chart')
    nba_shot_data_regular=nba_shotchart
    def draw_court(ax=None, color='blue', lw=2, outer_lines=False):
        # If an axes object isn't provided to plot onto, just get current one
        if ax is None:
            ax = plt.gca()
    
        # Create the various parts of an NBA basketball court
    
        # Create the basketball hoop
        # Diameter of a hoop is 18" so it has a radius of 9", which is a value
        # 7.5 in our coordinate system
        hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    
        # Create backboard
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)
    
        # The paint
        # Create the outer box 0f the paint, width=16ft, height=19ft
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                              fill=False)
        # Create the inner box of the paint, widt=12ft, height=19ft
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                              fill=False)
    
        # Create free throw top arc
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                             linewidth=lw, color=color, fill=False)
        # Create free throw bottom arc
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                                linewidth=lw, color=color, linestyle='dashed')
        # Restricted Zone, it is an arc with 4ft radius from center of the hoop
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                         color=color)
    
        # Three point line
        # Create the side 3pt lines, they are 14ft long before they begin to arc
        corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                                   color=color)
        corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
        # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
        # I just played around with the theta values until they lined up with the 
        # threes
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                        color=color)
    
        # Center Court
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                               linewidth=lw, color=color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                               linewidth=lw, color=color)
    
        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]
    
        if outer_lines:
            # Draw the half court line, baseline and side out bound lines
            outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                    color=color, fill=False)
            court_elements.append(outer_lines)
    
        # Add the court elements onto the axes
        for element in court_elements:
            ax.add_patch(element)
    
        return ax
    player=st.selectbox('Select', nba_shot_data_regular['PLAYER_NAME'].unique())
    player_shotchart_df=nba_shot_data_regular[(nba_shot_data_regular['PLAYER_NAME']==player)]
    league=nba_shot_data_regular[['GRID_TYPE','SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_ATTEMPTED_FLAG','SHOT_MADE_FLAG']]
    # Group by the specified columns and calculate the sum for each group
    league_avg = league.groupby(['GRID_TYPE', 'SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']).agg({
        'SHOT_ATTEMPTED_FLAG': 'sum',
        'SHOT_MADE_FLAG': 'sum'
    }).reset_index()
    
    # Calculate FG% for each group
    league_avg.rename(columns={'SHOT_ATTEMPTED_FLAG':'FGA','SHOT_MADE_FLAG':'FGM'},inplace=True)
    league_avg['FG_PCT'] = (league_avg['FGM']/league_avg['FGA']).round(3)    
    def sized_hexbin(ax, hc, hc2, cmap, norm):
        offsets = hc.get_offsets()
        orgpath = hc.get_paths()[0]
        verts = orgpath.vertices
        values1 = hc.get_array()
        values2 = hc2.get_array()
        ma = values1.max()
        patches = []
    
        for offset,val in zip(offsets,values1):
            # Adding condition for minimum size 
            # offset is the respective position of each hexagons
            
            # remove 0 to compare frequency without 0s
            filtered_list = list(filter(lambda num: num != 0, values1))
            
            # we also skip frequency counts that are 0s
            # this is to discount hexbins with no occurences
            # default value hexagons are the frequencies
            if (int(val) == 0):
                continue
            elif (percentileofscore(filtered_list, val) < 33.33):
                #print(percentileofscore(values1, val))
                #print("bot")
                v1 = verts*0.3 + offset
            elif (percentileofscore(filtered_list, val) > 69.99):
                #print(percentileofscore(values1, val))
                #print("top")
                v1 = verts + offset
            else:
                #print("mid")
                v1 = verts*0.6 + offset
            
            path = Path(v1, orgpath.codes)
            patch = PathPatch(path)
            patches.append(patch)
    
        pc = PatchCollection(patches, cmap=cmap, norm=norm)
        # sets color
        # so hexbin with C=data['FGP']
        pc.set_array(values2)
    
        ax.add_collection(pc)
        hc.remove()
        hc2.remove()
    
    def hexmap_chart(data, league_avg, title="", color="b",
                   xlim=(-250, 250), ylim=(422.5, -47.5), line_color="white",
                   court_color="#1a477b", court_lw=2, outer_lines=False,
                   flip_court=False, gridsize=None, 
                   ax=None, despine=False, **kwargs):
        
        LA = league_avg.loc[:,['SHOT_ZONE_AREA','SHOT_ZONE_RANGE', 'FGA', 'FGM']].groupby(['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE']).sum()
        LA['FGP'] = 1.0*LA['FGM']/LA['FGA']
        player = data.groupby(['SHOT_ZONE_AREA','SHOT_ZONE_RANGE','SHOT_MADE_FLAG']).size().unstack(fill_value=0)
        player['FGP'] = 1.0*player.loc[:,1]/player.sum(axis=1)
        player_vs_league = (player.loc[:,'FGP'] - LA.loc[:,'FGP'])*100  
    
        data = pd.merge(data, player_vs_league, on=['SHOT_ZONE_AREA', 'SHOT_ZONE_RANGE'], how='right')
        
        if ax is None:
            ax = plt.gca()
            ax.set_facecolor(court_color)
    
        if not flip_court:
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
        else:
            ax.set_xlim(xlim[::-1])
            ax.set_ylim(ylim[::-1])
    
        ax.tick_params(labelbottom="off", labelleft="off")
        ax.set_title(title, fontsize=18)
    
        # draws the court
        draw_court(ax, color=line_color, lw=court_lw, outer_lines=outer_lines)
    
        x = data['LOC_X']
        y = data['LOC_Y']
            
        # for diverging color map
        colors = ['#8c1515', '#ff7f0e', '#ffec7e', '#b2e78f', '#006400']
        cmap = ListedColormap(colors)
        # The 5 colors are separated by -9, -3, 0, 3, 9
        boundaries = [-np.inf, -9, -3, 0, 3, 9, np.inf]
        norm = BoundaryNorm(boundaries, cmap.N + 1, clip=True)
        
        # first hexbin required for bincount
        # second hexbin for the coloring of each hexagons
        hexbin = ax.hexbin(x, y, gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
        hexbin2 = ax.hexbin(x, y, C=data['FGP'], gridsize=40, cmap=cmap, norm=norm, extent=[-275, 275, -50, 425])
        sized_hexbin(ax, hexbin, hexbin2, cmap, norm) 
        
        # Set the spines to match the rest of court lines, makes outer_lines
        # somewhate unnecessary
        for spine in ax.spines:
            ax.spines[spine].set_lw(court_lw)
            ax.spines[spine].set_color(line_color)
        # cbar = plt.colorbar(hexbin2, ax=ax)
        # cbar.set_label('Your Colorbar Label')
        if despine:
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
    
        return ax  

    # Plot the hexmap using Matplotlib and get the figure
    fig, ax = plt.subplots(figsize=(8, 7))
    hexmap_chart(player_shotchart_df, league_avg, title=f"{player} Hex Chart 2023-24", ax=ax)
    draw_court(ax, color="blue", lw=2, outer_lines=False)
    player_id=player_shotchart_df['PLAYER_ID'].unique()[0]
    player_image_url = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"
    player_image = st.image(player_image_url,width=60)
    # Display the Matplotlib figure in Streamlit
    st.pyplot(fig, use_container_width=True)
    st.write(f"{player}'s Shooting Performance: ", "FG% =", "{0:.3f}".format(player_shotchart_df['SHOT_MADE_FLAG'].sum()/len(player_shotchart_df)), "({0}-{1})".format(player_shotchart_df['SHOT_MADE_FLAG'].sum(),len(player_shotchart_df)))
    st.subheader('NBA Player Stats Explorer')
    selected_year = st.selectbox('Year', list(reversed(range(1950,2025))))
    # Web scraping of NBA player stats
    @st.cache_data
    def load_data(year):
        url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
        html = pd.read_html(url, header = 0)
        df = html[0]
        raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        return playerstats
    playerstats = load_data(selected_year)
    
    # Sidebar - Team selection
    sorted_unique_team = sorted(playerstats.Tm.unique())
    selected_team = st.multiselect('Team', sorted_unique_team, sorted_unique_team)
    
    # Sidebar - Position selection
    unique_pos = ['C','PF','SF','PG','SG']
    selected_pos = st.multiselect('Position', unique_pos, unique_pos)
    
    # Filtering data
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]
    selected_column = st.selectbox("Select a column to sort:", ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'FG%', '3P%','FT%','ORB','DRB','TOV','FG','3P','MP','eFG%'])
    st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
    # Convert the selected column to float in the copy
    selected_column2 = f"{selected_column}_converted"
    df_selected_team[selected_column2] = df_selected_team[selected_column].astype(float)
    # Sort the DataFrame by the selected column in descending order
    df_selected_team = df_selected_team.sort_values(by=selected_column2, ascending=False)
    df_selected_team=df_selected_team.drop(columns=[selected_column2,'2PA','2P','2P%'])
    html = df_selected_team.style.hide(axis="index").to_html(escape=False)
    css = """
    <style>
        th, td {
            position: sticky;
            left: 0;
            background-color: white;
            z-index: 1;
        }
    </style>
    """
    st.markdown(css + html, unsafe_allow_html=True)
    # Download NBA player stats data
    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
        return href
    
    st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)
if page == "Badminton's Match":
    import glob

    # Specify the path where your CSV files are located
    files = glob.glob('data/rankings_*.csv')
    
    # Initialize an empty list to store DataFrames
    dfs = []
    
    # Loop through the list of files and read each CSV into a DataFrame
    for file in files:
        df = pd.read_csv(file)
        dfs.append(df)
    st.sidebar.title("Badminton's Headlines")
    headlinebadminton=pd.read_csv('data/badminton_news.csv')
    for index, title in enumerate(headlinebadminton['Title'], start=1):
        st.sidebar.write(f"{index}. {title}")
    # Concatenate all DataFrames into a single DataFrame
    result_df = pd.concat(dfs, ignore_index=True)
    # Sidebar: Category selection
    selected_category = st.selectbox("Select Category", result_df['Category'].unique()) 
    # Filter DataFrame based on the selected category
    filtered_df = result_df[result_df['Category'] == selected_category]
    filtered_df=filtered_df.drop(columns=['Breakdown','Category'])
    # Add medal emojis based on the Rank
    filtered_df['Rank'] = filtered_df['Rank'].astype(str)  # Convert Rank to string
    filtered_df.loc[filtered_df['Rank'] == '1', 'Rank'] = "🥇 1"  
    filtered_df.loc[filtered_df['Rank'] == '2', 'Rank'] = "🥈 2" 
    filtered_df.loc[filtered_df['Rank'] == '3', 'Rank'] = "🥉 3" 
    # Display the DataFrame with added medals
    st.markdown(filtered_df.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)
