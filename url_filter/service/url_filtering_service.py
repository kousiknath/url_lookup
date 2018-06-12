from url_filter.entity.url_query_state import URLQueryState
from url_filter.service.url_encoding_service import URLEncodingService
from url_filter.service.url_meta_service import URLMetaService


class URLFilterService(object):
    def __init__(self):
        self._url_encoding_service = URLEncodingService()
        self._url_meta_service = URLMetaService()

    def add_url(self, host, port=None, path_and_query_params=None, blacklist=False):
        """
        :param host: 
        :param port: 
        :param path_and_query_params: 
        :param blacklist: boolean flag indicating whether to blacklist the url or not.
        :return: 
        """
        url_hash = self._url_encoding_service.hashify(host, port=port, path_and_query_params=path_and_query_params)
        self._url_meta_service.create(host, url_hash, port=port,
                                      path_and_query_params=path_and_query_params, blacklist=blacklist)

    def check_url_safety(self, host, port=None, path_and_query_params=None):
        """
        1. Create the hash from url. Find out entry from db. If entry does not exist, 
        return resource not found. If entry exists - check if the corresponding host is blacklisted.
        If host is blacklisted, then return false. If host is active but url is blacklisted, return false.
        If both are non-blacklisted, then only return true.
        :param host: 
        :param port: 
        :param path_and_query_params: 
        :return: 
        """
        url_hash = self._url_encoding_service.hashify(host, port=port, path_and_query_params=path_and_query_params)
        url_meta = self._url_meta_service.get(host, url_hash)

        if not url_meta:
            return URLQueryState(False, None)

        url_meta = url_meta.last()

        is_safe = False
        if not url_meta.is_url_blacklisted and not url_meta.host.is_host_blacklisted:
            is_safe = True

        return URLQueryState(True, is_safe)
