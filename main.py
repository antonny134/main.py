import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()
PASTA_PROJETO = Path(__file__).parent
IMAGENS_PRODUTOS = {
    "1 imagem.jpg": PASTA_PROJETO / "1 imagem.jpg",
    "x tudão.jpg": PASTA_PROJETO / "x tudão.jpg",
    "bebida-suco-de-laranja.jpg": PASTA_PROJETO / "bebida-suco-de-laranja.jpg",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cardapio-t8lz.vercel.app",
        "https://antonny134.github.io",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://cardapio-iota-weld.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
FOTO = "https://commons.wikimedia.org/wiki/Special:FilePath/{}?width=600"



produtos = [
    {
        "id_produto": 1,
        "nome": "X tudo",
        "descricao": "Feito com calabresa, salsicha e bacon.",
        "url_foto": "/imagens/1 imagem.jpg",
        "valor": 29.50,
    },
    {
        "id_produto": 2,
        "nome": "X TUDÂO",
        "descricao": "2 calabressa 1 mortadela ",
        "url_foto": "/imagens/x tudão.jpg",
        "valor": 30.50,
    },
    {
        "id_produto": 3,
        "nome": "X-Burger",
        "descricao": "Hambúrguer, queijo derretido e pão macio.",
        "url_foto": FOTO.format("Cheeseburger_on_a_plate.jpg"),
        "valor": 18.00,
    },
    {
        "id_produto": 4,
        "nome": "X-Salada",
        "descricao": "Hambúrguer, queijo, alface e tomate.",
        "url_foto": FOTO.format("A_homemade_hamburger.jpg"),
        "valor": 20.00,
    },
    {
        "id_produto": 5,
        "nome": "X-Bacon",
        "descricao": "Hambúrguer, queijo e bastante bacon crocante.",
        "url_foto": FOTO.format("NYC-Diner-Bacon-Cheeseburger.jpg"),
        "valor": 24.00,
    },
    {
        "id_produto": 6,
        "nome": "X-Frango",
        "descricao": "Filé de frango empanado, queijo e salada.",
        "url_foto": FOTO.format("Chicken_Burger.jpg"),
        "valor": 22.00,
    },
    {
        "id_produto": 7,
        "nome": "Cachorro-quente",
        "descricao": "Pão, salsicha, molho e batata palha.",
        "url_foto": FOTO.format("Hot_dog_with_homemade_hot_dog_bun.jpg"),
        "valor": 15.00,
    },
    {
        "id_produto": 8,
        "nome": "Hot Dog Completo",
        "descricao": "Salsicha com vinagrete, milho e todos os molhos.",
        "url_foto": FOTO.format("Chicago-style_hot_dog_2.jpg"),
        "valor": 19.00,
    },
    {
        "id_produto": 9,
        "nome": "Misto Quente",
        "descricao": "Presunto e queijo derretido no pão na chapa.",
        "url_foto": FOTO.format("Grilled_ham_and_cheese_sandwich.jpg"),
        "valor": 12.00,
    },
    {
        "id_produto": 10,
        "nome": "Batata Frita",
        "descricao": "Porção de batata frita sequinha e crocante.",
        "url_foto": FOTO.format("Fresh_french_fries.jpg"),
        "valor": 16.00,
    },
    {
        "id_produto": 11,
        "nome": "Coxinha",
        "descricao": "Massa macia recheada com frango desfiado.",
        "url_foto": FOTO.format("Coxinha.jpg"),
        "valor": 7.00,
    },
    {
        "id_produto": 12,
        "nome": "Pastel",
        "descricao": "Pastel frito na hora, bem sequinho.",
        "url_foto": FOTO.format("Brazilian_pastel.jpg"),
        "valor": 9.00,
    },
]

bebidas = [
    {
        "id_produto": 13,
        "nome": "Suco de Laranja",
        "descricao": "Suco de laranja natural.",
        "url_foto": "/imagens/bebida-suco-de-laranja.jpg",
        "valor": 3.50,
    },
    {
        "id_produto": 14,
        "nome": "Suco de Manga",
        "descricao": "Suco de manga natural, bem gelado.",
        "url_foto": FOTO.format("Glass_of_Mango_Juice.jpg"),
        "valor": 5.00,
    },
    {
        "id_produto": 15,
        "nome": "Limonada",
        "descricao": "Limonada refrescante feita na hora.",
        "url_foto": FOTO.format("Mug_of_Lemonade.jpg"),
        "valor": 4.50,
    },
    {
        "id_produto": 16,
        "nome": "Chá Gelado",
        "descricao": "Chá gelado com gelo, para matar a sede.",
        "url_foto": FOTO.format("Glass_of_Iced_Tea.jpg"),
        "valor": 4.00,
    },
    {
        "id_produto": 17,
        "nome": "Água de Coco",
        "descricao": "Água de coco geladinha.",
        "url_foto": FOTO.format("Fresh_coconut_water.jpg"),
        "valor": 6.00,
    },
    {
        "id_produto": 18,
        "nome": "Café",
        "descricao": "Café passado na hora.",
        "url_foto": FOTO.format("A_small_cup_of_coffee.JPG"),
        "valor": 3.00,
    },
    {
        "id_produto": 19,
        "nome": "Milkshake de Morango",
        "descricao": "Milkshake cremoso de morango.",
        "url_foto": FOTO.format("Strawberry_milkshake.jpg"),
        "valor": 12.00,
    },
    {
        "id_produto": 20,
        "nome": "Água Mineral",
        "descricao": "Copo de água mineral gelada.",
        "url_foto": FOTO.format("Glass-of-water.jpg"),
        "valor": 2.50,
    },
    {
        "id_produto": 21,
        "nome": "Refrigerante de Cola",
        "descricao": "Refrigerante de cola gelado, com gelo.",
        "url_foto": FOTO.format("Glass_of_Cola.jpg"),
        "valor": 5.00,
    },
    {
        "id_produto": 22,
        "nome": "Vitamina de Banana com Morango",
        "descricao": "Vitamina batida com banana e morango.",
        "url_foto": FOTO.format("Banana_and_strawberry_smoothie.jpg"),
        "valor": 8.00,
    },
    {
        "id_produto": 23,
        "nome": "Chá de Hortelã",
        "descricao": "Chá quente de hortelã.",
        "url_foto": FOTO.format("Mint_tea_in_a_glass_(35948546).jpg"),
        "valor": 4.00,
    },
]

# ---------- Persistência em arquivo ----------
ARQUIVO_BANCO = PASTA_PROJETO / "banco.json"


def salvar_banco():
    ARQUIVO_BANCO.write_text(
        json.dumps({"produtos": produtos, "bebidas": bebidas}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def carregar_banco():
    if ARQUIVO_BANCO.is_file():
        dados = json.loads(ARQUIVO_BANCO.read_text(encoding="utf-8"))
        produtos[:] = dados["produtos"]  # [:] troca o conteúdo mantendo a mesma lista
        bebidas[:] = dados["bebidas"]


carregar_banco()


class NovoProduto(BaseModel):
    nome: str
    descricao: str = ""
    valor: float
    url_foto: str = ""
    categoria: str  # "lanche" ou "bebida"


# ---------- Rotas ----------
@app.get("/")
def inicio():
    return FileResponse(PASTA_PROJETO / "index.html")


@app.get("/imagens/{nome_arquivo}")
def imagem_produto(nome_arquivo: str):
    caminho = IMAGENS_PRODUTOS.get(nome_arquivo)
    if caminho is None or not caminho.is_file():
        raise HTTPException(status_code=404, detail="Imagem não encontrada.")
    return FileResponse(caminho)


@app.get("/produtos-lanche")
@app.get("/produtos")
def lista_produto():
    return produtos


@app.get("/produto-suco")
@app.get("/suco")
def lista_suco():
    return bebidas


@app.post("/produtos", status_code=201)
def adicionar_produto(novo: NovoProduto):
    proximo_id = max((p["id_produto"] for p in produtos + bebidas), default=0) + 1
    item = {
        "id_produto": proximo_id,
        "nome": novo.nome,
        "descricao": novo.descricao,
        "url_foto": novo.url_foto,
        "valor": novo.valor,
    }
    (bebidas if novo.categoria == "bebida" else produtos).append(item)
    salvar_banco()
    return item


@app.delete("/produtos/{id_produto}")
def apagar_produto(id_produto: int):
    for lista in (produtos, bebidas):
        for p in lista:
            if p["id_produto"] == id_produto:
                lista.remove(p)
                salvar_banco()
                return {"mensagem": "Produto removido."}
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


@app.get("/atualizar")
def colocar_produtos():
    return FileResponse(PASTA_PROJETO / "funcionario.html")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)