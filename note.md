# Note
  ## Recon Phase
    gobuster dns enum
    knockpy
    massdns to resolve subdomains ( check for A records) 
    /bin/massdns -r resolvers.txt -t A -o J subdomains.txt | jq 'select(.resp_type=="A") | .query_name' | sort -u
    Eyewitness or aquatone for screenshots
    python3 crawler.py -d <URL> -l <Levels Deep to Crawl> https://github.com/ghostlulzhacks/crawler/tree/master
    Wayback url - tomnomnom, https://github.com/xnl-h4ck3r/waymore
    Common crawl https://github.com/ghostlulzhacks/commoncrawl python cc.py -d <Domain>
     Then gobuster again, use seclist raft-large-directories.txt
    https://github.com/xnl-h4ck3r/xnLinkFinder
    https://github.com/GerbenJavado/LinkFinder

  ## Fingerprinting Phase
    ip / web analysis
    shodan
    nmap port scan / masscan sudo masscan -p<Port Here> <CIDR Range Here> --exclude <Exclude IP> --banners -oX <Out File Name>
    nikto
    Web Analysis
    Wappalyzer https://github.com/gokulapap/wappalyzer-cli
    Firewall https://github.com/EnableSecurity/wafw00f, https://github.com/0xInfection/Awesome-WAF#known-bypasses

  ## Exploitation Low hanging fruits
    Subdomain takeover https://github.com/haccer/subjack ./subjack -w <Subdomain List> -o results.txt -ssl -c fingerprints.json https://github.com/EdOverflow/can-i-take-over-xyz
    Github dorks https://github.com/techgaun/github-dorks/blob/master/github-dorks.txt
    https://github.com/ghostlulzhacks/s3brute python amazon-s3-enum.py -w BucketNames.txt -d <Domain Here>
    https://github.com/RhinoSecurityLabs/GCPBucketBrute python3 gcpbucketbrute.py -k <Domain Here> -u
    site:digitaloceanspaces.com <Domain Here> https://github.com/appsecco/spaces-finder 
    page 147

  ### Add to burp https://github.com/xnl-h4ck3r/GAP-Burp-Extension