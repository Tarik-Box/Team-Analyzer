#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: run.py
# Author: Tarik Ataia
# Date: 19.10.2025

# import necessary libraries
import pandas as pd # for data manipulation
import requests # for making HTTP requests
import colorama # for colored terminal text
from colorama import Fore, Style
colorama.init(autoreset=True) # initialize colorama

class StatsAnalyzer:
    '''
        This class handles fetching and analyzing football data from the StatsBomb Open Data API.
    '''
    def __init__(self,base_url='', season="2018/2019"):
        self.base_url = base_url
        self.season = season
        
        # competition id and season id will be set based on returned data from competitions.json
        self.competition_id = None
        self.season_id = None
        
        
    # method to fetch JSON data from a given URL
    # this method writen to not repeat the same code everytime we need to fetch JSON data from a URL  
    def get_json(self,url):
        '''
        This method fetches JSON data from the provided URL.
        '''
        try:
            req = requests.get(url)
            req.raise_for_status()
            return req.json()
        except requests.exceptions.RequestException as e:
            print(f"[-] Error fetching data from {url}: {e}")
            return None
        
    
    
    def fetch_competition_ids(self):
        
        '''
        this method will fetch competition infos such as competition id and season id
        '''
        competition_url = self.base_url + "competitions.json"
        competition_data = self.get_json(competition_url)
        # filter for La Liga competition
        for competition in competition_data:
            if competition['competition_name'] == 'La Liga' and competition['season_name'] == self.season:
                self.competition_id = competition['competition_id']
                self.season_id = competition['season_id']
                print(f"[+] Fetched competition info for La Liga {self.season}.")
                return self.competition_id, self.season_id
        return "[-] Competition info not found."
    
    def team_select(self, teams):
        '''
        This method prompts user to select a team from the fetched teams list.
        '''
        try:
            try:
                while True:
                    team_choice = input(Fore.GREEN + "    Your choice: " + Style.RESET_ALL).strip()
                    if team_choice in teams:
                        
                        return team_choice
                    else:
                        print(Fore.RED + "[-] Invalid team selection. Please choose a valid team from the list." + Style.RESET_ALL)
            except ValueError as e:
                print(Fore.RED + f"[-] An error occurred during team selection: {e}" + Style.RESET_ALL)
                return None
        except KeyboardInterrupt:
            exit(Fore.RED + "\n[-] User interrupted the team selection. Exiting ..." + Style.RESET_ALL)
    
    def fetch_teams(self):
        '''
        Fetch and display teams participating in the selected competition.
        '''
        if not (self.competition_id and self.season_id):
            self.fetch_competition_ids()

        matches_url = f"{self.base_url}matches/{self.competition_id}/{self.season_id}.json"
        data = self.get_json(matches_url)
        if not data:
            print("[-] Failed to fetch matches data.")
            return None

        # --- Using pandas to extract teams efficiently ---
        df = pd.DataFrame(data)

        # Extract team names from nested dicts using .apply()
        home_teams = df["home_team"].apply(lambda x: x["home_team_name"])
        away_teams = df["away_team"].apply(lambda x: x["away_team_name"])

        # Combine and sort
        all_teams = pd.concat([home_teams, away_teams]).drop_duplicates().sort_values().reset_index(drop=True)

        print(Fore.GREEN + f"[+] Teams found in La Liga {self.season}:" + Style.RESET_ALL)
        for team in all_teams:
            print(f"    - {team}")

        print(Fore.CYAN + "\n[+] Home Team Name: " + Style.RESET_ALL)
        team_choice1 = self.team_select(all_teams.tolist())

        print(Fore.CYAN + "\n[+] Away Team Name: " + Style.RESET_ALL)
        team_choice2 = self.team_select(all_teams.tolist())

        if team_choice1 == team_choice2:
            print(Fore.RED + "[-] Home and Away teams cannot be the same." + Style.RESET_ALL)
            return None

        print(f"\n[+] Selected match: {Fore.CYAN}{team_choice1}{Style.RESET_ALL} VS {Fore.CYAN}{team_choice2}{Style.RESET_ALL}")
        self.fetch_match_data(team_choice1, team_choice2)
        return all_teams.tolist()
        
        
    def fetch_match_data(self, home_team, away_team):
        """
        Fetch events data for a specific match between home_team and away_team if found.
        """
        # Get match ID first
        try:
            matches_url = f"{self.base_url}matches/{self.competition_id}/{self.season_id}.json"
            data = self.get_json(matches_url)
            for match in data:
                print("[+] Searching for the match...")
                print(f"********************************************")
                print(f"[+] {Fore.GREEN}Found match{Style.RESET_ALL}: {match['home_team']['home_team_name']} VS {match['away_team']['away_team_name']}")
                # check if this is the match we are looking for and get its match id
                if (match["home_team"]["home_team_name"] == home_team and 
                    match["away_team"]["away_team_name"] == away_team):
                    match_id = match["match_id"]
                    print(f"\n {Fore.YELLOW}[+] Found match ID:{Style.RESET_ALL} {match_id}")
                    events_url = f"{self.base_url}events/{match_id}.json"
                    events_data = self.get_json(events_url)
                    # if events data is found, return it
                    return events_data
            # if no match is found, inform the user with available teams and matches
            print(f"\n[-] {Style.BRIGHT}Match not found on statsbomb database.{Style.RESET_ALL} ")
            print('see available teams and matches above')
            return None
        except KeyboardInterrupt:
            exit(Fore.RED + "\n[-] User interrupted the match data fetching. Exiting ..." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"[-] An error occurred while fetching match data: {e}" + Style.RESET_ALL)
            return None
        
        
        
        
        
        
        
        
        
        
teset_analyzer = StatsAnalyzer(base_url="https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/", season="2018/2019")

teset_analyzer.fetch_teams()