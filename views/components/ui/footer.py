from nicegui import ui

def footer():
    with ui.column().classes('w-full text-white m-0 p-0').style('background-color: #333;'):
        with ui.row().classes('w-full px-10 py-10 justify-between flex-wrap m-0'):
            def footer_column(title: str, links: list[str]):
                with ui.column().classes('min-w-[150px] mr-10'):
                    ui.label(title.upper()).classes('text-cyan-400 font-bold mb-2')
                    for link in links:
                        ui.link(link, target='#').classes('text-sm text-gray-300 hover:underline')

            footer_column('Filmes', ['Todos', 'Estreias', 'Nos Cinemas', 'Em breve', 'Filmes Online', 'Filmes Grátis', 'Curtas Metragens'])
            footer_column('Séries', ['Todas', 'Estreias', 'No Ar', 'Em breve'])
            footer_column('Listas', ['Destaques', 'Populares', 'Populares da Semana', 'Recentes', 'Minhas Listas'])
            footer_column('Grupos', ['Grupos Populares', 'Posts Populares', 'Grupos Novos', 'Meus links', 'Criar um Grupo'])
            footer_column('O Filmow', ['Sobre o Filmow', 'Cadastrar filme', 'Perguntas Frequentes', 'Contato', 'Formatos de Anúncios'])

        with ui.row().classes('w-full text-gray-400 text-sm justify-between px-10 pb-6 pt-0 flex-wrap m-0'):
            with ui.row().classes('gap-4'):
                ui.link('Política de Privacidade', target='#').classes('hover:underline text-gray-400 no-underline')
                ui.link('Termos de Uso', target='#').classes('hover:underline text-gray-400 no-underline')

            ui.label('© 2016 Filmow. Todos os direitos reservados.')

            with ui.row().classes('gap-4'):
                for icon_name, href in [
                    ('fab fa-facebook', '#'),
                    ('fab fa-instagram', '#'),
                    ('fab fa-twitter', '#'),
                    ('fab fa-youtube', '#'),
                    ('fab fa-discord', '#')
                ]:
                    ui.icon(icon_name).classes('text-white cursor-pointer hover:text-cyan-400')