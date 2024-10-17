# API de Catálogo de Produtos

Uma API RESTful para gerenciar um catálogo de produtos, desenvolvida com Python e Flask.

## Funcionalidades

- Criar, ler, atualizar e deletar produtos (CRUD)
- Listar produtos com paginação
- Filtrar produtos por categoria e faixa de preço

## Tecnologias Utilizadas

- Python
- Flask
- SQLAlchemy
- Marshmallow

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/api-catalogo-produtos.git
   cd api-catalogo-produtos
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```
   python main.py
   ```

## Uso

A API estará disponível em `http://localhost:5000`. Use as seguintes rotas:

- POST /produtos: Criar um novo produto
- GET /produtos: Listar produtos (com opções de paginação e filtragem)
- GET /produtos/{id}: Obter detalhes de um produto específico
- PUT /produtos/{id}: Atualizar um produto
- DELETE /produtos/{id}: Deletar um produto

## Exemplos de Requisições

### Criar um produto
 ```
bash
curl -X POST -H "Content-Type: application/json" -d '{
  "nome": "Cadeira de Escritório",
  "descricao": "Cadeira ergonômica para escritório",
  "preco": 299.99,
  "quantidade_estoque": 50,
  "categoria": "Móveis"
}' http://localhost:5000/produtos
 ```

### Listar produtos com filtro e paginação
```
bash
curl "http://localhost:5000/produtos?categoria=Móveis&preco_min=100&preco_max=500&page=1&per_page=10"
```



