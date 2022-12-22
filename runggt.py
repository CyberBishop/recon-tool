# #
# A python script for bug bounty recon and finding low hanging fruits
#
#
# Author: @cyberbishop
# Version: 1
#
#
##

# Importing the required modules
import os
import subprocess
import requests
import sys
import re


# Set the target url
target_url = sys.argv[1]
print(target_url)