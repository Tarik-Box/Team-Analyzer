#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: run.py
# Author: Tarik Ataia
# Date: 19.10.2025

# import necessary libraries

from analyzer import StatsAnalyzer 
# Write analyzer module to make the code modular and organized and readable
# import StatsAnalyzer class from custom analyzer module .
# StatsAnalyzer class handles fetching and analyzing football data from StatsBomb Open Data API.
# As the code will grow, we will add more functionalities to this class.

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

BASE_URL = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/"


# function to display welcome message
def welcome_message():
    print(bnr.banners())
    print(Fore.CYAN + "\n[*] Welcome to BallAlysis - The Ultimate Football Data Analyzer!" + Style.RESET_ALL)
    print(Fore.GREEN + "\n[*] Developed by Tarik Ataia" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n[*] Let's kick off your football data analysis journey!" + Style.RESET_ALL)
    print(Fore.CYAN + "----------------------------------------" + Style.RESET_ALL)
    return


# function to get season input from user
def get_season():
    '''
        Function to get the season input from the user for analysis.
        As La Liga is the main focus of this tool and the most liga that has API data, we will provide options for La Liga seasons.
    '''
    try:
        print(Fore.CYAN + "\n[+] Available La Liga Seasons for Analysis:" + Style.RESET_ALL)
        print(Fore.YELLOW + "    1. 2018/2019" + Style.RESET_ALL)
        print(Fore.YELLOW + "    2. 2019/2020" + Style.RESET_ALL)
        try:
            print(Fore.YELLOW + "\n[+] Please select the season you want to analyze \n" + Style.RESET_ALL)
            # prompt user for season choice
            while True:
                season_choice = input(Fore.GREEN + "    Your choice: " + Style.RESET_ALL).strip()
                if season_choice == '1':
                    selected_season = '2018/2019'
                    print(f"\n[+] You have selected the {Fore.CYAN}{selected_season}{Style.RESET_ALL} season for analysis.")
                    return selected_season
                elif season_choice == '2':
                    selected_season = '2019/2020'
                    print(f"\n[+] You have selected the {Fore.CYAN}{selected_season}{Style.RESET_ALL} season for analysis.")
                    return selected_season
                else:
                    print(Fore.RED + "[!] Invalid choice. Please enter 1 or 2." + Style.RESET_ALL)
        # handle value error for invalid input
        except ValueError as e:
            print(Fore.RED + f"\n[!] Invalid input. Please enter a valid number. Error: {e}" + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"\n[!] An error occurred while selecting the season: {e}" + Style.RESET_ALL)
        return None







    
    
    
# main execution block
if __name__ == "__main__":
    try:
        welcome_message()
        # this script currently focuses on La Liga only on two seasons: 2018/2019 and 2019/2020
        # it can be extended to include more leagues and seasons ... etc in the future.
        # it made simple for project submission purposes.
        season = get_season()  # call the function to get selected season by user
        if season:
            analyzer = StatsAnalyzer(base_url=BASE_URL ,season=season)
            analyzer.main()
            
            
        else:
            print(Fore.RED + "[!] Season selection failed. Exiting ..." + Style.RESET_ALL)
            exit(1)
    except Exception as e:
        print(Fore.RED + f"\n[!] An unexpected error occurred: {e}" + Style.RESET_ALL)
        exit(1)
        
        
        
    # handle keyboard interrupt by user
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Process interrupted by user. Exiting ..." + Style.RESET_ALL)
        exit(0)