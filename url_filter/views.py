# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View

from url_filter.service.url_filtering_service import URLFilterService
from url_filter.service.url_encoding_service import URLEncodingService

from urlparse import urlparse

import json


class URLFilter(View):
    def __init__(self):
        super(URLFilter, self).__init__()
        self._url_service = URLFilterService()
        self._url_encoding_service = URLEncodingService()

    def get(self, request, *args, **kwargs):
        """
        Format of host_port is in: host:9080 or hostname or 123.21.23 or 231.445.233.11:9000 etc
        Format of url string & query params: a/b/c/d?key1=value1&key2=value2
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        host = kwargs.get(str('host'))
        port = kwargs.get(str('port')) or None
        path = kwargs.get(str('path')) or None

        # Validation
        if not host:
            return HttpResponseBadRequest("Host is a mandatory field in request.")

        query_string = ''
        splited_full_path = request.get_full_path().split('?')
        if len(splited_full_path) > 0:
            query_string = '?' + splited_full_path[1]

        if path and query_string:
            path = '/' + path + query_string

        # Serialize the host:port & url path to check in the data store.
        url_safety_result = self._url_service.check_url_safety(host,
                                                               port=port,
                                                               path_and_query_params=path)

        return self._get_response(url_safety_result, host, port=port, path_and_query_params=path)

    def _get_response(self, safety_info, host, port=None, path_and_query_params=None):
        message = ''
        if not safety_info.is_found:
            message = 'URL information not found in database'

        if not safety_info.is_safe:
            message = 'The url is blacklisted in system'

        data = dict()

        data['host'] = host
        data['port'] = port
        data['path'] = path_and_query_params
        data['is_safe'] = safety_info.is_safe or False
        data['message'] = message

        return HttpResponse(json.dumps(data))

    def post(self, request, *args, **kwargs):
        """
        This functionality is used to add url (host, port, other path) to the system.
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        if not body or not body.get('url'):
            return HttpResponseBadRequest("Request body must contain url that has to be saved.")
        blacklist = body.get('blacklist', False)

        url = body.get('url')
        if 'http' not in url:
            url = 'http://' + str(url)
        parsed_url = urlparse(url)

        self._url_service.add_url(parsed_url.hostname, port=str(parsed_url.port) if parsed_url.port else None,
                                  path_and_query_params=parsed_url.path + '?' + parsed_url.query if parsed_url.query
                                  else parsed_url.path,
                                  blacklist=blacklist)

        result = {'success': True, 'message': 'URL data updated successfully'}
        return HttpResponse(json.dumps(result))
