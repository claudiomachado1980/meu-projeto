import os

# Define onde estão os ficheiros
LOG_ENTRADA = "data/sample.log"
RELATORIO_SAIDA = "output/report.txt"

def processar_dados():
    print(f"A iniciar análise do ficheiro: {LOG_ENTRADA}...")
    
    try:
        with open(LOG_ENTRADA, "r") as ficheiro:
            linhas = ficheiro.readlines()
            contagem = len(linhas)
            
        # Cria o resumo no ficheiro de output
        with open(RELATORIO_SAIDA, "w") as relatorio:
            relatorio.write("=== RELATÓRIO DE ANÁLISE ===\n")
            relatorio.write(f"Ficheiro analisado: {LOG_ENTRADA}\n")
            relatorio.write(f"Total de linhas encontradas: {contagem}\n")
            relatorio.write("Status: Concluído com sucesso.\n")
            
        print(f"Sucesso! O relatório foi gerado em: {RELATORIO_SAIDA}")
        print(f"Foram processadas {contagem} linhas.")
        
    except FileNotFoundError:
        print("Erro: O ficheiro 'sample.log' não está na pasta 'data'.")

if __name__ == "__main__":
    processar_dados()
