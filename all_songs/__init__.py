# 전체곡 크롤러 패키지
from .ky_crawler import crawl_and_save as crawl_kumyoung
from .tj_crawler import crawl_and_save as crawl_taejin

__all__ = ["crawl_kumyoung", "crawl_taejin"]
