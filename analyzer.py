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
    def __init__(self, season="2018/2019", league=None, team=None):
        self.season = season
        self.league = league
        self.team = team
        
    # method to fetch JSON data from a given URL    
    def get_json(self,url):
        req = requests.get(url)
        req.raise_for_status()
        return req.json()