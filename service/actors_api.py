import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))
TOKEN = os.environ["TMDB_TOKEN"]

TMDB_BEARER_TOKEN = f"{TOKEN}"
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'pessoas_cache.json')
MASTER_DATABASE_FILE = os.path.join(os.path.dirname(__file__), 'pessoas_master_db.json')

def load_master_database():
    if not os.path.exists(MASTER_DATABASE_FILE):
        print("Banco de pessoas não encontrado. Será criado na primeira execução.")
        return None
        
    try:
        with open(MASTER_DATABASE_FILE, 'r', encoding='utf-8') as f:
            master_data = json.load(f)
        
        pessoas = master_data.get('pessoas', [])
        criado_em = master_data.get('criado_em', 'Desconhecido')
        total_pessoas = len(pessoas)
        return pessoas
        
    except Exception as e:
        print(f"Erro ao ler banco de pessoas: {e}")
        return None

def save_master_database(pessoas):
    try:
        master_data = {
            'criado_em': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'versao': '1.0',
            'total_pessoas': len(pessoas),
            'fonte': 'TMDb API - 500 páginas',
            'pessoas': pessoas
        }
        
        with open(MASTER_DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(master_data, f, ensure_ascii=False, indent=2)
        return True
        
    except Exception as e:
        print(f"Erro ao salvar banco de pessoas: {e}")
        return False

def buscar_pessoa_especifica(nome_pessoa):
    try:
        if not nome_pessoa or len(nome_pessoa.strip()) < 2:
            return None
            
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
        }
        
        url = f"{TMDB_BASE_URL}/search/person?query={nome_pessoa.strip()}&language=pt-BR"
        resposta = requests.get(url, headers=headers, timeout=8)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            resultados = dados.get('results', [])
            
            if resultados:
                pessoa = resultados[0]  
                return {
                    'tmdb_id': pessoa.get('id'),
                    'nome': pessoa.get('name'),
                    'foto_url': f"https://image.tmdb.org/t/p/w185{pessoa.get('profile_path')}" if pessoa.get('profile_path') else None
                }
        
        return None
        
    except Exception as e:
        print(f"Erro ao buscar pessoa específica: {e}")
        return None

def obter_pessoas_cinema():
    try:
        pessoas_master = load_master_database()
        if pessoas_master:
            return pessoas_master
        else:
            print("Banco de pessoas não encontrado, retornando lista vazia")
            return []
            
    except Exception as e:
        print(f"Erro ao obter pessoas: {e}")
        return []

def buscar_pessoa_no_master(nome_pessoa):

    try:
        if not nome_pessoa or len(nome_pessoa.strip()) < 2:
            return None
        
        pessoas_master = load_master_database()
        if not pessoas_master:
            return None
        
        nome_busca = nome_pessoa.strip()
        
        for pessoa in pessoas_master:
            if pessoa.get('nome', '').lower() == nome_busca.lower():
                return pessoa
        
        for pessoa in pessoas_master:
            if nome_busca.lower() in pessoa.get('nome', '').lower():
                return pessoa
        
        return None
        
    except Exception as e:
        print(f"Erro ao buscar pessoa no master: {e}")
        return None

def filtrar_pessoas_por_nome(termo_busca, limite=50):

    try:
        if not termo_busca or len(termo_busca.strip()) < 2:
            return []
        
        pessoas_master = load_master_database()
        if not pessoas_master:
            return []
        
        termo = termo_busca.lower().strip()
        pessoas_filtradas = []
        
        for pessoa in pessoas_master:
            nome = pessoa.get('nome', '').lower()
            if termo in nome:
                pessoas_filtradas.append(pessoa)
                if len(pessoas_filtradas) >= limite:
                    break
        
        return pessoas_filtradas
        
    except Exception as e:
        print(f"Erro ao filtrar pessoas: {e}")
        return []
def criar_banco_master_completo():

    print("=== CRIANDO BANCO DE PESSOAS ===")
    print("Esta operação pode demorar alguns minutos...")
    
    if not TMDB_BEARER_TOKEN or TMDB_BEARER_TOKEN == 'SEU_BEARER_TOKEN_AQUI':
        print("ERRO: Bearer Token da API TMDb não configurado")
        return False
    
    pessoas = []
    pessoas_ids = set() 
    
    try:
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_BEARER_TOKEN}"
        }
               
        max_paginas = 500
        
        for page in range(1, max_paginas + 1):
            try:
                url = f"{TMDB_BASE_URL}/person/popular?language=pt-BR&page={page}"
                resposta = requests.get(url, headers=headers, timeout=15)
                
                if resposta.status_code == 200:
                    dados = resposta.json()
                    for pessoa in dados.get('results', []):
                        nome = pessoa.get('name')
                        tmdb_id = pessoa.get('id')
                        
                        if nome and len(nome) > 1 and tmdb_id and tmdb_id not in pessoas_ids:
                            pessoas.append({
                                'tmdb_id': tmdb_id,
                                'nome': nome,
                                'foto_url': f"https://image.tmdb.org/t/p/w185{pessoa.get('profile_path')}" if pessoa.get('profile_path') else None
                            })
                            pessoas_ids.add(tmdb_id)
                
                elif resposta.status_code == 429: 
                    print(f"Rate limit na página {page}, aguardando...")
                    import time
                    time.sleep(3) 
                    continue
                
                elif resposta.status_code == 404:
                    print(f"Página {page} não encontrada, interrompendo busca")
                    break
                
                else:
                    print(f"Erro na página {page}: Status {resposta.status_code}")
                    continue
                
                if page % 50 == 0:
                    print(f"Progresso: {page}/{max_paginas} páginas - {len(pessoas)} pessoas coletadas")
                    
            except requests.exceptions.Timeout:
                print(f"Timeout na página {page}, continuando...")
                continue
            except Exception as e:
                print(f"Erro na página {page}: {e}")
                continue
        
        
        try:
            br_url = f"{TMDB_BASE_URL}/discover/movie?with_origin_country=BR&sort_by=popularity.desc&language=pt-BR"
            
            for page in range(1, 11): 
                try:
                    resp = requests.get(f"{br_url}&page={page}", headers=headers, timeout=10)
                    
                    if resp.status_code == 200:
                        filmes = resp.json().get('results', [])
                        
                        for filme in filmes:
                            filme_id = filme.get('id')
                            if not filme_id:
                                continue
                            
                            credits_url = f"{TMDB_BASE_URL}/movie/{filme_id}/credits?language=pt-BR"
                            resp_credits = requests.get(credits_url, headers=headers, timeout=8)
                            
                            if resp_credits.status_code == 200:
                                credits = resp_credits.json()
                                
                                for pessoa in credits.get('cast', [])[:15]:
                                    nome = pessoa.get('name')
                                    tmdb_id = pessoa.get('id')
                                    
                                    if nome and tmdb_id and tmdb_id not in pessoas_ids:
                                        pessoas.append({
                                            'tmdb_id': tmdb_id,
                                            'nome': nome,
                                            'foto_url': f"https://image.tmdb.org/t/p/w185{pessoa.get('profile_path')}" if pessoa.get('profile_path') else None
                                        })
                                        pessoas_ids.add(tmdb_id)
                                
                                for pessoa in credits.get('crew', []):
                                    nome = pessoa.get('name')
                                    tmdb_id = pessoa.get('id')
                                    job = pessoa.get('job', '')
                                    
                                    if job in ['Director', 'Writer', 'Producer', 'Executive Producer', 'Screenplay', 'Cinematography'] and nome and tmdb_id and tmdb_id not in pessoas_ids:
                                        pessoas.append({
                                            'tmdb_id': tmdb_id,
                                            'nome': nome,
                                            'foto_url': f"https://image.tmdb.org/t/p/w185{pessoa.get('profile_path')}" if pessoa.get('profile_path') else None
                                        })
                                        pessoas_ids.add(tmdb_id)
                            
                            import time
                            time.sleep(0.1)
                            
                except Exception as e:
                    print(f"Erro ao processar filmes brasileiros página {page}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Erro geral ao buscar filmes brasileiros: {e}")
        
        try:
            popular_url = f"{TMDB_BASE_URL}/movie/popular?language=pt-BR"
            
            for page in range(1, 6):  
                try:
                    resp = requests.get(f"{popular_url}&page={page}", headers=headers, timeout=10)
                    
                    if resp.status_code == 200:
                        filmes = resp.json().get('results', [])
                        
                        for filme in filmes[:10]: 
                            filme_id = filme.get('id')
                            if not filme_id:
                                continue
                            
                            credits_url = f"{TMDB_BASE_URL}/movie/{filme_id}/credits?language=pt-BR"
                            resp_credits = requests.get(credits_url, headers=headers, timeout=8)
                            
                            if resp_credits.status_code == 200:
                                credits = resp_credits.json()
                                
                                for pessoa in credits.get('cast', [])[:10]:
                                    nome = pessoa.get('name')
                                    tmdb_id = pessoa.get('id')
                                    
                                    if nome and tmdb_id and tmdb_id not in pessoas_ids:
                                        pessoas.append({
                                            'tmdb_id': tmdb_id,
                                            'nome': nome,
                                            'foto_url': f"https://image.tmdb.org/t/p/w185{pessoa.get('profile_path')}" if pessoa.get('profile_path') else None
                                        })
                                        pessoas_ids.add(tmdb_id)
                                
                                for pessoa in credits.get('crew', []):
                                    if pessoa.get('job') in ['Director', 'Writer'] and pessoa.get('name') and pessoa.get('id') and pessoa.get('id') not in pessoas_ids:
                                        pessoas.append({
                                            'tmdb_id': pessoa.get('id'),
                                            'nome': pessoa.get('name'),
                                            'foto_url': f"https://image.tmdb.org/t/p/w185{pessoa.get('profile_path')}" if pessoa.get('profile_path') else None
                                        })
                                        pessoas_ids.add(pessoa.get('id'))
                            
                            time.sleep(0.1)
                            
                except Exception as e:
                    print(f"Erro ao processar filmes populares página {page}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Erro geral ao buscar filmes populares: {e}")
        
        
        pessoas_ordenadas = sorted(pessoas, key=lambda x: x['nome'])
                
        if save_master_database(pessoas_ordenadas):      
            return True
        else:
            print("Erro ao salvar banco de pessoas")
            return False
            
    except Exception as e:
        print(f"Erro geral ao criar banco de pessoas: {e}")
        return False
