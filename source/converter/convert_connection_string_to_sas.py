import time
import hmac
import hashlib
import base64
import datetime
import sys
if sys.version_info[0] < 3:
    print("Running old python version: {}".format(sys.version_info[0]))
    import urllib
else:
    import urllib.parse

class AzureConnectionStringUtils:

    def __init__(self):
        pass

    def get_url(self, endpoint, eventhub_name, eventhub_url=False):
        https_endpoint = endpoint.replace("sb://", "https://")
        url = self.build_eventhub_url(https_endpoint, eventhub_name)
        if eventhub_url:
            return "{}{}".format(url, "/messages")
        else:
            return url

    def get_token(self, https_endpoint, sas_policy_name, sas_policy_key):
        uri = self.encode_url(https_endpoint)
        sas_key = sas_policy_key.encode('utf-8')

        time_now = time.time() + 1576800000 # +50 years
        converted_time = datetime.datetime.fromtimestamp(time_now).strftime('%Y-%m-%d %H:%M:%S')
        expiry = str(int(time_now))
        print("Expiry: {expiry}".format(expiry=converted_time))
        
        string_to_sign = (uri + '\n' + expiry).encode('utf-8')
        signed_hmac_sha256 = hmac.HMAC(sas_key, string_to_sign, hashlib.sha256)
        signature = self.generate_signature(signed_hmac_sha256)
        token = 'SharedAccessSignature sr={}&sig={}&se={}&skn={}'.format(uri, signature, expiry, sas_policy_name)
        return token

    def connection_string_to_dict(self, connection_string):
        splited_conn_string = connection_string.split(";")
        for x in splited_conn_string:
            try:
                conn_string_dict.update({x.split('=', 1)[0]: x.split('=', 1)[1]})
            except:
                conn_string_dict = {x.split('=', 1)[0]: x.split('=', 1)[1]}
        return conn_string_dict

    def build_eventhub_url(self, endpoint, eventhub_name):
        return "{endpoint}{eventhub_name}".format(endpoint=endpoint, eventhub_name=eventhub_name)

    def encode_url(self, url):
        try:
            uri = urllib.parse.quote_plus(url)
        except:
            uri = urllib.quote_plus(url)
        return uri

    def generate_signature(self, signed_hmac_sha256):
        try:
            return urllib.parse.quote(base64.b64encode(signed_hmac_sha256.digest()))
        except:
            return urllib.quote(base64.b64encode(signed_hmac_sha256.digest()))

def get_sas_info_from_connection_string(connection_string):
    autils = AzureConnectionStringUtils()
    conn_string_dict = autils.connection_string_to_dict(connection_string)

    eventhub_url =autils.get_url(conn_string_dict["Endpoint"], conn_string_dict["EntityPath"], eventhub_url=True)
    uri = autils.get_url(conn_string_dict["Endpoint"], conn_string_dict["EntityPath"])
    token = autils.get_token(uri, conn_string_dict["SharedAccessKeyName"], conn_string_dict["SharedAccessKey"])
    return {
        "eventhub_url": eventhub_url,
        "token: ": token
    }
