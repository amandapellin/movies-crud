import random
import time
import math
from nicegui import ui
from service.actors_api import obter_pessoas_cinema
from service.crud import SessionLocal, get_filmes
import json

def actors_list():
    ATORES_POR_PAGINA = 24
    pagina_atual:int = 1
    total_atores:list = []
    termo_busca:str = ''
    
    def carregar_todos_atores():
        try:
            nonlocal total_atores
            if not total_atores: 
                pessoas = obter_pessoas_cinema()
                random.seed(int(time.time()) // 3600)
                random.shuffle(pessoas)
                total_atores = pessoas
            return total_atores
        except Exception as e:
            ui.notify(f'Erro ao carregar atores: {str(e)}', type='negative')
            return []
    
    def obter_pagina_atores(pagina):
        atores = carregar_todos_atores()
        if termo_busca:
            atores = [a for a in atores if termo_busca in a['nome'].lower()]
        inicio = (pagina - 1) * ATORES_POR_PAGINA
        fim = inicio + ATORES_POR_PAGINA
        return atores[inicio:fim]
    
    def calcular_total_paginas():
        total = len([
            a for a in carregar_todos_atores()
            if termo_busca in a['nome'].lower()
        ]) if termo_busca else len(carregar_todos_atores())
        return math.ceil(total / ATORES_POR_PAGINA)
    
    def obter_filmes_ator(ator_nome):
        db = SessionLocal()
        try:
            filmes = get_filmes(db)
            filmes_ator = []
            
            for filme in filmes:
                pessoas_referencias = getattr(filme, 'pessoas_referencias', {})
                if isinstance(pessoas_referencias, str):
                    try:
                        pessoas_referencias = json.loads(pessoas_referencias)
                    except:
                        pessoas_referencias = {}
                
                participou = False
                papel = []
                
                diretor = pessoas_referencias.get('diretor', {})
                if isinstance(diretor, dict) and diretor.get('nome') == ator_nome:
                    participou = True
                    papel.append('Diretor')
                
                elenco = pessoas_referencias.get('elenco', [])
                for pessoa in elenco:
                    if isinstance(pessoa, dict) and pessoa.get('nome') == ator_nome:
                        participou = True
                        if 'Ator' not in papel:
                            papel.append('Ator')
                        break
                
                roteiristas = pessoas_referencias.get('roteiristas', [])
                for pessoa in roteiristas:
                    if isinstance(pessoa, dict) and pessoa.get('nome') == ator_nome:
                        participou = True
                        if 'Roteirista' not in papel:
                            papel.append('Roteirista')
                        break
                
                produtores = pessoas_referencias.get('produtores', [])
                for pessoa in produtores:
                    if isinstance(pessoa, dict) and pessoa.get('nome') == ator_nome:
                        participou = True
                        if 'Produtor' not in papel:
                            papel.append('Produtor')
                        break
                
                if participou:
                    filmes_ator.append({
                        'titulo': filme.titulo,
                        'ano': filme.ano_producao,
                        'papel': ' / '.join(papel)
                    })
            
            return filmes_ator
        finally:
            db.close()
    
    def exibir_detalhes_ator(ator):
        filmes = obter_filmes_ator(ator['nome'])
        
        with ui.dialog().props('maximized') as dialog:
            with ui.card().classes('w-full max-w-4xl mx-auto'):
                with ui.row().classes('items-center mb-4'):
                    if ator.get('foto_url'):
                        ui.image(ator['foto_url']).classes('w-32 h-32 rounded-full')
                    else:
                        ui.avatar(ator['nome'][:2], color='primary').classes('text-2xl w-32 h-32')
                    
                    with ui.column().classes('ml-4'):
                        ui.label(ator['nome']).classes('text-2xl font-bold')
                        ui.label(f'ID TMDB: {ator["tmdb_id"]}').classes('text-gray-600')
                
                ui.label('Filmes').classes('text-xl font-semibold mt-4 mb-2')
                
                if filmes:
                    colunas_filmes = [
                        {'name': 'titulo', 'label': 'Título', 'field': 'titulo', 'sortable': True, 'align': 'left'},
                        {'name': 'ano', 'label': 'Ano', 'field': 'ano', 'sortable': True},
                        {'name': 'papel', 'label': 'Papel', 'field': 'papel', 'align': 'left'}
                    ]
                    
                    ui.table(
                        columns=colunas_filmes,
                        rows=filmes,
                        row_key='titulo'
                    ).classes('w-full')
                else:
                    ui.label('Nenhum filme encontrado no banco de dados local.').classes('text-gray-500 italic')
                
                ui.button('Fechar', on_click=dialog.close).classes('mt-4')
        
        dialog.open()
    
    def ir_para_pagina(nova_pagina):
        nonlocal pagina_atual
        total_paginas = calcular_total_paginas()
        
        if 1 <= nova_pagina <= total_paginas:
            pagina_atual = nova_pagina
            carregar_e_exibir()
    
    def embaralhar_atores():
        nonlocal total_atores, pagina_atual
        pessoas = obter_pessoas_cinema()
        random.shuffle(pessoas)
        total_atores = pessoas
        pagina_atual = 1
        carregar_e_exibir()
        
    def atualizar_busca(e):
        nonlocal termo_busca, pagina_atual
        novo_valor = (e.value or '').strip().lower()
        if novo_valor != termo_busca:
            termo_busca = novo_valor
            pagina_atual = 1
            carregar_e_exibir()
    
    ui.label('Lista de Atores').classes('text-center w-full mt-8').style('color: #6E93D6; font-size: 200%; font-weight: 500; margin-bottom: 20px;')
    
    with ui.card().classes('w-full max-w-6xl mx-auto p-8'):
        with ui.row().classes('w-full justify-between items-center mb-4'):
            ui.input(
                placeholder='Buscar ator por nome...',
                on_change=atualizar_busca
            ).props('clearable').classes('w-full mb-4')
            with ui.row().classes('items-center gap-4'):
                info_label = ui.label('')
                ui.button('Atualizar', on_click=embaralhar_atores).classes('bg-blue-500 text-white')
            
            def alterar_itens_por_pagina(value):
                nonlocal ATORES_POR_PAGINA, pagina_atual
                ATORES_POR_PAGINA = int(value)
                pagina_atual = 1
                carregar_e_exibir()
            
            ui.select(
                options=[12, 24, 36, 48], 
                value=ATORES_POR_PAGINA,
                label='Por página',
                on_change=lambda e: alterar_itens_por_pagina(e.value)
            ).classes('w-32')
        
        with ui.row().classes('w-full gap-4 flex-wrap justify-center') as container:
            ui.label('Carregando...').classes('text-center')
        
        with ui.row().classes('w-full justify-center items-center mt-6 gap-4') as pagination_container:
            pass
        
        def criar_paginacao():
            pagination_container.clear()
            total_paginas = calcular_total_paginas()
            
            if total_paginas <= 1:
                return
            
            with pagination_container:
                ui.button(
                    'Anterior', 
                    on_click=lambda: ir_para_pagina(pagina_atual - 1)
                ).props('flat').classes('mr-2').set_enabled(pagina_atual > 1)
                
                inicio = max(1, pagina_atual - 2)
                fim = min(total_paginas, pagina_atual + 2)
                
                if inicio > 1:
                    ui.button('1', on_click=lambda: ir_para_pagina(1)).props('flat')
                    if inicio > 2:
                        ui.label('...').classes('px-2')
                
                for p in range(inicio, fim + 1):
                    if p == pagina_atual:
                        ui.button(str(p)).props('color=primary')
                    else:
                        ui.button(str(p), on_click=lambda page=p: ir_para_pagina(page)).props('flat')
                
                if fim < total_paginas:
                    if fim < total_paginas - 1:
                        ui.label('...').classes('px-2')
                    ui.button(str(total_paginas), on_click=lambda: ir_para_pagina(total_paginas)).props('flat')
                
                ui.button(
                    'Próximo', 
                    on_click=lambda: ir_para_pagina(pagina_atual + 1)
                ).props('flat').classes('ml-2').set_enabled(pagina_atual < total_paginas)
        
        def carregar_e_exibir():
            container.clear()
            
            atores = obter_pagina_atores(pagina_atual)
            total_paginas = calcular_total_paginas()
            total_pessoas = len(carregar_todos_atores())
            
            info_label.text = f'Página {pagina_atual} de {total_paginas} • {total_pessoas} atores total'
            
            if not atores:
                with container:
                    ui.label('Nenhum ator encontrado.').classes('text-gray-500')
                return
            
            for ator in atores:
                with container:
                    with ui.card().classes('w-64 h-80 items-center cursor-pointer hover:shadow-lg transition-shadow').on('click', lambda a=ator: exibir_detalhes_ator(a)):
                        with ui.column().classes('items-center p-4 h-full'):
                            if ator.get('foto_url'):
                                ui.image(ator['foto_url']).classes('w-24 h-24 rounded-full object-cover')
                            else:
                                ui.avatar(ator['nome'][:2], color='primary').classes('text-xl w-24 h-24')
                            
                            ui.label(ator['nome']).classes('text-center font-semibold mt-2 text-sm line-clamp-2')
                            
                            filmes_count = len(obter_filmes_ator(ator['nome']))
                            ui.label(f'{filmes_count} filme(s)').classes('text-gray-600 text-xs mt-1')
                            
                            ui.label('Clique para detalhes').classes('text-blue-500 text-xs mt-auto')
            
            criar_paginacao()
    
        ui.timer(0.1, carregar_e_exibir, once=True)