import random
from collections import defaultdict

# Lista completa de jogadores com suas classes
todos_jogadores = {
    "A": ["ADRIANO", "FABIANO", "ANDERSON", "DAVI", "FABRIEL"],
    "B": ["RAVEL", "THAIEMY", "IVANIA", "ERICK", "TAILINE"],
    "C": ["LUCAS", "FERNANDA", "YASMIN"],
    "D": ["DUDA", "LARA", "THOBIAS"]
}

# >>>>> Só edite esta lista para colocar os presentes no jogo <<<<<
"""
presentes = ["ADRIANO", "IVANIA", "ERICK", "THOBIAS", "FABIANO", "FERNANDA", "LARA", "THAIEMY", "ANDERSON", 
             "DUDA", "DAVI", "TAILINE", "RAVEL", "YASMIN", "LUCAS"]
"""

presentes = ["ANDERSON", "FABRIEL", "TAILINE", "RAVEL", "ADRIANO", "FABIANO", "IVANIA", "FERNANDA"]

# Pontuação por classe
forca_classe = {"A": 6, "B": 4, "C": 3, "D": 1}


def filtrar_presentes(lista_presentes, todos_jogadores):
    """
    Retorna apenas os jogadores presentes com suas classes.
    Ex: {"ADRIANO": "A", "ERICK": "B", ...}
    """
    presentes_por_classe = {}
    for classe, nomes in todos_jogadores.items():
        for nome in nomes:
            if nome in lista_presentes:
                presentes_por_classe[nome] = classe
    return presentes_por_classe


def montar_times(jogadores_presentes, max_por_time=4):
    """
    Monta times equilibrados com base na pontuação das classes.
    """
    jogadores = list(jogadores_presentes.items())  # [(nome, classe), ...]
    random.shuffle(jogadores)  # embaralha para variar

    # Quantos times formados
    n_times = max(2, (len(jogadores) + max_por_time - 1) // max_por_time)

    # Estrutura dos times
    times = defaultdict(list)
    pontos = [0] * n_times  # controle da força de cada time

    # Distribui jogadores tentando equilibrar a soma dos pontos
    for nome, classe in sorted(jogadores, key=lambda x: forca_classe[x[1]], reverse=True):
        # Escolhe o time mais fraco no momento
        idx = min(range(n_times), key=lambda i: pontos[i])
        times[idx].append(nome)
        pontos[idx] += forca_classe[classe]

    return times, pontos


# ----------------- Execução principal -----------------
if __name__ == "__main__":
    jogadores_presentes = filtrar_presentes(presentes, todos_jogadores)
    times, pontos = montar_times(jogadores_presentes, max_por_time=5)

    print("\n--- TIMES SORTEADOS ---")
    print(f"Total de jogadores presentes: {len(presentes)}")
    print(f"Total de times formados: {len(times)}\n")

    for t, lista in times.items():
        print(f"Time {t+1} ({pontos[t]} pts): {', '.join(lista)}")
