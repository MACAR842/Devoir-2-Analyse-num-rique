import math
from Bissection import Bissection
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