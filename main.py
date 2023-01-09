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
import multiprocessing
import os
import subprocess
import requests
import sys
import re


# Set the target url
target_url = sys.argv[1]

# Create a new folder for target
# if not os.path.exists(target_url):
#   os.makedirs(target_url)

# Change the working directory to the target folder
# os.chdir(target_url)


# Starting Subdomain Enumeration
def sublist3r(target_url):
  subprocess.run(["sublist3r", "-d", target_url, "-o", "sublist3r.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  print('Sublist3r Done...\n')


def amass(target_url):
  subprocess.run(["amass", "enum", "-d", target_url, "-o", "amass.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  print('Amass Done...\n')


def subfinder(target_url):
  subprocess.run(["subfinder", "-d", target_url, "-o", "subfinder.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  print('Subfinder Done...\n')


def assetfinder(target_url):
  result = subprocess.run(["assetfinder", "-subs-only", "cu.edu.ng"], stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.DEVNULL)

  with open("assetfinder.txt", "w") as f:
      f.write(result.stdout)
  print('Assetfinder Done...\n')


def read_file(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()


def write_file(lines, filename):
    with open(filename, "w") as f:
        for line in lines:
            f.write(line + "\n")


def combine_subdomains():
  directory = "./" # current directory
  subdomains = set()
  for filename in os.listdir(directory):
      if filename.endswith(".txt"):
          lines = read_file(filename)
          subdomains.update(lines)
  subdomains = list(subdomains)
  subdomains.sort()
  write_file(subdomains, "subdomains.txt")


def subdomain_enumeration():
  # Create a new folder for subdomains
  if not os.path.exists('subdomains'):
    os.makedirs('subdomains')

  # Change the working directory to the subdomains folder
  os.chdir('subdomains')

  with multiprocessing.Pool(4) as p:
    p.map(sublist3r, [target_url])
    p.map(amass, [target_url])
    p.map(subfinder, [target_url])
    p.map(assetfinder, [target_url])
  
  combine_subdomains()

  # Change the working directory to the target folder
  os.chdir('..')


def massdns_resolution():
  # Create a new folder for massdns
  if not os.path.exists('massdns'):
    os.makedirs('massdns')

  # Change the working directory to the massdns folder
  os.chdir('massdns')
  # Run massdns and save the output to a file
  subprocess.run(["massdns", "-r", "/home/alvin/Tools/resolvers_trusted.txt", "-t", "A", "-o", "J", "-w", "massdns.json", "../subdomains/subdomains.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  # Extract the subdomains using jq
  subdomains = subprocess.run(["jq", 'select(.type=="A") | .name', "massdns.json"], capture_output=True).stdout.decode('utf-8')

  subdomains = subdomains.split('\n')
  # Strip the quotes from the beginning and end of each line and remove the period from the end
  subdomains = [subdomain.strip('"').rstrip(".") for subdomain in subdomains]

  # Write the subdomains to a text file
  with open("resolved_subdomains.txt", "w") as f:
      for subdomain in subdomains:
          f.write(subdomain + "\n")
  
  os.chdir('..')

def run_httpx():
# Create a new folder for httpx
  if not os.path.exists('httpx'):
    os.makedirs('httpx')

  # Change the working directory to the httpx folder
  os.chdir('httpx')

  # Run httpx to find live subdomains
  subprocess.run(["httpx", "-l", "../massdns/resolved_subdomains.txt", "-p", "http:80", "-p", "https:443", "-p", "https:80", "-p", "http:81", "-p", "http:3000", "-p", "https:3000", "-p", "http:3001", "-p", "https:3001", "-p", "http:8000", "-p", "http:8080", "-p", "https:8080", "-p", "https:8443", "-o", "httpx.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  # Change the working directory to the target folder
  os.chdir('..')


def gowitness_screenshot():
  # Create a new folder for screenshots
  if not os.path.exists('gowitness'):
    os.makedirs('gowitness')

  # Change the working directory to the gowitness folder
  os.chdir('gowitness')

  # Run gowitness to take screenshots of the subdomains
  subprocess.run(["gowitness", "file", "-f", "../httpx/httpx.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  # Change the working directory to the target folder
  os.chdir('..')


def web_crawling():
  # Create a new folder for web crawling
  if not os.path.exists('webcraw'):
    os.makedirs('webcraw')

  # Change the working directory to the webcraw folder
  os.chdir('webcraw')

  # Run Crawler, Waymore and common crawl
  def crawler():
    with open("../httpx/httpx.txt") as f:
      for subdomain in f:
        subdomain = subdomain.strip()
        subprocess.run(["python3", "/home/alvin/bb/bin/crawler/crawler.py", "-d", subdomain, "-l", "2"])#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["python3", "/home/alvin/bb/bin/waymore/waymore.py", "-d", subdomain, "-l", "2"])#, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print('Crawler Done...\n')

  crawler()


# Python init function
if __name__ == '__main__':
  # subdomain_enumeration()
  # massdns_resolution()
  # run_httpx()
  # gowitness_screenshot()
  web_crawling()