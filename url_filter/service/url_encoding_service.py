import hashlib


class URLEncodingService(object):
    """
    This class is supposed to contain hashing logic related to url encoding.
    This is created as a service so that it can be handled independently.
    """
    def hashify(self, host, port=None, path_and_query_params=None):
        if not host:
            raise ValueError("Host is mandatory for encoding url")

        url = host
        if port:
            url = url + ":" + str(port)
        if path_and_query_params:
            url = url + path_and_query_params

        hasher = hashlib.sha1()
        hasher.update(url)
        return hasher.hexdigest()
