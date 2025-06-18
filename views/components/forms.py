from datetime import datetime
from nicegui import ui
from models.filme import Genero, Classificacao
from service.actors_api import obter_pessoas_cinema
from service.country_api import obter_paises
from service.crud import SessionLocal, create_filme_with_pessoas, update_filme
from views.components.date_input import date_input


paises = None
pessoas_cinema = None

def lazy_load_data():
    global paises, pessoas_cinema
    if paises is None:
        paises = obter_paises()
    if pessoas_cinema is None:
        pessoas_cinema = obter_pessoas_cinema()
    return paises, pessoas_cinema


def form(filme=None):
    paises, pessoas_cinema = lazy_load_data()
    nomes_pessoas = [pessoa['nome'] for pessoa in pessoas_cinema]


    titulo_pagina = 'Editar Filme' if filme else 'Cadastro de Filmes'
    ui.label(titulo_pagina).classes('text-center w-full mt-8').style('color: #6E93D6; font-size: 200%; font-weight: 500; margin-bottom: 20px;')
    with ui.card().classes('w-full max-w-2xl mx-auto p-8'):
        with ui.row().classes('gap-4 items-center'):
            titulo_input = ui.input('Título').classes('w-full mb-4')
            ano_input = ui.input('Ano de produção').classes('w-48 mb-4')
            estreia_input = date_input()
            duracao_input = ui.input('Duração').classes('w-48 mb-4')
        pais_select = ui.select(options=paises, multiple=True, label='País de origem').classes('w-full mb-4').props('use-chips')
        with ui.row().classes('gap-8'):
            genero_select = ui.select(options=[g.value for g in Genero], multiple=True, label='Gênero').classes('w-72 mb-4').props('use-chips')
            classificacao_select = ui.select(options=[c.value for c in Classificacao], label='Classificação').classes('w-72 mb-4').props('use-chips')
        with ui.row().classes('gap-8'):
            nota_input = ui.input('Nota média').classes('w-72 mb-4')
            votos_input = ui.input('Total de votos').classes('w-72 mb-4')
        with ui.row().classes('gap-8'):
            diretor_select = ui.select(options=nomes_pessoas, label='Diretor').classes('w-72 mb-4').props('use-input')
            elenco_select = ui.select(options=nomes_pessoas, multiple=True, label='Elenco').classes('w-72 mb-4').props('use-chips use-input')
        with ui.row().classes('gap-8'):
            roteiristas_select = ui.select(options=nomes_pessoas, multiple=True, label='Roteiristas').classes('w-72 mb-4').props('use-chips use-input')
            produtores_select = ui.select(options=nomes_pessoas, multiple=True, label='Produtores').classes('w-72 mb-4').props('use-chips use-input')
        poster_input = ui.input('URL do poster').classes('w-full mb-4')
        sinopse_textarea = ui.textarea('Sinopse do filme').classes('w-full mb-4')

        if filme:
            titulo_input.value = filme.titulo or ''
            ano_input.value = str(filme.ano_producao) if filme.ano_producao else ''
            duracao_input.value = str(filme.duracao) if filme.duracao else ''
            
            if filme.estreia:
                estreia_input.value = filme.estreia.strftime('%d/%m/%Y')
            
            if filme.generos:
                if hasattr(filme.generos[0], 'value'):
                    genero_select.value = [g.value for g in filme.generos]
                else:
                    genero_select.value = filme.generos
            
            if filme.classificacao:
                if hasattr(filme.classificacao, 'value'):
                    classificacao_select.value = filme.classificacao.value
                else:
                    classificacao_select.value = filme.classificacao
            
            nota_input.value = str(filme.nota_media) if filme.nota_media else ''
            votos_input.value = str(filme.total_votos) if filme.total_votos else ''
            pais_select.value = filme.pais_origem if filme.pais_origem else []  
            sinopse_textarea.value = filme.sinopse or ''
            poster_input.value = filme.poster_url or ''
            
            if filme.pessoas_referencias and filme.pessoas_referencias.get('diretor'):
                diretor_select.value = filme.pessoas_referencias['diretor']['nome']
            if filme.pessoas_referencias and filme.pessoas_referencias.get('elenco'):
                elenco_select.value = [pessoa['nome'] for pessoa in filme.pessoas_referencias['elenco']]
            if filme.pessoas_referencias and filme.pessoas_referencias.get('roteiristas'):
                roteiristas_select.value = [pessoa['nome'] for pessoa in filme.pessoas_referencias['roteiristas']]
            if filme.pessoas_referencias and filme.pessoas_referencias.get('produtores'):
                produtores_select.value = [pessoa['nome'] for pessoa in filme.pessoas_referencias['produtores']]

        def salvar_filme():
            try:
                if not titulo_input.value:
                    ui.notify('Título é obrigatório', type='negative')
                    return
                if not ano_input.value:
                    ui.notify('Ano de produção é obrigatório', type='negative')
                    return
                if not duracao_input.value:
                    ui.notify('Duração é obrigatória', type='negative')
                    return
                if not estreia_input.value:
                    ui.notify('Data de estreia é obrigatória', type='negative')
                    return
                if not classificacao_select.value:
                    ui.notify('Classificação é obrigatória', type='negative')
                    return
                
                filme_data = {
                    'titulo': titulo_input.value,
                    'ano_producao': int(ano_input.value),
                    'duracao': int(duracao_input.value),
                    'estreia': datetime.strptime(estreia_input.value, '%d/%m/%Y').date(),
                    'generos': [g for g in genero_select.value] if genero_select.value else [],
                    'classificacao': Classificacao(classificacao_select.value),
                    'nota_media': float(nota_input.value) if nota_input.value else None,
                    'total_votos': int(votos_input.value) if votos_input.value else None,
                    'pais_origem': pais_select.value,
                    'sinopse': sinopse_textarea.value,
                    'poster_url': poster_input.value
                }
                
                pessoas_data = {
                    'diretor': diretor_select.value,
                    'elenco': elenco_select.value,
                    'roteiristas': roteiristas_select.value,
                    'produtores': produtores_select.value,
                    'pessoas_tmdb': pessoas_cinema
                }
                
                db = SessionLocal()
                try:
                    if filme:
                        filme_salvo = update_filme(db, filme.id, filme_data, pessoas_data)
                        ui.notify(f'Filme "{filme_salvo.titulo}" atualizado com sucesso!', type='positive')
                        ui.navigate.to('/filmes')  
                    else:
                        filme_salvo = create_filme_with_pessoas(db, filme_data, pessoas_data)
                        ui.notify(f'Filme "{filme_salvo.titulo}" salvo com sucesso!', type='positive')

                    titulo_input.value = ''
                    ano_input.value = ''
                    duracao_input.value = ''
                    estreia_input.value = ''
                    genero_select.value = []
                    classificacao_select.value = None
                    nota_input.value = ''
                    votos_input.value = ''
                    pais_select.value = []
                    sinopse_textarea.value = ''
                    poster_input.value = ''
                    diretor_select.value = None
                    elenco_select.value = []
                    roteiristas_select.value = []
                    produtores_select.value = []
                finally:
                    db.close()
                                
            except ValueError as e:
                ui.notify(f'Erro de validação: {str(e)}', type='negative')
            except Exception as e:
                ui.notify(f'Erro ao salvar filme: {str(e)}', type='negative')
        ui.button('Salvar', on_click=salvar_filme).classes('mt-4 w-full')