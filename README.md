
# gmalvertising - Google Malvertising

Perform Google searches for software that is being
abused by threat actors.

## Setup

```
python3 -m venv env
source env/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## Customize

Legitmate advertising domains should be added to
`allowed-custom.txt`

Discovered malicious domains should be added to
`malicious-custom.txt`

## Run

```bash
./gsearch.sh | tee -a "findings-$(date +%Y%m%d).txt"
```

## Example Output

```bash
$ ./gsearch.sh | tee -a findings.txt
Fri Jan 27 09:27:52 AM EST 2023
Fri Jan 27 09:29:32 AM EST 2023
Found https://anydeks-access.com/ output/20230127/anydesk-1674840572.html
```

Found files can be opened locally in Chrome to see
them in their full glory.  From there you can right-click on the
link to grab it.

```bash
$ google-chrome output/teamviewer-1674573968.html
Opening in existing browser session.
```

![Fake teamviewer ad](teaimviewer.png)

