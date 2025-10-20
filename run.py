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
import banners as bnr # custom module for displaying banners


'''

This is the main execution file for BallAlysis - Simple Football Data Analyzer.
It imports necessary libraries and displays a welcome message using the custom banners module.
This script fetches and analyzes football data and players stats from StatsBomb Open Data API.
Github Repo :  https://github.com/statsbomb/open-data/tree/master

'''






# function to display welcome message
def welcome_message():
    print(bnr.banners())
    print(Fore.CYAN + "\n\t\t[*] Welcome to BallAlysis - The Ultimate Football Data Analyzer!" + Style.RESET_ALL)
    print(Fore.GREEN + "\n\t\t[*] Developed by Tarik Ataia" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n\t\t[*] Let's kick off your football data analysis journey!" + Style.RESET_ALL)
    print("\n") # add a newline for better readability  
    print(Fore.CYAN + "----------------------------------------" + Style.RESET_ALL)
    print("\n") # add a newline for better readability
    return
    
    
    
# main execution block
if __name__ == "__main__":
    try:
        welcome_message()
    # handle keyboard interrupt by user
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Process interrupted by user. Exiting ..." + Style.RESET_ALL)
        exit(0)