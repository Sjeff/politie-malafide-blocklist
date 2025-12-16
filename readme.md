# Dutch Police Malicious Traders Blocklist

Automatically updated blocklist of fraudulent webshops and traders as published by the Dutch National Police.

## About this list

This repository scrapes the official list of malicious traders from [politie.nl](https://www.politie.nl/aangifte-of-melding-doen/bekende-malafide-handelspartijen.html) daily and automatically generates a blocklist in ADGuard format.

The list contains domains of webshops and traders that have been identified as fraudulent by the Dutch police. The police advises against any transactions with these parties.

## Usage

### ADGuard Home / ADGuard DNS

Add the following URL as a custom filter:
```
https://gist.githubusercontent.com/Sjeff/b215b0c5e12c6d5ac725f618e2111c32/raw/23da28a79fbe8223c66df29dcba560d68512ef1a/politie-malafide-blocklist.txt
```

**Steps:**
1. Open ADGuard settings
2. Go to Filters → DNS blocklists (or Custom filtering rules)
3. Click "Add blocklist" or "Add custom filter"
4. Paste the URL above
5. Save

### Other DNS blockers

The list uses Adblock Plus format and works with most DNS-level blockers such as Pi-hole, NextDNS, and uBlock Origin.

## Automatic updates

This list is automatically updated daily at 06:00 UTC via GitHub Actions. Changes on the politie.nl website are reflected in the blocklist within 24 hours.

Last update: [automatically generated in the blocklist itself]

## Source

All data comes from the official politie.nl website. This repository is not affiliated with or endorsed by the Dutch National Police.

## License

The data originates from a public government source. The script and automation are free to use.

## Disclaimer

This list is automatically generated based on public information. Use at your own risk. Always verify the trustworthiness of webshops yourself before making a purchase.