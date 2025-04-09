# 인기곡 크롤러 패키지
from .ky_crawler import crawl_and_save as crawl_kumyoung_popular
from .tj_crawler import crawl_and_save as crawl_taejin_popular

__all__ = ["crawl_kumyoung_popular", "crawl_taejin_popular"]
