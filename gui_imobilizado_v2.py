# =============================================================================
# SISTEMA DE GESTÃO DE IMOBILIZADO ESCOLAR — V2 (Designer Maintenance Tracker)
# Ficheiro: gui_imobilizado_v2.py
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import hashlib
from datetime import datetime

# =============================================================================
# DADOS BASE
# =============================================================================

CATEGORIAS = [
    "Mobiliário", "Equipamento Informático", "Equipamento Laboratorial",
    "Material Didático", "Material Administrativo", "Outro"
]
ESTADOS = ["Novo", "Bom", "Danificado", "Em Reparação", "Inutilizado"]
LOCALIZACOES = [
    "Sala 1", "Sala 2", "Sala 3", "Sala 4", "Sala 5",
    "Sala 6", "Sala 7", "Sala 8", "Sala 9", "Sala 10",
    "Laboratório", "Biblioteca", "Secretaria",
    "Sala de Professores", "Armazém", "Direção", "Refeitório"
]
TIPOS_BENS = {
    "Mesa Aluno":        {"categoria": "Mobiliário",               "radical": "MSA"},
    "Mesa Professor":    {"categoria": "Mobiliário",               "radical": "MSP"},
    "Cadeira Aluno":     {"categoria": "Mobiliário",               "radical": "CAA"},
    "Cadeira Professor": {"categoria": "Mobiliário",               "radical": "CAP"},
    "Quadro Branco":     {"categoria": "Material Didático",        "radical": "QBR"},
    "Computador":        {"categoria": "Equipamento Informático",  "radical": "COM"},
    "Projetor":          {"categoria": "Equipamento Informático",  "radical": "PRJ"},
    "Armário":           {"categoria": "Material Administrativo",  "radical": "ARM"},
    "Livro":             {"categoria": "Material Didático",        "radical": "LIV"},
    "Microscópio":       {"categoria": "Equipamento Laboratorial", "radical": "MIC"},
    "Impressora":        {"categoria": "Equipamento Informático",  "radical": "IMP"},
    "Outro":             {"categoria": "Outro",                    "radical": "OUT"},
}
FICHEIRO_DADOS = "inventario.txt"
FICHEIRO_UTILIZADORES = "utilizadores.txt"
FICHEIRO_HISTORICO = "historico.txt"

# =============================================================================
# PALETA — Dark Theme (inspirado no Maintenance Tracker)
# =============================================================================

BG         = "#0d1117"   # fundo geral
BG2        = "#161b22"   # painel / header
BG3        = "#1c2230"   # cards
BG4        = "#21293a"   # card hover / input
BORDA      = "#30363d"   # bordas suaves
BORDA2     = "#3a4555"   # bordas médias
TX         = "#e6edf3"   # texto principal
TX2        = "#8b949e"   # texto secundário
TX3        = "#6e7681"   # texto muito suave

# Accent colors
VERDE      = "#3fb950"   # Novo / sucesso
VERDE_BG   = "#0f3020"
AZUL       = "#58a6ff"   # Bom / informação
AZUL_BG    = "#0d2a4a"
AMARELO    = "#d29922"   # Em Reparação / aviso
AMARELO_BG = "#2e2208"
VERMELHO   = "#f85149"   # Danificado / erro
VERMELHO_BG= "#2e0a09"
CINZA      = "#6e7681"   # Inutilizado
CINZA_BG   = "#161b22"
LARANJA    = "#e3b341"   # Upcoming

# Accent principal (botões primários)
ACCENT     = "#238636"
ACCENT_H   = "#2ea043"
ACCENT2    = "#1f6feb"
ACCENT2_H  = "#388bfd"

# Estado -> (text_color, bg_color, dot_color)
ESTADO_STYLE = {
    "Novo":         (VERDE,    VERDE_BG,    VERDE),
    "Bom":          (AZUL,     AZUL_BG,     AZUL),
    "Danificado":   (VERMELHO, VERMELHO_BG, VERMELHO),
    "Em Reparação": (AMARELO,  AMARELO_BG,  AMARELO),
    "Inutilizado":  (CINZA,    CINZA_BG,    CINZA),
}

# Ícone unicode por categoria
CAT_ICON = {
    "Mobiliário":               "🪑",
    "Equipamento Informático":  "💻",
    "Equipamento Laboratorial": "🔬",
    "Material Didático":        "📚",
    "Material Administrativo":  "🗂",
    "Outro":                    "📦",
}

# =============================================================================
# LÓGICA DE NEGÓCIO
# =============================================================================

inventario = []

def validar_formato_id(id_bem):
    id_bem = id_bem.strip().upper()
    if len(id_bem) != 7: return False
    if not id_bem[:3].isalpha(): return False
    if not id_bem[3:].isdigit(): return False
    return True

def criar_bem(id_bem, nome, categoria, estado, localizacao):
    return {"id": id_bem.strip().upper(), "nome": nome.strip(),
            "categoria": categoria.strip(), "estado": estado.strip(),
            "localizacao": localizacao.strip()}

def bem_para_linha(b):
    return f"{b['id']};{b['nome']};{b['categoria']};{b['estado']};{b['localizacao']}\n"

def linha_para_bem(linha):
    linha = linha.strip()
    if not linha: return None
    p = linha.split(";")
    if len(p) != 5: return None
    id_b, nome, cat, est, loc = [x.strip() for x in p]
    if not id_b or not nome: return None
    return criar_bem(id_b, nome, cat, est, loc)

def carregar_dados():
    global inventario
    inventario = []
    try:
        with open(FICHEIRO_DADOS, "r", encoding="utf-8") as f:
            for l in f:
                b = linha_para_bem(l)
                if b: inventario.append(b)
        return len(inventario)
    except FileNotFoundError:
        return 0

def guardar_dados():
    with open(FICHEIRO_DADOS, "w", encoding="utf-8") as f:
        for b in inventario:
            f.write(bem_para_linha(b))

def _gerar_novo_id(radical):
    nums = [int(b["id"][len(radical):]) for b in inventario
            if b["id"].startswith(radical) and b["id"][len(radical):].isdigit()]
    prox = max(nums) + 1 if nums else 1
    return f"{radical}{str(prox).zfill(4)}"

def obter_radical(nome):
    if nome in TIPOS_BENS: return TIPOS_BENS[nome]["radical"]
    letras = "".join(c for c in nome.upper() if c.isalpha())
    return letras[:3] if len(letras) >= 3 else "BEM"

def obter_categoria(nome):
    if nome in TIPOS_BENS: return TIPOS_BENS[nome]["categoria"]
    return "Outro"

def _id_existe(id_bem):
    return any(b["id"] == id_bem for b in inventario)

# =============================================================================
# GESTÃO DE UTILIZADORES
# =============================================================================

def _hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

def carregar_utilizadores():
    utilizadores = {}
    try:
        with open(FICHEIRO_UTILIZADORES, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or ":" not in linha:
                    continue
                nome, senha_hash = linha.split(":", 1)
                utilizadores[nome.strip()] = senha_hash.strip()
    except FileNotFoundError:
        pass
    return utilizadores

def guardar_utilizadores(utilizadores):
    with open(FICHEIRO_UTILIZADORES, "w", encoding="utf-8") as f:
        for nome, senha_hash in utilizadores.items():
            f.write(f"{nome}:{senha_hash}\n")

def registar_acao(utilizador, acao, id_bem, detalhe=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"{ts};{utilizador};{acao};{id_bem};{detalhe}\n"
    with open(FICHEIRO_HISTORICO, "a", encoding="utf-8") as f:
        f.write(linha)

def carregar_historico():
    entradas = []
    try:
        with open(FICHEIRO_HISTORICO, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split(";", 4)
                if len(partes) == 5:
                    entradas.append({
                        "ts": partes[0], "utilizador": partes[1],
                        "acao": partes[2], "id_bem": partes[3], "detalhe": partes[4]
                    })
    except FileNotFoundError:
        pass
    return entradas

def contar_por_campo(campo):
    r = {}
    for b in inventario:
        v = b.get(campo, "—") or "—"
        r[v] = r.get(v, 0) + 1
    return r

# =============================================================================
# HELPERS DE WIDGET
# =============================================================================

def btn_primary(parent, text, cmd, **kw):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=ACCENT, fg="#ffffff", activebackground=ACCENT_H,
                  activeforeground="#ffffff", relief="flat", bd=0,
                  font=("Segoe UI", 9, "bold"), cursor="hand2",
                  pady=7, padx=14, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=ACCENT_H))
    b.bind("<Leave>", lambda e: b.config(bg=ACCENT))
    return b

def btn_secondary(parent, text, cmd, **kw):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=ACCENT2, fg="#ffffff", activebackground=ACCENT2_H,
                  activeforeground="#ffffff", relief="flat", bd=0,
                  font=("Segoe UI", 9, "bold"), cursor="hand2",
                  pady=7, padx=14, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=ACCENT2_H))
    b.bind("<Leave>", lambda e: b.config(bg=ACCENT2))
    return b

def btn_ghost(parent, text, cmd, ativo=False, **kw):
    cor_bg = BG4 if ativo else BG2
    cor_tx = TX if ativo else TX2
    b = tk.Button(parent, text=text, command=cmd,
                  bg=cor_bg, fg=cor_tx, activebackground=BG4,
                  activeforeground=TX, relief="flat", bd=0,
                  font=("Segoe UI", 9), cursor="hand2",
                  pady=5, padx=12, **kw)
    return b

def dark_entry(parent, var=None, w=20, **kw):
    e = tk.Entry(parent, textvariable=var, width=w,
                 bg=BG4, fg=TX, insertbackground=TX,
                 relief="flat", bd=0, font=("Segoe UI", 10),
                 highlightthickness=1,
                 highlightbackground=BORDA2,
                 highlightcolor=AZUL, **kw)
    return e

def dark_combo(parent, values, var=None, w=24):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("MT.TCombobox",
        fieldbackground=BG4, background=BG4,
        foreground=TX, arrowcolor=TX2,
        bordercolor=BORDA2, selectbackground=BG4,
        selectforeground=TX)
    cb = ttk.Combobox(parent, values=values, textvariable=var,
                      width=w, style="MT.TCombobox",
                      state="readonly", font=("Segoe UI", 10))
    return cb

def label(parent, text, size=10, cor=TX, bold=False, **kw):
    return tk.Label(parent, text=text, bg=parent["bg"], fg=cor,
                    font=("Segoe UI", size, "bold" if bold else "normal"), **kw)

def separador(parent):
    tk.Frame(parent, bg=BORDA, height=1).pack(fill="x", padx=0, pady=0)

# =============================================================================
# JANELA DE AUTENTICAÇÃO
# =============================================================================

class JanelaAuth(tk.Tk):
    def __init__(self):
        super().__init__()
        self.autenticado = False
        self.utilizador = None
        self.title("Gestão de Imobilizado Escolar — Autenticação")
        self.configure(bg=BG)
        self.resizable(False, False)

        self._utilizadores = carregar_utilizadores()
        self._modo = "registar" if not self._utilizadores else "login"

        if self._modo == "registar":
            self.geometry("420x460")
        else:
            self.geometry("420x370")

        self._construir()

    def _construir(self):
        # Header idêntico ao da App principal
        hdr = tk.Frame(self, bg=BG2)
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=BORDA, height=1).pack(fill="x", side="bottom")
        inner = tk.Frame(hdr, bg=BG2)
        inner.pack(padx=24, pady=14)
        tk.Label(inner, text="⚙", bg=BG2, fg=VERDE,
                 font=("Segoe UI", 22)).pack(side="left", padx=(0, 10))
        txt_fr = tk.Frame(inner, bg=BG2)
        txt_fr.pack(side="left")
        tk.Label(txt_fr, text="Imobilizado  Escolar", bg=BG2, fg=TX,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(txt_fr, text="MONITORIZAR  •  GERIR  •  MANTER",
                 bg=BG2, fg=TX3, font=("Segoe UI", 8)).pack(anchor="w")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=40, pady=24)

        if self._modo == "registar":
            self._construir_registo(body)
        else:
            self._construir_login(body)

    def _construir_registo(self, parent):
        tk.Label(parent, text="Criar Conta de Utilizador", bg=BG, fg=TX,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Label(parent,
                 text="Não existe nenhum utilizador. Crie uma conta para continuar.",
                 bg=BG, fg=TX3, font=("Segoe UI", 9),
                 wraplength=320, justify="left").pack(anchor="w", pady=(0, 18))

        var_user = tk.StringVar()
        var_pass = tk.StringVar()
        var_pass2 = tk.StringVar()

        tk.Label(parent, text="Nome de utilizador:", bg=BG, fg=TX2,
                 font=("Segoe UI", 9)).pack(anchor="w")
        e_user = dark_entry(parent, var_user, w=30)
        e_user.pack(fill="x", pady=(2, 12))

        tk.Label(parent, text="Senha:", bg=BG, fg=TX2,
                 font=("Segoe UI", 9)).pack(anchor="w")
        e_pass = dark_entry(parent, var_pass, w=30)
        e_pass.config(show="●")
        e_pass.pack(fill="x", pady=(2, 12))

        tk.Label(parent, text="Confirmar senha:", bg=BG, fg=TX2,
                 font=("Segoe UI", 9)).pack(anchor="w")
        e_pass2 = dark_entry(parent, var_pass2, w=30)
        e_pass2.config(show="●")
        e_pass2.pack(fill="x", pady=(2, 18))

        lbl_erro = tk.Label(parent, text="", bg=BG, fg=VERMELHO,
                            font=("Segoe UI", 9))
        lbl_erro.pack(anchor="w", pady=(0, 8))

        def criar():
            user = var_user.get().strip()
            senha = var_pass.get()
            senha2 = var_pass2.get()
            if not user:
                lbl_erro.config(text="O nome de utilizador é obrigatório.")
                return
            if len(user) < 3:
                lbl_erro.config(text="O nome deve ter pelo menos 3 caracteres.")
                return
            if not senha:
                lbl_erro.config(text="A senha é obrigatória.")
                return
            if len(senha) < 4:
                lbl_erro.config(text="A senha deve ter pelo menos 4 caracteres.")
                return
            if senha != senha2:
                lbl_erro.config(text="As senhas não coincidem.")
                return
            self._utilizadores[user] = _hash_senha(senha)
            guardar_utilizadores(self._utilizadores)
            self.autenticado = True
            self.utilizador = user
            self.destroy()

        btn_primary(parent, "Criar Conta e Entrar", criar).pack(fill="x")
        e_user.focus_set()
        self.bind("<Return>", lambda e: criar())

    def _construir_login(self, parent):
        tk.Label(parent, text="Iniciar Sessão", bg=BG, fg=TX,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        tk.Label(parent,
                 text="Introduza as suas credenciais para aceder ao sistema.",
                 bg=BG, fg=TX3, font=("Segoe UI", 9),
                 wraplength=320, justify="left").pack(anchor="w", pady=(0, 18))

        var_user = tk.StringVar()
        var_pass = tk.StringVar()

        tk.Label(parent, text="Nome de utilizador:", bg=BG, fg=TX2,
                 font=("Segoe UI", 9)).pack(anchor="w")
        e_user = dark_entry(parent, var_user, w=30)
        e_user.pack(fill="x", pady=(2, 12))

        tk.Label(parent, text="Senha:", bg=BG, fg=TX2,
                 font=("Segoe UI", 9)).pack(anchor="w")
        e_pass = dark_entry(parent, var_pass, w=30)
        e_pass.config(show="●")
        e_pass.pack(fill="x", pady=(2, 18))

        lbl_erro = tk.Label(parent, text="", bg=BG, fg=VERMELHO,
                            font=("Segoe UI", 9))
        lbl_erro.pack(anchor="w", pady=(0, 8))

        def entrar():
            user = var_user.get().strip()
            senha = var_pass.get()
            if not user or not senha:
                lbl_erro.config(text="Preencha todos os campos.")
                return
            senha_hash = self._utilizadores.get(user)
            if senha_hash and senha_hash == _hash_senha(senha):
                self.autenticado = True
                self.utilizador = user
                self.destroy()
            else:
                lbl_erro.config(text="Utilizador ou senha incorretos.")
                var_pass.set("")
                e_pass.focus_set()

        btn_primary(parent, "Entrar", entrar).pack(fill="x")
        e_user.focus_set()
        self.bind("<Return>", lambda e: entrar())

# =============================================================================
# JANELA PRINCIPAL
# =============================================================================

class App(tk.Tk):
    def __init__(self, utilizador=""):
        super().__init__()
        self._utilizador = utilizador
        self.title("Gestão de Imobilizado Escolar")
        self.geometry("1180x740")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)

        self._filtro_ativo = "Todos"
        self._pesq_var = tk.StringVar()
        self._pesq_var.trace_add("write", lambda *_: self._refresh_cards())

        n = carregar_dados()
        self._construir()
        self._refresh_stats()
        self._refresh_cards()
        self._set_status(f"✔  {n} bem(ns) carregado(s)." if n else "Inventário vazio — comece por registar um bem.")
        self.protocol("WM_DELETE_WINDOW", self._fechar)

    # ─────────────────────────────────────────────────────────────────────────
    # CONSTRUÇÃO
    # ─────────────────────────────────────────────────────────────────────────

    def _construir(self):
        self._build_header()
        self._build_body()

    def _build_header(self):
        hdr = tk.Frame(self, bg=BG2, pady=0)
        hdr.pack(fill="x")
        tk.Frame(hdr, bg=BORDA, height=1).pack(fill="x", side="bottom")

        inner = tk.Frame(hdr, bg=BG2)
        inner.pack(fill="x", padx=24, pady=14)

        # Logo + título
        logo_fr = tk.Frame(inner, bg=BG2)
        logo_fr.pack(side="left")
        tk.Label(logo_fr, text="⚙", bg=BG2, fg=VERDE,
                 font=("Segoe UI", 22)).pack(side="left", padx=(0, 10))
        txt_fr = tk.Frame(logo_fr, bg=BG2)
        txt_fr.pack(side="left")
        tk.Label(txt_fr, text="Imobilizado  Escolar", bg=BG2, fg=TX,
                 font=("Segoe UI", 15, "bold")).pack(anchor="w")
        tk.Label(txt_fr, text="MONITORIZAR  •  GERIR  •  MANTER",
                 bg=BG2, fg=TX3, font=("Segoe UI", 8)).pack(anchor="w")

        # Botões direita
        btns = tk.Frame(inner, bg=BG2)
        btns.pack(side="right")
        btn_secondary(btns, "+ Registar Bem", self._abrir_registar).pack(side="left", padx=(0, 8))
        btn_primary(btns, "+ Registar Serviço", self._abrir_alterar_estado).pack(side="left")

        # Utilizador autenticado
        if self._utilizador:
            usr_fr = tk.Frame(inner, bg=BG2)
            usr_fr.pack(side="right", padx=(0, 20))
            tk.Label(usr_fr, text="👤", bg=BG2, fg=TX3,
                     font=("Segoe UI", 11)).pack(side="left", padx=(0, 4))
            tk.Label(usr_fr, text=self._utilizador, bg=BG2, fg=TX2,
                     font=("Segoe UI", 9)).pack(side="left")

    def _build_body(self):
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_main(body)

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG2, width=200)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        tk.Frame(sb, bg=BORDA, width=1).pack(side="right", fill="y")

        # "Guardar e Sair" fixo no fundo — sempre visível
        bottom = tk.Frame(sb, bg=BG2)
        bottom.pack(side="bottom", fill="x")
        tk.Frame(bottom, bg=BORDA, height=1).pack(fill="x", padx=10, pady=(8, 0))
        b_sair = tk.Button(bottom, text="💾  Guardar e Sair", command=self._fechar,
                           bg=BG2, fg=TX2, activebackground=BG4, activeforeground=VERMELHO,
                           relief="flat", bd=0, font=("Segoe UI", 9),
                           cursor="hand2", anchor="w", padx=14, pady=8)
        b_sair.pack(fill="x")

        # Canvas rolável para o menu
        sb_canvas = tk.Canvas(sb, bg=BG2, highlightthickness=0, bd=0)
        sb_vsb = tk.Scrollbar(sb, orient="vertical", command=sb_canvas.yview)
        sb_canvas.configure(yscrollcommand=sb_vsb.set)
        sb_vsb.pack(side="right", fill="y")
        sb_canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(sb_canvas, bg=BG2)
        win_id = sb_canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_canvas_resize(event):
            sb_canvas.itemconfig(win_id, width=event.width)
        sb_canvas.bind("<Configure>", _on_canvas_resize)

        def _on_inner_resize(event):
            sb_canvas.configure(scrollregion=sb_canvas.bbox("all"))
        inner.bind("<Configure>", _on_inner_resize)

        def _sb_scroll(e):
            sb_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        sb_canvas.bind("<Enter>", lambda e: self.bind_all("<MouseWheel>", _sb_scroll))
        sb_canvas.bind("<Leave>", lambda e: self.unbind_all("<MouseWheel>"))

        self._nav_btns = []
        secoes = [
            ("NAVEGAÇÃO", [
                ("  Ativos",           self._tab_ativos,          "🗂"),
                ("  Histórico",        self._tab_historico,       "🕓"),
                ("  Histórico Ações",  self._tab_historico_acoes, "📋"),
            ]),
            ("GESTÃO", [
                ("  Alterar Estado",  self._abrir_alterar_estado,      "✏"),
                ("  Mover Bem",       self._abrir_alterar_localizacao, "📍"),
                ("  Remover Bem",     self._abrir_remover,             "🗑"),
            ]),
            ("RELATÓRIOS", [
                ("  Rel. Geral",      self._rel_geral,       "📊"),
                ("  Por Categoria",   self._rel_categoria,   "🏷"),
                ("  Por Estado",      self._rel_estado,      "🔄"),
                ("  Por Localização", self._rel_localizacao, "📍"),
                ("  Exportar TXT",    self._exportar_txt,    "💾"),
            ]),
            ("IMPORTAÇÃO", [
                ("  Importar Simples",  self._importar_simples,  "📥"),
                ("  Importar Flexível", self._importar_flexivel, "🔀"),
            ]),
        ]

        for titulo, items in secoes:
            tk.Label(inner, text=titulo, bg=BG2, fg=TX3,
                     font=("Segoe UI", 8, "bold"),
                     anchor="w").pack(fill="x", padx=14, pady=(14, 2))
            for texto, cmd, ico in items:
                b = tk.Button(inner, text=f"{ico}{texto}", command=cmd,
                              bg=BG2, fg=TX2, activebackground=BG4,
                              activeforeground=TX, relief="flat", bd=0,
                              font=("Segoe UI", 9), cursor="hand2",
                              anchor="w", padx=14, pady=5)
                b.pack(fill="x")
                b.bind("<Enter>", lambda e, w=b: w.config(bg=BG4, fg=TX))
                b.bind("<Leave>", lambda e, w=b: w.config(bg=BG2, fg=TX2))
                self._nav_btns.append(b)

    def _build_main(self, parent):
        self._main = tk.Frame(parent, bg=BG)
        self._main.pack(side="left", fill="both", expand=True)

        self._build_stats_bar()
        self._build_filtros()
        self._build_cards_area()
        self._build_statusbar()

    def _build_stats_bar(self):
        self._stats_frame = tk.Frame(self._main, bg=BG, pady=16)
        self._stats_frame.pack(fill="x", padx=20)

        self._stat_widgets = {}
        stats_def = [
            ("danificados",  "Danificados",   VERMELHO,   VERMELHO_BG, "🔴"),
            ("reparacao",    "Em Reparação",  AMARELO,    AMARELO_BG,  "🟡"),
            ("bom",          "Bom / Novo",    VERDE,      VERDE_BG,    "🟢"),
            ("total",        "Total de Bens", TX2,        BG3,         "📦"),
        ]
        for key, label_txt, cor, bg_c, ico in stats_def:
            card = tk.Frame(self._stats_frame, bg=bg_c,
                            highlightthickness=1, highlightbackground=BORDA2)
            card.pack(side="left", expand=True, fill="x", padx=6, ipady=12)
            tk.Label(card, text=ico, bg=bg_c, fg=cor,
                     font=("Segoe UI", 16)).pack(side="left", padx=(16, 8))
            info = tk.Frame(card, bg=bg_c)
            info.pack(side="left", pady=4)
            num_lbl = tk.Label(info, text="0", bg=bg_c, fg=cor,
                               font=("Segoe UI", 24, "bold"))
            num_lbl.pack(anchor="w")
            tk.Label(info, text=label_txt, bg=bg_c, fg=TX2,
                     font=("Segoe UI", 9)).pack(anchor="w")
            self._stat_widgets[key] = num_lbl

    def _build_filtros(self):
        fr = tk.Frame(self._main, bg=BG)
        fr.pack(fill="x", padx=20, pady=(0, 12))

        filtros_fr = tk.Frame(fr, bg=BG)
        filtros_fr.pack(side="left")

        self._filtro_buttons = {}
        filtros = [("Todos", None), ("Bom", "Bom"), ("Novo", "Novo"),
                   ("Danificado", "Danificado"), ("Em Reparação", "Em Reparação"),
                   ("Inutilizado", "Inutilizado")]
        for texto, valor in filtros:
            ativo = (texto == "Todos")
            b = btn_ghost(filtros_fr, texto, lambda v=texto: self._set_filtro(v), ativo=ativo)
            b.pack(side="left", padx=3)
            self._filtro_buttons[texto] = b

        # Pesquisa
        pesq_fr = tk.Frame(fr, bg=BG3, highlightthickness=1,
                           highlightbackground=BORDA2)
        pesq_fr.pack(side="right", padx=4)
        tk.Label(pesq_fr, text="🔍", bg=BG3, fg=TX2,
                 font=("Segoe UI", 11)).pack(side="left", padx=(8, 2))
        e = tk.Entry(pesq_fr, textvariable=self._pesq_var,
                     bg=BG3, fg=TX, insertbackground=TX,
                     relief="flat", bd=0, font=("Segoe UI", 10), width=22)
        e.pack(side="left", padx=(0, 8), pady=6)
        e.insert(0, "Pesquisar...")
        e.bind("<FocusIn>", lambda ev: e.delete(0, "end") if e.get() == "Pesquisar..." else None)
        e.bind("<FocusOut>", lambda ev: e.insert(0, "Pesquisar...") if not e.get() else None)

    def _build_cards_area(self):
        wrapper = tk.Frame(self._main, bg=BG)
        wrapper.pack(fill="both", expand=True, padx=14)

        canvas = tk.Canvas(wrapper, bg=BG, highlightthickness=0)
        vsb = tk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self._cards_inner = tk.Frame(canvas, bg=BG)
        self._cards_win = canvas.create_window((0, 0), window=self._cards_inner, anchor="nw")

        def _on_resize(event):
            canvas.itemconfig(self._cards_win, width=event.width)
        canvas.bind("<Configure>", _on_resize)

        def _on_frame_resize(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self._cards_inner.bind("<Configure>", _on_frame_resize)

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self._canvas = canvas

    def _build_statusbar(self):
        sb = tk.Frame(self._main, bg=BG2, height=28)
        sb.pack(fill="x", side="bottom")
        tk.Frame(sb, bg=BORDA, height=1).pack(fill="x", side="top")
        self._status_lbl = tk.Label(sb, text="", bg=BG2, fg=TX2,
                                     font=("Segoe UI", 9), anchor="w", padx=16)
        self._status_lbl.pack(side="left", fill="x")
        self._total_lbl = tk.Label(sb, text="", bg=BG2, fg=TX3,
                                    font=("Segoe UI", 9), anchor="e", padx=16)
        self._total_lbl.pack(side="right")

    # ─────────────────────────────────────────────────────────────────────────
    # REFRESH
    # ─────────────────────────────────────────────────────────────────────────

    def _refresh_stats(self):
        total = len(inventario)
        dani = sum(1 for b in inventario if b["estado"] == "Danificado")
        rep  = sum(1 for b in inventario if b["estado"] == "Em Reparação")
        bom  = sum(1 for b in inventario if b["estado"] in ("Bom", "Novo"))
        self._stat_widgets["total"].config(text=str(total))
        self._stat_widgets["danificados"].config(text=str(dani))
        self._stat_widgets["reparacao"].config(text=str(rep))
        self._stat_widgets["bom"].config(text=str(bom))

    def _set_filtro(self, valor):
        self._filtro_ativo = valor
        for k, b in self._filtro_buttons.items():
            ativo = (k == valor)
            b.config(bg=BG4 if ativo else BG2, fg=TX if ativo else TX2)
        self._refresh_cards()

    def _refresh_cards(self):
        # limpar
        for w in self._cards_inner.winfo_children():
            w.destroy()

        termo = self._pesq_var.get().lower()
        if termo == "pesquisar...": termo = ""

        filtro = self._filtro_ativo
        lista = [
            b for b in inventario
            if (filtro == "Todos" or b["estado"] == filtro)
            and (not termo or termo in b["id"].lower()
                 or termo in b["nome"].lower()
                 or termo in b["localizacao"].lower())
        ]

        if not lista:
            tk.Label(self._cards_inner, text="Nenhum bem encontrado.",
                     bg=BG, fg=TX3, font=("Segoe UI", 12)).pack(pady=40)
            self._total_lbl.config(text=f"Total: 0 de {len(inventario)}")
            return

        # Grid 3 colunas
        COLS = 3
        for i, bem in enumerate(lista):
            row, col = divmod(i, COLS)
            self._card(self._cards_inner, bem).grid(
                row=row, column=col, padx=8, pady=8, sticky="nsew")

        for c in range(COLS):
            self._cards_inner.columnconfigure(c, weight=1, minsize=260)

        self._total_lbl.config(text=f"Total: {len(lista)} de {len(inventario)}")

    def _card(self, parent, bem):
        est = bem["estado"]
        cor_tx, cor_bg, cor_dot = ESTADO_STYLE.get(est, (TX2, BG3, TX2))
        cat_icon = CAT_ICON.get(bem["categoria"], "📦")

        card = tk.Frame(parent, bg=BG3,
                        highlightthickness=1, highlightbackground=BORDA)
        card.configure(cursor="hand2")

        # ── Cabeçalho ─────────────────────────────────────────────
        hdr = tk.Frame(card, bg=BG3)
        hdr.pack(fill="x", padx=16, pady=(14, 4))

        tk.Label(hdr, text=f"{cat_icon}  {bem['nome']}", bg=BG3, fg=TX,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(side="left")

        # Botões editar/remover no canto
        act = tk.Frame(hdr, bg=BG3)
        act.pack(side="right")
        tk.Button(act, text="✏", bg=BG3, fg=TX2, relief="flat", bd=0,
                  cursor="hand2", font=("Segoe UI", 11),
                  command=lambda b=bem: self._editar_bem(b)).pack(side="left", padx=2)
        tk.Button(act, text="🗑", bg=BG3, fg=TX2, relief="flat", bd=0,
                  cursor="hand2", font=("Segoe UI", 11),
                  command=lambda b=bem: self._remover_direto(b)).pack(side="left", padx=2)

        tk.Label(card, text=bem["categoria"], bg=BG3, fg=TX3,
                 font=("Segoe UI", 9), anchor="w").pack(fill="x", padx=16)

        # ── Separador ─────────────────────────────────────────────
        tk.Frame(card, bg=BORDA, height=1).pack(fill="x", padx=16, pady=8)

        # ── Localização + ID ──────────────────────────────────────
        info = tk.Frame(card, bg=BG3)
        info.pack(fill="x", padx=16, pady=2)
        tk.Label(info, text="📍", bg=BG3, fg=TX3,
                 font=("Segoe UI", 10)).pack(side="left")
        tk.Label(info, text=bem["localizacao"], bg=BG3, fg=TX2,
                 font=("Segoe UI", 9)).pack(side="left", padx=4)

        info2 = tk.Frame(card, bg=BG3)
        info2.pack(fill="x", padx=16, pady=2)
        tk.Label(info2, text="🔑", bg=BG3, fg=TX3,
                 font=("Segoe UI", 10)).pack(side="left")
        tk.Label(info2, text=bem["id"], bg=BG3, fg=TX2,
                 font=("Segoe UI", 9)).pack(side="left", padx=4)

        tk.Frame(card, bg=BORDA, height=1).pack(fill="x", padx=16, pady=8)

        # ── Rodapé: badge de estado ────────────────────────────────
        rodape = tk.Frame(card, bg=BG3)
        rodape.pack(fill="x", padx=16, pady=(0, 14))

        badge_fr = tk.Frame(rodape, bg=cor_bg,
                             highlightthickness=1, highlightbackground=cor_dot)
        badge_fr.pack(side="left")
        tk.Label(badge_fr, text="●", bg=cor_bg, fg=cor_dot,
                 font=("Segoe UI", 7)).pack(side="left", padx=(6, 2), pady=3)
        tk.Label(badge_fr, text=est, bg=cor_bg, fg=cor_tx,
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 6), pady=3)

        # Duplo clique → detalhes
        for widget in [card, hdr, info, info2]:
            widget.bind("<Double-1>", lambda e, b=bem: self._ver_detalhes(b))

        # Hover
        def _hover_on(e, c=card):
            c.config(highlightbackground=BORDA2)
        def _hover_off(e, c=card):
            c.config(highlightbackground=BORDA)
        card.bind("<Enter>", _hover_on)
        card.bind("<Leave>", _hover_off)

        return card

    # ─────────────────────────────────────────────────────────────────────────
    # TABS (placeholder)
    # ─────────────────────────────────────────────────────────────────────────

    def _tab_ativos(self):
        self._set_filtro("Todos")
        self._set_status("📋  Vista de ativos.")

    def _tab_historico(self):
        self._janela_relatorio("Histórico / Relatório Geral", self._preencher_geral)

    def _tab_historico_acoes(self):
        entradas = carregar_historico()

        win = tk.Toplevel(self)
        win.title("Histórico de Ações")
        win.geometry("860x520")
        win.configure(bg=BG2)
        win.transient(self)

        tk.Label(win, text="📋  Histórico de Ações por Utilizador", bg=BG2, fg=TX,
                 font=("Segoe UI", 13, "bold")).pack(pady=(18, 6), padx=20, anchor="w")
        tk.Frame(win, bg=BORDA, height=1).pack(fill="x")

        # Filtro por utilizador
        filtro_fr = tk.Frame(win, bg=BG2)
        filtro_fr.pack(fill="x", padx=16, pady=8)
        tk.Label(filtro_fr, text="Filtrar utilizador:", bg=BG2, fg=TX2,
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
        utilizadores_unicos = sorted({e["utilizador"] for e in entradas})
        var_filtro = tk.StringVar(value="Todos")
        cb_filtro = dark_combo(filtro_fr, ["Todos"] + utilizadores_unicos, var_filtro, w=20)
        cb_filtro.pack(side="left")

        # Tabela
        cols = ("Data/Hora", "Utilizador", "Ação", "ID Bem", "Detalhe")
        style = ttk.Style()
        style.configure("H.Treeview", background=BG3, foreground=TX,
                        fieldbackground=BG3, rowheight=24,
                        font=("Segoe UI", 9))
        style.configure("H.Treeview.Heading", background=BG2, foreground=TX2,
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("H.Treeview", background=[("selected", BG4)])

        frm_tree = tk.Frame(win, bg=BG)
        frm_tree.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        vsb = tk.Scrollbar(frm_tree, orient="vertical")
        tree = ttk.Treeview(frm_tree, columns=cols, show="headings",
                            style="H.Treeview", yscrollcommand=vsb.set)
        vsb.config(command=tree.yview)

        larguras = [140, 110, 130, 80, 340]
        for col, larg in zip(cols, larguras):
            tree.heading(col, text=col)
            tree.column(col, width=larg, anchor="w", minwidth=60)

        vsb.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        def preencher(filtro="Todos"):
            tree.delete(*tree.get_children())
            lista = entradas if filtro == "Todos" else [e for e in entradas if e["utilizador"] == filtro]
            for e in reversed(lista):
                tree.insert("", "end", values=(
                    e["ts"], e["utilizador"], e["acao"], e["id_bem"], e["detalhe"]
                ))

        preencher()
        var_filtro.trace_add("write", lambda *_: preencher(var_filtro.get()))

        total_lbl = tk.Label(win, text=f"{len(entradas)} registo(s) no total",
                             bg=BG2, fg=TX3, font=("Segoe UI", 9))
        total_lbl.pack(pady=(0, 4))

        tk.Button(win, text="Fechar", command=win.destroy,
                  bg=BG4, fg=TX2, relief="flat", bd=0,
                  font=("Segoe UI", 9), cursor="hand2",
                  pady=6, padx=14).pack(pady=8)

    # ─────────────────────────────────────────────────────────────────────────
    # MODAIS
    # ─────────────────────────────────────────────────────────────────────────

    def _modal(self, titulo, w=460, h=420):
        win = tk.Toplevel(self)
        win.title(titulo)
        win.geometry(f"{w}x{h}")
        win.configure(bg=BG2)
        win.grab_set()
        win.resizable(False, False)
        win.transient(self)
        return win

    def _modal_titulo(self, win, texto):
        tk.Label(win, text=texto, bg=BG2, fg=TX,
                 font=("Segoe UI", 13, "bold")).pack(pady=(18, 4), padx=20, anchor="w")
        tk.Frame(win, bg=BORDA, height=1).pack(fill="x", padx=0)

    def _campo(self, frm, row, texto, widget_fn):
        tk.Label(frm, text=texto, bg=BG2, fg=TX2,
                 font=("Segoe UI", 9), anchor="w").grid(
                     row=row, column=0, sticky="w", padx=14, pady=5)
        w = widget_fn()
        w.grid(row=row, column=1, sticky="ew", padx=14, pady=5)
        return w

    # ── REGISTAR ─────────────────────────────────────────────────

    def _abrir_registar(self):
        win = self._modal("Registar Novo Bem", 460, 400)
        self._modal_titulo(win, "Registar Novo Bem")

        frm = tk.Frame(win, bg=BG2)
        frm.pack(fill="both", expand=True, pady=8)
        frm.columnconfigure(1, weight=1)

        var_tipo = tk.StringVar()
        var_cat  = tk.StringVar()
        var_id   = tk.StringVar()
        var_est  = tk.StringVar()
        var_loc  = tk.StringVar()

        cb_tipo = self._campo(frm, 0, "Tipo de Bem:",
                              lambda: dark_combo(frm, list(TIPOS_BENS.keys()), var_tipo))
        cb_tipo.current(0)

        e_cat = self._campo(frm, 1, "Categoria:",
                            lambda: dark_entry(frm, var_cat))
        e_cat.config(state="disabled",
                     disabledbackground=BG3, disabledforeground=TX3)

        e_id = self._campo(frm, 2, "ID Gerado:",
                           lambda: dark_entry(frm, var_id))
        e_id.config(state="disabled",
                    disabledbackground=BG3, disabledforeground=VERDE)

        cb_est = self._campo(frm, 3, "Estado:",
                             lambda: dark_combo(frm, ESTADOS, var_est))
        cb_est.current(0)

        cb_loc = self._campo(frm, 4, "Localização:",
                             lambda: dark_combo(frm, LOCALIZACOES, var_loc))
        cb_loc.current(0)

        def _auto(*_):
            t = var_tipo.get()
            var_cat.set(obter_categoria(t))
            var_id.set(_gerar_novo_id(obter_radical(t)))

        var_tipo.trace_add("write", _auto)
        _auto()

        def confirmar():
            t = var_tipo.get()
            novo_id = _gerar_novo_id(obter_radical(t))
            bem = criar_bem(novo_id, t, obter_categoria(t),
                            var_est.get(), var_loc.get())
            inventario.append(bem)
            guardar_dados()
            registar_acao(self._utilizador, "Registou", novo_id,
                          f"{t} — {var_loc.get()} — {var_est.get()}")
            self._refresh_stats()
            self._refresh_cards()
            self._set_status(f"✔  '{t}' registado com ID {novo_id}.")
            win.destroy()

        self._rodape_modal(win, confirmar, "✔  Registar", ACCENT)

    # ── ALTERAR ESTADO ────────────────────────────────────────────

    def _abrir_alterar_estado(self, bem_pre=None):
        win = self._modal("Alterar Estado", 440, 300)
        self._modal_titulo(win, "Alterar Estado do Bem")

        frm = tk.Frame(win, bg=BG2)
        frm.pack(fill="both", expand=True, pady=8)
        frm.columnconfigure(1, weight=1)

        var_id  = tk.StringVar(value=bem_pre["id"] if bem_pre else "")
        var_est = tk.StringVar()

        self._campo(frm, 0, "ID do Bem:",
                    lambda: dark_entry(frm, var_id))

        lbl_atual = tk.Label(frm, text="—", bg=BG2, fg=AMARELO,
                             font=("Segoe UI", 10, "bold"), anchor="w")
        tk.Label(frm, text="Estado Atual:", bg=BG2, fg=TX2,
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", padx=14, pady=5)
        lbl_atual.grid(row=1, column=1, sticky="w", padx=14)

        cb_est = self._campo(frm, 2, "Novo Estado:",
                             lambda: dark_combo(frm, ESTADOS, var_est))
        if bem_pre and bem_pre["estado"] in ESTADOS:
            cb_est.current(ESTADOS.index(bem_pre["estado"]))
        else:
            cb_est.current(0)

        if bem_pre:
            lbl_atual.config(text=bem_pre["estado"])

        def _atualizar(*_):
            b = next((x for x in inventario if x["id"] == var_id.get().upper()), None)
            lbl_atual.config(text=b["estado"] if b else "— não encontrado —")
            if b and b["estado"] in ESTADOS:
                cb_est.current(ESTADOS.index(b["estado"]))

        var_id.trace_add("write", _atualizar)

        def confirmar():
            b = next((x for x in inventario if x["id"] == var_id.get().upper()), None)
            if not b:
                messagebox.showerror("Erro", "Bem não encontrado.", parent=win)
                return
            estado_anterior = b["estado"]
            b["estado"] = var_est.get()
            guardar_dados()
            registar_acao(self._utilizador, "Alterou Estado", b["id"],
                          f"{estado_anterior} → {var_est.get()}")
            self._refresh_stats()
            self._refresh_cards()
            self._set_status(f"✔  Estado de {b['id']} → '{var_est.get()}'.")
            win.destroy()

        self._rodape_modal(win, confirmar, "✔  Confirmar", VERDE)

    def _editar_bem(self, bem):
        self._abrir_alterar_estado(bem)

    # ── ALTERAR LOCALIZAÇÃO ───────────────────────────────────────

    def _abrir_alterar_localizacao(self):
        win = self._modal("Alterar Localização", 440, 280)
        self._modal_titulo(win, "Mover Bem")

        frm = tk.Frame(win, bg=BG2)
        frm.pack(fill="both", expand=True, pady=8)
        frm.columnconfigure(1, weight=1)

        var_id  = tk.StringVar()
        var_loc = tk.StringVar()

        self._campo(frm, 0, "ID do Bem:", lambda: dark_entry(frm, var_id))

        lbl_atual = tk.Label(frm, text="—", bg=BG2, fg=AMARELO,
                             font=("Segoe UI", 10, "bold"), anchor="w")
        tk.Label(frm, text="Localização Atual:", bg=BG2, fg=TX2,
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", padx=14, pady=5)
        lbl_atual.grid(row=1, column=1, sticky="w", padx=14)

        cb_loc = self._campo(frm, 2, "Nova Localização:",
                             lambda: dark_combo(frm, LOCALIZACOES, var_loc))
        cb_loc.current(0)

        def _atualizar(*_):
            b = next((x for x in inventario if x["id"] == var_id.get().upper()), None)
            lbl_atual.config(text=b["localizacao"] if b else "— não encontrado —")

        var_id.trace_add("write", _atualizar)

        def confirmar():
            b = next((x for x in inventario if x["id"] == var_id.get().upper()), None)
            if not b:
                messagebox.showerror("Erro", "Bem não encontrado.", parent=win)
                return
            loc_anterior = b["localizacao"]
            b["localizacao"] = var_loc.get()
            guardar_dados()
            registar_acao(self._utilizador, "Moveu", b["id"],
                          f"{loc_anterior} → {var_loc.get()}")
            self._refresh_cards()
            self._set_status(f"✔  {b['id']} movido para '{var_loc.get()}'.")
            win.destroy()

        self._rodape_modal(win, confirmar, "✔  Confirmar", AZUL)

    # ── REMOVER ───────────────────────────────────────────────────

    def _abrir_remover(self):
        win = self._modal("Remover Bem", 420, 240)
        self._modal_titulo(win, "Remover Bem do Inventário")

        frm = tk.Frame(win, bg=BG2)
        frm.pack(fill="both", expand=True, pady=8)
        frm.columnconfigure(1, weight=1)

        var_id = tk.StringVar()
        self._campo(frm, 0, "ID do Bem:", lambda: dark_entry(frm, var_id))

        lbl_nome = tk.Label(frm, text="—", bg=BG2, fg=TX2,
                            font=("Segoe UI", 9), anchor="w")
        tk.Label(frm, text="Nome:", bg=BG2, fg=TX2,
                 font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", padx=14, pady=5)
        lbl_nome.grid(row=1, column=1, sticky="w", padx=14)

        def _atualizar(*_):
            b = next((x for x in inventario if x["id"] == var_id.get().upper()), None)
            lbl_nome.config(text=b["nome"] if b else "— não encontrado —")

        var_id.trace_add("write", _atualizar)

        def confirmar():
            b = next((x for x in inventario if x["id"] == var_id.get().upper()), None)
            if not b:
                messagebox.showerror("Erro", "Bem não encontrado.", parent=win)
                return
            if messagebox.askyesno("Confirmar",
                                   f"Remover '{b['nome']}' ({b['id']})?",
                                   parent=win):
                registar_acao(self._utilizador, "Removeu", b["id"],
                              f"{b['nome']} — {b['categoria']} — {b['localizacao']}")
                inventario.remove(b)
                guardar_dados()
                self._refresh_stats()
                self._refresh_cards()
                self._set_status(f"🗑  Bem '{b['id']}' removido.")
                win.destroy()

        self._rodape_modal(win, confirmar, "🗑  Remover", VERMELHO)

    def _remover_direto(self, bem):
        if messagebox.askyesno("Confirmar Remoção",
                               f"Remover '{bem['nome']}' ({bem['id']})?",
                               parent=self):
            registar_acao(self._utilizador, "Removeu", bem["id"],
                          f"{bem['nome']} — {bem['categoria']} — {bem['localizacao']}")
            inventario.remove(bem)
            guardar_dados()
            self._refresh_stats()
            self._refresh_cards()
            self._set_status(f"🗑  Bem '{bem['id']}' removido.")

    # ── VER DETALHES ──────────────────────────────────────────────

    def _ver_detalhes(self, bem):
        win = self._modal(f"Detalhes — {bem['id']}", 420, 360)
        self._modal_titulo(win, "Detalhes do Bem")

        est = bem["estado"]
        cor_tx, cor_bg, cor_dot = ESTADO_STYLE.get(est, (TX2, BG3, TX2))
        cat_icon = CAT_ICON.get(bem["categoria"], "📦")

        frm = tk.Frame(win, bg=BG2)
        frm.pack(fill="both", expand=True, padx=20, pady=10)
        frm.columnconfigure(1, weight=1)

        campos = [
            ("ID:",          bem["id"],          VERDE),
            ("Nome:",        bem["nome"],         TX),
            ("Categoria:",   f"{cat_icon}  {bem['categoria']}", TX2),
            ("Localização:", f"📍  {bem['localizacao']}", AZUL),
        ]
        for i, (lbl_t, val, cor) in enumerate(campos):
            tk.Label(frm, text=lbl_t, bg=BG2, fg=TX3,
                     font=("Segoe UI", 9)).grid(row=i, column=0, sticky="w", pady=7)
            tk.Label(frm, text=val, bg=BG2, fg=cor,
                     font=("Segoe UI", 10, "bold")).grid(row=i, column=1, sticky="w", padx=12, pady=7)

        # Badge estado
        tk.Frame(win, bg=BORDA, height=1).pack(fill="x", padx=16, pady=4)
        badge_row = tk.Frame(win, bg=BG2)
        badge_row.pack(pady=6)
        badge_fr = tk.Frame(badge_row, bg=cor_bg,
                             highlightthickness=1, highlightbackground=cor_dot)
        badge_fr.pack(side="left")
        tk.Label(badge_fr, text="●", bg=cor_bg, fg=cor_dot,
                 font=("Segoe UI", 9)).pack(side="left", padx=(8, 2), pady=4)
        tk.Label(badge_fr, text=est, bg=cor_bg, fg=cor_tx,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8), pady=4)

        btns = tk.Frame(win, bg=BG2)
        btns.pack(pady=8)
        btn_primary(btns, "✏  Editar",
                    lambda b=bem: [win.destroy(), self._abrir_alterar_estado(b)]).pack(side="left", padx=6)
        tk.Button(btns, text="Fechar", command=win.destroy,
                  bg=BG4, fg=TX2, activebackground=BG3,
                  relief="flat", bd=0, font=("Segoe UI", 9),
                  cursor="hand2", pady=7, padx=14).pack(side="left", padx=6)

    # ── RODAPÉ DOS MODAIS ─────────────────────────────────────────

    def _rodape_modal(self, win, confirmar_fn, texto_ok, cor_ok):
        tk.Frame(win, bg=BORDA, height=1).pack(fill="x", side="bottom", pady=(0, 0))
        btns = tk.Frame(win, bg=BG2)
        btns.pack(side="bottom", pady=12)
        b_ok = tk.Button(btns, text=texto_ok, command=confirmar_fn,
                         bg=cor_ok, fg="white", activebackground=cor_ok,
                         relief="flat", bd=0, font=("Segoe UI", 9, "bold"),
                         cursor="hand2", pady=7, padx=16)
        b_ok.pack(side="left", padx=6)
        tk.Button(btns, text="✖  Cancelar", command=win.destroy,
                  bg=BG4, fg=TX2, activebackground=BG3,
                  relief="flat", bd=0, font=("Segoe UI", 9),
                  cursor="hand2", pady=7, padx=14).pack(side="left", padx=6)

    # ─────────────────────────────────────────────────────────────────────────
    # RELATÓRIOS
    # ─────────────────────────────────────────────────────────────────────────

    def _janela_relatorio(self, titulo, preencher_fn):
        win = tk.Toplevel(self)
        win.title(titulo)
        win.geometry("580x500")
        win.configure(bg=BG2)
        win.transient(self)

        tk.Label(win, text=titulo, bg=BG2, fg=TX,
                 font=("Segoe UI", 13, "bold")).pack(pady=(18, 6), padx=20, anchor="w")
        tk.Frame(win, bg=BORDA, height=1).pack(fill="x")

        txt = tk.Text(win, bg=BG, fg=TX, font=("Consolas", 10),
                      relief="flat", bd=0, padx=16, pady=12, wrap="word")
        txt.pack(fill="both", expand=True, padx=16, pady=8)

        preencher_fn(txt)
        txt.config(state="disabled")

        tk.Button(win, text="Fechar", command=win.destroy,
                  bg=BG4, fg=TX2, relief="flat", bd=0,
                  font=("Segoe UI", 9), cursor="hand2",
                  pady=6, padx=14).pack(pady=8)

    def _preencher_geral(self, txt):
        txt.tag_configure("h", foreground=AZUL, font=("Consolas", 11, "bold"))
        txt.tag_configure("s", foreground=AMARELO, font=("Consolas", 10, "bold"))
        txt.tag_configure("v", foreground=TX)
        total = len(inventario)
        txt.insert("end", f"Total de bens: {total}\n\n", "h")
        for campo, lbl in [("categoria","Por Categoria"),("estado","Por Estado"),("localizacao","Por Localização")]:
            txt.insert("end", f"\n━━ {lbl} ━━\n", "s")
            for k, v in sorted(contar_por_campo(campo).items()):
                barra = "█" * min(v*2, 28)
                txt.insert("end", f"  {k:<32} {v:>4}  {barra}\n", "v")

    def _rel_geral(self):
        self._janela_relatorio("Relatório Geral", self._preencher_geral)

    def _rel_categoria(self):
        def p(txt):
            txt.tag_configure("s", foreground=AMARELO, font=("Consolas",10,"bold"))
            txt.tag_configure("v", foreground=TX)
            txt.insert("end", "━━ Por Categoria ━━\n\n", "s")
            for k, v in sorted(contar_por_campo("categoria").items()):
                txt.insert("end", f"  {k:<32} {v:>4}  {'█'*min(v*2,28)}\n","v")
        self._janela_relatorio("Por Categoria", p)

    def _rel_estado(self):
        def p(txt):
            txt.tag_configure("s", foreground=AMARELO, font=("Consolas",10,"bold"))
            txt.insert("end", "━━ Por Estado ━━\n\n", "s")
            for k, v in sorted(contar_por_campo("estado").items()):
                cor, _, _ = ESTADO_STYLE.get(k, (TX, BG3, TX))
                txt.tag_configure(k, foreground=cor)
                txt.insert("end", f"  {k:<32} {v:>4}  {'█'*min(v*2,28)}\n", k)
        self._janela_relatorio("Por Estado", p)

    def _rel_localizacao(self):
        def p(txt):
            txt.tag_configure("s", foreground=AMARELO, font=("Consolas",10,"bold"))
            txt.tag_configure("v", foreground=TX)
            txt.insert("end", "━━ Por Localização ━━\n\n", "s")
            for k, v in sorted(contar_por_campo("localizacao").items()):
                txt.insert("end", f"  {k:<32} {v:>4}  {'█'*min(v*2,28)}\n","v")
        self._janela_relatorio("Por Localização", p)

    def _exportar_txt(self):
        os.makedirs("relatorios_exportados", exist_ok=True)
        nome = "relatorios_exportados/relatorio_inventario.txt"
        with open(nome, "w", encoding="utf-8") as f:
            f.write("RELATÓRIO GERAL DO INVENTÁRIO\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total: {len(inventario)}\n")
            f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for campo, lbl in [("categoria","Categoria"),("estado","Estado"),("localizacao","Localização")]:
                f.write(f"\n{lbl}:\n")
                for k, v in sorted(contar_por_campo(campo).items()):
                    f.write(f"  - {k}: {v}\n")
            f.write("\n\nListagem completa:\n")
            f.write("-"*80+"\n")
            f.write(f"{'ID':<10} {'Nome':<30} {'Categoria':<25} {'Estado':<15} Localização\n")
            f.write("-"*80+"\n")
            for b in inventario:
                f.write(f"{b['id']:<10} {b['nome']:<30} {b['categoria']:<25} {b['estado']:<15} {b['localizacao']}\n")
        messagebox.showinfo("Exportado", f"Relatório guardado em:\n{nome}", parent=self)
        self._set_status(f"💾  Relatório exportado para '{nome}'.")

    # ─────────────────────────────────────────────────────────────────────────
    # IMPORTAÇÃO SIMPLES
    # ─────────────────────────────────────────────────────────────────────────

    def _importar_simples(self):
        win = self._modal("Importar — Formato Simples", 520, 360)
        self._modal_titulo(win, "Importar Bens (Formato Fixo)")

        tk.Label(win,
                 text="Estrutura esperada:\n  id;nome;categoria;estado;localizacao\n\nExemplo:\n  COM0001;Computador;Equipamento Informático;Bom;Sala 1",
                 bg=BG2, fg=TX3, font=("Segoe UI", 9),
                 justify="left").pack(padx=20, pady=8, anchor="w")

        frm = tk.Frame(win, bg=BG2)
        frm.pack(fill="x", padx=20)
        frm.columnconfigure(1, weight=1)

        var_path = tk.StringVar()
        tk.Label(frm, text="Ficheiro:", bg=BG2, fg=TX2,
                 font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", padx=4, pady=6)
        dark_entry(frm, var_path, w=36).grid(row=0, column=1, sticky="ew", padx=4, pady=6)

        def escolher():
            p = filedialog.askopenfilename(parent=win, title="Escolher ficheiro",
                                           filetypes=[("TXT/CSV","*.txt *.csv"),("Todos","*.*")])
            if p: var_path.set(p)

        btn_ghost(frm, "...", escolher).grid(row=0, column=2, padx=4)

        lbl_res = tk.Label(win, text="", bg=BG2, fg=VERDE,
                           font=("Segoe UI", 9), justify="left")
        lbl_res.pack(padx=20, pady=4, anchor="w")

        def importar():
            cam = var_path.get().strip().replace('"','')
            if not cam:
                messagebox.showwarning("Aviso","Selecione um ficheiro.",parent=win)
                return
            imp = dup = inv = 0
            try:
                with open(cam,"r",encoding="utf-8") as f:
                    for linha in f:
                        if not linha.strip(): continue
                        n = linha.strip().lower().replace("localização","localizacao")
                        if n == "id;nome;categoria;estado;localizacao": continue
                        b = linha_para_bem(linha)
                        if not b: inv += 1; continue
                        if not validar_formato_id(b["id"]):
                            b["id"] = _gerar_novo_id(obter_radical(b["nome"]))
                        if _id_existe(b["id"]): dup += 1; continue
                        inventario.append(b); imp += 1
                guardar_dados()
                registar_acao(self._utilizador, "Importou (simples)", "—",
                              f"{imp} importado(s), {dup} duplicado(s), {inv} inválido(s)")
                self._refresh_stats(); self._refresh_cards()
                lbl_res.config(text=f"✔  Importados: {imp}   Duplicados: {dup}   Inválidos: {inv}")
                self._set_status(f"📥  Importação simples: {imp} bem(ns).")
            except FileNotFoundError:
                messagebox.showerror("Erro","Ficheiro não encontrado.",parent=win)
            except UnicodeDecodeError:
                messagebox.showerror("Erro","Erro de codificação. Guarde como UTF-8.",parent=win)
            except Exception as e:
                messagebox.showerror("Erro",str(e),parent=win)

        self._rodape_modal(win, importar, "📥  Importar", ACCENT2)

    # ─────────────────────────────────────────────────────────────────────────
    # IMPORTAÇÃO FLEXÍVEL
    # ─────────────────────────────────────────────────────────────────────────

    def _importar_flexivel(self):
        win = tk.Toplevel(self)
        win.title("Importar — Mapeamento Flexível")
        win.geometry("620x560")
        win.configure(bg=BG2)
        win.grab_set(); win.transient(self)

        tk.Label(win, text="Importação Flexível", bg=BG2, fg=TX,
                 font=("Segoe UI", 13, "bold")).pack(pady=(18,4), padx=20, anchor="w")
        tk.Frame(win, bg=BORDA, height=1).pack(fill="x")
        tk.Label(win,
                 text="Importa ficheiros com qualquer estrutura de colunas (separadores ; e ,).",
                 bg=BG2, fg=TX3, font=("Segoe UI", 9)).pack(padx=20, pady=4, anchor="w")

        # Passo 1 — ficheiro
        frm1 = tk.LabelFrame(win, text=" 1. Ficheiro ", bg=BG2, fg=TX2,
                              font=("Segoe UI", 9), bd=1, relief="groove")
        frm1.pack(fill="x", padx=16, pady=6)
        row_p = tk.Frame(frm1, bg=BG2)
        row_p.pack(fill="x", padx=10, pady=6)
        var_path = tk.StringVar()
        dark_entry(row_p, var_path, w=44).pack(side="left", padx=(0,6))

        colunas_f = []; vars_map = {}; sep_usado = [";"]
        var_est_p = tk.StringVar(value=ESTADOS[1])
        var_loc_p = tk.StringVar(value=LOCALIZACOES[0])

        frm_mapa = tk.LabelFrame(win, text=" 2. Mapeamento ", bg=BG2, fg=TX2,
                                  font=("Segoe UI", 9), bd=1, relief="groove")
        frm_mapa.pack(fill="x", padx=16, pady=6)

        frm_def = tk.LabelFrame(win, text=" 3. Valores Padrão ", bg=BG2, fg=TX2,
                                 font=("Segoe UI", 9), bd=1, relief="groove")
        frm_def.pack(fill="x", padx=16, pady=6)

        lbl_res2 = tk.Label(win, text="", bg=BG2, fg=VERDE,
                             font=("Segoe UI", 9), justify="left")
        lbl_res2.pack(padx=20, pady=2, anchor="w")

        def carregar_cab():
            cam = var_path.get().strip().replace('"','')
            if not cam or not os.path.isfile(cam):
                messagebox.showwarning("Aviso","Selecione um ficheiro válido.",parent=win)
                return
            try:
                with open(cam,"r",encoding="utf-8") as f:
                    linhas = f.readlines()
                linha_cab = next((l for l in linhas if l.strip()),"")
                sep = ";" if ";" in linha_cab else ("," if "," in linha_cab else None)
                if not sep:
                    messagebox.showerror("Erro","Separador não detetado.",parent=win); return
                sep_usado[0] = sep
                cols = [c.strip() for c in linha_cab.split(sep)]
                colunas_f.clear(); colunas_f.extend(cols)
                for w2 in frm_mapa.winfo_children(): w2.destroy()
                for w2 in frm_def.winfo_children(): w2.destroy()
                vars_map.clear()
                opcoes = ["(não existe)"] + cols
                campos_mapa = [
                    ("Nome (obrigatório)","nome",True),
                    ("ID","id",False),
                    ("Categoria","categoria",False),
                    ("Estado","estado",False),
                    ("Localização","localizacao",False),
                ]
                tk.Label(frm_mapa,text="Campo",bg=BG2,fg=TX3,
                         font=("Segoe UI",8,"bold")).grid(row=0,column=0,padx=10,pady=2)
                tk.Label(frm_mapa,text="Coluna no Ficheiro",bg=BG2,fg=TX3,
                         font=("Segoe UI",8,"bold")).grid(row=0,column=1,padx=10,pady=2)
                for i,(lbl_t,chave,obrig) in enumerate(campos_mapa):
                    tk.Label(frm_mapa,text=lbl_t,bg=BG2,
                             fg=TX if obrig else TX2,
                             font=("Segoe UI",9)).grid(row=i+1,column=0,sticky="w",padx=10,pady=2)
                    v = tk.StringVar()
                    vars_map[chave] = v
                    cb2 = dark_combo(frm_mapa, opcoes, v, w=22)
                    cb2.grid(row=i+1,column=1,sticky="ew",padx=10,pady=2)
                    for j,c in enumerate(cols):
                        if chave in c.lower() or c.lower() in chave:
                            cb2.current(j+1); break
                    else:
                        cb2.current(1 if obrig and cols else 0)
                # Defaults
                fd = tk.Frame(frm_def, bg=BG2)
                fd.pack(fill="x", padx=10, pady=6)
                tk.Label(fd,text="Estado padrão:",bg=BG2,fg=TX2,
                         font=("Segoe UI",9)).grid(row=0,column=0,sticky="w",padx=4)
                cb_ep = dark_combo(fd, ESTADOS, var_est_p, w=16)
                cb_ep.grid(row=0,column=1,padx=8); cb_ep.current(1)
                tk.Label(fd,text="Localização padrão:",bg=BG2,fg=TX2,
                         font=("Segoe UI",9)).grid(row=0,column=2,sticky="w",padx=4)
                cb_lp = dark_combo(fd, LOCALIZACOES, var_loc_p, w=16)
                cb_lp.grid(row=0,column=3,padx=8); cb_lp.current(0)
                lbl_res2.config(text=f"✔  {len(cols)} colunas detetadas. Defina o mapeamento.")
            except Exception as e:
                messagebox.showerror("Erro",str(e),parent=win)

        def escolher_flex():
            p = filedialog.askopenfilename(parent=win, title="Escolher ficheiro",
                                           filetypes=[("TXT/CSV","*.txt *.csv"),("Todos","*.*")])
            if p: var_path.set(p); carregar_cab()

        btn_ghost(row_p, "Escolher...", escolher_flex).pack(side="left")

        def importar_flex():
            cam = var_path.get().strip().replace('"','')
            if not cam: messagebox.showwarning("Aviso","Selecione um ficheiro.",parent=win); return
            if not vars_map: messagebox.showwarning("Aviso","Carregue o ficheiro primeiro.",parent=win); return
            idx_nome_val = vars_map.get("nome",tk.StringVar()).get()
            if idx_nome_val == "(não existe)":
                messagebox.showerror("Erro","O campo Nome é obrigatório.",parent=win); return

            def ci(chave):
                val = vars_map[chave].get()
                if val == "(não existe)" or not val: return None
                return colunas_f.index(val) if val in colunas_f else None

            i_nome=ci("nome"); i_id=ci("id"); i_cat=ci("categoria")
            i_est=ci("estado"); i_loc=ci("localizacao")
            imp=dup=inv=total=0
            sep=sep_usado[0]; ep=var_est_p.get(); lp=var_loc_p.get() or "Sem localização"

            try:
                with open(cam,"r",encoding="utf-8") as f:
                    linhas=f.readlines()
                skip=False
                for linha in linhas:
                    if not linha.strip(): continue
                    if not skip: skip=True; continue
                    total+=1
                    vals=[v.strip() for v in linha.split(sep)]
                    if len(vals)<len(colunas_f): inv+=1; continue
                    nome=vals[i_nome] if i_nome is not None and i_nome<len(vals) else ""
                    if not nome: inv+=1; continue
                    id_b=vals[i_id].upper() if i_id is not None and i_id<len(vals) else ""
                    if not id_b or not validar_formato_id(id_b):
                        id_b=_gerar_novo_id(obter_radical(nome))
                    if _id_existe(id_b): dup+=1; continue
                    cat=(vals[i_cat] if i_cat is not None and i_cat<len(vals) else "") or "Outro"
                    est=(vals[i_est] if i_est is not None and i_est<len(vals) else "") or ep
                    loc=(vals[i_loc] if i_loc is not None and i_loc<len(vals) else "") or lp
                    inventario.append(criar_bem(id_b,nome,cat,est,loc)); imp+=1
                guardar_dados()
                registar_acao(self._utilizador, "Importou (flexível)", "—",
                              f"{imp} importado(s), {dup} duplicado(s), {inv} inválido(s)")
                self._refresh_stats(); self._refresh_cards()
                lbl_res2.config(text=f"✔  Importados: {imp}   Duplicados: {dup}   Inválidos: {inv}")
                self._set_status(f"🔀  Importação flexível: {imp} bem(ns).")
            except Exception as e:
                messagebox.showerror("Erro",str(e),parent=win)

        tk.Frame(win, bg=BORDA, height=1).pack(fill="x", side="bottom", pady=0)
        btns = tk.Frame(win, bg=BG2)
        btns.pack(side="bottom", pady=10)
        btn_primary(btns, "🔀  Importar", importar_flex).pack(side="left", padx=6)
        tk.Button(btns, text="✖  Fechar", command=win.destroy,
                  bg=BG4, fg=TX2, relief="flat", bd=0,
                  font=("Segoe UI", 9), cursor="hand2",
                  pady=7, padx=14).pack(side="left", padx=6)

    # ─────────────────────────────────────────────────────────────────────────
    # STATUS + FECHAR
    # ─────────────────────────────────────────────────────────────────────────

    def _set_status(self, msg, cor=TX2):
        self._status_lbl.config(text=msg, fg=cor)

    def _fechar(self):
        guardar_dados()
        self.destroy()


# =============================================================================
if __name__ == "__main__":
    auth = JanelaAuth()
    auth.mainloop()
    if auth.autenticado:
        app = App(utilizador=auth.utilizador)
        app.mainloop()
