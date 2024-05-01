from scapy.all import IP, ICMP, sr1
from cache import Cache


class Tracer:
    def __init__(self, no_cache, max_ttl, ip):
        self.ip = ip
        self.use_cache = not no_cache
        self.max_ttl = max_ttl
        self.cache = Cache('cache.json')
        self.cache_key = f'{ip}-{max_ttl}'

    def show(self, ttl=1, src=None):
        if src:
            print(f'\033[1;32m{str(ttl).rjust(3, " ")} \033[0m{src}')
        else:
            print(f'\033[1;31m{str(ttl).rjust(3, " ")} \033[0m*')

    def display_cached_values(self):
        cache = self.cache.load()
        cache = cache[self.cache_key]

        for hop in cache:
            self.show(*hop)

    def test(self, ttl):
        ip = IP(
            dst=self.ip,
            ttl=ttl
        )

        icmp = ICMP()

        return sr1(ip / icmp, verbose=False, timeout=1)

    def trace(self):
        if self.use_cache and self.cache.has_cache(self.cache_key):
            self.display_cached_values()
        else:
            cache = self.cache.load()

            cache[self.cache_key] = []

            found, ttl = set(), 1

            while True:
                res = self.test(ttl)

                if res:
                    if res.src in found: break
                    else: found.add(res.src)

                    cache[self.cache_key].append((ttl, res.src))
                    self.show(ttl, res.src)
                else:
                    cache[self.cache_key].append((ttl, None))
                    self.show(ttl)

                if ttl >= self.max_ttl: break

                ttl += 1

            self.cache.write(cache)

        return self.cache.load()[self.cache_key]

