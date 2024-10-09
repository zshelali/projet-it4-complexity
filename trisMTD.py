import random
import time
import matplotlib.pyplot as plt
import copy
import sys
import multiprocessing as mp
from multiprocessing.pool import ThreadPool



sys.setrecursionlimit(10000)

def isSorted(l):
    return all(l[i] <= l[i + 1] for i in range(len(l) - 1))

def areSorted(ll):
    for i, l in enumerate(ll):
        if not isSorted(l):
            return (False, i)
    return (True, 0)

def create_data(nlist=15, nval=200):
    listDataRandom = []
    listDataSorted = []
    listDataInversedSorted = []
    sizeArrays = []

    for i in range(1, nlist + 1):
        s = nval * i
        dataRandom = list(range(s))
        dataSorted = list(range(s))
        dataInversed = list(range(s))
        dataInversed.reverse()
        random.shuffle(dataRandom)

        listDataRandom.append(dataRandom)
        listDataSorted.append(dataSorted)
        listDataInversedSorted.append(dataInversed)
        sizeArrays.append(s)

    return sizeArrays, listDataRandom, listDataSorted, listDataInversedSorted

def sort_and_time(fct_tri, data, surplace):
    """Fonction de tri et de mesure du temps pour multiprocessing."""
    start = time.perf_counter()
    if surplace:
        fct_tri(data)
    else:
        data = fct_tri(data)
    end = time.perf_counter()
    return end - start

def executerTriMTD(fct_tri, color, nom, nlist=15, nval=200, surplace=True):
    axis, listDataRandom, listDataSorted, listDataInvertedSorted = create_data(nlist, nval)
    toplotRandom = []
    toplotSorted = []
    toplotInverted = []

    dataTestRandom = copy.deepcopy(listDataRandom)
    dataTestSorted = copy.deepcopy(listDataSorted)
    dataTestInverted = copy.deepcopy(listDataInvertedSorted)

    with ThreadPool(processes=mp.cpu_count()) as pool:
        toplotRandom = pool.starmap(sort_and_time, [(fct_tri, dataTestRandom[i], surplace) for i in range(len(axis))])
        toplotSorted = pool.starmap(sort_and_time, [(fct_tri, dataTestSorted[i], surplace) for i in range(len(axis))])
        toplotInverted = pool.starmap(sort_and_time, [(fct_tri, dataTestInverted[i], surplace) for i in range(len(axis))])

    (ok1, ipb1) = areSorted(dataTestRandom)
    (ok2, ipb2) = areSorted(dataTestSorted)
    (ok3, ipb3) = areSorted(dataTestInverted)

    if not ok1:
        print(nom + ' data random incorrect, liste #' + str(ipb1))
    else:
        plt.plot(axis, toplotRandom, '-' + color, label=nom + ' (random)')
    if not ok2:
        print(nom + ' data Sorted incorrect, liste #' + str(ipb2))
    else:
        plt.plot(axis, toplotSorted, '--' + color, label=nom + ' (Sorted)')
    if not ok3:
        print(nom + ' data Inverted incorrect, liste #' + str(ipb3))
    else:
        plt.plot(axis, toplotInverted, ':' + color, label=nom + ' (Inverted)')
    plt.legend()
    plt.xlabel("Taille des tableaux")
    plt.ylabel("Temps d'exécution (s)")
    plt.title(f"Performance de {nom}")
    plt.show()


# tempsF = 0

# def bubble_sort(A):
#     global tempsF
#     temps1 = time.perf_counter()  # Enregistrer l'heure de début avec haute précision
#     n = len(A)
#     flag = 1
#     for i in range(n-1):
#         flag = 0
#         for j in range(n-1-i):
#             if A[j] > A[j+1]:            
#                 A[j], A[j+1] = A[j+1], A[j]  # Échange des éléments
#                 flag = 1
#         if flag == 0:  # Si aucun échange n'a été fait, le tableau est déjà trié
#             break
#     temps2 = time.perf_counter()  # Enregistrer l'heure de fin
#     tempsF = temps2 - temps1  
#     return A


# executerTriMTD(bubble_sort, 'r', 'Bubble sort')