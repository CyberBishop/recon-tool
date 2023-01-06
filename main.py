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

# Create a new folder for target
if not os.path.exists(target_url):
  os.makedirs(target_url)

# Change the working directory to the target folder
os.chdir(target_url)

# Starting Subdomain Enumeration
def subdomain_enumeration():
  print('Starting Subdomain Enumeration\n')

  # Use subdomain enumeration tools to find subdomains
  # Sublist3r, amass, findomain, subfinder, assetfinder

  print('Running Sublist3r...\n')
  sublist3r_output = subprocess.run(['sublist3r', '-d', target_url], capture_output=True)

  print('Running Amass...\n')
  amass_output = subprocess.run(['amass', 'enum', '-d', target_url], capture_output=True)

  print('Running Subfinder...\n')
  subfinder_output = subprocess.run(['subfinder', '-d', target_url], capture_output=True)

  print('Running Assetfinder...\n')
  assetfinder_output = subprocess.run(['assetfinder', '-subs-only', target_url], capture_output=True)

  subdomains = set()

  # Combine the output of the tools and extract the subdomains 4th level domains
  subdomains = re.findall(r'[\w\.-]+\.([\w\.-]+\.[\w]+)', sublist3r_output.stdout.decode('utf-8'))
  subdomains += re.findall(r'[\w\.-]+\.([\w\.-]+\.[\w]+)', amass_output.stdout.decode('utf-8'))
  subdomains += re.findall(r'[\w\.-]+\.([\w\.-]+\.[\w]+)', subfinder_output.stdout.decode('utf-8'))
  subdomains += re.findall(r'[\w\.-]+\.([\w\.-]+\.[\w]+)', assetfinder_output.stdout.decode('utf-8'))



  # Remove the duplicates
  subdomains = list(subdomains)

  # Write the subdomains to a file
  with open('subdomains.txt', 'w') as f:
    for subdomain in subdomains:
      f.write(subdomain + '\n')

# Python init function
if __name__ == '__main__':
  subdomain_enumeration()


# Note
### Recon Phase
  # gobuster dns enum
  # knockpy
  # massdns to resolve subdomains ( check for A records) 
  ## /bin/massdns -r resolvers.txt -t A -o J subdomains.txt | jq 'select(.resp_type=="A") | .query_name' | sort -u
  # Eyewitness or aquatone for screenshots
  # python3 crawler.py -d <URL> -l <Levels Deep to Crawl> https://github.com/ghostlulzhacks/crawler/tree/master
  # Wayback url - tomnomnom, https://github.com/xnl-h4ck3r/waymore
  # Common crawl https://github.com/ghostlulzhacks/commoncrawl python cc.py -d <Domain>
  # Then gobuster again, use seclist raft-large-directories.txt
  # https://github.com/xnl-h4ck3r/xnLinkFinder
  # https://github.com/GerbenJavado/LinkFinder

### Fingerprinting Phase
  ## ip / web analysis
  # shodan
  # nmap port scan / masscan sudo masscan -p<Port Here> <CIDR Range Here> --exclude <Exclude IP> --banners -oX <Out File Name>
  # nikto
  ## Web Analysis
  # Wappalyzer https://github.com/gokulapap/wappalyzer-cli
  # Firewall https://github.com/EnableSecurity/wafw00f, https://github.com/0xInfection/Awesome-WAF#known-bypasses

### Exploitation Low hanging fruits
  # Subdomain takeover https://github.com/haccer/subjack ./subjack -w <Subdomain List> -o results.txt -ssl -c fingerprints.json https://github.com/EdOverflow/can-i-take-over-xyz
  # Github dorks https://github.com/techgaun/github-dorks/blob/master/github-dorks.txt
  # https://github.com/ghostlulzhacks/s3brute python amazon-s3-enum.py -w BucketNames.txt -d <Domain Here>
  # https://github.com/RhinoSecurityLabs/GCPBucketBrute python3 gcpbucketbrute.py -k <Domain Here> -u
  # site:digitaloceanspaces.com <Domain Here> https://github.com/appsecco/spaces-finder 
  # page 147

# Add to burp https://github.com/xnl-h4ck3r/GAP-Burp-Extension