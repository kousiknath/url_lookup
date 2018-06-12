from url_filter.models import URLMeta, Host
from url_filter.service.url_partitioning_service import URLPartitioningService


class URLMetaService(object):
    """
    This url meta service takes into consideration the partitioning of database.
    Currently database is partitioned based on host name provided in the api request.
    """
    def __init__(self):
        self._url_partitioning_service = URLPartitioningService()

    def get(self, host, url_hash):
        partition_info = self._url_partitioning_service.get_partition_info(host)

        url_meta = URLMeta.objects.using(partition_info.partition_name).filter(hash=url_hash)
        return url_meta

    def create(self, host, url_hash, port=None, path_and_query_params=None, blacklist=False):
        partition_info = self._url_partitioning_service.get_partition_info(host)

        host_obj, created = Host.objects.using(partition_info.partition_name).get_or_create(host_name=host)
        existing_url_obj = URLMeta.objects.using(partition_info.partition_name).filter(hash=url_hash)
        if existing_url_obj:
            existing_url_obj.update(is_url_blacklisted=blacklist)
        else:
            params = {
                'host': host_obj,
                'hash': url_hash,
                'is_url_blacklisted': blacklist
            }

            if port:
                params['port'] = port
            if path_and_query_params:
                params['path'] = path_and_query_params

            URLMeta.objects.using(partition_info.partition_name).create(**params)
