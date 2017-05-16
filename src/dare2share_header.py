#!/usr/bin/env python

import sys


COLOUR_RED		= "\033[1;31m"  
COLOUR_BLUE		= "\033[1;34m"
COLOUR_CYAN		= "\033[1;36m"
COLOUR_GREEN	= "\033[0;32m"
COLOUR_RESET	= "\033[0;0m"
COLOUR_BOLD		= "\033[;1m"
COLOUR_REVERSE	= "\033[;7m"

DARE2SHARE_HEADER = """
#########################################################################
#                                                                       #
#      #                                                   ######       #
#      #                                                 ##      ##     #
#      #                                                ##        ##    #
#      #                                                ############    #
#   ####  ####   ####  ###      ###                           #         #
#  #   #      # #     #   #    #   #         #                #         #
# #    #  ### # #     # ##    #     #        #               ##         #
#  #   # #    # #     #       #     #        #                          #
#   ####  ##### #      ####        #         #                          #
#                                 #    ####  # ###   ####   ####  ###   #
#                               #     #      #    #      # #     #   #  #
#                              #       ####  #    #  ### # #     # ##   #
#                             #            # #    # #    # #     #      #
#                             ######   ####  #    #  ##### #      ####  #
#                                                                       #
#########################################################################
#                                                                       #
# BLUETOOTH LOW ENERGY (IBEACON) TRACKING                               #
#                                                                       #
#########################################################################
#                                                                       #
# Project: dare2share - Junge Akademie - Technical University of Munich #
# Mail:    dare2share@jungeakademie.tum.de                              #
# Authors: David Wei, Gunther Bidlingmaier, Max Bauer                   #
# Date:    16/05/2017                                                   #
# Version: 0.0                                                          #
# Python:  2.7                                                          #
# Source:  github.com/dare2share/ble_tracking                           #
#                                                                       #
#########################################################################
"""

def printHeader():
	print(COLOUR_BLUE)
	print(DARE2SHARE_HEADER)
	print(COLOUR_RESET)
