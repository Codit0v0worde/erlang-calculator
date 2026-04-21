import math

# ---------- Эрланг B ----------
def erlang_b(v, a):
    if v == 0:
        return 1.0
    s = 0.0
    term = 1.0
    for i in range(1, v + 1):
        term *= a / i
        s += term
    return term / (1 + s)

def erlang_b_inv_v_p(a, p_target, max_v=1000):
    for v in range(1, max_v + 1):
        if erlang_b(v, a) <= p_target:
            return v
    return max_v

def erlang_b_inv_v_m(a, m_target, max_v=1000):
    for v in range(1, max_v + 1):
        pb = erlang_b(v, a)
        m = a * (1 - pb)
        if m >= m_target:
            return v
    return max_v

def erlang_b_overload(v, p_measured, p_norm, max_a=1000.0, step=0.01):
    a_meas = find_a_erlang_b(v, p_measured, max_a, step)
    a_norm = find_a_erlang_b(v, p_norm, max_a, step)
    if a_meas == 0:
        return 0.0
    return (a_meas - a_norm) / a_meas * 100

def find_a_erlang_b(v, p_target, max_a=1000.0, step=0.01):
    a = 0.0
    while a <= max_a:
        if erlang_b(v, a) >= p_target:
            return a
        a += step
    return max_a

# ---------- Энгсет ----------
def engset_b(v, a, N):
    if v >= N:
        return 0.0
    p = [1.0]
    for i in range(1, v + 1):
        p.append(p[-1] * (N - i + 1) * a / i)
    sum_p = sum(p)
    return p[v] / sum_p if sum_p > 0 else 0.0

def engset_inv_v_p(a, N, p_target, max_v=None):
    if max_v is None:
        max_v = N
    for v in range(1, min(max_v, N) + 1):
        if engset_b(v, a, N) <= p_target:
            return v
    return N

def engset_inv_v_m(a, N, m_target, max_v=None):
    if max_v is None:
        max_v = N
    for v in range(1, min(max_v, N) + 1):
        p = [1.0]
        for i in range(1, v + 1):
            p.append(p[-1] * (N - i + 1) * a / i)
        sum_p = sum(p)
        m = sum(i * p[i] for i in range(v + 1)) / sum_p
        if m >= m_target:
            return v
    return N

def engset_overload(v, N, p_measured, p_norm, max_a=10.0, step=0.001):
    a_meas = find_a_engset(v, N, p_measured, max_a, step)
    a_norm = find_a_engset(v, N, p_norm, max_a, step)
    if a_meas == 0:
        return 0.0
    return (a_meas - a_norm) / a_meas * 100

def find_a_engset(v, N, p_target, max_a=10.0, step=0.001):
    a = 0.0
    while a <= max_a:
        if engset_b(v, a, N) >= p_target:
            return a
        a += step
    return max_a

# ---------- Эрланг C ----------
def erlang_c(v, a):
    if v == 0:
        return 1.0
    pb = erlang_b(v, a)
    rho = a / v
    if rho >= 1.0:
        return 1.0
    return (v * pb) / (v - a * (1 - pb))

def erlang_c_inv_v_p(a, p_target, max_v=1000):
    for v in range(max(1, int(a) + 1), max_v + 1):
        if erlang_c(v, a) <= p_target:
            return v
    return max_v

def erlang_c_overload(v, p_measured, p_norm):
    a_meas = find_a_erlang_c(v, p_measured)
    a_norm = find_a_erlang_c(v, p_norm)
    if a_meas == 0:
        return 0.0
    return (a_meas - a_norm) / a_meas * 100

def find_a_erlang_c(v, p_target, max_a=1000.0, step=0.01):
    a = 0.0
    while a <= max_a:
        if erlang_c(v, a) >= p_target:
            return a
        a += step
    return max_a

# ---------- Групповое поступление ----------
def batch_erlang_b(v, a, k):
    return erlang_b(v, a * k)

def batch_inv_v_p(a, k, p_target, max_v=1000):
    for v in range(1, max_v + 1):
        if batch_erlang_b(v, a, k) <= p_target:
            return v
    return max_v

def batch_inv_v_m(a, k, m_target, max_v=1000):
    for v in range(1, max_v + 1):
        pb = batch_erlang_b(v, a, k)
        m = a * k * (1 - pb)
        if m >= m_target:
            return v
    return max_v

def batch_overload(v, k, p_measured, p_norm):
    a_meas = find_a_batch(v, k, p_measured)
    a_norm = find_a_batch(v, k, p_norm)
    if a_meas == 0:
        return 0.0
    return (a_meas - a_norm) / a_meas * 100

def find_a_batch(v, k, p_target, max_a=1000.0, step=0.01):
    a = 0.0
    while a <= max_a:
        if batch_erlang_b(v, a, k) >= p_target:
            return a
        a += step
    return max_a