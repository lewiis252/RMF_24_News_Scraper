# RMF_24_News_Scraper
This app will automaticaly download and sent news from RMF24.pl. You need python and packages from requirements.txt to run it. 
This script automatically sent files from files_to_sent folder to your kindle and move sended files to sended folder.
**Just change your mail, kindle's mail and password** at the beggining of rmf24_scraper.py.
Remember, you must do something like **Turn Allow less secure apps to ON in your email service** (gmail in this example)

## Requirements
``` sh
pip install -r requirements.txt
```

## Usage of scraper

```sh
git clone git@github.com:lewiis252/RMF_24_News_Scraper.git
```

After setting your virtual enviroment you must provide your emails and password - go and edit rmf24_scraper.py (html file will be create without this but won't send to your kindle device). Then simply run that file. 
