# coding: utf-8

# import numpy
import math
from statistics import median


def phi_parallel_corner_br187(W_m, H_m, S_m, multiplier=1):
    """

    :param W_m: width of emitter panel
    :param H_m: height of emitter panel
    :param S_m: separation distance from EMITTER TO RECEIVER
    :return phi: configuration factor
    """

    # Calculate view factor, phi
    X = W_m / S_m
    Y = H_m / S_m
    a = 1 / 2 / math.pi
    b = X / (1 + X ** 2) ** 0.5
    c = math.atan(Y / (1 + X ** 2) ** 0.5)
    d = Y / (1 + Y ** 2) ** 0.5
    e = math.atan(X / (1 + Y ** 2) ** 0.5)
    phi = a * (b * c + d * e)

    return phi * multiplier


def phi_perpendicular_corner_br187(W_m, H_m, S_m, multiplier=1):
    """

    :param W_m:
    :param H_m:
    :param S_m:
    :param multiplier:
    :return:
    """
    X = W_m / S_m
    Y = H_m / S_m

    a = 1 / 2 / math.pi
    b = math.atan(X)
    c = 1 / (Y ** 2 + 1) ** 0.5
    d = math.atan(X / (Y ** 2 + 1) ** 0.5)

    phi = a * (b - c * d)

    return phi * multiplier


def phi_parallel_any_br187(W_m, H_m, w_m, h_m, S_m):
    r"""
    Equation in LaTeX \phi=\frac{1}{2\pi}\left(\frac{X}{\sqrt{1+X^2}}\cdot\tan^{-1}\left({\frac{Y}{\sqrt{1+X^2}}}\right)
    +\frac{Y}{\sqrt{1+Y^2}}\cdot\tan^{-1}\left({\frac{X}{\sqrt{1+Y^2}}}\right)\right)
    :param W_m:
    :param H_m:
    :param w_m:
    :param h_m:
    :param S_m:
    :return:
    """
    phi = [
        phi_parallel_corner_br187(*P[0:-1], S_m, P[-1])
        for P in four_planes(W_m, H_m, w_m, h_m)
    ]
    return sum(phi)


def phi_perpendicular_any_br187(W_m, H_m, w_m, h_m, S_m):
    four_P = four_planes(W_m, H_m, w_m, h_m)
    phi = [phi_perpendicular_corner_br187(*P[0:-1], S_m, P[-1]) for P in four_P]
    return sum(phi)


def four_planes(W_m: float, H_m: float, w_m: float, h_m: float) -> tuple:
    """

    :param W_m:
    :param H_m:
    :param w_m:
    :param h_m:
    :return:
    """

    # COORDINATES
    o = (0, 0)
    e1 = (0, 0)
    e2 = (W_m, H_m)
    r1 = (w_m, h_m)

    # GLOBAL MIN, MEDIAN AND MAX
    min_ = (min([W_m, w_m, 0]), min([H_m, h_m, 0]))
    mid_ = (median([W_m, w_m, 0]), median([H_m, h_m, 0]))
    max_ = (max([W_m, w_m, 0]), max([H_m, h_m, 0]))

    # FOUR PLANES
    A = 0, 0, 0
    B = 0, 0, 0
    C = 0, 0, 0
    D = 0, 0, 0

    # RECEIVER AT CORNER
    if e1 == e2 or e1 == r1 or e1 == (e2[0], r1[1]) or e1 == (r1[0], e2[1]):
        A = (max_[0] - min_[0], max_[1] - min_[1], 1)
        B = (0, 0, 0)
        C = (0, 0, 0)
        D = (0, 0, 0)

        # A = phi_parallel_corner_br187(*A, S_m)
        #
        # phi = A

    # RECEIVER ON EDGE
    elif ((r1[0] == e1[0] or r1[0] == e2[0]) and e1[1] < r1[1] < e2[1]) or (
        (r1[1] == e1[1] or r1[1] == e2[1]) and e1[0] < r1[0] < e2[0]
    ):
        # vertical edge
        if (r1[0] == e1[0] or r1[0] == e2[0]) and e1[1] < r1[1] < e2[1]:
            A = (max_[0] - min_[0], max_[1] - mid_[1], 1)
            B = (max_[0] - min_[0], mid_[1] - min_[1], 1)
            C = (0, 0, 0)
            D = (0, 0, 0)

        # horizontal edge
        elif (r1[1] == e1[1] or r1[1] == e2[1]) and e1[0] < r1[0] < e2[0]:
            A = (max_[0] - mid_[0], max_[1] - min_[1], 1)
            B = (mid_[0] - min_[0], max_[1] - min_[1], 1)
            C = (0, 0, 0)
            D = (0, 0, 0)
        else:
            print("error")

    # RECEIVER WITHIN EMITTER
    elif o[0] < w_m < W_m and o[1] < h_m < H_m:
        A = (mid_[0] - min_[0], mid_[1] - min_[1], 1)
        B = (max_[0] - mid_[0], max_[1] - mid_[1], 1)
        C = (mid_[0] - min_[0], max_[1] - mid_[1], 1)
        D = (max_[0] - mid_[0], mid_[1] - min_[1], 1)

    # RECEIVER OUTSIDE EMITTER
    else:
        # within y-axis range max[1] and min[1], far right
        if min_[1] < r1[1] < max_[1] and r1[0] == max_[0]:
            A = max_[0] - min_[0], max_[1] - mid_[1], 1
            B = max_[0] - min_[0], mid_[1] - min_[1], 1
            C = max_[0] - mid_[0], max_[1] - mid_[1], -1  # negative
            D = max_[0] - mid_[0], mid_[1] - min_[1], -1  # negative
        # within y-axis range max[1] and min[1], far left
        elif min_[1] < r1[1] < max_[1] and r1[0] == min_[0]:
            A = max_[0] - min_[0], max_[1] - mid_[1], 1
            B = max_[0] - min_[0], mid_[1] - min_[1], 1
            C = mid_[0] - min_[0], max_[1] - mid_[1], -1  # negative
            D = mid_[0] - min_[0], mid_[1] - min_[1], -1  # negative
        # within x-axis range max[0] and min[0], far top
        elif min_[0] < r1[0] < max_[0] and r1[1] == max_[1]:
            A = max_[0] - mid_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], max_[1] - min_[1], 1
            C = max_[0] - mid_[0], max_[1] - mid_[1], -1
            D = mid_[0] - min_[0], max_[1] - mid_[1], -1
        # within x-axis range max[0] and min[0], far bottom
        elif min_[0] < r1[0] < max_[0] and r1[1] == min_[1]:
            A = max_[0] - mid_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], max_[1] - min_[1], 1
            C = max_[0] - mid_[0], mid_[1] - min_[1], -1
            D = mid_[0] - min_[0], mid_[1] - min_[1], -1
        # receiver out, within 1st quadrant
        elif r1[0] == max_[0] and r1[1] == max_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = max_[0] - mid_[0], max_[1] - mid_[1], 1
            C = max_[0] - mid_[0], max_[1] - min_[1], -1
            D = max_[0] - min_[0], max_[1] - mid_[1], -1
        # receiver out, within 2nd quadrant
        elif r1[0] == max_[0] and r1[1] == min_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = max_[0] - mid_[0], mid_[1] - min_[1], 1
            C = max_[0] - min_[0], mid_[1] - min_[1], -1
            D = max_[0] - mid_[0], max_[1] - min_[1], -1
        # receiver out, within 3rd quadrant
        elif r1[0] == min_[0] and r1[1] == min_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], mid_[1] - min_[1], 1
            C = mid_[0] - min_[0], max_[1] - min_[1], -1
            D = max_[0] - min_[0], mid_[1] - min_[1], -1
        # receiver out, within 4th quadrant
        elif r1[0] == min_[0] and r1[1] == max_[1]:
            A = max_[0] - min_[0], max_[1] - min_[1], 1
            B = mid_[0] - min_[0], max_[1] - mid_[1], 1
            C = mid_[0] - min_[0], max_[1] - min_[1], -1
            D = max_[0] - min_[0], max_[1] - mid_[1], -1
        # unkown
        else:
            return math.nan, math.nan, math.nan

    return A, B, C, D


def test_phi_parallel_any_br187():

    # All testing values are taken from independent sources

    # check receiver at emitter corner
    assert abs(phi_parallel_any_br187(*(10, 10, 0, 0, 10)) - 0.1385316060) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 0, 10, 10)) - 0.1385316060) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 10, 10, 10)) - 0.1385316060) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 10, 0, 10)) - 0.1385316060) < 1e-8

    # check receiver on emitter edge
    assert abs(phi_parallel_any_br187(*(10, 10, 2, 0, 10)) - 0.1638694545) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 2, 10, 10)) - 0.1638694545) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 0, 2, 10)) - 0.1638694545) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 10, 2, 10)) - 0.1638694545) < 1e-8

    # check receiver within emitter, center
    assert abs(phi_parallel_any_br187(*(10, 10, 5, 5, 10)) - 0.2394564705) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 2, 2, 10)) - 0.1954523349) < 1e-8

    # check receiver fall outside, side ways
    assert abs(phi_parallel_any_br187(*(10, 10, 5, 15, 10)) - 0.0843536644) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 5, -5, 10)) - 0.0843536644) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 15, 5, 10)) - 0.0843536644) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, -5, 5, 10)) - 0.0843536644) < 1e-8

    # check receiver fall outside, 1st quadrant
    assert abs(phi_parallel_any_br187(*(10, 10, 20, 15, 10)) - 0.0195607021) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, 20, -5, 10)) - 0.0195607021) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, -10, -5, 10)) - 0.0195607021) < 1e-8
    assert abs(phi_parallel_any_br187(*(10, 10, -10, 15, 10)) - 0.0195607021) < 1e-8


def test_phi_perpendicular_any_br187():

    # All testing values are taken from independent sources

    # check receiver at emitter corner
    assert abs(phi_perpendicular_any_br187(10, 10, 0, 0, 10) - 0.05573419700) < 1e-8

    # check receiver on emitter edge
    assert abs(phi_perpendicular_any_br187(10, 10, 2, 0, 10) - 0.06505816388) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 2, 10, 10) - 0.06505816388) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 0, 2, 10) - 0.04656468770) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 10, 2, 10) - 0.04656468770) < 1e-8

    # check receiver fall outside, side ways
    assert abs(phi_perpendicular_any_br187(10, 10, 5, -10, 10) - 0.04517433814) < 1e-8
    assert abs(phi_perpendicular_any_br187(10, 10, 5, 20, 10) - 0.04517433814) < 1e-8


if __name__ == "__main__":
    test_phi_perpendicular_any_br187()
    test_phi_parallel_any_br187()
