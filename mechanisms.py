# -*- coding: utf-8 -*-
import numpy as np

# Constantes que l'on peut changer en fonction des tests de jouabilité
# probabilités de mourir
proba_die = [0,0.2,0.4,0.6]
# probabilité du pollant de faire changer de sexe (identique pour chaque polluant)
proba_pol = [0,0.25,0.50,0.75]
# # # gender id
# l_genders = ['male', 'intersexe', 'female']
nr_boucles_changement_sexe = 2


def change_sex_or_die(gender, polluants, depolluants, verbose=False):
    """
    Pour chaque poisson on calcule ce qu'il devient :
    - s'il meurt
    - s'il change de sexe
    La probabilité de changé de sexe est appliqué un nombre de fois défini par nr_boucles_changement_sexe

    Inputs:
        - gender : string:
            'male', 'female'
        - polluants : [int, int, int]
            polluants[0] : féminise
            polluants[1] : masculinise
            polluants[2] : tue
        - depolluants
            dépoluants agissent sur chaque polluant (apparié 1 à 1)

    Outputs :
        new_sex : string: 'dead', 'male', 'female', 'intersexe'


    """
    # niveau de polluants
    niv_pol = clean_up(polluants, depolluants)
    if verbose:
        print("polluants:")
        print(polluants)
        print("niv_pol:")
        print(niv_pol)

    # est-ce que le poisson meurt ?
    if proba_die[niv_pol[2]] > np.random.uniform(0,1):
        return 'dead'

    if gender == "male":
        g_id = 0
    elif gender == "female" or gender == "femelle":
        g_id = 2

    # on exécute nr_boucles fois l'action, une fois pour chaque polluant
    for i in range(nr_boucles_changement_sexe):
        if verbose:
            print("begin: g_id", g_id)
        # on applique la proba du polluant féminisant
        if proba_pol[niv_pol[0]] > np.random.uniform(0,1):
            g_id += 1
            if verbose:
                print("after fem: g_id", g_id)
        # on applique la proba du polluant masculinisant
        if proba_pol[niv_pol[1]] > np.random.uniform(0,1):
            g_id -= 1
            if verbose:
                print("after masc: g_id", g_id)
    if verbose:
        print("FINAL g_id:", g_id)

    # on détermine le sexe final du poisson
    new_sex = None
    if g_id < 0.666:
        new_sex = "male"
    elif g_id < 1.333:
        new_sex = "intersexe"
    elif g_id >= 1.333:
        new_sex = "female"
    else:
        print("ERROR: VALUE IMPOSSIBLE")

    return new_sex




    # Default for william
    # # est-ce qu'il change de sexe ?
    # elif 0.5 > np.random.uniform(0,1):
    #     if gender == "male":
    #         return "female"
    #     else:
    #         return "male"
    # else:
    #     return gender






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
