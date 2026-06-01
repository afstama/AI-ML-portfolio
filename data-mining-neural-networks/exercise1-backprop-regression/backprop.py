import math

def sigma(x):
    return 1/(1+math.e**(-x))

def dSigma(x):
    s = sigma(x)
    return s*(1-s)


def backprop(w_ye1, w_ye2, b_y, w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, x1, x2, x3):
    e1 = w_e1x1*x1+w_e1x2*x2+b_e1
    e2 = w_e2x1*x1+w_e2x2*x2+b_e2

    y = w_ye1*sigma(e1)+w_ye2*sigma(e2)+b_y

    dy = (x3-y)
    de1 = dy*dSigma(e1)
    de2 = dy*dSigma(e2)

    dw_ye1 = w_ye1-dy*e1
    dw_ye2 = w_ye2-dy*e2
    db_y = b_y-dy
    dw_e1x1 = w_e1x1-de1*x1
    dw_e1x2 = w_e1x2-de1*x2
    dw_e2x1 = w_e2x1-de2*x1
    dw_e2x2 = w_e2x2-de2*x2
    db_e1 = b_e1-de1
    db_e2 = b_e2-de2

    return dw_e1x1, dw_e1x2, db_e1, dw_e2x1, dw_e2x2, db_e2, dw_ye1, dw_ye2, db_y

# x1 = 1
# x2 = 1
# x3 = -1

# w_ye1 = -0.5
# w_ye2 = 2.3
# b_y = 0.4
# w_e1x1 = 0.2
# w_e1x2 = -1.2
# b_e1 = 0.4
# w_e2x1 = -0.7
# w_e2x2 = -0.7
# b_e2 = 0.7

# w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, w_ye1, w_ye2, b_y = backprop(w_ye1, w_ye2, b_y, w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, x1, x2, x3)

# x1 = 0
# x2 = -2
# x3 = 1

# w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, w_ye1, w_ye2, b_y = backprop(w_ye1, w_ye2, b_y, w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, x1, x2, x3)

# x1 = -1
# x2 = 1
# x3 = 1

# w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, w_ye1, w_ye2, b_y = backprop(w_ye1, w_ye2, b_y, w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, x1, x2, x3)

# # print(w_e1x1, w_e1x2, b_e1, w_e2x1, w_e2x2, b_e2, w_ye1, w_ye2, b_y)

# x1 = 1
# x2 = 1
# x3 = -1

# e1 = w_e1x1*x1+w_e1x2*x2+b_e1
# e2 = w_e2x1*x1+w_e2x2*x2+b_e2

# y = w_ye1*sigma(e1)+w_ye2*sigma(e2)+b_y

# print(y)


# x1 = 1; x2 = 1; x3 = -1

# e1 = 0.2*x1-1.2*x2+0.4
# e2 = -0.7*x1-0.7*x1+0.7
# y = -0.5*sigma(e1)+2.3*sigma(e2)+0.4
# print(y)

# d_y = y-x3
# w_ye1 = -0.5-d_y*sigma(e1)
# w_ye2 = 2.3-d_y*sigma(e2)
# w_yb = 0.4-d_y*1

# d_e1 = d_y*-0.5*dSigma(e1)
# d_e2 = d_y*2.3*dSigma(e2)

# w_e1x1 = 0.2-d_e1*x1
# w_e1x2 = -1.2-d_e1*x2
# w_e1b = 0.4-d_e1*1
# w_e2x1 = -0.7-d_e2*x2
# w_e2x2 = -0.7-d_e2*x2
# w_e2b = 0.7-d_e2*1



def backprop(w_ye1, w_ye2, w_yb, w_e1x1, w_e1x2, w_e1b, w_e2x1, w_e2x2, w_e2b, x1, x2, x3):
    e1 = w_e1x1*x1 + w_e1x2*x2 + w_e1b
    e2 = w_e2x1*x1 + w_e2x2*x2 + w_e2b
    y = w_ye1*sigma(e1) + w_ye2*sigma(e2) + w_yb

    d_y = y-x3
    dw_ye1 = w_ye1-d_y*sigma(e1)
    dw_ye2 = w_ye2-d_y*sigma(e2)
    dw_yb = w_yb-d_y*1

    d_e1 = d_y*w_ye1*dSigma(e1)
    d_e2 = d_y*w_ye2*dSigma(e2)

    dw_e1x1 = w_e1x1-d_e1*x1
    dw_e1x2 = w_e2x2-d_e1*x2
    dw_e1b = w_e1b-d_e1*1
    dw_e2x1 = w_e2x1-d_e2*x1
    dw_e2x2 = w_e2x2-d_e2*x2
    dw_e2b = w_e2b-d_e2*1

    e1 = dw_e1x1*x1 + dw_e1x2*x2 + dw_e1b
    e2 = dw_e2x1*x1 + dw_e2x2*x2 + dw_e2b
    y = dw_ye1*sigma(e1) + dw_ye2*sigma(e2) + dw_yb

    return dw_ye1, dw_ye2, dw_yb, dw_e1x1, dw_e1x2, dw_e1b, dw_e2x1, dw_e2x2, dw_e2b, y

w_ye1, w_ye2, w_yb, w_e1x1, w_e1x2, w_e1b, w_e2x1, w_e2x2, w_e2b, y = backprop(-0.5, 2.3, 0.4, 0.2, -1.2, 0.4, -0.7, -0.7, 0.7, 1, 1, -1)
print(-1, y)
w_ye1, w_ye2, w_yb, w_e1x1, w_e1x2, w_e1b, w_e2x1, w_e2x2, w_e2b, y = backprop(w_ye1, w_ye2, w_yb, w_e1x1, w_e1x2, w_e1b, w_e2x1, w_e2x2, w_e2b, 0, -2, 1)
print(1, y)
w_ye1, w_ye2, w_yb, w_e1x1, w_e1x2, w_e1b, w_e2x1, w_e2x2, w_e2b, y = backprop(w_ye1, w_ye2, w_yb, w_e1x1, w_e1x2, w_e1b, w_e2x1, w_e2x2, w_e2b, -1, 1, 1)
print(1, y)
print(w_ye1, w_ye2, w_yb, w_e1x1, w_e1x2, w_e1b, w_e2x1, w_e2x2, w_e2b, y)