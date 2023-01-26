import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import streamlit as st
import json

import warnings

warnings.filterwarnings('ignore')

# Opening JSON file
with open('teams_demo.json') as json_file:
    team_dict = json.load(json_file)

team_df = pd.DataFrame.from_dict(team_dict)

teams = team_df['Team'].tolist()


class Match():
    '''
    Match Webscraping and Analysis.
    Scraping Matches and

    Parameters
    ----------
    agent : string, default= Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36
        a characteristic string that lets servers and network peers identify the application,
        operating system, vendor, and/or version of the requesting user agent.

    '''

    def __init__(self,
                 agent='Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'):
        self.agent = agent

    def last_fixtures(self, team, league):
        '''
        Obtain last 5 fixtures

        Parameters
        ----------
        team : string,
            name of team

        league : string,
            name of league

        Returns
        -------
        C : dict
            Returns last 5 fixtures

        '''
        url = team_df[(team_df['Team'] == team) & (team_df['League'] == league)]['url'].values[0]
        response = requests.get(url, headers={'User-Agent': self.agent})

        try:
            st.write(response)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all('table', class_='matches')
            st.write(str(table))
            st.markdown(table[0], unsafe_allow_html=True)
            df = pd.read_html(str(table))[0]
        #     df.drop(df.columns[-2:], axis=1, inplace=True)
        #     df.rename(columns={'Outcome': 'Home team', 'Home team': 'Outcome', 'Score/Time': 'Away team',
        #                        'Competition': 'League'}, inplace=True)
            st.dataframe(data=df)
            # return df[:5], df[5:]
        except ImportError:
            return ('incorect teamname, country or both')


####################################################################
# streamlit
##################################################################

st.header('Football Fixtures Scraper')

st.image(
    'https://i0.wp.com/fiftyfc.com/wp-content/uploads/2020/06/black-white-soccer-ball-on-grass-field-web-heade'
    'r-1.jpg?fit=1200%2C352&ssl=1'
)

st.markdown('Get the next and last fixtures of teams')

# Select a user id
team_ = st.selectbox(
    "Enter Team Name", teams
)

select_df = team_df[team_df['Team'] == team_]
leagues = select_df['League'].tolist()

league_ = st.selectbox(
    "Enter League Name", leagues
)

if st.button('Fixtures'):
    matches = Match()
    matches.last_fixtures(team_, league_)
    # # Indexing from 1
    # last_5.index = np.arange(1, len(last_5) + 1)
    #
    # # Rename column and start index from 1
    # next_5.rename(columns={'Outcome': 'Time'}, inplace=True)
    # next_5.index = np.arange(1, len(next_5) + 1)
    #
    # st.subheader("Next 5 Fixtures")
    # st.dataframe(data=next_5)
    #
    # st.subheader("Last 5 Fixtures")
    # st.dataframe(data=last_5)
