from nicegui import ui
from views.components.ui.header import header as render_header
from views.components.ui.footer import footer as render_footer

def layout(content_func, current_page='Filmes'):
    with ui.column().classes('w-full min-h-screen gap-0'):
        render_header(current_page)
        
        with ui.column().classes('flex-grow items-center w-full mb-4'):
            content_func()
        
        render_footer()