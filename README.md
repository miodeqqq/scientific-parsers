SCIENTIFIC TOOLS - USAGE OF GROBID & TIKA
=========================================

Current stable version: v1.0
Release date: 03.12.2016

### Author:

* Maciej Januszewski (maciek@mjanuszewski.pl)

### About:

**GROBID** - machine learning framework to parse PDF files and to extract information such as title, abstract, authors, affiliations, keywords, etc, from journal publications.

**TIKA** - toolkit detects and extracts metadata and text from over a thousand different file types (such as PPT, XLS, and PDF).

### Requirements:
* Python 3.x;
* requests;
* Grobid;
* Tika;

### Installing Grobid & Tika (docker):

**Grobid**
```
docker pull lfoppiano/grobid:0.4.1
```
```
docker run -t --rm -p 1234:8080 lfoppiano/grobid:0.4.1
```

**Tika**
```
docker pull logicalspark/docker-tikaserver
```
```
docker run -d -p 9876:9998 logicalspark/docker-tikaserver
```


### Usage:
- ***send PDFs to Grobid:***
```
./pdf_to_grobid.py pdfs_data_directory grobid_output_data_directory grobid
```
where `grobid` is url for Grobid's requests, defined in utils as:
```
    'grobid': 'http://localhost:1234/processFulltextDocument',
```

- ***send PDFs to Tika***:
```
./pdf_to_tika.py pdfs_data_directory tika_output_data_directory tika
```
where `tika` is url for Tika's requests, defined in utils as:
```
    'tika': 'http://localhost:9876/tika',
```