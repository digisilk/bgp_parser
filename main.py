import sys
from mrtparse import *
from bgpdump import *
from dbconnection import DBConnection
import pandas as pd

# ASContainer - Stores information about about each AS in a given country and their respective neighbour ASes
class ASContainer:
    def __init__(self, country_as_list):
        self.country_as_list = country_as_list
        self.as_dict = { _as : set() for _as in self.country_as_list }
    
    # Return list of neighbouring ASes
    def get_neighbour_as(self):
        neighbour_as = { _as for value in self.as_dict.values() for _as in value }
        return neighbour_as
    

class ASInfo:
    def __init__(self, asn = 0, org_info = '', country_code = '', peer_asn_list = []):
        self.asn = asn                         # ASN
        self.org_info = org_info               # Organization Information
        self.country_code = country_code       # Country Code, e.g. US - United States
        self.peer_asn_list = peer_asn_list
        

def main():
    file_path, country_code = sys.argv[1], sys.argv[2]
    # Connect to database
    db = DBConnection()
    
    data = db.find('country', country_code)                         # Dataset of ASes within a country
    country_asn = list(map(lambda entry: int(entry[0]), data))       # List of ASNs within a country
    as_container = ASContainer(country_asn)
    
    # Parse through the dataset
    for entry in Reader(file_path):
        if entry.err:
            continue
        b = BgpDump()
        b.td_v2(entry.data, as_container)
    

    # Save values from the database
    neighbour_as = { asn : ASInfo(asn = asn) for asn in as_container.get_neighbour_as() }
    for asn in neighbour_as.keys():
        _as = db.find_one('asn', asn)
        if _as is None:
            print(asn)
            neighbour_as[asn].org_info = "Bogon"
            neighbour_as[asn].country_code = "ZZ"
        else:
            neighbour_as[asn].org_info = _as[1]
            neighbour_as[asn].country_code = _as[2]
    db.close()

    writer = pd.ExcelWriter('neighbour_as.xlsx')
    # Load neighbour AS values to a dataframe
    df = pd.DataFrame(
        map(lambda as_info: (as_info.asn, as_info.org_info, as_info.country_code), neighbour_as.values()), 
        columns = ['ASN', 'Organization', 'Country']
    )

    # Add country code
    df2 = pd.DataFrame(
        { (kz_asn, asn) for kz_asn, value in as_container.as_dict.items() for asn in value },
        columns = ['KZ ASN', 'ASN']
    )
    df2.head()

    df.to_excel(writer, index = False, header = True, sheet_name = 'Country')
    df2.to_excel(writer, index = False, header = True, sheet_name = 'ASN Map')
    
    writer.save()
    

if __name__ == '__main__':
    main()
