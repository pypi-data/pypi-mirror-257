# This configuration has been configured for this demo, not all
# normal sigal settings have an effect in this theme.

# ---------------------
# General configuration
# ---------------------

source = 'source'
destination = 'output'
theme = ''  # theme is automatically set by the theme plugin.
title = 'Photography'
author = '153957 Photography'
author_link = 'https://arne.delaat.net/'
use_orig = True

# --------------------
# Thumbnail generation
# --------------------

make_thumbs = True
thumb_dir = 'thumbnails'
thumb_size = (280, 140)
thumb_fit = False
albums_sort_attr = ['meta.order', 'name']
medias_sort_attr = 'date'
ignore_directories: list[str] = []
ignore_files: list[str] = []

# --------
# Plugins
# --------

plugins: list[str] = ['theme_153957.full_menu', 'theme_153957.theme']
