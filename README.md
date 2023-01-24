
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

