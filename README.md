# BGP Parser
## Background
This project was created for the purpose of finding closest neighbour Autonomous Systems for each country. The code parses through RIPE daily datasets and produces an excel file. The file contains information about neighbour ASes for a particular country, such as AS Number, owning organization and country of location.

## Setup
1. To run the code, you need to install Python and PIP
```
$ sudo apt-get install python3 pip3
```

###

2. Clone the repository
```
$ git clone git@github.com:alisherzhaken/bgp_parser.git
```
3. Install dependencies
```
$ pip3 install -r requirements.txt
```

## Usage
1. Setup the local database
```
$ python3 db_loader.py
```  
2. Run the code
```
$ python3 <file_path> <country_code>
```

## Example
```
$ python3 db_loader.py
$ python3 bview.20210627.1600.gz KZ
```
The output file will contain information about closest neighbour ASes for Kazakhstan.

ASN | Organization | Country
----|--------------|--------
25091 | IP-MAX | CH
20485 | TRANSTELECOM Moscow, Russia | RU
15881 | TAJIK-TRANSIT-TELECOM-AS SATURN | TJ
13335 | CLOUDFLARENET | US
8732 | COMCOR-AS Moscow | RU
...|...|...