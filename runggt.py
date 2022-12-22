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

# Use subdomain enumeration tools to find subdomains
# Sublist3r, amass, findomain, subfinder, assetfinder
sublist3r_output = subprocess.run(['sublist3r', '-d', target_url], capture_output=True)
amass_output = subprocess.run(['amass', 'enum', '-d', target_url], capture_output=True)
findomain_output = subprocess.run(['findomain', '-t', target_url], capture_output=True)
subfinder_output = subprocess.run(['subfinder', '-d', target_url], capture_output=True)
assetfinder_output = subprocess.run(['assetfinder', '-subs-only', target_url], capture_output=True)

# Combine the output of the tools and extract the subdomains
subdomains = set()
subdomains.update(re.findall(r'([\w-]*\.[\w-]*\.\w+)', sublist3r_output.stdout.decode('utf-8')))
subdomains.update(re.findall(r'([\w-]*\.[\w-]*\.\w+)', amass_output.stdout.decode('utf-8')))
subdomains.update(re.findall(r'([\w-]*\.[\w-]*\.\w+)', findomain_output.stdout.decode('utf-8')))
subdomains.update(re.findall(r'([\w-]*\.[\w-]*\.\w+)', subfinder_output.stdout.decode('utf-8')))
subdomains.update(re.findall(r'([\w-]*\.[\w-]*\.\w+)', assetfinder_output.stdout.decode('utf-8')))

# Write the subdomains to a file
with open('subdomains.txt', 'w') as f:
  for subdomain in subdomains:
    f.write(subdomain + '\n')