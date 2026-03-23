import re
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# GitHub credentials uit environment variables
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GIST_ID = os.environ.get('GIST_ID')


def _is_valid_domain(text):
    return bool(re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$', text))


def scrape_urls():
    """Scrape URLs van politie.nl"""
    url = "https://www.politie.nl/aangifte-of-melding-doen/bekende-malafide-handelspartijen.html"

    response = requests.get(url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    urls = []
    in_url_section = False

    for item in soup.find_all('li'):
        text = item.get_text(strip=True)

        if "URL's:" in text or ("URL" in text and ':' in text):
            in_url_section = True
            continue

        if 'E-mailadressen:' in text:
            break

        if in_url_section and text:
            if _is_valid_domain(text):
                urls.append(f"||{text}^")
            else:
                print(f"⚠ Ongeldig domein overgeslagen: {text!r}")

    return urls


def create_blocklist_content(urls):
    """Maak de blocklist content"""
    lines = [
        "[Adblock Plus 2.0]",
        "! Title: Politie.nl Malafide Handelspartijen",
        "! Description: Blokkeerlijst van malafide webshops volgens politie.nl",
        "! Homepage: https://www.politie.nl/aangifte-of-melding-doen/bekende-malafide-handelspartijen.html",
        f"! Total entries: {len(urls)}",
        "!",
        *urls,
    ]
    return "\n".join(lines)


def get_current_gist_content():
    """Haal huidige gist content en filename op. Geeft (content, filename) of (None, None) terug."""
    if not GIST_ID:
        return None, None

    url = f"https://api.github.com/gists/{GIST_ID}"
    response = requests.get(url, headers=_get_gist_headers())

    if response.status_code == 200:
        gist_data = response.json()
        filename = list(gist_data['files'].keys())[0]
        return gist_data['files'][filename]['content'], filename

    return None, None


def update_gist(content, current_filename=None):
    """Update bestaande gist of maak nieuwe aan"""
    if GIST_ID:
        filename = current_filename or "politie-malafide-blocklist.txt"
        return _update_existing_gist(content, filename)
    return _create_new_gist(content)


def _get_gist_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }


def _update_existing_gist(content, filename):
    url = f"https://api.github.com/gists/{GIST_ID}"
    data = {"files": {filename: {"content": content}}}
    response = requests.patch(url, headers=_get_gist_headers(), json=data)

    if response.status_code == 200:
        print(f"✓ Gist succesvol geüpdatet: {response.json()['html_url']}")
        return True

    print(f"✗ Fout bij updaten: {response.status_code}\n{response.text}")
    return False


def _create_new_gist(content):
    data = {
        "description": "Politie.nl Malafide Handelspartijen - ADGuard Blocklist (Auto-updated)",
        "public": True,
        "files": {
            "politie-malafide-blocklist.txt": {"content": content}
        }
    }
    response = requests.post("https://api.github.com/gists", headers=_get_gist_headers(), json=data)

    if response.status_code == 201:
        info = response.json()
        print(f"✓ Nieuwe gist aangemaakt: {info['html_url']}")
        print(f"Gist ID: {info['id']} — voeg toe aan repository secrets!")
        return True

    print(f"✗ Fout bij aanmaken: {response.status_code}\n{response.text}")
    return False


def main():
    print("Scraping politie.nl...")
    urls = scrape_urls()
    print(f"Gevonden: {len(urls)} URLs")

    new_content = create_blocklist_content(urls)
    current_content, current_filename = get_current_gist_content()

    if current_content and current_content.strip() == new_content.strip():
        print("Geen wijzigingen gedetecteerd. Gist niet geüpdatet.")
        return

    print("Wijzigingen gedetecteerd. Updating gist...")
    update_gist(new_content, current_filename)


if __name__ == "__main__":
    main()
