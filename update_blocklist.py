import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# GitHub credentials uit environment variables
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GIST_ID = os.environ.get('GIST_ID')

def scrape_urls():
    """Scrape URLs van politie.nl"""
    url = "https://www.politie.nl/aangifte-of-melding-doen/bekende-malafide-handelspartijen.html"
    
    response = requests.get(url)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    urls = []
    list_items = soup.find_all('li')
    in_url_section = False
    
    for item in list_items:
        text = item.get_text(strip=True)
        
        if "URL's:" in text or "URL" in text and ':' in text:
            in_url_section = True
            continue
        
        if 'E-mailadressen:' in text:
            in_url_section = False
            break
        
        if in_url_section and text:
            urls.append(f"||{text}^")
    
    return urls

def create_blocklist_content(urls):
    """Maak de blocklist content"""
    content = "[Adblock Plus 2.0]\n"
    content += "! Title: Politie.nl Malafide Handelspartijen\n"
    content += "! Description: Blokkeerlijst van malafide webshops volgens politie.nl\n"
    content += "! Homepage: https://www.politie.nl/aangifte-of-melding-doen/bekende-malafide-handelspartijen.html\n"
    content += f"! Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
    content += f"! Total entries: {len(urls)}\n"
    content += "!\n"
    content += "\n".join(urls)
    
    return content

def get_current_gist_content():
    """Haal huidige gist content op"""
    if not GIST_ID:
        return None
    
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        gist_data = response.json()
        filename = list(gist_data['files'].keys())[0]
        return gist_data['files'][filename]['content']
    
    return None

def update_gist(content):
    """Update bestaande gist of maak nieuwe aan"""
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    if GIST_ID:
        # Update bestaande gist
        url = f"https://api.github.com/gists/{GIST_ID}"
        
        # Haal huidige filename op
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            current_gist = response.json()
            filename = list(current_gist['files'].keys())[0]
        else:
            filename = "politie-malafide-blocklist.txt"
        
        data = {
            "files": {
                filename: {
                    "content": content
                }
            }
        }
        
        response = requests.patch(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            print("✓ Gist succesvol geüpdatet")
            gist_info = response.json()
            print(f"Gist URL: {gist_info['html_url']}")
            return True
        else:
            print(f"✗ Fout bij updaten: {response.status_code}")
            print(response.text)
            return False
    else:
        # Maak nieuwe gist aan
        url = "https://api.github.com/gists"
        
        data = {
            "description": "Politie.nl Malafide Handelspartijen - ADGuard Blocklist (Auto-updated)",
            "public": True,
            "files": {
                "politie-malafide-blocklist.txt": {
                    "content": content
                }
            }
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 201:
            gist_info = response.json()
            print("✓ Nieuwe gist aangemaakt")
            print(f"Gist URL: {gist_info['html_url']}")
            print(f"Gist ID: {gist_info['id']}")
            print(f"\nVoeg deze GIST_ID toe aan je repository secrets!")
            return True
        else:
            print(f"✗ Fout bij aanmaken: {response.status_code}")
            print(response.text)
            return False

def main():
    print("Scraping politie.nl...")
    urls = scrape_urls()
    print(f"Gevonden: {len(urls)} URLs")
    
    # Maak nieuwe content
    new_content = create_blocklist_content(urls)
    
    # Check of er wijzigingen zijn
    current_content = get_current_gist_content()
    
    if current_content and current_content.strip() == new_content.strip():
        print("Geen wijzigingen gedetecteerd. Gist niet geüpdatet.")
        return
    
    print("Wijzigingen gedetecteerd. Updating gist...")
    update_gist(new_content)

if __name__ == "__main__":
    main()