from url_filter.entity.partition_info import PartitionInfo
from url_filter.service.url_encoding_service import URLEncodingService
from url_lookup import settings


TOTAL_PARTITIONS = 2
DEFAULT_PARTITION_INDEX = 0


class URLPartitioningService(object):

    def __init__(self):
        self._url_encoding_service = URLEncodingService()

    def get_partition_info(self, host):
        if settings.DISABLE_DB_PARTITIONING:
            return PartitionInfo(DEFAULT_PARTITION_INDEX,
                                 settings.STATIC_DATABASE_PARTITION_META.get(DEFAULT_PARTITION_INDEX))

        host_hash_digest = self._url_encoding_service.hashify(host)
        int_hash = int(host_hash_digest, 16) % 100000
        partition_index = int_hash % TOTAL_PARTITIONS
        partition_name = settings.STATIC_DATABASE_PARTITION_META.get(partition_index)

        return PartitionInfo(partition_index, partition_name)
