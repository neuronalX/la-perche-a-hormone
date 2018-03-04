# -*- coding: utf-8 -*-
import numpy as np


proba_die = [0,0.2,0.4,0.6]

def change_sex_or_die(gender, polluants, depolluants):
    """
    Pour chaque poisson on calcule ce qu'il devient :
    - s'il meurt
    - s'il change de sex

    polluants[0] : féminise
    polluants[1] : masculinise
    polluants[2] : tue

    dépoluants agissent sur chaque polluant (apparié 1 à 1)

    """
    # niveau de polluants
    niv_pol = clean_up(polluants, depolluants)

    # est-ce que le poisson meurt ?
    if proba_die[niv_pol[2]] > np.random.uniform(0,1):
        return 'dead'
    # est-ce qu'il change de sexe ?
    elif 0.5 > np.random.uniform(0,1):
        if gender == "male":
            return "female"
        else:
            return "male"
    else:
        return gender





def clean_up(polluants, depolluants):
    """
    Dépolluer l'environnement

    Format des entrées :
    self.polluants = [0,0,0]
    self.depolluants = [0,0,0]
    """
    new_polluants = [None]*3
    # pour chaque couple polluant/dépolluant
    for i, (p, d) in enumerate(zip(polluants, depolluants)):
        #on soustrait la valeur du pollant en fonction de son dépolluant
        new_p = p - d
        # on remet à 0 si c'est négatif
        new_p = (new_p > 0) * new_p

        new_polluants[i] = new_p

    return new_polluants
