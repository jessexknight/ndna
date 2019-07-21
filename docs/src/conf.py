import sys
import os

sys.path.insert(0, os.path.abspath('../../ndna/'))

# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    # 'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['templates']
# exclude_patterns = ['modules.rst']

source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
project = 'ndna'
author = 'Jesse Knight'

version = '0.0'
release = '0.0'
language = None
today_fmt = '%Y %B %d'
default_role = None

add_function_parentheses = True
add_module_names = True
autodoc_member_order = 'bysource'
pygments_style = 'sphinx'
keep_warnings = False
todo_include_todos = False

napoleon_use_rtype = False

# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_path = ['themes',]
html_theme_options = {}
html_title = 'NDNA Documentation'
html_short_title = 'NDNA'
html_logo    = 'static/icon/favicon.ico'
html_favicon = 'static/icon/favicon.ico' # 16x16 or 32x32 .ico
html_static_path = ['static']
html_extra_path = []
html_last_updated_fmt = '%Y %b %d'
html_use_smartypants = True
html_sidebars = {}
html_additional_pages = {}
html_domain_indices = True
html_use_index = True
html_split_index = False
html_show_sourcelink = False
html_show_sphinx = True
html_show_copyright = True
html_use_opensearch = ''
html_file_suffix = None
html_search_language = 'en'
html_search_options = {'type': 'default'}

def setup(app):
  app.add_stylesheet('css/custom.css')

# -- Python functions -----------------------------------------------------
