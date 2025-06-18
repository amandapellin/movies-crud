from nicegui import ui, app
import os
import locale
from service.actors_api import criar_banco_master_completo
from views.form_views import render_form_page
from views.film_views import render_film_info_page
from views.movie_list_view import render_movie_list_page
from views.actors_list_view import render_actors_list_page
from service.crud import init_db

def configure_locale():
    try:
        locales_to_try = [
            'pt_BR.UTF-8',  
            'pt_BR',            
        ]
        
        for loc in locales_to_try:
            try:
                locale.setlocale(locale.LC_TIME, loc)
                return True
            except locale.Error:
                continue
        return False
        
    except Exception as e:
        return False

def configure():
    ui.add_head_html('''
        <script>
            if (window.Quasar) {
                window.Quasar.lang.set(window.Quasar.lang.ptBR);
            }
        </script>
    ''')
    ui.add_body_html('''
        <style>
            body { 
                margin: 0; 
                padding: 0; 
            }
            .nicegui-content {
                padding: 0;
                
            }
            .q-tab:hover {
                color: #023D67 !important;
                background-color: rgba(8, 145, 178, 0.1) !important;
            }
            .q-tab--active {
                color: #023D67 !important;
                font-weight: 600 !important;
            }
            .q-tab__indicator {
                background-color: #023D67 !important;
                height: 3px !important;
            }
        </style>
    ''')

@ui.page('/')
def index():
    configure()
    render_movie_list_page()

@ui.page('/form')
def form_page():
    configure()
    render_form_page()

@ui.page('/form/{filme_id}')
def edit_movie_page(filme_id: int):
    configure()
    render_form_page(filme_id)
    
@ui.page('/filmes')
def movie_list_page():
    configure()
    render_movie_list_page()
    
@ui.page('/film-info/{filme_id}')
def film_info_page(filme_id: int):
    configure()
    render_film_info_page(filme_id)

@ui.page('/atores')
def actors_page():
    configure()
    render_actors_list_page()

if __name__ in {"__main__", "__mp_main__"}:
    configure_locale()
    init_db()
    master_db_path = os.path.join('service', 'pessoas_master_db.json')
    if not os.path.exists(master_db_path):
        print("Banco de atores não encontrado. Criando...")
        criar_banco_master_completo()
    ui.run(title="Sistema de Filmes", language='pt-BR')