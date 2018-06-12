# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from url_filter.service.url_filtering_service import URLFilterService
from url_filter.service.url_encoding_service import URLEncodingService
from url_filter.service.url_partitioning_service import URLPartitioningService
from url_filter.models import URLMeta, Host

from url_lookup import settings


class URLFilterServiceTest(TestCase):
    def setUp(self):
        self._url_filter_service = URLFilterService()
        self._url_encoding_service = URLEncodingService()
        self._url_partitioning_service = URLPartitioningService()

        self.host = '124.21.34.1'
        self.port = '9000'
        self.path = 'test/test1?key=value'

        self.url_hash = self._url_encoding_service.hashify(self.host, port=self.port, path_and_query_params=self.path)
        self.partition_index = self._url_partitioning_service.get_partition_info(self.host)

    def test_add_url(self):
        self._url_filter_service.add_url(self.host, port=self.port, path_and_query_params=self.path)
        url_meta_obj = URLMeta.objects.using(settings.STATIC_DATABASE_PARTITION_META
                                             .get(self.partition_index))\
            .get(hash=self.url_hash)

        assert url_meta_obj.host.host_name == self.host
        assert url_meta_obj.port == self.port
        assert url_meta_obj.path == self.path

    def test_safe_url(self):
        self._url_filter_service.add_url(self.host, port=self.port, path_and_query_params=self.path)
        url_safety_obj = self._url_filter_service.check_url_safety(self.host, port=self.port,
                                                                   path_and_query_params=self.path)

        assert url_safety_obj.is_safe is True

    def test_unsafe_url(self):
        self._url_filter_service.add_url(self.host, port=self.port, path_and_query_params=self.path, blacklist=True)
        url_safety_obj = self._url_filter_service.check_url_safety(self.host, port=self.port,
                                                                   path_and_query_params=self.path)

        assert url_safety_obj.is_safe is False

    def test_url_when_unsafe_host(self):
        self._url_filter_service.add_url(self.host, port=self.port, path_and_query_params=self.path, blacklist=False)

        Host.objects.using(settings.STATIC_DATABASE_PARTITION_META
                           .get(self.partition_index)).filter(host_name=self.host)\
            .update(is_host_blacklisted=True)

        url_safety_obj = self._url_filter_service.check_url_safety(self.host, port=self.port,
                                                                   path_and_query_params=self.path)

        assert url_safety_obj.is_safe is False


