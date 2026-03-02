import math
from Bissection import Bissection
from pointfixe import pointfixe
def F(x):
    return math.exp(x) -  x/2 -5

resultat = Bissection(F, 1, 2, 0.5e-5, 18)
print(resultat)

# les lignes de codes ci dessous nous ont été utiliser pour calculer certaines valeurs pour le rapport
# si nous aurions utiliser une calculatrice nous aurions perdu de la précision

# pour la question d)
erreurO = math.exp(1.7726325988769531)
#print('erreurO = ', {erreurO})
rapporterreur = (erreurO) / 0.5
#print('erreur = ', {rapporterreur})

# pour la question e)
valeurO = math.exp(1.7726325988769531)
#print('valeurO = ', {valeurO})
valeurD = 5 - ((1.7726325988769531) / 2) 
#print('valeurD = ', {valeurD})

# --- Fonctions de point fixe (celles données dans l'énoncé) ---
def g1(Q: float) -> float:
    # g1(Q) = ln(5 - Q/2)
    return math.log(5 - Q / 2)


def g2(Q: float) -> float:
    # g2(Q) = 10 - 2 e^Q
    return 10 - 2 * math.exp(Q)

def f_newton(Q: float) -> float:
    # f(Q) = e^Q + Q/2 - 5
    return math.exp(Q) + Q / 2 - 5


def fp_newton(Q: float) -> float:
    # f'(Q) = e^Q + 1/2
    return math.exp(Q) + 0.5


def gN(Q: float) -> float:
    # Newton sous forme point fixe : Q_{n+1} = Q_n - f(Q_n)/f'(Q_n)
    return Q - f_newton(Q) / fp_newton(Q)


# --- Outil pour construire/afficher le tableau demandé ---
def construire_lignes_tableau(iterations: list[float], max_n: int | None = None) -> list[str]:
    """
    Retourne les lignes du tableau sous forme de strings, pour pouvoir les print.
    Colonnes:
      n, Qn, |en|≈|Qn-Qn-1|, |e(n+1)/e(n)|, |e(n+1)/e(n)^2|, |e(n+1)/e(n)^3|
    """
    N = len(iterations) - 1
    if max_n is None or max_n > N:
        max_n = N

    # e[n] = |Qn - Q(n-1)| (approx de l'erreur absolue)
    e = [None] * (max_n + 1)
    for n in range(1, max_n + 1):
        e[n] = abs(iterations[n] - iterations[n - 1])

    lignes = []
    entete = (
        f"{'n':>3} {'Qn':>20} {'|en|≈|Qn-Qn-1|':>18} "
        f"{'|e(n+1)/e(n)|':>16} {'|e(n+1)/e(n)^2|':>18} {'|e(n+1)/e(n)^3|':>18}"
    )
    lignes.append(entete)
    lignes.append("-" * len(entete))

    for n in range(0, max_n + 1):
        Qn = iterations[n]

        en_str = "-"
        if n >= 1:
            en_str = f"{e[n]:.9g}"

        r1_str = r2_str = r3_str = "-"
        if n >= 1 and n < max_n:
            en = e[n]
            en1 = e[n + 1]
            if en is not None and en1 is not None and en != 0:
                r1_str = f"{abs(en1 / en):.9g}"
                r2_str = f"{abs(en1 / (en**2)):.9g}"
                r3_str = f"{abs(en1 / (en**3)):.9g}"

        lignes.append(
            f"{n:>3} {Qn:>20.14f} {en_str:>18} {r1_str:>16} {r2_str:>18} {r3_str:>18}"
        )

    return lignes


def imprimer_tableau(iterations: list[float], titre: str, max_n: int | None = None) -> None:
    print("\n" + "=" * 100)
    print(titre)
    print("=" * 100)
    for ligne in construire_lignes_tableau(iterations, max_n=max_n):
        print(ligne)

# --- Steffensen (Aitken Δ²) ---
def steffensen(g):
    def gS(Q: float) -> float:
        y = g(Q)        # g(Q)
        z = g(y)        # g(g(Q))
        denom = z - 2*y + Q
        if denom == 0:
            return y    # fallback pour éviter division par 0
        return Q - (y - Q)**2 / denom
    return gS


if __name__ == "__main__":
    # Paramètres imposés par l'énoncé
    Q0 = 1.0
    tolr = 1e-8
    nmax = 150

    # --- g1 : tableau complet jusqu'à convergence ---
    it_g1 = pointfixe(g1, Q0, tolr, nmax)
    imprimer_tableau(
        it_g1,
        "Tableau (1) - Point fixe avec g1(Q) = ln(5 - Q/2) : convergence attendue d'ordre 1"
    )

    # --- g2 : seulement 5 premières itérations (jusqu'à Q5) ---
    it_g2 = pointfixe(g2, Q0, tolr, nmax)
    imprimer_tableau(
        it_g2,
        "Tableau (2) - Point fixe avec g2(Q) = 10 - 2 e^Q : divergence attendue (afficher jusqu'à Q5)",
        max_n=5
    )
    it_gN = pointfixe(gN, Q0, tolr, nmax)

    with open("tableau_newton.txt", "w", encoding="utf-8") as f:
        f.write("Tableau (3) - Newton\n")
        for ligne in construire_lignes_tableau(it_gN):
            f.write(ligne + "\n")
    
    imprimer_tableau(
        it_gN,
        "Tableau (3) - Newton via gN(Q) = Q - f(Q)/f'(Q) : convergence attendue d'ordre 2"
    )

    # --- m) Steffensen sur g1, g2, gN ---
    g1S = steffensen(g1)
    g2S = steffensen(g2)
    gNS = steffensen(gN)

    it_g1S = pointfixe(g1S, Q0, tolr, nmax)
    it_g2S = pointfixe(g2S, Q0, tolr, nmax)
    it_gNS = pointfixe(gNS, Q0, tolr, nmax)

    # Réutilise EXACTEMENT la même fonction d'affichage que pour j/l
    imprimer_tableau(it_g1S, "Tableau (4) - Steffensen appliqué à g1")
    imprimer_tableau(it_g2S, "Tableau (5) - Steffensen appliqué à g2 (jusqu'à Q10)", max_n=10)
    imprimer_tableau(it_gNS, "Tableau (6) - Steffensen appliqué à gN (Newton)")