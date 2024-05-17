from flask_caching import Cache
import socket
import os
enable_memcache = os.getenv("ENABLE_MEMCACHE", False)
if(enable_memcache):
    _, _, ips = socket.gethostbyname_ex('bernos-memcache-memcached.default.svc.cluster.local')
    # _, _, ips = socket.gethostbyname_ex(socket.gethostname())
    print(ips)
    memcache_servers = tuple(ips)
    print(memcache_servers)
    cache = Cache(config={'CACHE_TYPE': 'memcached',
                            'CACHE_MEMCACHED_SERVERS': memcache_servers,
                            'CACHE_KEY_PREFIX': 'bernospc'})
else:
    cache = Cache(config={'CACHE_TYPE': 'simple'})

cache2 = Cache(config={'CACHE_TYPE':'simple'})