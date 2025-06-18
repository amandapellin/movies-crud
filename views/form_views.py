from nicegui import ui
from views.components.ui.layout import layout
from views.components.forms import form
from service.crud import SessionLocal, get_filme_by_id as get_filme

def render_form_page(filme_id: int = None):
    ui.add_head_html('''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    ''')
    if filme_id:
        db = SessionLocal()
        try:
            filme = get_filme(db, filme_id)
            layout(lambda: form(filme))
        finally:
            db.close()
    else:
        layout(form)

