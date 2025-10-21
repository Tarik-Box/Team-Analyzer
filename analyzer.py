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
        
    
    
    def get_competition_infos(self):
        
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
            while True:
                team_choice = input(Fore.GREEN + "    Your choice: " + Style.RESET_ALL).strip()
                if team_choice in teams:
                    
                    return team_choice
                else:
                    print(Fore.RED + "[-] Invalid team selection. Please choose a valid team from the list." + Style.RESET_ALL)
        except ValueError as e:
            print(Fore.RED + f"[-] An error occurred during team selection: {e}" + Style.RESET_ALL)
            return None
    
    def fetch_teams(self):
        '''
        This method fetches and display teams for the selected season.
        '''
        # first ensure competition_id and season_id are set
        self.get_competition_infos()
        if not self.competition_id or not self.season_id:
            print("[-] Competition ID or Season ID not set. Please fetch competition infos first.")
            return None
        
        teams_url = f"{self.base_url}/matches/{self.competition_id}/{self.season_id}.json"
        teams_data = self.get_json(teams_url)
        if teams_data:
            print(f"[+] Fetched teams data for La Liga {self.season}.\n")
            teams = set()
            for match in teams_data:
                teams.add(match['home_team']['home_team_name'])
                teams.add(match['away_team']['away_team_name'])
            for team in sorted(teams):
                print(Fore.GREEN + Style.BRIGHT + f"    - {team}" + Style.RESET_ALL)
            print(Fore.CYAN + "\n[+] Home Team Name: " + Style.RESET_ALL)
            # this will call team_select method to prompt user for team selection
            team_choice1 = self.team_select(teams)
            print(Fore.CYAN + "\n[+] Away Team Name: " + Style.RESET_ALL)
            team_choice2 = self.team_select(teams)
            if team_choice1 == team_choice2: # home and away teams cannot be the same
                print(Fore.RED + "[-] Home and Away teams cannot be the same. Exiting ..." + Style.RESET_ALL)
                return None
            print(f"\n[+] You have selected {Fore.CYAN}{team_choice1}{Style.RESET_ALL} VS{Fore.CYAN} {team_choice2 }{Style.RESET_ALL} match for analysis.")
            # function will return a set of teams to use where needed
            return teams
        else:
            print("[-] Failed to fetch teams data.")
            return None
        
        
    
        
        
        
        
        
        
        
        
        
teset_analyzer = StatsAnalyzer(base_url="https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/", season="2019/2020")

teset_analyzer.fetch_teams()