# pointfixe.py
# MAT-2910 Devoir 2 - méthode du point fixe

from typing import Callable, List


def pointfixe(
    fonction_pointfixe: Callable[[float], float],
    Q0: float,
    tolr: float,
    nmax: int
) -> List[float]:
    """
    Calcule les itérations de la méthode du point fixe : Q_{n+1} = g(Q_n)

    Paramètres
    ----------
    fonction_pointfixe : Callable[[float], float]
        La fonction g(Q) dont on cherche un point fixe.
    Q0 : float
        Valeur initiale.
    tolr : float
        Tolérance sur l'erreur relative (critère d'arrêt).
    nmax : int
        Nombre maximal d'itérations.

    Retour
    ------
    iterations : list[float]
        Liste contenant Q0, Q1, ..., Qn.
    """
    if nmax < 0:
        raise ValueError("nmax doit être >= 0")
    if tolr <= 0:
        raise ValueError("tolr doit être > 0")

    iterations: List[float] = [float(Q0)]

    # Cas trivial: si nmax == 0, on retourne seulement Q0
    if nmax == 0:
        return iterations

    for _ in range(nmax):
        Qn = iterations[-1]
        Qnp1 = float(fonction_pointfixe(Qn))
        iterations.append(Qnp1)

        # Erreur relative ~ |Q_{n+1} - Q_n| / |Q_{n+1}|
        denom = abs(Qnp1)
        if denom == 0.0:
            # Si Q_{n+1} = 0, on tombe sur une erreur relative non définie.
            # On utilise alors l'erreur absolue comme critère.
            err_rel = abs(Qnp1 - Qn)
        else:
            err_rel = abs(Qnp1 - Qn) / denom

        if err_rel < tolr:
            break

    return iterations