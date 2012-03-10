import base64
import StringIO
import gzip
def decode_client_data(request_object):
    if(request_object.META.get('HTTP_CONTENT_ENCODING',None)!=None):
        return decompress_data(request_object.raw_post_data)
    else:
        if request_object.raw_post_data.startswith('H4'):
            return decompress_data(request_object.raw_post_data)
        else:
            return request_object.raw_post_data
        
def decompress_data(raw_data):
    gzip_string = base64.standard_b64decode(str(raw_data))
    url_file_handle=StringIO(gzip_string)
    gzip_file_handle = gzip.GzipFile(fileobj=url_file_handle)
    decompressed_data = gzip_file_handle.read()
    gzip_file_handle.close()
    return decompressed_data