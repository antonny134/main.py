import base64
import os
import math
import json
import mimetypes
from pathlib import Path
from typing import Literal
import webbrowser
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI()
PASTA_PROJETO = Path(__file__).parent
IMAGENS_PRODUTOS = {
    "1 imagem.jpg": PASTA_PROJETO / "1 imagem.jpg",
    "x tudão.jpg": PASTA_PROJETO / "x tudão.jpg",
    "bebida-suco-de-laranja.jpg": PASTA_PROJETO / "bebida-suco-de-laranja.jpg",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
FOTO = "https://commons.wikimedia.org/wiki/Special:FilePath/{}?width=600"


produtos = [
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
    if os.environ.get("VERCEL"):
        return  # disco somente leitura na Vercel: alterações ficam só em memória
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
    nome: str = Field(min_length=1)
    descricao: str = ""
    valor: float = Field(gt=0, allow_inf_nan=False)
    url_foto: str = ""
    categoria: Literal["lanche", "bebida"] = "lanche"


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
    if not novo.nome.strip():
        raise HTTPException(status_code=422, detail="O nome do produto é obrigatório.")
    proximo_id = max((p["id_produto"] for p in produtos + bebidas), default=0) + 1
    item = {
        "id_produto": proximo_id,
        "nome": novo.nome.strip(),
        "descricao": novo.descricao,
        "url_foto": novo.url_foto,
        "valor": novo.valor,
    }
    (bebidas if novo.categoria == "bebida" else produtos).append(item)
    salvar_banco()
    return item


@app.put("/produtos/{id_produto}")
def atualizar_produto(id_produto: int, atualizado: NovoProduto):
    if not atualizado.nome.strip():
        raise HTTPException(status_code=422, detail="O nome do produto é obrigatório.")
    for lista in (produtos, bebidas):
        for item in lista:
            if item["id_produto"] == id_produto:
                item.update(
                    nome=atualizado.nome.strip(),
                    descricao=atualizado.descricao,
                    url_foto=atualizado.url_foto,
                    valor=atualizado.valor,
                )
                if atualizado.categoria == "bebida" and lista is produtos:
                    produtos.remove(item)
                    bebidas.append(item)
                elif atualizado.categoria == "lanche" and lista is bebidas:
                    bebidas.remove(item)
                    produtos.append(item)
                salvar_banco()
                return item
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


@app.delete("/produtos/{id_produto}")
def apagar_produto(id_produto: int):
    for lista in (produtos, bebidas):
        for p in lista:
            if p["id_produto"] == id_produto:
                lista.remove(p)
                salvar_banco()
                return {"mensagem": "Produto removido."}
    raise HTTPException(status_code=404, detail="Produto não encontrado.")


@app.get("/config")
def iniciar_janela():
    # Importado aqui para a API rodar em servidores sem Tk (ex.: Vercel).
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk

    janela = tk.Tk()
    janela.title("Gerenciador de produtos")
    janela.geometry("900x560")
    janela.minsize(720, 420)

    cabecalho = tk.Frame(janela, padx=20, pady=16)
    cabecalho.pack(fill="x")
    tk.Label(
        cabecalho,
        text="Produtos do cardápio",
        font=("Arial", 20, "bold"),
    ).pack(side="left")
    tk.Button(
        cabecalho,
        text="Novo produto",
        command=lambda: abrir_formulario(),
    ).pack(side="right")

    filtros = tk.Frame(janela, padx=20)
    filtros.pack(fill="x", pady=(0, 10))
    tk.Label(filtros, text="Categoria:").pack(side="left", padx=(0, 8))
    filtro_categoria = tk.StringVar(value="Todos")
    seletor_categoria = ttk.Combobox(
        filtros,
        textvariable=filtro_categoria,
        values=("Todos", "Lanche", "Bebida"),
        state="readonly",
        width=14,
    )
    seletor_categoria.pack(side="left")

    quadro_lista = tk.Frame(janela, padx=20)
    quadro_lista.pack(fill="both", expand=True)
    colunas = ("categoria", "nome", "valor")
    tabela = ttk.Treeview(quadro_lista, columns=colunas, show="headings")
    tabela.heading("categoria", text="Categoria")
    tabela.heading("nome", text="Produto")
    tabela.heading("valor", text="Preço")
    tabela.column("categoria", width=120, anchor="center")
    tabela.column("nome", width=450)
    tabela.column("valor", width=130, anchor="e")
    barra = ttk.Scrollbar(quadro_lista, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=barra.set)
    tabela.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")

    status = tk.StringVar()
    tk.Label(janela, textvariable=status, anchor="w", padx=20, pady=8).pack(
        fill="x"
    )

    def obter_produto_selecionado():
        selecao = tabela.selection()
        if not selecao:
            messagebox.showinfo(
                "Selecione um produto",
                "Selecione um produto na lista para continuar.",
                parent=janela,
            )
            return None
        categoria, id_produto = selecao[0].split(":", 1)
        lista = bebidas if categoria == "bebida" else produtos
        return categoria, lista, next(
            item for item in lista if item["id_produto"] == int(id_produto)
        )

    def atualizar_lista(*_):
        categoria_filtrada = filtro_categoria.get().lower()
        tabela.delete(*tabela.get_children())
        itens = [
            ("lanche", item) for item in produtos
        ] + [("bebida", item) for item in bebidas]
        for categoria, item in itens:
            if categoria_filtrada not in ("todos", categoria):
                continue
            tabela.insert(
                "",
                "end",
                iid=f"{categoria}:{item['id_produto']}",
                values=(
                    "Bebida" if categoria == "bebida" else "Lanche",
                    item["nome"],
                    f"R$ {item['valor']:.2f}".replace(".", ","),
                ),
            )
        status.set(f"{len(tabela.get_children())} produto(s) exibido(s)")

    def abrir_formulario(produto_existente=None):
        formulario = tk.Toplevel(janela)
        formulario.title(
            "Editar produto" if produto_existente else "Novo produto"
        )
        formulario.transient(janela)
        formulario.resizable(False, False)
        formulario.grab_set()

        quadro = tk.Frame(formulario, padx=20, pady=18)
        quadro.pack(fill="both", expand=True)
        campos = {}
        valores = {
            "Nome": produto_existente["nome"] if produto_existente else "",
            "Descrição": produto_existente["descricao"] if produto_existente else "",
            "Preço (R$)": str(produto_existente["valor"]) if produto_existente else "",
            "URL da foto": produto_existente["url_foto"] if produto_existente else "",
        }
        foto = {"uri": None}
        if valores["URL da foto"].startswith("data:"):
            foto["uri"] = valores["URL da foto"]
            valores["URL da foto"] = "[arquivo] imagem atual"

        def escolher_imagem():
            caminho = filedialog.askopenfilename(
                parent=formulario,
                title="Escolher imagem",
                filetypes=[
                    ("Imagens", "*.png *.jpg *.jpeg *.gif *.webp"),
                    ("Todos os arquivos", "*.*"),
                ],
            )
            if not caminho:
                return
            arquivo = Path(caminho)
            tipo = mimetypes.guess_type(arquivo.name)[0] or ""
            if not tipo.startswith("image/"):
                messagebox.showerror(
                    "Arquivo inválido",
                    "Escolha um arquivo de imagem (png, jpg, gif ou webp).",
                    parent=formulario,
                )
                return
            try:
                dados = arquivo.read_bytes()
            except OSError as erro:
                messagebox.showerror(
                    "Não foi possível ler",
                    f"Não foi possível abrir a imagem:\n{erro}",
                    parent=formulario,
                )
                return
            if len(dados) > 3 * 1024 * 1024:
                messagebox.showerror(
                    "Imagem muito grande",
                    "Escolha uma imagem de até 3 MB.",
                    parent=formulario,
                )
                return
            foto["uri"] = f"data:{tipo};base64," + base64.b64encode(dados).decode("ascii")
            campos["URL da foto"].delete(0, "end")
            campos["URL da foto"].insert(0, f"[arquivo] {arquivo.name}")

        for linha, (rotulo, valor) in enumerate(valores.items()):
            tk.Label(quadro, text=rotulo).grid(
                row=linha, column=0, sticky="w", pady=6
            )
            if rotulo == "URL da foto":
                linha_foto = tk.Frame(quadro)
                linha_foto.grid(row=linha, column=1, sticky="ew", pady=6)
                campo = tk.Entry(linha_foto, width=34)
                campo.insert(0, valor)
                campo.pack(side="left", fill="x", expand=True)
                tk.Button(
                    linha_foto, text="Escolher arquivo…", command=escolher_imagem
                ).pack(side="left", padx=(6, 0))
            else:
                campo = tk.Entry(quadro, width=48)
                campo.insert(0, valor)
                campo.grid(row=linha, column=1, sticky="ew", pady=6)
            campos[rotulo] = campo

        tk.Label(quadro, text="Categoria").grid(
            row=len(valores), column=0, sticky="w", pady=6
        )
        categoria = tk.StringVar(
            value="Bebida" if produto_existente in bebidas else "Lanche"
        )
        ttk.Combobox(
            quadro,
            textvariable=categoria,
            values=("Lanche", "Bebida"),
            state="readonly",
            width=45,
        ).grid(row=len(valores), column=1, sticky="ew", pady=6)

        def salvar_formulario():
            nome = campos["Nome"].get().strip()
            descricao = campos["Descrição"].get().strip()
            url_foto = campos["URL da foto"].get().strip()
            if url_foto.startswith("[arquivo]") and foto["uri"]:
                url_foto = foto["uri"]
            try:
                valor = float(campos["Preço (R$)"].get().replace(",", "."))
                if not math.isfinite(valor) or valor <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Preço inválido",
                    "Informe um preço maior que zero.",
                    parent=formulario,
                )
                return
            if not nome:
                messagebox.showerror(
                    "Nome obrigatório",
                    "Informe o nome do produto.",
                    parent=formulario,
                )
                return

            nova_categoria = (
                "bebida" if categoria.get() == "Bebida" else "lanche"
            )
            novo_item = {
                "nome": nome,
                "descricao": descricao,
                "url_foto": url_foto,
                "valor": valor,
            }

            editando = produto_existente is not None
            if editando:
                categoria_antiga = (
                    "bebida" if produto_existente in bebidas else "lanche"
                )
                lista_antiga = bebidas if categoria_antiga == "bebida" else produtos
                posicao = lista_antiga.index(produto_existente)
                original = produto_existente.copy()
                lista_destino = bebidas if nova_categoria == "bebida" else produtos
                produto_existente.update(novo_item)
                if nova_categoria != categoria_antiga:
                    lista_antiga.pop(posicao)
                    lista_destino.append(produto_existente)
            else:
                proximo_id = max(
                    (item["id_produto"] for item in produtos + bebidas),
                    default=0,
                ) + 1
                produto_novo = {"id_produto": proximo_id, **novo_item}
                lista_destino = bebidas if nova_categoria == "bebida" else produtos
                lista_destino.append(produto_novo)

            try:
                salvar_banco()
            except OSError as erro:
                if editando:
                    if nova_categoria != categoria_antiga:
                        lista_destino.remove(produto_existente)
                        lista_antiga.insert(posicao, produto_existente)
                    produto_existente.clear()
                    produto_existente.update(original)
                else:
                    lista_destino.remove(produto_novo)
                messagebox.showerror(
                    "Não foi possível salvar",
                    f"O produto não foi salvo no banco de dados:\n{erro}",
                    parent=formulario,
                )
                return

            atualizar_lista()
            formulario.destroy()

        botoes = tk.Frame(quadro)
        botoes.grid(row=len(valores) + 1, column=0, columnspan=2, pady=(14, 0))
        tk.Button(botoes, text="Salvar", command=salvar_formulario).pack(
            side="left", padx=5
        )
        tk.Button(botoes, text="Cancelar", command=formulario.destroy).pack(
            side="left", padx=5
        )
        formulario.bind("<Return>", lambda _: salvar_formulario())
        campos["Nome"].focus_set()

    def editar_selecionado():
        selecionado = obter_produto_selecionado()
        if selecionado:
            abrir_formulario(selecionado[2])

    def excluir_selecionado():
        selecionado = obter_produto_selecionado()
        if not selecionado:
            return
        _, lista, item = selecionado
        if not messagebox.askyesno(
            "Excluir produto",
            f'Deseja excluir "{item["nome"]}"?',
            parent=janela,
        ):
            return
        posicao = lista.index(item)
        lista.pop(posicao)
        try:
            salvar_banco()
        except OSError as erro:
            lista.insert(posicao, item)
            messagebox.showerror(
                "Não foi possível salvar",
                f"O produto não foi excluído do banco de dados:\n{erro}",
                parent=janela,
            )
            return
        atualizar_lista()

    def abrir_cardapio():
        if not webbrowser.open("https://cardapio-iota-weld.vercel.app"):
            messagebox.showerror(
                "Não foi possível abrir",
                "O cardápio não pôde ser aberto no navegador.",
                parent=janela,
            )

    botoes = tk.Frame(janela, padx=20, pady=12)
    botoes.pack(fill="x")
    tk.Button(botoes, text="Configurar / trocar", command=editar_selecionado).pack(
        side="left", padx=(0, 8)
    )
    tk.Button(botoes, text="Excluir", command=excluir_selecionado).pack(
        side="left", padx=8
    )
    tk.Button(botoes, text="Acionar cardápio", command=abrir_cardapio).pack(
        side="right"
    )

    tabela.bind("<Double-1>", lambda _: editar_selecionado())
    seletor_categoria.bind("<<ComboboxSelected>>", atualizar_lista)
    atualizar_lista()
    janela.mainloop()


if __name__ == "__main__":
    iniciar_janela()