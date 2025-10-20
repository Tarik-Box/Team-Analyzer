#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
'''
###

This is a simple file that contains Banners and welcome msg only !
to give the script better interface and give the user better UXI 
as well a litel about the script itself

*********************
* Its an old banners file that i've written years ago , and reused it now with some editing
*********************

###
__author__ = "Tarik Ataia"
__copyright__ = "Copyright (C) 2025"
__license__ = "Free - Public - Open Source"
__version__ = "1.0
'''

import sys
import time
import os
import random
import platform

from colorama import Fore

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
RESET = Fore.RESET
exitingRED= "\n\n[ {}Exiting .. !{} ]\n".format(RED,RESET)
exiting = "\n\n[ {}Thank You For Using Analyzer{} ]\n".format(CYAN,RESET)

try:

	rabit =f'''
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
######################################
	back=f"""
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
######################################
	msf=f'''
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
######################################

except KeyboardInterrupt:
	print(exiting)
#----------------------------------------------------------------------
def banners():
    try:
      if 'win' in platform.system() or 'Win' in platform.system():
        os.system("cls")
      else:
        os.system('clear')
        
      print(f"\n\t\tSession Started at : {GREEN} {time.ctime()} \n\t\t\t\t{GREEN}Writen By CoNdA{RESET}\n")

      bnrlist = [rabit, msf, back]
      xrand = random.choice(bnrlist)
      if xrand == back:
        starting = "\t\t\t“The quieter you become, the more you are able to hear.”\n"
        for x in starting:
          sys.stdout.write(x)
          sys.stdout.flush()
          time.sleep(0.02)
      else:
        pass
      return xrand
    except KeyboardInterrupt:
      print('\n', exitingRED)