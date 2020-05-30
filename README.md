# BBC URL to txt

Single script that takes bbc radio playlist url and saves the tracks as txt

Requirements:  
- python 3.6+
- bs4

## Install

`pip install -r requirements.txt`

## Usage
```
python bbc_url_to_txt.py -url {url} --output-filepath {full_path.txt}
```

Example:  
```
python bbc_url_to_txt.py -url https://www.bbc.co.uk/sounds/play/m000jfcw --output-filepath ~/Desktop/gilles_peterson_2020_05_23.txt
```
