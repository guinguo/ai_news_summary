"""
网站配置模块，定义要爬取的网站信息和特定规则
"""
# 网站配置列表
SITES = [
    {
        "name": "开源中国",
        "url": "https://www.oschina.net",
        "crawler_type": "common",  # 使用通用爬虫
        "parser_type": "common",   # 使用通用解析器
        "article_selector": {
            "list": ".news-list .news-item",  # 文章列表选择器
            "title": "h3 a",                 # 标题选择器
            "link": "h3 a[href]",            # 链接选择器
            "content": ".article-content"    # 内容选择器
        },
        "custom_rules": {}  # 自定义规则（如有）
    },
    {
        "name": "网易",
        "url": "https://www.163.com",
        "crawler_type": "common",
        "parser_type": "common",
        "article_selector": {
            "list": ".news_title",
            "title": "h1",
            "link": "a[href]",
            "content": ".post_body"
        },
        "custom_rules": {}
    },
    # 其他网站配置可以根据README文件中的表格添加...
]

# 网站分类 - 可以根据需要进行分类
SITE_CATEGORIES = {
    "tech": ["开源中国", "科技日报", "IT之家", "腾讯科技", "cnbeta"],
    "finance": ["财联社", "证券日报", "第一财经", "华尔街见闻", "新浪财经"],
    "news": ["网易", "凤凰网", "央视网", "网易新闻"]
}