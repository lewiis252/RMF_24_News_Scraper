# RMF_24_News_Scraper
This app will automaticaly download and send news from RMF24.pl. You need python and packages from requirements.txt to run it. 
This script automatically sent files from files_to_sent folder to your kindle and move sended files to sended folder.
**Just provide your mail, kindle's mail and password** in .env file (look below).
Remember, you must do something like **Turn Allow less secure apps to ON in your email service** (gmail in this example)

## Requirements
``` sh
pip install -r requirements.txt
```

## Usage of scraper

```sh
git clone git@github.com:lewiis252/RMF_24_News_Scraper.git
```

After setting your virtual enviroment you must provide your emails and password - create .env file in spiders directory and fill it like this:

```sh
# login settings
sender_email = 'my_email.com'
receiver_email = 'my_device_mail@kindle.com'
password = 'passsword'
```

Then simply run rmf24_scraper.py file. 

## New google security policy
Follow this guide to send via gmail. 
https://stackoverflow.com/questions/72478573/sending-and-email-using-python-problem-causes-by-last-google-policy-update-on
