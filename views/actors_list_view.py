from nicegui import ui
from views.components.actors_list import actors_list
from views.components.ui.layout import layout

def render_actors_list_page():
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    ''')
    layout(lambda: actors_list(), current_page='Atores')
    
ui.page('/atores')(render_actors_list_page) 
