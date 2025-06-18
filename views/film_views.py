from nicegui import ui
from views.components.ui.layout import layout
from views.components.film_info import film_info
def render_film_info_page(filme_id: int = None):
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    ''')
    layout(lambda: film_info(filme_id))