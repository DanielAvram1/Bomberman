def alpha_beta(state, estimate, alpha=float('-inf'), beta=float('inf')):
    nr_noduri = 1
    # daca sunt la o frunza in arborele alpha-beta sau la o stare finala
    if state.depth == 0 or state.is_final(state.current, state.opponent)\
            or state.is_final(state.opponent, state.current):
        state.estimation = estimate(state)
        return state, nr_noduri

    if alpha > beta:
        return state, nr_noduri  # este intr-un interval invalid deci nu o mai procesez

    possible_moves = state.generate_moves()


    if len(possible_moves) == 0:
        state.estimation = float('-inf')
        return state, nr_noduri

    if state.current.is_max:
        possible_moves = sorted(possible_moves, key=lambda x: estimate(x), reverse=True)
        curr_estimation = float('-inf')  # in aceasta variabila calculam maximul



        for move in possible_moves:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            new_state, curr_nr_noduri = alpha_beta(move, estimate, alpha, beta)  # aici construim subarborele pentru stare_noua
            nr_noduri += curr_nr_noduri
            if curr_estimation < new_state.estimation:
                state.next_state = new_state
                curr_estimation = new_state.estimation
            if alpha < new_state.estimation:
                alpha = new_state.estimation
                if alpha >= beta:
                    break
    else:
        curr_estimation = float('inf')
        possible_moves = sorted(possible_moves, key=lambda x: estimate(x))
        for move in possible_moves:
            # calculeaza estimarea
            new_state, curr_nr_noduri = alpha_beta(move, estimate, alpha, beta)  # aici construim subarborele pentru stare_noua
            nr_noduri += curr_nr_noduri
            if (curr_estimation > new_state.estimation):
                state.next_state = new_state
                curr_estimation = new_state.estimation
            if (beta > new_state.estimation):
                beta = new_state.estimation
                if alpha >= beta:
                    break
    if state.next_state is None:
        state.estimation = estimate(state)
    else:
        state.estimation = state.next_state.estimation
    return state, nr_noduri
