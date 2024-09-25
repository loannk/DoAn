import heapq
import pandas as pd

class Node:
    def __init__(self, state, g=0, h=0, parent=None, action=None):
        self.state = state  # Current set of substances
        self.g = g  # Cost from start to node
        self.h = h  # Heuristic cost from node to goal
        self.f = g + h  # Total cost
        self.parent = parent  # Parent node
        self.action = action  # Action leading to this node

    def __lt__(self, other):
        return self.f < other.f

def heuristic(state, goal):
    return len(goal - state)

def a_star(F, A, B):
    open_list = []
    closed_list = set()
    start_node = Node(A, 0, heuristic(A, B))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if B.issubset(current_node.state):
            path = []
            node = current_node
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return True, path

        closed_list.add(frozenset(current_node.state))

        for reaction in F:
            reactants, products = reaction[1], reaction[2]
            if reactants.issubset(current_node.state):
                new_state = current_node.state.union(products)
                if frozenset(new_state) in closed_list:
                    continue

                g = current_node.g + 1
                h = heuristic(new_state, B)
                new_node = Node(new_state, g, h, current_node, reaction)

                heapq.heappush(open_list, new_node)

    return False, []

def MangTinhToan(F, A, B):
    sol = []
    Aold = set()
    if B.issubset(A):
        return [True, sol]

    solFound = False
    while not solFound and A != Aold:
        Aold = A.copy()
        for reaction in F[:]:
            reactants, products = reaction[1], reaction[2]
            M = reactants.union(products)
            v = products
            temp = M.difference(A)
            if temp.issubset(v):
                A.update(products)
                A.update(reactants)
                sol.append(reaction)
                F.remove(reaction)
            if B.issubset(A):
                solFound = True
                break

    return solFound, sol

def ktra_loigiai(F, A, B):
    A_temp = A.copy()
    solFound = False
    for reaction in F:
        reactants, products = reaction[1], reaction[2]
        M = reactants.union(products)
        v = products
        temp = M.difference(A_temp)
        if temp.issubset(v):
            A_temp.update(products)
            A_temp.update(reactants)
        if B.issubset(A_temp):
            solFound = True
            break
    return solFound

def loiGiaiTot(F, A, B):
    D = F.copy()
    for reaction in F[:]:
        D_temp = [x for x in D if x != reaction]
        if ktra_loigiai(D_temp, A, B):
            D = D_temp
    return D

def Rutgon_giathiet(F, A, B):
    A_ = A.copy()
    A_temp = A.copy()
    Aold = None
    while A != Aold:
        Aold = A.copy()
        for x in A:
            temp = A_temp.difference({x})
            Anew = A_.difference({x})
            result = ktra_loigiai(F, temp, B)
            if result:
                A_ = Anew
    return A_

def Baodong(F, reactants):
    B = set(reactants)
    B1 = set()
    sol = []
    while B != B1:
        B1 = B.copy()
        for reaction in F[:]:
            reactants, products = reaction[1], reaction[2]
            M = reactants.union(products)
            v = products
            temp = M.difference(B)
            if temp.issubset(v):
                B.update(products)
                sol.append(reaction)
                F.remove(reaction)
    return B, sol

def ChuoiPU(F, chuoi):
    result = []

    for i in range(len(chuoi) - 1):
        found = False
        for reaction in F:
            reactants, products = reaction[1], reaction[2]
            if chuoi[i] in reactants and chuoi[i + 1] in products:
                result.append(reaction)
                found = True
                break
        if not found:
            return ["Khong co du co so tri thuc"]
    if len(result) == len(chuoi) - 1:
        return result

def tim_pu(F, A, B):
    result = []
    found = False
    for reaction in F:
        reactants, products = reaction[1], reaction[2]
        if A.issubset(reactants) and B.issubset(products):
            result.append(reaction)
            found = True
            break
    if found:
        return [True, result]
    else:
        return [False, []]

def read_excel(file_path):
    df = pd.read_excel(file_path)
    reactions = []
    for index, row in df.iterrows():
        reaction_name = row['stt']
        reactants = set(row['chatpu'].upper().split(','))
        products = set(row['sp'].upper().split(','))
        reactions.append([reaction_name, reactants, products])
    return reactions

def MTT(file_path, A, B, chuoi):
    F = read_excel(file_path)

    # Step 1: Reduce hypothesis
    Anew = Rutgon_giathiet(F, A, B)
    Atemp = Anew.copy()

    # Step 2: Solve the main problem
    result = MangTinhToan(F.copy(), Anew, B)
    if result[0]:
        best_result = loiGiaiTot(result[1], Atemp, B)
        main_reactions = best_result
    else:
        result1 = tim_pu(F, Anew, B)
        if result1[0]:
            main_reactions = result1[1]
        else:
            main_reactions = []

    chain_reactions = ChuoiPU(F, chuoi)

    return main_reactions, chain_reactions

def baodong(file_path, C):
    F = read_excel(file_path)
    closure, closure_reactions = Baodong(F, C)
    return closure, closure_reactions

def LoigiaiToiUu(file_path, A, B):
    F = read_excel(file_path)
    found, solution = a_star(F, A, B)
    return found, solution
