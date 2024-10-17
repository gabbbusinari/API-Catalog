from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

class ProdutoSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    descricao = fields.Str()
    preco = fields.Float(required=True)
    quantidade_estoque = fields.Int(required=True)
    categoria = fields.Str(required=True)

produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)

@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.json
    novo_produto = Produto(
        nome=dados['nome'],
        descricao=dados.get('descricao'),
        preco=dados['preco'],
        quantidade_estoque=dados['quantidade_estoque'],
        categoria=dados['categoria']
    )
    db.session.add(novo_produto)
    db.session.commit()
    return produto_schema.jsonify(novo_produto), 201

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    # Parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Parâmetros de filtragem
    categoria = request.args.get('categoria')
    preco_min = request.args.get('preco_min', type=float)
    preco_max = request.args.get('preco_max', type=float)
    
    # Iniciar a query
    query = Produto.query
    
    # Aplicar filtros
    if categoria:
        query = query.filter(Produto.categoria == categoria)
    if preco_min is not None:
        query = query.filter(Produto.preco >= preco_min)
    if preco_max is not None:
        query = query.filter(Produto.preco <= preco_max)
    
    # Aplicar paginação
    paginated_produtos = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Preparar resposta
    result = {
        'produtos': produtos_schema.dump(paginated_produtos.items),
        'total': paginated_produtos.total,
        'pages': paginated_produtos.pages,
        'page': page,
        'per_page': per_page
    }
    
    return jsonify(result)

@app.route('/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    produto = Produto.query.get_or_404(id)
    return produto_schema.jsonify(produto)

@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)
    dados = request.json
    produto.nome = dados.get('nome', produto.nome)
    produto.descricao = dados.get('descricao', produto.descricao)
    produto.preco = dados.get('preco', produto.preco)
    produto.quantidade_estoque = dados.get('quantidade_estoque', produto.quantidade_estoque)
    produto.categoria = dados.get('categoria', produto.categoria)
    db.session.commit()
    return produto_schema.jsonify(produto)

@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
