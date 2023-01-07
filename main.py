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
if not os.path.exists(target_url):
  os.makedirs(target_url)

# Change the working directory to the target folder
os.chdir(target_url)


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
    # p.map(amass, [target_url])
    p.map(subfinder, [target_url])
    p.map(assetfinder, [target_url])
  
  combine_subdomains()

  # Change the working directory to the target folder
  os.chdir('..')


def massdns_resolution():
  # Run massdns
  massdns_command = ["massdns", "-r", "/home/alvin/Tools/resolvers_trusted.txt", "-t", "A", "-o", "J", "subdomains/subdomains.txt"]
  massdns_output = subprocess.run(massdns_command, stdout=subprocess.PIPE, universal_newlines=True)

  # Run jq
  jq_command = ["jq", 'select(.type=="A") | .name ']
  jq_output = subprocess.run(jq_command, input=massdns_output.stdout, stdout=subprocess.PIPE, universal_newlines=True)

  # Run sort
  sort_command = ["sort", "-u"]
  sort_output = subprocess.run(sort_command, input=jq_output.stdout, stdout=subprocess.PIPE, universal_newlines=True)

  # Print the output
  print(sort_output.stdout)


# Python init function
if __name__ == '__main__':
  # subdomain_enumeration()
  massdns_resolution()