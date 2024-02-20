import urllib3


class ProxyManagerPool:
    def __init__(self, proxies):
        """
        proxies: 스키마를 키로 하고 프록시 URL 목록을 값으로 하는 딕셔너리
                 예: {'http': ['http://proxy1.com', 'http://proxy2.com'], 'https': ['https://proxy1.com']}
        """
        self.proxies = proxies
        self.managers = {}
        for schema, proxy in self.proxies.items():
            self.managers[schema] = urllib3.ProxyManager(proxy_url=proxy)
            #self.managers[schema] = [urllib3.ProxyManager(proxy_url=proxy) for proxy in proxy_list]

    def request(self, method, url, **kwargs):
        """
        주어진 URL의 스키마에 맞는 프록시 매니저를 사용하여 요청을 보냅니다.
        """
        schema = url.split(':')[0]  # URL에서 스키마 추출 (예: 'http', 'https')
        if schema in self.managers:
            # 스키마에 해당하는 첫 번째 프록시 매니저 사용
            # 필요에 따라 로드 밸런싱이나 장애 대비를 위한 로직 추가 가능
            manager = self.managers[schema]
            return manager.request(method, url, **kwargs)
        else:
            raise ValueError("Unsupported schema: {}".format(schema))