from css_html_js_minify import process_single_css_file, process_single_js_file
import os

# Ruta de tus archivos estáticos
STATIC_CSS_DIR = 'app/static/css/'
STATIC_JS_DIR = 'app/static/js/'

# Minificar archivos CSS
for file in os.listdir(STATIC_CSS_DIR):
    if file.endswith('.css'):
        process_single_css_file(os.path.join(STATIC_CSS_DIR, file), overwrite=True)

# Minificar archivos JS
for file in os.listdir(STATIC_JS_DIR):
    if file.endswith('.js'):
        process_single_js_file(os.path.join(STATIC_JS_DIR, file), overwrite=True)