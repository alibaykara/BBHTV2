#!/usr/bin/env python3
import os
import sys
import subprocess

def check_root():
    if os.geteuid() != 0:
        print("This script must be run as root!")
        sys.exit(1)

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: An issue occurred while running {command}")
        print(f"Error details: {e}")

def ask_yes_no(question):
    while True:
        response = input(f"{question} (yes/no): ").lower().strip()
        if response in ['yes', 'no']:
            return response == 'yes'
        print("Please answer with 'yes' or 'no'")

def setup_main_directory():
    # Create BBHTV2 directory
    main_dir = os.path.expanduser("~/BBHTV2")
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    os.chdir(main_dir)
    return main_dir

def install_golang():
    print("[+] Installing Golang...")
    run_command("wget https://dl.google.com/go/go1.23.5.linux-amd64.tar.gz")
    run_command("tar -xvf go1.23.5.linux-amd64.tar.gz")
    run_command("mv go /usr/local")
    
    # Set up Go environment variables
    if not os.path.exists("/usr/local/go"):
        print("Error: Go installation failed!")
        sys.exit(1)
    
    # Create GOPATH directory in root
    go_path = "/root/go"
    if not os.path.exists(go_path):
        os.makedirs(go_path)
    
    # Add Go paths to .bashrc
    bashrc_path = "/root/.bashrc"
    with open(bashrc_path, "a") as f:
        f.write("\n# Golang Paths\n")
        f.write('export GOPATH=/root/go\n')
        f.write('export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin\n')
    
    # Update path for current session
    os.environ["GOPATH"] = go_path
    os.environ["PATH"] = f"{os.environ['PATH']}:/usr/local/go/bin:{go_path}/bin"
    
    # Cleanup
    run_command("rm go1.23.5.linux-amd64.tar.gz")

def install_tools(main_dir):
    print("[+] Installing security tools...")
    
    tools = {
        "Amass": {
            "dir": "amass",
            "cmd": "go install -v github.com/OWASP/Amass/v3/...@master"
        },
        "Aquatone": {
            "dir": "aquatone",
            "cmd": "wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip && unzip aquatone_linux_amd64_1.7.0.zip && mv aquatone /usr/local/bin/ && rm -rf aquatone_linux_amd64_1.7.0.zip LICENSE.txt README.md"
        },
        "Arjun": {
            "dir": "arjun",
            "cmd": "pip3 install arjun"
        },
        "Asnlookup": {
            "dir": "asnlookup",
            "cmd": "pip3 install asnlookup"
        },
        "Assetfinder": {
            "dir": "assetfinder",
            "cmd": "go install -v github.com/tomnomnom/assetfinder@latest"
        },
        "Autorecon": {
            "dir": "autorecon",
            "cmd": "pip3 install git+https://github.com/Tib3rius/AutoRecon.git"
        },
        "Awscli": {
            "dir": "awscli",
            "cmd": "pip3 install awscli"
        },
        "Bakejs": {
            "dir": "bakejs",
            "cmd": "npm install -g bakejs"
        },
        "BBQSQL": {
            "dir": "bbqsql",
            "cmd": "pip3 install bbqsql"
        },
        "BBOT": {
            "dir": "bbot",
            "cmd": "pip3 install bbot"
        },
        "BucketFinder": {
            "dir": "bucketfinder",
            "cmd": "git clone https://github.com/jordanpotti/BucketFinder.git ."
        },
        "BucketLoot": {
            "dir": "bucketloot",
            "cmd": "pip3 install bucketloot"
        },
        "Censys": {
            "dir": "censys",
            "cmd": "pip3 install censys"
        },
        "cloudFlair": {
            "dir": "cloudflair",
            "cmd": "pip3 install cloudflair"
        },
        "cloudlist": {
            "dir": "cloudlist",
            "cmd": "pip3 install cloudlist"
        },
        "dirbuster": {
            "dir": "dirbuster",
            "cmd": "apt-get install -y dirbuster"
        },
        "dirsearch": {
            "dir": "dirsearch",
            "cmd": "git clone https://github.com/maurosoria/dirsearch.git ."
        },
        "dnsgen": {
            "dir": "dnsgen",
            "cmd": "pip3 install dnsgen"
        },
        "dnsrecon": {
            "dir": "dnsrecon",
            "cmd": "pip3 install dnsrecon"
        },
        "dnsx": {
            "dir": "dnsx",
            "cmd": "go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
        },
        "EyeWitness": {
            "dir": "eyewitness",
            "cmd": "git clone https://github.com/FortyNorthSecurity/EyeWitness.git . && ./setup/setup.sh"
        },
        "ffuf": {
            "dir": "ffuf",
            "cmd": "go install -v github.com/ffuf/ffuf@latest"
        },
        "Findomain": {
            "dir": "findomain",
            "cmd": "curl -LO https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux && chmod +x findomain-linux && mv findomain-linux /usr/local/bin/findomain"
        },
        "feroxbuster": {
            "dir": "feroxbuster",
            "cmd": "curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/master/install-nix.sh | bash"
        },
        "gau": {
            "dir": "gau",
            "cmd": "go install github.com/lc/gau/v2/cmd/gau@latest"
        },
        "github-dorks": {
            "dir": "github-dorks",
            "cmd": "git clone https://github.com/techgaun/github-dorks.git ."
        },
        "github-search": {
            "dir": "github-search",
            "cmd": "pip3 install github-search"
        },
        "gitrob": {
            "dir": "gitrob",
            "cmd": "go install github.com/michenriksen/gitrob@latest"
        },
        "gitleaks": {
            "dir": "gitleaks",
            "cmd": "go install github.com/zricethezav/gitleaks/v7@latest"
        },
        "gobuster": {
            "dir": "gobuster",
            "cmd": "go install github.com/OJ/gobuster/v3@latest"
        },
        "gowitness": {
            "dir": "gowitness",
            "cmd": "go install github.com/sensepost/gowitness@latest"
        },
        "Havij": {
            "dir": "havij",
            "cmd": "wget https://github.com/UltimateHackers/Havij/archive/master.zip && unzip master.zip && rm master.zip"
        },
        "httpx": {
            "dir": "httpx",
            "cmd": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
        },
        "Httprobe": {
            "dir": "httprobe",
            "cmd": "go install github.com/tomnomnom/httprobe@latest"
        },
        "interactsh": {
            "dir": "interactsh",
            "cmd": "go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest"
        },
        "JSParser": {
            "dir": "jsparser",
            "cmd": "git clone https://github.com/nahamsec/JSParser.git . && python3 setup.py install"
        },
        "js-beautify": {
            "dir": "js-beautify",
            "cmd": "npm install -g js-beautify"
        },
        "jsmapfinder": {
            "dir": "jsmapfinder",
            "cmd": "pip3 install jsmapfinder"
        },
        "katana": {
            "dir": "katana",
            "cmd": "go install github.com/projectdiscovery/katana/cmd/katana@latest"
        },
        "knockpy": {
            "dir": "knockpy",
            "cmd": "pip3 install knockpy"
        },
        "lazys3": {
            "dir": "lazys3",
            "cmd": "pip3 install lazys3"
        },
        "LinkFinder": {
            "dir": "linkfinder",
            "cmd": "git clone https://github.com/GerbenJavado/LinkFinder.git . && python3 setup.py install"
        },
        "massdns": {
            "dir": "massdns",
            "cmd": "git clone https://github.com/blechschmidt/massdns.git . && make"
        },
        "naabu": {
            "dir": "naabu",
            "cmd": "go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"
        },
        "nuclei": {
            "dir": "nuclei",
            "cmd": "go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"
        },
        "nmap": {
            "dir": "nmap",
            "cmd": "apt-get install -y nmap"
        },
        "osmedeus": {
            "dir": "osmedeus",
            "cmd": "git clone https://github.com/j3ssie/Osmedeus.git . && ./install.sh"
        },
        "paramspider": {
            "dir": "paramspider",
            "cmd": "git clone https://github.com/devanshbatham/ParamSpider.git ."
        },
        "rustscan": {
            "dir": "rustscan",
            "cmd": "cargo install rustscan"
        },
        "s3scanner": {
            "dir": "s3scanner",
            "cmd": "pip3 install s3scanner"
        },
        "Seclists collection": {
            "dir": "seclists",
            "cmd": "apt-get install -y seclists"
        },
        "shuffledns": {
            "dir": "shuffledns",
            "cmd": "go install github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest"
        },
        "sqlmap-dev": {
            "dir": "sqlmap-dev",
            "cmd": "git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev"
        },
        "subdomain.py": {
            "dir": "subdomain.py",
            "cmd": "git clone https://github.com/aboul3la/Sublist3r.git . && pip3 install -r requirements.txt"
        },
        "subfinder": {
            "dir": "subfinder",
            "cmd": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
        },
        "subjack": {
            "dir": "subjack",
            "cmd": "go install github.com/haccer/subjack@latest"
        },
        "target.py": {
            "dir": "target.py",
            "cmd": "git clone https://github.com/devanshbatham/ParamSpider.git ."
        },
        "teh_s3_bucketeers": {
            "dir": "teh_s3_bucketeers",
            "cmd": "git clone https://github.com/tomdev/teh_s3_bucketeers.git ."
        },
        "truffleHog": {
            "dir": "trufflehog",
            "cmd": "pip3 install truffleHog"
        },
        "Unfurl": {
            "dir": "unfurl",
            "cmd": "go install github.com/tomnomnom/unfurl@latest"
        },
        "urlfinder": {
            "dir": "urlfinder",
            "cmd": "pip3 install urlfinder"
        },
        "urlhunter": {
            "dir": "urlhunter",
            "cmd": "go install github.com/utkusen/urlhunter@latest"
        },
        "virtual-host-discovery": {
            "dir": "virtual-host-discovery",
            "cmd": "git clone https://github.com/jobertabma/virtual-host-discovery.git ."
        },
        "Waybackurls": {
            "dir": "waybackurls",
            "cmd": "go install github.com/tomnomnom/waybackurls@latest"
        },
        "webscreenshot": {
            "dir": "webscreenshot",
            "cmd": "pip3 install webscreenshot"
        },
        "WPScanAPI": {
            "dir": "wpscanapi",
            "cmd": "gem install wpscan"
        },
        "wpscan": {
            "dir": "wpscan",
            "cmd": "gem install wpscan"
        },
        "wpcli": {
            "dir": "wpcli",
            "cmd": "curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp"
        }
    }
    
    # Install each tool in its own directory
    for tool_name, tool_info in tools.items():
        tool_dir = os.path.join(main_dir, tool_info["dir"])
        print(f"\n[+] Installing {tool_name} in {tool_dir}")
        
        if not os.path.exists(tool_dir):
            os.makedirs(tool_dir)
        
        os.chdir(tool_dir)
        run_command(tool_info["cmd"])

def install_dependencies():
    print("[+] Installing required packages...")
    run_command("apt-get update")
    run_command("apt-get install -y git python3 python3-pip wget unzip")
    
    if ask_yes_no("Do you want to install Golang?"):
        install_golang()
    else:
        print("Skipping Golang installation...")

def main():
    print("BBHTV2 Tools Installer - Starting Installation\n")
    
    check_root()
    main_dir = setup_main_directory()
    install_dependencies()
    install_tools(main_dir)
    
    print("\n[+] Installation completed!")
    print(f"[+] All tools have been installed in {main_dir}")
    print("[+] Go has been installed in /usr/local/go")
    print("[+] Go workspace is set to /root/go")
    
    if os.path.exists("/usr/local/go"):
        print("\n[*] Note: To use Go tools, you need to either restart your terminal session or run:")
        print("source /root/.bashrc")

if __name__ == "__main__":
    main()
