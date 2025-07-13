class MWebAuthRegistry:
    SKIP_EXACT_URLS: dict[str, list[str]] = {}
    SKIP_PREFIXES: dict[str, list[str]] = {}

    @staticmethod
    def _init_skip_url_list(tenant: str = "default"):
        if tenant not in MWebAuthRegistry.SKIP_EXACT_URLS:
            MWebAuthRegistry.SKIP_EXACT_URLS[tenant] = []

        if tenant not in MWebAuthRegistry.SKIP_PREFIXES:
            MWebAuthRegistry.SKIP_PREFIXES[tenant] = []

    @staticmethod
    def add_skip_exact_url(url: str, tenant: str = "default"):
        MWebAuthRegistry._init_skip_url_list(tenant=tenant)
        MWebAuthRegistry.SKIP_EXACT_URLS[tenant].append(url)

    @staticmethod
    def add_skip_prefixe_url(url: str, tenant: str = "default"):
        MWebAuthRegistry._init_skip_url_list(tenant=tenant)
        MWebAuthRegistry.SKIP_PREFIXES[tenant].append(url)

    @staticmethod
    def add_exact_url_list_in_skip(urls: list, tenant: str = "default"):
        MWebAuthRegistry._init_skip_url_list(tenant=tenant)
        if urls and isinstance(urls, list):
            MWebAuthRegistry.SKIP_EXACT_URLS[tenant] += urls

    @staticmethod
    def add_prefix_url_list_in_skip(urls: list, tenant: str = "default"):
        MWebAuthRegistry._init_skip_url_list(tenant=tenant)
        if urls and isinstance(urls, list):
            MWebAuthRegistry.SKIP_PREFIXES[tenant] += urls

    @staticmethod
    def get_skip_exact_urls(tenant: str = "default"):
        if tenant not in MWebAuthRegistry.SKIP_EXACT_URLS:
            return []
        return MWebAuthRegistry.SKIP_EXACT_URLS[tenant]

    @staticmethod
    def get_skip_prefixes(tenant: str = "default"):
        if tenant not in MWebAuthRegistry.SKIP_PREFIXES:
            return []
        return MWebAuthRegistry.SKIP_PREFIXES[tenant]
