import networkx as nx

def sucesores_lista_S(Pert,S):
    sucesores = []
    for i in range(len(S)):
        for j in Pert.successors(S[i]):
            if j not in sucesores:
                sucesores.append(j)
    return sucesores

def predecesores_lista_sucesores(Pert,sucesores):
    diccionario_de_predecesores = {}
    for i in range(len(sucesores)):
        predecesores_de_cada_sucesor = []
        for j in Pert.predecessors(sucesores[i]):
            predecesores_de_cada_sucesor.append(j)
        diccionario_de_predecesores[sucesores[i]] = predecesores_de_cada_sucesor
    return diccionario_de_predecesores


def valor_a(Pert,predecesores_dic,indice,diccionario_a):
    maximo = []
    for i in range(len(predecesores_dic[indice])):
        maximo.append(diccionario_a[predecesores_dic[indice][i]] + Pert[predecesores_dic[indice][i]][indice]['weight'])
    return max(maximo)

def valor_b(Pert,diccionario_b,indice,sucesores):
    minimo = []
    for i in range(len(sucesores)):
        minimo.append(diccionario_b[sucesores[i]] - Pert[indice][sucesores[i]]['weight'])
    return min(minimo)

def holguras(Pert,diccionario_a,diccionario_b):
    arcos = list(Pert.edges)
    holguras = {}
    for i in range(len(arcos)):
            holguras[(arcos[i][0],arcos[i][1])] = diccionario_b[arcos[i][1]] - diccionario_a[arcos[i][0]] - Pert[arcos[i][0]][arcos[i][1]]['weight']
    return holguras

def PERT(Pert,I,F):
    S = [I]
    a = {I : 0}
    while len(S) != len(Pert.nodes):
        sucesores = sucesores_lista_S(Pert,S)
        predecesores = predecesores_lista_sucesores(Pert,sucesores)
        for i in range(len(sucesores)):
            if sucesores[i] not in S: 
                if set(predecesores[sucesores[i]]) <= set(S):
                    a[sucesores[i]] = valor_a(Pert,predecesores,sucesores[i],a)
                    S.append(sucesores[i])

    S = [F]
    b = {F : a[F]}
    while len(S) != len(Pert.nodes):
        predecesores = predecesores_lista_sucesores(Pert,S)
        for i in predecesores:
            sucesores = predecesores[i]
            for j in sucesores:
                if j not in S:
                    if set(sucesores_lista_S(Pert,[j])) <= set(S):
                        b[j] = valor_b(Pert,b,j,sucesores_lista_S(Pert,[j]))
                        S.append(j)

    Holguras = holguras(Pert,a,b)
    Ruta_critica = []
    for i in Holguras:
        if Holguras[i] == 0:
            Ruta_critica.append(i)


    print(f'Calendario de fechas mas próximas: {a}\nCalendario de fechas mas lejanas: {b}\nHolguras: {Holguras}\nRuta critica: {Ruta_critica}')
    nx.draw_planar(Pert)