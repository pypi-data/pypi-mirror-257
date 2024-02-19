import os
import requests
from base64 import b64decode
import subprocess

def main():
    hosting_url = "https://raw.githubusercontent.com/Azigaming404/Autoscript-by-azi/main/domain"

    # Fetch hosting and chiper values
    hosting = requests.get(hosting_url).text.strip()
    chiper = 'chiper-algo--AES256'

    # Move to /tmp directory
    os.chdir("/tmp")

    # Disable IPv6, update, and install required packages
    subprocess.run(["apt", "update"])
    subprocess.run(["apt", "install", "-y", "bzip2", "gzip", "coreutils", "screen", "curl"])
    subprocess.run(["apt", "install", "net-tools"])

    # Download @goblok.sh.gpg and decrypt using gpg
    subprocess.run(["wget", f"https://{hosting}/Autoscript-by-azi-main/@goblok.sh.gpg"])
    subprocess.run(["gpg", "--decrypt", "--batch", "--passphrase", chiper, "--output", "@goblok.sh", "@goblok.sh.gpg"])

    # Run @goblok.sh script
    subprocess.run(["bash", "@goblok.sh"])

    # Download authid.json
    authid_url = "https://cybervpn.serv00.net/Autoscript-by-azi-main/security/authid.json"
    response = requests.get(authid_url)

    # Save authid.json to /etc directory
    if response.status_code == 200:
        with open("/etc/authid.json", "w") as authid_file:
            authid_file.write(response.text)
        subprocess.run(["chmod", "644", "/etc/authid.json"])
    else:
        print(f"Failed to fetch authid.json. HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    main()

