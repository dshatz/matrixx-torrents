import feedparser
import requests
import os
import subprocess
from fileinput import filename
from urllib.parse import urlencode

# Configuration (Using GitHub Secrets)
RSS_FEED_URL = "https://sourceforge.net/projects/projectmatrixx/rss?path=/"
KEYWORD = "lemonadep"
# REMOTE_HOST = os.getenv("REMOTE_HOST")
# REMOTE_USER = os.getenv("REMOTE_USER")
REMOTE_SCRIPT_PATH = os.getenv("REMOTE_SCRIPT_PATH", "~/rss_script.sh")

# Parse RSS feed
def fetch_feed():
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries

# Find new lemonadep release
def find_new_release(entries):
    print("Looking for releases")
    for entry in entries:
        print(entry.title)
        if "official-" + KEYWORD in entry.title.lower():
            return entry.link
    return None

# # Run remote command via SSH
# def run_remote_command(command):
#     ssh_command = f"ssh {REMOTE_USER}@{REMOTE_HOST} -o StrictHostKeyChecking=no 'nohup {command} > ~/rss_script.log 2>&1 &'"
#     subprocess.run(ssh_command, shell=True)


# Execute script on remote machine
# def execute_remote_script(url):
#     run_remote_command(f"bash {REMOTE_SCRIPT_PATH} {url}")



if __name__ == "__main__":
    entries = fetch_feed()
    new_release = find_new_release(entries)
    params = {"use_mirror": "netcologne", "r": new_release}
    if new_release:
        print(f"New release found: {new_release}")
        mirror_url = f"{new_release}?{urlencode(params)}"
        print(f"Mirror url {mirror_url}")
        filename = new_release.split('/download')[0].split(KEYWORD + '/')[1]
        print(f"Filename {filename}")
        command = f"bash ~/rss_script.sh \"{new_release}?{urlencode(params)}\" \"{filename}\""
        subprocess.run(command, shell=True)
