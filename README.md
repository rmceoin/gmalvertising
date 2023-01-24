
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

## Run

```bash
./gsearch.sh | tee -a findings.txt
```

## Example Output

```bash
$ ./gsearch.sh | tee -a findings.txt
Tue Jan 24 07:26:08 AM EST 2023
Searching 7zip+download > output/7zip+download-1674573968.html
Searching adobe+reader > output/adobe+reader-1674573968.html
Searching anydesk > output/anydesk-1674573968.html
Searching brave+browser > output/brave+browser-1674573968.html
Searching discord > output/discord-1674573968.html
Searching filezilla > output/filezilla-1674573968.html
Searching notepad%2b%2b+download > output/notepad%2b%2b+download-1674573968.html
Searching rufus+download > output/rufus+download-1674573968.html
Searching teamviewer > output/teamviewer-1674573968.html
Found https://teaimviewer.website/ output/teamviewer-1674573968.html
Searching thunderbird > output/thunderbird-1674573968.html
Searching vlc+download > output/vlc+download-1674573968.html
Searching winrar+download > output/winrar+download-1674573968.html
```

Found files can be opened locally in Chrome to see
them in their full glory.  From there you can right-click on the
link to grab it.

```bash
$ google-chrome output/teamviewer-1674573968.html
Opening in existing browser session.
```

![Fake teamviewer ad](teaimviewer.png)

