from nicegui import ui
from views.components.movie_list import movie_list
from views.components.ui.layout import layout

def render_movie_list_page():
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    ''')
    layout(lambda: movie_list(), current_page='Filmes')

ui.page('/filmes')(render_movie_list_page)