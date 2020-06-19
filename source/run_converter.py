import sys
from converter.convert_connection_string_to_sas import get_sas_info_from_connection_string

def main(conn_string):
    print("################################################")
    print("Created: \n")
    print(get_sas_info_from_connection_string(conn_string))
    print("################################################")
main(sys.argv[1])