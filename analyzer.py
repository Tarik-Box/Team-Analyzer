#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: run.py
# Author: Tarik Ataia
# Date: 19.10.2025

# import necessary libraries
import sys
import time
import pandas as pd # for data manipulation
import requests # for making HTTP requests
import colorama # for colored terminal text
from colorama import Fore, Style
colorama.init(autoreset=True) # initialize colorama

class StatsAnalyzer:
    """
        This class handles fetching and analyzing football data from the StatsBomb Open Data API.
    """
    def __init__(self,base_url='', season="2018/2019"):
        self.base_url = base_url
        self.season = season
        # competition id and season id will be set based on returned data from competitions.json
        self.competition_id = None
        self.season_id = None
        
    # method to fetch JSON data from a given URL
    # this method writen to not repeat the same code everytime we need to fetch JSON data from a URL  
    def get_json(self,url):
        """
        This method fetches JSON data from the provided URL.
        """
        try:
            req = requests.get(url , timeout=10)
            req.raise_for_status()
            return req.json()
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[-] Error fetching data from {url}: {e}" + Style.RESET_ALL)
            return None

    def fetch_competition_ids(self):
        
        """
        this method will fetch competition infos such as competition id and season id
        """
        competition_url = self.base_url + "competitions.json"
        competition_data = self.get_json(competition_url)
        # filter for La Liga competition
        for competition in competition_data:
            if competition['competition_name'] == 'La Liga' and competition['season_name'] == self.season:
                self.competition_id = competition['competition_id']
                self.season_id = competition['season_id']
                print(f"[+] Fetched competition info for La Liga {self.season}.")
                return self.competition_id, self.season_id
        print("[-] Competition info not found.")
        return None

    
    def team_select(self, teams):
        """
        This method prompts user to select a team from the fetched teams list.
        """
        try:
            try:
                # Prepare for case-insensitive selection:
                # - Build a lowercase lookup list from the provided 'teams' iterable.
                teams_l = [t.lower() for t in teams]
                while True:
                    team_choice = input(Fore.GREEN + "    Your choice: " + Style.RESET_ALL).strip()
                    if team_choice.lower() in teams_l:
                        return teams[teams_l.index(team_choice.lower())]
                    else:
                        print(Fore.RED + "[-] Invalid team selection. Please choose a valid team from the list." + Style.RESET_ALL)
            except ValueError as e:
                print(Fore.RED + f"[-] An error occurred during team selection: {e}" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\n[-] User interrupted the team selection. Exiting ..." + Style.RESET_ALL)
            sys.exit(0)
    
    def fetch_teams(self):
        """
        Fetch and display teams participating in the selected competition.
        """
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

        print(Fore.GREEN + f"\n[+] Teams found in La Liga:\n" + Style.RESET_ALL)
        for team in all_teams:
            sys.stdout.write(f"\n\t{Fore.CYAN}{team}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.02)
        print("\n" + "-"*50)
        print(f"{Fore.RED}\n\n!--> Note: If the selected match is not found!\n  Try to pick *Barcelona* as they have the most matches on the StatsBomb API\n")
        

        print(Fore.CYAN + "\n[+] Home Team Name: " + Style.RESET_ALL)
        # get home team from team_select method
        selected_home_team = self.team_select(all_teams.tolist())

        print(Fore.CYAN + "\n[+] Away Team Name: " + Style.RESET_ALL)
        # get home team from team_select method
        selected_away_team = self.team_select(all_teams.tolist())

        if selected_home_team == selected_away_team:
            print(Fore.RED + "[-] Home and Away teams cannot be the same." + Style.RESET_ALL)
            return self.fetch_teams()

        print(f"\n[+] Selected match: {Fore.CYAN}{selected_home_team}{Style.RESET_ALL} VS {Fore.CYAN}{selected_away_team}{Style.RESET_ALL}")
        self.fetch_match_data(selected_home_team, selected_away_team)
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
                print(f"[+] {Fore.GREEN}Found match{Style.RESET_ALL}: {match['home_team']['home_team_name']} VS {match['away_team']['away_team_name']}")
                # check if this is the match we are looking for and get its match id
                if (match["home_team"]["home_team_name"].lower() == home_team.lower() and 
                    match["away_team"]["away_team_name"].lower() == away_team.lower()):
                    match_id = match["match_id"]
                    print("[+] Fetching events data for the match...")
                    print("*"*70)
                    print(f"\n {Fore.YELLOW}[+] Found match ID:{Style.RESET_ALL} {match_id}")
                    events_url = f"{self.base_url}events/{match_id}.json"
                    
                    print(Fore.CYAN + "\n[+] Match Events Data URL:\n" + Style.RESET_ALL, events_url)
                    
                    events_data = self.get_json(events_url)
                    # if events data is found, return it
                    self.analyze_match_summary(events_data)
                    return events_data
                
            # if no match is found, inform the user with available teams and matches
            print(f"\n[-] {Style.BRIGHT}Match not found on statsbomb database.{Style.RESET_ALL} ")
            print('see available teams and matches above')
            return None
        except KeyboardInterrupt:
            exit(Fore.RED + "\n[-] User interrupted the match data fetching. Exiting ..." + Style.RESET_ALL)
        
    def analyze_match_summary(self, events):
        """
        Analyze full match events and produce a summary table for each team.
        """
        records = [] # an empty list to hold event records
        for e in events:
            if not e: 
                continue
            # as the events data is nested JSON, we need can use .get() method to safely extract values and avoid KeyErrors (*_-)
            records.append({
                "team": e.get("team", {}).get("name"),
                "event": e.get("type", {}).get("name"),
                "outcome": e.get("shot", {}).get("outcome", {}).get("name") if "shot" in e else None,
                "pass_type": e.get("pass", {}).get("type", {}).get("name") if "pass" in e else None,
                "card_type": e.get("foul_committed", {}).get("card", {}).get("name") if "foul_committed" in e else None
            })
        df = pd.DataFrame(records)

        df = df.dropna(subset=["team"])

        stats = {}
        # .unique() to get unique team names , it will return a Numpy array > "ndarray"
        for team in df["team"].unique():
            team_df = df[df["team"] == team]
            
            shots = len(team_df[team_df["event"] == "Shot"])
            goals = len(team_df[(team_df["event"] == "Shot") & (team_df["outcome"] == "Goal")])
            passes = len(team_df[team_df["event"] == "Pass"])
            fouls = len(team_df[team_df["event"] == "Foul Committed"])
            corners = len(team_df[(team_df["event"] == "Pass") & (team_df["pass_type"] == "Corner")])
            yellow_cards = len(team_df[team_df["card_type"] == "Yellow Card"])
            red_cards = len(team_df[team_df["card_type"] == "Red Card"])

            # store stats in a dictionary declared above , the key is the team name
            
            stats[team] = {
                "Shots": shots,
                "Goals": goals,
                "Passes": passes,
                "Fouls": fouls,
                "Corners": corners,
                "Yellow Cards": yellow_cards,
                "Red Cards": red_cards
            }

        # display stats in a tabular format using pandas DataFrame
        stats_df = pd.DataFrame(stats).T  #
        # fill NaN values with 0 and convert to integer type for better readability
        stats_df = stats_df.fillna(0).astype(int)
        
        # print final score
        if len(stats_df) == 2:
            teams = stats_df.index.tolist()
            score = f"{teams[0]} {stats_df.loc[teams[0], 'Goals']} - {stats_df.loc[teams[1], 'Goals']} {teams[1]}"
            print(Fore.CYAN + "\n[+] Final Score:" + Style.RESET_ALL, Fore.YELLOW + score + Style.RESET_ALL + "\n")
        print("*"*70)
        summary = "\n[+] Match Summary Table:\n"
        for s in summary:
            sys.stdout.write(f"{Fore.CYAN}{s}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.05)
        # print the stats dataframe
        print(stats_df)

        print(Fore.GREEN + "\n[!] Match analysis completed successfully!" + Style.RESET_ALL)
        if self.indvidual_stats_prompt():
            self.analyze_player_stats(events)
        return stats_df
    
    def indvidual_stats_prompt(self):
        """
            prompt user to continue to individual player stats analysis or exit
        """
        try:
            while True:
                choice = input(Fore.GREEN + "\n[+] Do you want to analyze this match individual player stats?  (y/n): " + Style.RESET_ALL).strip().lower()
                if choice == 'y':
                    return True
                elif choice == 'n':
                    print(Fore.CYAN + "\n[+] Exiting individual players stats analysis." + Style.RESET_ALL)
                    return False
                else:
                    print(Fore.RED + "[-] Invalid choice. Please enter 'y' or 'n'." + Style.RESET_ALL)
            
        except KeyboardInterrupt as e:
            print(Fore.RED + f"[-] An error occurred in individual stats analysis: {e}" + Style.RESET_ALL)
            return None
        
    def analyze_player_stats(self, events):
        """
        Analyze individual player statistics from match events.
        Arguments:
            events (list): List of event dictionaries from the match.
        Returns:
            pd.DataFrame: DataFrame containing individual player statistics.   
        """
        records = [] 
        # iterate over each event in the events list
        for e in events:
            # extract relevant details using .get() to avoid KeyErrors
            player = e.get("player", {}).get("name")
            team = e.get("team", {}).get("name")
            event_type = e.get("type", {}).get("name")
            # skip events without player or team info
            if not player or not team:
                continue

            outcome = e.get("shot", {}).get("outcome", {}).get("name") if "shot" in e else None
            pass_type = e.get("pass", {}).get("type", {}).get("name") if "pass" in e else None
            # append event record to the records list declared above
            records.append({
                "player": player,
                "team": team,
                "event": event_type,
                "outcome": outcome,
                "pass_type": pass_type,
            })
        # convert records list to pandas DataFrame
        df = pd.DataFrame(records)
        df = df.dropna(subset=["player", "team"])

        stats = [] # an empty list to hold player stats dictionaries
        # iterate over each unique player in the DataFrame
        for player in df["player"].unique():
            player_df = df[df["player"] == player]
            team_name = player_df["team"].iloc[0]

            shots = len(player_df[player_df["event"] == "Shot"])
            goals = len(player_df[(player_df["event"] == "Shot") & (player_df["outcome"] == "Goal")])
            passes = len(player_df[player_df["event"] == "Pass"])
            
            short_name = " ".join(player.split()[:3])
            stats.append({
                "player": short_name,
                "team": team_name,
                "Shots": shots,
                "Goals": goals,
                "Passes": passes
            })
        stats_df = pd.DataFrame(stats)
        stats_df = stats_df.sort_values(["team", "Goals", "Shots"], ascending=[True, False, False])
        print("*"*70)
        statistics = "\n\t\t\t[+] Player Statistics:\n"
        for st in statistics:
            sys.stdout.write(f"{Fore.CYAN}{st}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.08)
        print("\n")
        print("*"*70)
        stats_df.reset_index(drop=True, inplace=True)
        print(f"\n{stats_df}")
        print(Fore.GREEN + "\n[!] Individual player stats analysis completed successfully!\n" + Style.RESET_ALL)
        print("*"*70)
        self.thank_you_message()
        return stats_df
    
    def thank_you_message(self):
        """
        Display a thank you message to the user.
        """
        messages = [
            "\n[+] Thank you for using Ballalysis - Football Match Stats Analyzer!",
            "\n[+] Developed by Tarik Ataia.",
            "\n[+] Goodbye!"
        ]
        time.sleep(0.5)
        for msg in messages:
            for char in msg + "\n":
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.05)
                
    def main(self):
        self.fetch_teams()
        return True