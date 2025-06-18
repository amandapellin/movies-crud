from nicegui import ui

def header(current_page='Filmes'):
    with ui.column().classes('w-full m-0 p-0').style('background-color: #333333; gap: 0;'):
        with ui.row().classes('w-full text-white p-4 items-center justify-between m-0').style('background-color: #333; margin: 0; padding-left: 1rem; padding-right: 1rem;'):
            with ui.row().classes('items-center gap-8'):
                ui.image('https://ui.fstatic.com/static/images/header-filmow-logo.png').style('width: 40px; height: auto;') 
                ui.label('A sua rede social de filmes e séries').classes('text-sm ml-2 text-gray-400')

            with ui.row().classes('gap-2'):
                ui.input(placeholder="Buscar filmes e séries").props('outlined rounded dense clearable dark color=white').classes('w-64').style('background-color: #333; color: white;').props('prefix-icon="search"')
                ui.button('Login', on_click=lambda: print('Login')).props('flat').classes('text-white')
                ui.button('Cadastre-se', on_click=lambda: print('Cadastro')).props('flat').classes('text-white')
        
        with ui.row().classes('w-full m-0 p-0 justify-center').style('background-color: #e8e8e8; margin-top: -1px;'):
            with ui.element('div').classes('w-full max-w-screen-xl mx-auto'):
                with ui.tabs(value=current_page).classes('w-full').props('active-color="#0891b2" indicative-color="#0891b2"') as tabs:
                    tab_options = ['Início', 'Filmes', 'Séries', 'TV', 'Listas', 'Atores', 'Usuários', 'Notícias', 'Grupos']
                    tab_routes = {
                        'Filmes': '/filmes',
                        'Início': '/',
                        'Atores': '/atores',
                    }

                    for tab_name in tab_options:
                        tab = ui.tab(tab_name).classes('text-gray-700')
                        
                        if tab_name in tab_routes:
                            tab.on('click', lambda e, route=tab_routes[tab_name]: ui.navigate.to(route))