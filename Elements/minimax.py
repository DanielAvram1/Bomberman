
def min_max(state, estimate):
    nr_noduri = 1
    # daca sunt la o frunza in arborele minimax sau la o stare finala
    if state.depth == 0 or state.is_final(state.current, state.opponent)\
            or state.is_final(state.opponent, state.current):
        state.estimation = estimate(state)
        return state, nr_noduri

    # calculez toate mutarile posibile din starea curenta
    possible_moves = state.generate_moves()

    if len(possible_moves) == 0:
        state.estimation = float('-inf')
        return state, nr_noduri

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    moves_with_estimations = [min_max(x, estimate) for x in possible_moves]  # expandez(constr subarb) fiecare nod x din mutari posibile


    if state.current.is_max:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        for m in moves_with_estimations:
            nr_noduri += m[1]
        state.next_state, _ = max(moves_with_estimations, key=lambda x: x[0].estimation)  # def f(x): return x.estimare -----> key=f
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        for m in moves_with_estimations:
            nr_noduri += m[1]
        state.next_state, _ = min(moves_with_estimations, key=lambda x: x[0].estimation)

    state.estimation = state.next_state.estimation
    return state, nr_noduri