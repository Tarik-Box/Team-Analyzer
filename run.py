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








# function to display welcome message
def welcome_message():
    print(bnr.banners())    
    
    
    
# main execution block
if __name__ == "__main__":
    try:
        welcome_message()
    # handle keyboard interrupt by user
    except KeyboardInterrupt:
        print(Fore.RED + "\n[!] Process interrupted by user. Exiting ..." + Style.RESET_ALL)
        exit(0)