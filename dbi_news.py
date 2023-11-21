import streamlit as st
import pandas as pd
import requests
from nba_api.live.nba.endpoints import scoreboard
from PIL import Image
from wordcloud import WordCloud
from datetime import date, datetime, timedelta
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
    date_offsets = [-1, 0, 1]
    
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
            df['Home Leader Name'] = df['Home Leader Name'].apply(lambda x: f"<a href='https://en.wikipedia.org/wiki/{x.replace(' ', '_')}' target='_blank'>{x}</a>")
            df['Away Leader Name'] = df['Away Leader Name'].apply(lambda x: f"<a href='https://en.wikipedia.org/wiki/{x.replace(' ', '_')}' target='_blank'>{x}</a>")

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
    df_important2 = df_important
    df_important2[['MIN', 'PLUS_MINUS', 'PTS', 'AST', 'REB', 'FG_PCT', 'FG3_PCT']] = df_important2[['MIN', 'PLUS_MINUS', 'PTS', 'AST', 'REB', 'FG_PCT', 'FG3_PCT']].applymap('{:,.2f}'.format)
    st.markdown(df_important2.style.hide(axis="index").to_html(escape=False), unsafe_allow_html=True)
    col1, col2, col3, col4,col5,col6,col7 = st.columns(7)
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
    # Assuming df_selected_team is your DataFrame
    columns_to_exclude = ['Player', 'Pos', 'Tm']

    # Get a list of columns to convert to float
    columns_to_convert = [col for col in df_selected_team.columns if col not in columns_to_exclude]

    # Convert columns to float
    df_selected_team[columns_to_convert] = df_selected_team[columns_to_convert].astype(float)
    st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
    st.dataframe(df_selected_team.style.hide(axis="index"), height=800, sort_mode="multi")
    
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

