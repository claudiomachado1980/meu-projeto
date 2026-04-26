# 📋 Analisador de Logs de Sistema

Script Bash para análise de ficheiros de log de sistemas informáticos.  
Desenvolvido no âmbito da atividade prática do módulo de Linha de Comandos.

---

## 📁 Estrutura do Projeto

```
projeto/
├── analyzer_final.sh     # Script principal (versão final completa)
├── auto_analyzer.sh      # Script de automação automática
├── analyzer.sh           # Versão 1 — relatório simples
├── analyzer2.sh          # Versão 2 — contagem de erros com loop
├── analyzer3.sh          # Versão 3 — menu interativo
├── 10000.log             # Ficheiro de logs para análise
└── README.md             # Este ficheiro
```

---

## 🚀 Como Utilizar

### Modo interativo (menu)
```bash
./analyzer_final.sh 10000.log
```

### Modo automático (gera relatório sem interação)
```bash
./analyzer_final.sh 10000.log --auto
```

### Filtrar por utilizador
```bash
./analyzer_final.sh 10000.log user=user13
```

### Filtrar por tipo de ação
```bash
./analyzer_final.sh 10000.log action=DOWNLOAD
./analyzer_final.sh 10000.log action=ERROR
./analyzer_final.sh 10000.log action=UPLOAD
./analyzer_final.sh 10000.log action=LOGIN
```

### Combinar filtros
```bash
./analyzer_final.sh 10000.log user=user13 action=DOWNLOAD
```

### Automação com script dedicado
```bash
./auto_analyzer.sh 10000.log
```

---

## 📊 Funcionalidades do Menu Interativo

| Opção | Descrição |
|-------|-----------|
| 1  | Total de linhas no ficheiro |
| 2  | Total de eventos de erro |
| 3  | Número de IPs únicos |
| 4  | IP com mais acessos |
| 5  | Total de downloads |
| 6  | Total de uploads |
| 7  | Total de erros com código 500 |
| 8  | Utilizador mais ativo |
| 9  | Recurso mais acedido |
| 10 | Top 5 IPs com mais acessos |
| 11 | Utilizador que fez mais downloads |
| 12 | IP que gerou mais erros 500 |
| 13 | Recurso que gera mais erros |
| 14 | Relatório completo no terminal |
| 15 | Guardar relatório em ficheiro |
| 0  | Sair |

---

## 📄 Relatório Gerado

O relatório é guardado automaticamente com a data no nome:
```
relatorio_2026-04-25.txt
```

Conteúdo do relatório:
```
==============================================
         RELATÓRIO FINAL DE ANÁLISE
==============================================
Ficheiro analisado : 10000.log
Data de geração    : 2026-04-25 09:40:16

--- ESTATÍSTICAS GERAIS ---
Total de linhas        : 10000
Total de erros         : 1662
IPs únicos             : 58
Utilizadores únicos    : 24

--- ATIVIDADE ---
Downloads              : 1726
Uploads                : 1618
Erros 500              : 396

--- TOPS ---
Top IP                 : 192.168.1.10 (208 acessos)
Utilizador mais ativo  : user10 (442 ações)
Recurso mais acedido   : /files/doc.pdf (1709 vezes)
Utilizador c/ mais DL  : user14 (90 downloads)
IP com mais erros 500  : 192.168.1.40 (15 erros 500)
Recurso com mais erros : /api/data (286 erros)

--- TOP 5 IPs ---
  208 acessos  →  192.168.1.10
  206 acessos  →  192.168.1.14
  204 acessos  →  192.168.1.9
  195 acessos  →  192.168.1.53
  192 acessos  →  192.168.1.5
==============================================
```

---

## 🧩 Estrutura do Código (analyzer_final.sh)

O script está organizado em 6 secções:

| Secção | Descrição |
|--------|-----------|
| 1 | Validação de argumentos e filtros |
| 2 | Funções reutilizáveis para cada análise |
| 3 | Geração do relatório em ficheiro |
| 4 | Menu interativo com opções |
| 5 | Modo automático (`--auto`) |
| 6 | Loop principal do menu |

### Funções disponíveis
```bash
total_linhas()          # Conta linhas
total_erros()           # Conta erros (com while loop)
ips_unicos()            # Conta IPs únicos
total_downloads()       # Conta downloads
total_uploads()         # Conta uploads
erros_500()             # Conta erros 500
top_ip()                # IP mais frequente
top5_ips()              # Top 5 IPs
utilizador_mais_ativo() # Utilizador com mais ações
recurso_mais_acedido()  # Recurso mais acedido
user_mais_downloads()   # Utilizador com mais downloads
ip_mais_erros500()      # IP com mais erros 500
recurso_mais_erros()    # Recurso com mais erros
utilizadores_unicos()   # Número de utilizadores únicos
gerar_relatorio()       # Cria o ficheiro de relatório
```

---

## 🔧 Requisitos

- Sistema operativo: Linux / macOS / WSL
- Shell: Bash 4.0 ou superior
- Ferramentas necessárias: `awk`, `grep`, `sort`, `uniq`, `wc`, `head`

---

## 📌 Formato do Ficheiro de Log

Cada linha segue a estrutura:
```
<timestamp> <IP> <utilizador> <ação> <recurso> <status>
```

Exemplo:
```
2026-03-01T08:00:00 192.168.1.12 user3 LOGIN /login OK
2026-03-01T08:01:52 192.168.1.52 user19 ERROR /login 404
```

Ações possíveis: `LOGIN`, `LOGOUT`, `DOWNLOAD`, `UPLOAD`, `ACCESS`, `ERROR`  
Status possíveis: `OK`, `401`, `403`, `404`, `500`
