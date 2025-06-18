from nicegui import ui
from service.crud import SessionLocal, get_filme_by_name, get_filmes

def movie_list():
    columns = [
        {'name': 'titulo', 'label': 'Título', 'field': 'titulo', 'sortable': True},
        {'name': 'ano_producao', 'label': 'Ano', 'field': 'ano_producao', 'sortable': True},
        {'name': 'generos', 'label': 'Gêneros', 'field': 'generos'},
        {'name': 'classificacao', 'label': 'Classificação', 'field': 'classificacao'},
        {'name': 'nota_media', 'label': 'Nota', 'field': 'nota_media', 'sortable': True},
        {'name': 'pais_origem', 'label': 'País', 'field': 'pais_origem'},
        {'name': 'acoes', 'label': 'Ações', 'field': 'acoes'},
    ]
    def buscar_filmes(termo_busca):
        db = SessionLocal()
        try:
            if not termo_busca:
                return carregar_filmes()
                
            filmes = get_filme_by_name(db, termo_busca)
            if not filmes:
                ui.notify('Nenhum filme encontrado com esse título.', type='warning')
                return []
            if not isinstance(filmes, list):
                filmes = [filmes]
            for filme in filmes:
                if filme.generos:
                    if hasattr(filme.generos[0], 'value'):
                        filme.generos = ', '.join([g.value for g in filme.generos])
                    else:
                        filme.generos = ', '.join(filme.generos)
                else:
                    filme.generos = ''
                
                if filme.classificacao:
                    if hasattr(filme.classificacao, 'value'):
                        filme.classificacao = filme.classificacao.value
                    else:
                        filme.classificacao = str(filme.classificacao)
                else:
                    filme.classificacao = ''
            filmes = [{'id': f.id, 'titulo': f.titulo, 'ano_producao': f.ano_producao,
                      'generos': f.generos, 'classificacao': f.classificacao,
                      'nota_media': f.nota_media if f.nota_media else '',
                      'pais_origem': ', '.join(f.pais_origem) if f.pais_origem else '',
                      'acoes': f.id} for f in filmes]
            return filmes
        finally:
            db.close()
            
    def carregar_filmes():
        db = SessionLocal()
        try:
            filmes = get_filmes(db)
            rows = []
            for filme in filmes:
                if filme.generos:
                    if hasattr(filme.generos[0], 'value'):
                        generos_str = ', '.join([g.value for g in filme.generos])
                    else:
                        generos_str = ', '.join(filme.generos)
                else:
                    generos_str = ''
                
                if filme.classificacao:
                    if hasattr(filme.classificacao, 'value'):
                        classificacao_str = filme.classificacao.value
                    else:
                        classificacao_str = str(filme.classificacao)
                else:
                    classificacao_str = ''
                
                rows.append({
                    'id': filme.id,
                    'titulo': filme.titulo,
                    'ano_producao': filme.ano_producao,
                    'generos': generos_str,
                    'classificacao': classificacao_str,
                    'nota_media': filme.nota_media if filme.nota_media else '',
                    'pais_origem': ', '.join(filme.pais_origem) if filme.pais_origem else '',
                    'acoes': filme.id 
                })
            return rows
        finally:
            db.close()
    
    def excluir_filme(filme_id):
        from service.crud import delete_filme
        db = SessionLocal()
        try:
            delete_filme(db, filme_id)
            ui.notify('Filme excluído com sucesso!', type='positive')
            tabela.rows = carregar_filmes() 
        except Exception as e:
            ui.notify(f'Erro ao excluir filme: {str(e)}', type='negative')
        finally:
            db.close()
    
    def editar_filme(filme_id):
        ui.navigate.to(f'/form/{filme_id}')
    
    ui.label('Lista de Filmes').classes('text-center w-full mt-8').style('color: #6E93D6; font-size: 200%; font-weight: 500; margin-bottom: 20px;')
    
    with ui.card().classes('w-full max-w-6xl mx-auto p-8'):
        with ui.row().classes('justify-between mb-4 w-full'):
            ui.input('Pesquisar', placeholder='Digite o título do filme', on_change=lambda e: setattr(tabela, 'rows', buscar_filmes(e.sender.value))).classes('w-1/3')
            with ui.row().classes('justify-end items-center mb-4 w-1/2'):
                ui.button('Atualizar Lista', on_click=lambda: setattr(tabela, 'rows', carregar_filmes())).classes('mb-4 ml-2').props('color="primary"')
                ui.button('Adicionar Filme', on_click=lambda: ui.navigate.to('/form')).classes('mb-4 ml-2').props('color="accent"')
        
        tabela = ui.table(
            columns=columns,
            rows=carregar_filmes(),
            row_key='id'
        ).classes('w-full')
        
        tabela.add_slot('body-cell-acoes', '''
            <q-td :props="props">
                <q-btn flat round color="primary" icon="edit" size="sm" 
                       @click.stop="$parent.$emit('edit', props.row)" />
                <q-btn flat round color="negative" icon="delete" size="sm"
                       @click.stop="$parent.$emit('delete', props.row)" />
            </q-td>
        ''')
        
        tabela.props('tbody-style="cursor: pointer"')
        tabela.on('rowClick', lambda e: ui.navigate.to(f'/film-info/{e.args[1]["id"]}'))
        
        tabela.on('edit', lambda e: editar_filme(e.args['id']))
        tabela.on('delete', lambda e: excluir_filme(e.args['id']))