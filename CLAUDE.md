# Politie Malafide Blocklist

Python scraper that scrapes fraudulent webshop domains from politie.nl and publishes them as an Adblock Plus DNS blocklist to a GitHub Gist.

## Key Commands
- `pytest test_update_blocklist.py -v` — run all tests
- `python update_blocklist.py` — run scraper locally (needs `GITHUB_TOKEN` + `GIST_ID` env vars)

## Project Notes
- No `requirements.txt` — deps (`requests`, `beautifulsoup4`, `pytest`) are installed inline in the workflow
- Code, comments, and print output are in Dutch
- Blocklist format: Adblock Plus (`||domain.tld^`)
- GitHub Actions runs daily at 06:00 UTC; secrets: `GIST_TOKEN`, `GIST_ID`
- Only two Python files: `update_blocklist.py` (scraper + gist logic) and `test_update_blocklist.py` (unit tests)
