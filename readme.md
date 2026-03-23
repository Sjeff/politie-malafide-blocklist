<div align="center">

# 🚨 Politie Malafide Blocklist

**Automatically updated DNS blocklist of fraudulent webshops and merchants**
Based on the official list published by the Dutch National Police.

<br>

[![Update](https://img.shields.io/badge/⏰%20update-daily%2006%3A00%20UTC-brightgreen?style=for-the-badge)](https://github.com/Sjeff/politie-malafide-blocklist/actions)
[![Format](https://img.shields.io/badge/📄%20format-AdGuard%20%2F%20Adblock%20Plus-2ea8e0?style=for-the-badge)]()
[![Source](https://img.shields.io/badge/🔎%20source-politie.nl-ff6600?style=for-the-badge)](https://www.politie.nl/aangifte-of-melding-doen/bekende-malafide-handelspartijen.html)
[![Built with Claude](https://img.shields.io/badge/🤖%20built%20with-Claude%20AI-7c3aed?style=for-the-badge&logo=anthropic)](https://claude.ai)

</div>

---

## 📖 What does this project do?

The Dutch National Police publishes a public list of webshops and merchants flagged as fraudulent. This project scrapes that list daily via GitHub Actions and converts it into a DNS blocklist ready for use in AdGuard Home, Pi-hole, NextDNS, and other DNS-level filters.

```
politie.nl → Python scraper → GitHub Actions (06:00 UTC) → GitHub Gist → your DNS filter
```

---

## ⚡ Usage

### 🛡️ AdGuard Home / AdGuard DNS

Add the following URL as a custom blocklist:

```
https://gist.githubusercontent.com/Sjeff/b215b0c5e12c6d5ac725f618e2111c32/raw/politie-malafide-blocklist.txt
```

**Steps:**
1. Open AdGuard Home → **Filters** → **DNS Blocklists**
2. Click **Add Blocklist**
3. Paste the URL above
4. Save and restart if prompted

---

### 🕳️ Pi-hole

1. Go to **Settings** → **Adlists**
2. Add the URL
3. Click **Update Gravity**

---

### 🌐 NextDNS / uBlock Origin

The list uses the **Adblock Plus format** (`||domain.nl^`) and is compatible with all common DNS-level blockers.

---

## 🔄 Automatic updates

| Property | Value |
|---|---|
| Frequency | Every day |
| Time | 06:00 UTC |
| Lag after change on politie.nl | ≤ 24 hours |
| Manual trigger | Available via the Actions tab |
| Change detection | Gist is only updated when new entries are detected |

The GitHub Actions workflow runs on `ubuntu-latest` with Python 3.10 and automatically installs the required dependencies (`requests`, `beautifulsoup4`).

---

## 🗂️ Project structure

```
politie-malafide-blocklist/
├── .github/
│   └── workflows/
│       └── update-blocklist.yml   # GitHub Actions workflow (daily, 06:00 UTC)
├── update_blocklist.py            # Scraper + Gist updater
└── readme.md
```

---

## 🔧 Self-hosting

### Required repository secrets

| Secret | Description |
|---|---|
| `GIST_TOKEN` | GitHub Personal Access Token with `gist` scope |
| `GIST_ID` | ID of the target Gist (leave empty on first run — created automatically) |

### First run

1. Fork this repository
2. Create a GitHub Personal Access Token with the `gist` scope
3. Add `GIST_TOKEN` as a repository secret
4. Leave `GIST_ID` empty on first run — the script will create a new Gist and print its ID
5. Add the printed `GIST_ID` as a repository secret
6. Subsequent runs will only update the Gist when changes are detected

---

## 📋 Blocklist format

The generated blocklist follows the **Adblock Plus 2.0** format:

```
[Adblock Plus 2.0]
! Title: Politie.nl Malafide Handelspartijen
! Description: Blokkeerlijst van malafide webshops volgens politie.nl
! Homepage: https://www.politie.nl/...
! Total entries: <count>
!
||fraudulent-shop.nl^
||scammer.com^
...
```

---

## ⚠️ Source and disclaimer

All data is sourced from [politie.nl](https://www.politie.nl/aangifte-of-melding-doen/bekende-malafide-handelspartijen.html). This project is **not affiliated with or endorsed by the Dutch National Police**.

The list is generated automatically from public government data. Always verify the trustworthiness of a webshop independently before making a purchase.

---

## 🤖 Built with Claude AI

<div align="center">

[![Claude AI](https://img.shields.io/badge/Claude%20AI-Anthropic-7c3aed?style=for-the-badge&logo=anthropic&logoColor=white)](https://claude.ai)

**This project was built in collaboration with [Claude](https://claude.ai) by Anthropic.**
Claude assisted with the scraper design, GitHub Actions workflow, Gist integration, and this documentation.

</div>

---

## 📄 License

Data is sourced from a public government source. The code and automation are free to use.
