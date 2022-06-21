from core.util import read_yaml


class Remote:
    cos: str
    wiki: str


class Bucket:
    enabled: bool
    region: str
    secret_id: str
    secret_key: str
    bucket_name: str


class ResourceConfig:
    remote: Remote
    bucket: Bucket


resource_config: ResourceConfig = read_yaml('config/remote.yaml')
