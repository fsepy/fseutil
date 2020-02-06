

def clause_15_6_6_e_merging_flow_1(
        N: float,
        X: float,
        D: float,
        S_up: float,
        W_SE: float,
):
    """Calculates merging flow at final exit level in accordance with Figure 6 (1 of 3) in BD 9999:2017, page 68.
    Merging flow from stair with storey exit at final exit level.

    :param N: is the number of people served by the final exit level storey exit.
    :param D: is the lesser distance from the final exit level storey exit or the lowest riser from the upward portion of the stair, in metres (m).
    :param S_up: is the stair width for the upward portion of the stair, in millimetres (mm).
    :param W_SE: is the width of the final exit level storey exit, in millimetres (mm).
    :param X: is the minimum door width per person (see 16.6 and Clause 18), in millimetres (mm).
    :return W_FE: is the width of the final exit, in millimetres (mm).
    """

    # convert unit
    S_up *= 1000.  # [m] -> [mm]
    W_SE *= 1000.  # [m] -> [mm]
    X *= 1000.  # [m] -> [mm]

    # calculate exit capacity
    if N > 60 and D < 2:
        W_FE = S_up + W_SE
    else:
        W_FE = N * X + 0.75 * S_up

    # check against absolute minimum width
    W_FE = max([W_FE, S_up])

    # convert unit
    W_FE /= 1000.  # [mm] -> [m]

    return W_FE
