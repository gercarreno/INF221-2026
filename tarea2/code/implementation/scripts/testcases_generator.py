"""
Este codigo debe generar casos de prueba para los algoritmos implementados en C++, en la carpeta code/implementation/data/inputs/
"""

import os
import random
import string
import sys


def random_anime_name(length=10):
    # Strings formados por letras minúsculas, números o guiones bajos, sin espacios.
    chars = string.ascii_lowercase + string.digits + "_"
    return "".join(random.choices(chars, k=length))

def generate_test_case(filename, n):
    # Asegurar que Q <= 700, q_i <= 30 y que cada anime tenga al menos 1 capítulo
    q_list = []
    Q_remaining = 700
    for i in range(n):
        animes_left = n - 1 - i
        # q_i máximo es 30, pero no puede consumir lo que necesitan los demás para tener al menos 1
        max_q = min(30, Q_remaining - animes_left)
        if max_q < 1:
            max_q = 1

        q_i = random.randint(1, max_q)
        q_list.append(q_i)
        Q_remaining -= q_i

    M = random.randint(1, 3000)
    E = random.randint(1, 500)

    with open(filename, "w", encoding="utf-8") as f:
        # Primera línea: n M E
        f.write(f"{n} {M} {E}\n")

        for i in range(n):
            anime_name = random_anime_name(random.randint(5, 15))
            b_i = random.randint(0, 10**9)
            q_i = q_list[i]

            # Línea de anime: anime_i q_i b_i
            f.write(f"{anime_name} {q_i} {b_i}\n")

            # Líneas de capítulos: t_i,j c_i,j v_i,j
            for _ in range(q_i):
                t_ij = random.randint(1, 300)
                c_ij = random.randint(1, 100)
                v_ij = random.randint(1, 10**9)
                f.write(f"{t_ij} {c_ij} {v_ij}\n")


def main():
    # Tipos de casos
    # n ∈ {3,5,8}       casos pequeños
    # n ∈ {20,40,80}    casos medianos
    # n ∈ {100,150,200} casos grandes
    SMALL_NS = [3, 5, 8]
    MEDIUM_NS = [20, 40, 80]
    LARGE_NS = [100, 150, 200]

    cases_per_n = 3

    # --small | --medium | --large
    args = sys.argv[1:]
    if "--small" in args:
        ns_to_generate = SMALL_NS
    elif "--medium" in args:
        ns_to_generate = MEDIUM_NS
    elif "--large" in args:
        ns_to_generate = LARGE_NS
    else:
        ns_to_generate = SMALL_NS + MEDIUM_NS + LARGE_NS  # completa por defecto

    output_dir = "./data/inputs/"
    os.makedirs(output_dir, exist_ok=True)

    total = 0
    for n in ns_to_generate:
        for i in range(1, cases_per_n + 1):
            # testcases_{n}_{i}.txt
            filename = os.path.join(output_dir, f"testcases_{n}_{i}.txt")
            generate_test_case(filename, n)
            print(f"  Generado: testcases_{n}_{i}.txt")
            total += 1

    print(f"\n{total} casos generados en '{output_dir}'.")


if __name__ == "__main__":
    main()
