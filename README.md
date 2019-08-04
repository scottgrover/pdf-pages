# pdf-pages 
Download and store webpages as PDF

### Prerequisites:
Python3 / pip3

### Set up:
```
pip3 install -r requirements.txt
python3 pdf-pages.py --help
```

### Usage: 
#### To add a file you'd like to download:
We store links / output file names, we add stored links to the sqlite database with the add command. 
```
python3 pdf-pages.py add <url> <output file>
```

#### To delete a file you've previously added:
```
python3 pdf-pages.py delete <output file>
```

#### Show contents of sqlitedb:
```
python3 pdf-pages.py show
```

#### To initiate downloads of the pages you've added:
```
python3 pdf-pages.py download
```

#### Add contents of csv to sqlite db:
```
python pdf-pages.py csv <path to csv file>
```

