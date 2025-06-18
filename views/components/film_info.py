import json
from nicegui import ui

from service.crud import SessionLocal, get_filme_by_id as get_filme

def film_info(filme_id: int = None):
    if filme_id:
        db = SessionLocal()
        try:
            filme = get_filme(db, filme_id)
            if not filme:
                ui.label('Filme não encontrado').classes('text-red-500 text-center mt-8')
                return
        finally:
            db.close()
    else:
        filme = None
    
    with ui.column().classes('w-full gap-0 mt-0'):
        with ui.row().classes('w-full justify-between items-center'):
            with ui.element('div').classes('w-full backdrop-blur-md').style('background: linear-gradient(90deg, rgba(29,32,31,0.7), rgba(34,49,39,0.7)); display: flex; align-items: center; gap: 10px; padding: 15px;'):
                poster_url = filme.poster_url if filme and filme.poster_url else 'static/pearl_poster.jpg'
                ui.image(poster_url).classes('poster-image w-48').style('border-radius: 4px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 3px solid #e0e0e0;')
                with ui.card().classes('no-shadow w-full p-4').style('background: transparent;'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.column():
                            with ui.row().classes('items-center gap-2'):
                                titulo = filme.titulo if filme else 'Filme não encontrado'
                                ano = filme.ano_producao if filme else ''
                                ui.label(titulo).classes('text-3xl font-bold text-white')
                                ui.label(str(ano)).classes('text-xsm font-regular text-white')

                            with ui.row().classes('mt-3 gap-2'):
                                with ui.dropdown_button('✓ Já Vi', color='#C7CCB9', auto_close=True).classes('rounded text-black'):
                                    ui.item('1 vez').classes('text-sm')
                                    ui.item('2 vezes').classes('text-sm')
                                    ui.item('3 vezes').classes('text-sm')
                                    ui.item('4 vezes').classes('text-sm')
                                    ui.item('5 vezes').classes('text-sm')
                                    ui.separator()
                                    ui.item('Perdi a conta').classes('text-sm')
                                ui.button('+ Quero Ver', color='#C7CCB9').classes('rounded')
                                ui.button('📋', color='#C7CCB9').classes('rounded')
                                ui.button('❤️', color='#C7CCB9').classes('rounded')
                                ui.button('📤 Indicar', color='#C7CCB9').classes('rounded')
                        
                with ui.card().classes('w-1/4 mt-4 p-4 no-shadow').style('background: transparent; gap: 1px'):
                    with ui.button_group():
                        ui.button('MÉDIA\nGERAL', color='#FFC43D').classes('text-md font-regular text-gray-600 whitespace-pre-line').style('border-right: 1px solid #F9DC5C;')
                        nota_media = filme.nota_media if filme and filme.nota_media else '0.0'
                        ui.button(str(nota_media), color='#FFC43D').classes('text-2xl font-bold text-gray-600')
                    total_votos = filme.total_votos if filme and filme.total_votos else 0
                    ui.label(f'baseado em {total_votos} votos').classes('text-xsm text-white text-center mt-2')
                
        with ui.row().classes('w-full justify-between items-center mt-0').style('background-color:#0891b2'):
            with ui.element('div').classes('w-3/5 max-w-screen-xl ml-4'):
                with ui.tabs().classes('w-full').props('active-color="#6E8894"') as tabs:
                    for tab_name in ['Perfil', 'Ficha Técnica', 'Comentários', 'Notícias', 'Assista Agora']:
                        ui.tab(tab_name).classes('text-white')
            with ui.row().classes('w-1/4 justify-center gap-1'): 
                ui.label('Sua avaliação:').classes('text-sm font-bold text-white')
                for i in range(5):
                    if i < 4:
                        ui.icon('star', color='gold').classes('text-lg')
                    else:
                        ui.icon('star_border', color='white').classes('text-lg')
     
        with ui.column().classes('w-full max-w-screen-xl mx-auto'):
            with ui.tab_panels(tabs, value='Ficha Técnica').classes('w-full'):
                
                with ui.tab_panel('Perfil'):
                    sinopse = filme.sinopse if filme and filme.sinopse else 'Sinopse não disponível.'
                    ui.label('Sinopse').classes('text-2xl font-bold mb-4').style('color: #353535')
                    ui.label(sinopse).classes('text-lg leading-relaxed')
                
                with ui.tab_panel('Ficha Técnica'):
                    _render_ficha_tecnica(filme)
                
                with ui.tab_panel('Comentários'):
                    ui.label('Comentários dos usuários...').classes('text-lg')
                
                with ui.tab_panel('Notícias'):
                    ui.label('Últimas notícias...').classes('text-lg')
                
                with ui.tab_panel('Assista Agora'):
                    ui.label('Onde assistir...').classes('text-lg')
def _render_ficha_tecnica(filme):
    with ui.row().classes('w-full justify-between items-center'):
        ui.label('Ficha Técnica Completa').classes('text-2xl font-bold mb-6').style('color: #353535')
        
        with ui.grid(columns=2).classes('w-full justify-between gap-24'):
            with ui.column().classes('w-full space-y-0 gap-0'):
                _render_info_row('Título', filme.titulo if filme else 'N/A', True)
                _render_info_row('Ano produção', str(filme.ano_producao) if filme else 'N/A', False)
                
                diretor_nome = _get_diretor_nome(filme)
                _render_info_row_with_chip('Dirigido por', diretor_nome, True)
                
                estreia_text = filme.estreia.strftime('%d de %B de %Y') if filme and filme.estreia else 'N/A'
                _render_info_row('Estreia', estreia_text, False)
                
                duracao_text = f'{filme.duracao} minutos' if filme and filme.duracao else 'N/A'
                _render_info_row('Duração', duracao_text, True)
                
                classificacao = _get_classificacao_display(filme)
                _render_info_row_with_rating('Classificação', classificacao, False)
                
                generos = _get_generos_display(filme)
                _render_info_genero('Gêneros', generos, True)
                
                pais_origem = _get_paises_display(filme)
                _render_info_pais_origem('País de origem', pais_origem)
            
            with ui.column().classes('w-full space-y-0'):
                _render_pessoas_section('Elenco', filme, 'elenco')
                
                _render_pessoas_section('Roteiristas', filme, 'roteiristas')
                
                _render_pessoas_section('Produtores', filme, 'produtores')

def _render_info_row(label, value, is_odd):
    bg_class = 'background-color: #F9F9F9;' if is_odd else ''
    with ui.row().classes('items-center w-full py-3 pl-2').style(f'{bg_class} border-bottom: 1px solid #e0e0e0;'):
        ui.label(label).classes('font-bold w-32')
        ui.label(value).classes('flex-grow')

def _render_info_row_with_chip(label, value, is_odd):
    bg_class = 'background-color: #F9F9F9;' if is_odd else ''
    with ui.row().classes('items-center w-full py-3 pl-2').style(f'{bg_class} border-bottom: 1px solid #e0e0e0;'):
        ui.label(label).classes('font-bold w-32')
        if value and value != 'N/A':
            ui.chip(value, color='#D8D8D8').style('border-radius: 0px;')
        else:
            ui.label('N/A').classes('flex-grow')

def _render_info_row_with_rating(label, value, is_odd):
    bg_class = 'background-color: #F9F9F9;' if is_odd else ''
    with ui.row().classes('items-center w-full py-3 pl-2').style(f'{bg_class} border-bottom: 1px solid #e0e0e0'):
        ui.label(label).classes('font-bold w-32')
        if value and value != 'N/A':
            with ui.row().classes('items-center gap-2 flex-grow'):
                ui.html(f'<span class="age-rating" style="background-color: #000000; color: white; padding: 2px 6px; border-radius: 3px; font-weight: bold;">{value}</span>')
                ui.label(f'{value} - Classificação indicativa')
        else:
            ui.label('N/A').classes('flex-grow')
            
def _render_info_genero(label, value, is_odd):
    bg_class = 'background-color: #F9F9F9;' if is_odd else ''
    with ui.row().classes('items-center w-full py-3 pl-2').style(f'{bg_class} border-bottom: 1px solid #e0e0e0'):
        ui.label(label).classes('font-bold w-32')
        if value and value != 'N/A':
            with ui.row().classes('flex-wrap gap-1'):
                for genero in value.split(','):
                    ui.chip(genero, color='#D8D8D8').style('border-radius: 0px;')
        else:
            ui.label('N/A').classes('flex-grow')

def _render_info_pais_origem(label, value):
    with ui.row().classes('items-center w-full py-3 pl-2').style('border-bottom: 1px solid #e0e0e0'):
        ui.label(label).classes('font-bold w-32')
        if value and value != 'N/A':
            with ui.row().classes('flex-wrap gap-1'):
                for pais in value.split(','):
                    ui.chip(pais, color='#D8D8D8').style('border-radius: 0px;')
        else:
            ui.label('N/A').classes('flex-grow')
    
def _render_pessoas_section(titulo, filme, categoria):
    ui.label(titulo).classes('text-xl font-medium mb-2').style('color:#353535')
    
    pessoas = _get_pessoas_por_categoria(filme, categoria)
    
    if pessoas:
        with ui.grid(columns=2).classes('w-full justify-between items-start gap-6 mb-6'):
            for pessoa in pessoas:
                with ui.row().classes('items-center gap-4'):
                    foto_url = pessoa.get('foto_url', 'static/images.jpg')
                    ui.image(foto_url).classes('w-16 h-16').style('border-radius: 4px; box-shadow: 0 4px 8px rgba(0,0,0,0.3);')
                    ui.link(pessoa.get('nome', 'Nome não disponível'), '#').classes('font-medium text-md')
    else:
        ui.label('Informação não disponível').classes('text-gray-500 italic mb-6')
    
def _get_diretor_nome(filme):
    if not filme or not filme.pessoas_referencias:
        return 'N/A'
    
    pessoas_referencias = filme.pessoas_referencias
    if isinstance(pessoas_referencias, str):
        try:
            pessoas_referencias = json.loads(pessoas_referencias)
        except:
            return 'N/A'
    
    diretor = pessoas_referencias.get('diretor', {})
    if isinstance(diretor, dict):
        return diretor.get('nome', 'N/A')
    return 'N/A'

def _get_classificacao_display(filme):
    if not filme or not filme.classificacao:
        return 'N/A'
    
    if hasattr(filme.classificacao, 'value'):
        return filme.classificacao.value
    else:
        return str(filme.classificacao)

def _get_pessoas_por_categoria(filme, categoria):
    if not filme or not filme.pessoas_referencias:
        return []
    
    pessoas_referencias = filme.pessoas_referencias
    if isinstance(pessoas_referencias, str):
        try:
            pessoas_referencias = json.loads(pessoas_referencias)
        except:
            return []
    
    return pessoas_referencias.get(categoria, [])

def _get_generos_display(filme):
    if not filme or not filme.generos:
        return 'N/A'
    
    generos = [g.value if hasattr(g, 'value') else g for g in filme.generos]
    return ', '.join(generos) if generos else 'N/A'

def _get_paises_display(filme):
    if not filme or not filme.pais_origem:
        return 'N/A'
    
    return ', '.join(filme.pais_origem) if filme.pais_origem else 'N/A'