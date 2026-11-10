AUTHOR = 'Sergio Delgado Quintero'
SITENAME = 'Tribu'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Atlantic/Canary'

DEFAULT_LANG = 'es'

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

THEME = 'themes/m.css/pelican-theme'
THEME_STATIC_DIR = 'static'
DIRECT_TEMPLATES = ['index']

M_CSS_FILES = [
    'https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,400i,600,600i%7CSource+Code+Pro:400,400i,600',
    '/static/m-dark.css',
]
M_THEME_COLOR = '#22272e'

PLUGIN_PATHS = ['themes/m.css/plugins']
PLUGINS = [
    'm.htmlsanity',
    'm.components',
    'm.images',
    'm.code',
    'm.link',
    'm.gh',
]

M_SITE_LOGO_TEXT = 'Tribu Hub'

M_LINKS_NAVBAR1 = [
    (
        'Page 1',
        'page1/',
        'page1',
        [('Page 1.1', 'page1.1/', 'page1.1')],
    ),
    (
        'Page 2',
        'page2/',
        'page2',
        [('Page 2.1', 'page2.1/', 'page2.1')],
    ),
    ('Blog', 'blog/', 'blog', []),
]

INDEX_URL = 'blog/'
INDEX_SAVE_AS = 'blog/index.html'

PAGE_PATHS = ['pages']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

ARTICLE_PATHS = ['blog']
ARTICLE_URL = 'blog/{slug}/'
ARTICLE_SAVE_AS = 'blog/{slug}/index.html'

M_SHOW_AUTHOR_LIST = True

M_LINKS_FOOTER1 = [('Your Brand', '/'), ('Features', 'features/'), ('Showcase', 'showcase/')]

M_LINKS_FOOTER2 = [
    ('Download', 'download/'),
    ('Packages', 'download/packages/'),
    ('Source', 'download/source/'),
]

M_LINKS_FOOTER3 = [
    ('Contact', ''),
    ('E-mail', 'mailto:you@your.brand'),
    ('GitHub', 'https://github.com/your-brand'),
]

M_FINE_PRINT = """
| Your Brand. Copyright © `You <mailto:you@your.brand>`_, 2017. All rights reserved.
| Tribu. Powered by `Pelican <https://getpelican.com/>`_ and `m.css <https://mcss.mosra.cz/>`_.
"""
