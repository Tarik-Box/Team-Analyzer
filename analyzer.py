#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: run.py
# Author: Tarik Ataia
# Date: 19.10.2025

# import necessary libraries
import pandas as pd # for data manipulation
import requests # for making HTTP requests


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
                return
        return "[-] Competition info not found."