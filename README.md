# Instructions #

Ingram wanted us to pay like 10k to get images and inventory details. So, here is your hack!

- pull the code (branch master)
- put the NEW.csv file inside the ingram_scraper folder
- run the scraper with this command: $./run.sh
- type CTRL+C (only once) to stop it. If you run again, it will continue from the point it stopped
- if you want to start from begin, the command is: $./restart.sh

* the images will be saved to tmp/images
* the csv will be saved to tmp/export.csv

*ah you need to install python dependencies. run this command:*
$ pip install -f requirements.txt