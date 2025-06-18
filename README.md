# CRUD de Filmes

Um sistema CRUD (Create, Read, Update, Delete) para gerenciamento de filmes desenvolvido em Python usando NiceGUI para a interface web, seguindo o padrão MVC (Model-View-Controller).

## Para executar o projeto

O arquivo principal do projeto é o **app.py**, que define as rotas da aplicação e configurações globais.
Logo, para executar: 
```bash
python app.py
```
**movies.db** Banco de Dados SQLite que armazena os filmes.

O projeto possui também um "banco master" com atores cadastrados no arquivo **pessoas_master_db.json**. Ao executar pela primeira vez a aplicação, ele pode demorar pois cria/atualiza esse arquivo, para que não execute essa criação/atualização, comentar as seguintes linhas no arquivo principal:
``` 
    master_db_path = os.path.join('service', 'pessoas_master_db.json')
    if not os.path.exists(master_db_path):
        print("Banco de atores não encontrado. Criando...")
        criar_banco_master_completo()
```

## Estrutura do projeto

O projeto está dividido em camadas:
- models: Camada de dados que contém as classes filme e pessoa.
- service: Camada de negócio e integração, contendo as operações CRUD, Modelos SQLAlchemy para ORM e integração com APIs.
- views: Camada de apresentação, contendo as páginas listadas no arquivo principal e componentes reutilizáveis.