#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
banners.py - simple ASCII banners and welcome messages for BallAlysis

This module provides a small `banners()` function that returns a random
banner string and prints a short startup line. Kept intentionally small
and dependency-free (uses colorama for colors).

Author: Tarik Ataia
License: Free - Public - Open Source
Version: 1.0
"""

import sys
import time
import os
import random
import platform

from colorama import Fore

# Color aliases
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
RESET = Fore.RESET

EXITING_RED = "\n\n[ {}Exiting .. !{} ]\n".format(RED, RESET)
EXITING_MSG = "\n\n[ {}Thank You For Using Analyzer{} ]\n".format(CYAN, RESET)


# ASCII banners (kept as module-level constants)
RABBIT_BANNER = f'''
     Trace program: running
           wake up, Neo...
            {CYAN}CoNdA{RESET} has you
        follow the {YELLOW}YELLOW{RESET} rabbit.
       knock, knock, {CYAN}Neo{YELLOW}.

                        (`.         ,-,
                        ` `.    ,;' /
                         `.  ,'/ .'
                          `. X /.'
                .-;--''--.._` ` (
              .'            /   `
             ,           ` '   Q '
             ,         ,   `._    )
          ,.|         '     `-.;_'
          :  . `  ;    `  ` --,.._;
           ' `    ,   )   .'
              `._ ,  '   /_
                 ; ,''-,;' ``-
                  ``-..__``--`
{RESET}
'''

BACK_BANNER = f"""
                 ....';:::clc;..                                   
                            ..;clol.                               
             ...',,,,,;;;::ccclllod:                               
                             ..,:c:;                               
                      .,,;;,::;,'..''                              
                .''',,..            cd;'....      *...               
            ...'.                  .;OK0xdxkOko;,. >...             
          ..                      c0x;.      .':oxxx,;,.           
                                .kO,               .:okoc          
                                cK,                   cK0d.        
                                k0.                     'cd:.      
                                x0.                        :'                               
                                    xkOkdoc;,.            
                                            ;lxxoc::,.       
                                                     .,;. .,,'     
     > > > >{GREEN} Track {RESET}                     .;.   '.   
                                                          .,    .. 
          {GREEN} No ! <<<< BackTrack{RESET}                             '    . 
                                                             ,     
                                                              .    
                                                              .
"""

MSF_BANNER = f'''
 ______________________________________________________________________________
                          {RED} SuperHack II Logon{RESET}                                  
|______________________________________________________________________________|
|                                                                              |
|                 User Name:          [   {RED}CoNdA-CoDe{RESET}    ]                      |
|                                                                              |
|                 Password:            [ ************* ]                       |
|                                                                              |
|                           	   	   {GREEN}[ OK ]{RESET}                              |
|______________________________________________________________________________|
|                                                                              |
|______________________________________________________________________________|
'''


def clear_console():
    """Clear terminal screen in a cross-platform way."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def banners():
    """
    Return a random banner string and print a short startup line.

    Usage:
        print(banners())
    """
    try:
        clear_console()
        # neat startup line
        print(f"\n\t\tSession Started at : {GREEN}{time.ctime()}{RESET}\n\t\t\t\t{GREEN}Written By CoNdA{RESET}\n")

        banner_list = [RABBIT_BANNER, MSF_BANNER, BACK_BANNER]
        chosen = random.choice(banner_list)

        if chosen is BACK_BANNER:
            starting = "\t\t\t'The quieter you become, the more you are able to hear.'\n"
            for ch in starting:
                sys.stdout.write(ch)
                sys.stdout.flush()
                time.sleep(0.02)

        return chosen

    except KeyboardInterrupt:
        # user aborted banner display
        print("\n", EXITING_RED)
        return ""  # return empty string so caller can continue gracefully
      
