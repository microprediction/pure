#!/usr/bin/env python3
"""Checks for every formula and number in mathematics-welfare.tex.

Symbolic checks use sympy; numerical ones use scipy. Run from this directory:
    python3 verify_claims.py
Exit status is nonzero if any check fails.
"""
import math
import numpy as np
import sympy as sp
from scipy import integrate, optimize

FAILS = []

def check(name, ok, detail=""):
    print(f"{'ok  ' if ok else 'FAIL'} {name}{'  ' + detail if detail else ''}")
    if not ok:
        FAILS.append(name)

# ---------------------------------------------------------------- Eq (2): Pareto excess value
v, c, v0, alpha = sp.symbols("v c v_0 alpha", positive=True)
pdf = alpha * v0**alpha / v**(alpha + 1)                       # Pareto density on [v0, inf)
g_sym = sp.simplify(sp.integrate((v - c) * pdf, (v, c, sp.oo), conds="none"))
g_claim = v0**alpha * c**(1 - alpha) / (alpha - 1)
check("Eq (2): g(c) = v0^a c^(1-a)/(a-1) on c >= v0",
      sp.simplify(g_sym - g_claim) == 0, str(g_sym))
elas = sp.simplify(sp.diff(sp.log(g_claim), sp.log(c)) if False else sp.diff(g_claim, c) * c / g_claim)
check("Eq (2): elasticity of g in c is -(alpha-1)", sp.simplify(elas + (alpha - 1)) == 0)
# numeric spot check
a_, c_, v0_ = 1.5, 2.0, 1.0
num = integrate.quad(lambda x: (x - c_) * a_ * v0_**a_ / x**(a_ + 1), c_, np.inf)[0]
check("Eq (2): numeric g at alpha=1.5,c=2", abs(num - v0_**a_ * c_**(1 - a_) / (a_ - 1)) < 1e-9)

# ---------------------------------------------------------------- Jensen: D >= exp(-rho E T)
rho = 0.05
T = np.random.default_rng(0).exponential(30.0, 200_000)
D = np.mean(np.exp(-rho * T)); Dj = math.exp(-rho * T.mean())
check("Jensen: E[e^{-rho T}] >= e^{-rho E[T]}", D >= Dj, f"{D:.4f} >= {Dj:.4f}")
tau_ce = -math.log(D) / rho
check("certainty-equivalent lag below the mean lag", tau_ce < T.mean(), f"{tau_ce:.1f} < {T.mean():.1f}")

# ---------------------------------------------------------------- Eq (3): segment averaging identity
kQ, kH, eps, delta = sp.symbols("kappa_Q kappa_H epsilon delta", positive=True)
WQ0, WH0 = sp.symbols("W_Q0 W_H0", positive=True)
WQ1, WH1 = kQ * WQ0, kH * WH0
kappa_total = (WQ1 + WH1) / (WQ0 + WH0)
check("Eq (3): kappa = (kQ + eps kH)/(1+eps) with eps = WH0/WQ0",
      sp.simplify(kappa_total.subs(WH0, eps * WQ0) - (kQ + eps * kH) / (1 + eps)) == 0)
delta_def = WH1 / WQ1
check("Eq (3): kappa = kQ (1+delta)/(1+eps) with delta = WH1/WQ1",
      sp.simplify((kappa_total - kQ * (1 + delta_def) / (1 + WH0 / WQ0))) == 0)
check("Eq (3): weighted average lies between kQ and kH",
      all(min(q, h) <= (q + e * h) / (1 + e) <= max(q, h)
          for q, h, e in [(7.6, 30, 0.1), (99, 1089, 1.0), (5, 5, 3)]))

# ---------------------------------------------------------------- Eq (4): within-segment product and Prop 1 comparative statics
n, m, q0, q1, D0, D1 = sp.symbols("n m q_0 q_1 D_0 D_1", positive=True)
kappa_seg = (q1 / q0) * m**(alpha - 1) * (D1 / D0)
check("Remark 1: segment multiplier decreasing in q0", sp.simplify(sp.diff(kappa_seg, q0)).is_negative)
check("Remark 1: segment multiplier decreasing in D0", sp.simplify(sp.diff(kappa_seg, D0)).is_negative)
check("Remark 1: single known user (q0=q1, D0=D1) leaves m^(alpha-1)",
      sp.simplify(kappa_seg.subs({q0: q1, D0: D1}) - m**(alpha - 1)) == 0)

# ---------------------------------------------------------------- Table 1 arithmetic
rows = {"mild": dict(n=3, mcost=(3, 1.2), rho=0.03, dt=25, eps=0.1, dlt=0.1, kL=1.0),
        "large": dict(n=10, mcost=(10, 1.5), rho=0.03, dt=40, eps=0.1, dlt=1.1, kL=1.0),
        "extreme": dict(n=30, mcost=(10, 2.0), rho=0.05, dt=50, eps=0.1, dlt=10, kL=0.7)}
stated = {"mild": dict(cost=1.2, lag=2.1, kQ=7.6, tail=1, kM=7.6, ratio=7.6),
          "large": dict(cost=3, lag=3.3, kQ=99, tail=1.9, kM=190, ratio=190),
          "extreme": dict(cost=10, lag=12, kQ=3600, tail=10, kM=36000, ratio=51000)}
def close(x, y, tol=0.06):  # entries are rounded before multiplying
    return abs(x - y) / y <= tol
for col, r in rows.items():
    cost = r["mcost"][0] ** (r["mcost"][1] - 1)
    lag = math.exp(r["rho"] * r["dt"])
    st = stated[col]
    kQ_ = r["n"] * st["cost"] * st["lag"]          # rounded channel entries, as the paper says
    tail = (1 + r["dlt"]) / (1 + r["eps"])
    kM = st["kQ"] * st["tail"]
    ratio = st["kM"] / r["kL"]
    check(f"Table 1 {col}: cost m^(a-1)", close(cost, st["cost"]), f"{cost:.2f} vs {st['cost']}")
    check(f"Table 1 {col}: lag e^(rho dt)", close(lag, st["lag"]), f"{lag:.2f} vs {st['lag']}")
    check(f"Table 1 {col}: kappa_Q", close(kQ_, st["kQ"]), f"{kQ_:.1f} vs {st['kQ']}")
    check(f"Table 1 {col}: tail (1+delta)/(1+eps)", close(tail, st["tail"]), f"{tail:.2f} vs {st['tail']}")
    check(f"Table 1 {col}: kappa_M", close(kM, st["kM"]), f"{kM:.0f} vs {st['kM']}")
    check(f"Table 1 {col}: ratio at unit elasticity", close(ratio, st["ratio"]), f"{ratio:.0f} vs {st['ratio']}")

# ---------------------------------------------------------------- value-weighted reach example
a_, v0_, c_ = 1.5, 1.0, 1.0
total = v0_**a_ * c_**(1 - a_) / (a_ - 1)                      # = 2
x = 0.1 ** (-1 / a_)                                           # top-decile threshold
top = integrate.quad(lambda t: (t - c_) * a_ * v0_**a_ / t**(a_ + 1), x, np.inf)[0]
check("value-weighted example: threshold 4.64", abs(x - 4.64) < 0.01, f"{x:.2f}")
check("value-weighted example: top decile holds ~65% of value", abs(top / total - 0.646) < 0.005, f"{top/total:.3f}")
check("value-weighted example: universal reach multiplies by ~1.5, not 10", abs(total / top - 1.55) < 0.01, f"{total/top:.2f}")

# ---------------------------------------------------------------- Eq (5): spending optimum and elasticity
S, a, V, gam = sp.symbols("S a V gamma", positive=True)
obj = a * V * S**gam - S
Sstar = sp.solve(sp.diff(obj, S), S)[0]
check("Eq (5): S* = (gamma a V)^(1/(1-gamma))", sp.simplify(Sstar - (gam * a * V) ** (1 / (1 - gam))) == 0)
check("Eq (5): d log S*/d log V = 1/(1-gamma)", sp.simplify(sp.diff(sp.log(Sstar), V) * V - 1 / (1 - gam)) == 0)
check("Eq (5): d log S*/d log a = 1/(1-gamma)", sp.simplify(sp.diff(sp.log(Sstar), a) * a - 1 / (1 - gam)) == 0)
check("Eq (5): second-order condition (concave objective)", sp.simplify(sp.diff(obj, S, 2).subs(gam, sp.Rational(1, 2))).is_negative)
res = optimize.minimize_scalar(lambda s: -(2.0 * 5.0 * s**0.5 - s), bounds=(1e-6, 1e4), method="bounded")
check("Eq (5): numeric optimum at gamma=1/2, aV=10", abs(res.x - (0.5 * 10) ** 2) < 1e-3, f"{res.x:.4f} vs 25")

# local elasticity for general I(S): 1/eta with eta = -d log I'(S)/d log S
I = sp.Function("I")
FOC = sp.Eq(V * sp.diff(I(S), S), 1)
eta = -sp.diff(sp.log(sp.diff(I(S), S)), S) * S
# implicit differentiation: V I'(S*) = 1  =>  dS/dV = -I'/(V I'')  =>  d log S/d log V = -I'/(S I'') = 1/eta
dlogS_dlogV = sp.simplify(-sp.diff(I(S), S) / (S * sp.diff(I(S), S, 2)))
check("general I(S): d log S*/d log V = 1/eta(S*)", sp.simplify(dlogS_dlogV - 1 / eta) == 0)
check("power law: eta = 1-gamma", sp.simplify(eta.subs(I(S), a * S**gam).doit() - (1 - gam)) == 0)

# saturating counterexample I(S) = 1 - e^{-S}
Ssat = sp.solve(sp.Eq(V * sp.exp(-S), 1), S)[0]
check("saturating I: S* = log V", sp.simplify(Ssat - sp.log(V)) == 0)
elas_sat = sp.simplify(sp.diff(Ssat, V) * V / Ssat)
check("saturating I: elasticity 1/log V, below one for V > e",
      sp.simplify(elas_sat - 1 / sp.log(V)) == 0 and float(elas_sat.subs(V, 10)) < 1)

# ---------------------------------------------------------------- Remark: the wedge
W, P, kW, kP = sp.symbols("W P kappa_W kappa_P", positive=True)
Ssoc = (gam * a * W) ** (1 / (1 - gam)); Spriv = (gam * a * P) ** (1 / (1 - gam))
check("wedge: S_soc/S_priv = (W/P)^(1/(1-gamma))", sp.simplify(Ssoc / Spriv - (W / P) ** (1 / (1 - gam))) == 0)
wedge_after = (gam * a * kW * W) ** (1 / (1 - gam)) / (gam * a * kP * P) ** (1 / (1 - gam))
check("wedge: multiplied by (kW/kP)^(1/(1-gamma))",
      sp.simplify(wedge_after / (Ssoc / Spriv) - (kW / kP) ** (1 / (1 - gam))) == 0)

# ---------------------------------------------------------------- Eq (6): fixed-budget ratio
M, L, B, aM, aL, VM, VL, lam = sp.symbols("M L B a_M a_L V_M V_L lambda", positive=True)
Lag = aM * VM * M**gam + aL * VL * L**gam - lam * (M + L - B)
sol_ratio = sp.solve([sp.diff(Lag, M), sp.diff(Lag, L)], [lam, M], dict=True)[0][M] / L
check("Eq (6): M/L = (aM VM / aL VL)^(1/(1-gamma))",
      sp.simplify(sol_ratio - (aM * VM / (aL * VL)) ** (1 / (1 - gam))) == 0)
g_, A, Bv = 0.5, 3.0, 1.0   # numeric: budget 10, aM VM = 3, aL VL = 1
res = optimize.minimize_scalar(lambda mm: -(A * mm**g_ + Bv * (10 - mm) ** g_), bounds=(1e-6, 10 - 1e-6), method="bounded")
check("Eq (6): numeric fixed-budget optimum matches ratio", abs(res.x / (10 - res.x) - (A / Bv) ** (1 / (1 - g_))) < 1e-3,
      f"{res.x/(10-res.x):.3f} vs {(A/Bv)**2:.3f}")
check("Eq (6): kappa_M, kappa_L scale the ratio by (kM/kL)^(1/(1-gamma))",
      sp.simplify(sol_ratio.subs({VM: kW * VM, VL: kP * VL}) / sol_ratio - (kW / kP) ** (1 / (1 - gam))) == 0)

# ---------------------------------------------------------------- screening cost: sign condition
q, K, gc, Dd = sp.symbols("q K g D", positive=True)
Cq = sp.Function("C")(q)
Wq = K * q * gc * Dd - Cq
check("screening: dW/dq > 0 iff K g D > C'(q)", sp.simplify(sp.diff(Wq, q) - (K * gc * Dd - sp.diff(Cq, q))) == 0)

# ---------------------------------------------------------------- numbers quoted in the text
check("lag: e^{0.03*40} ~ 3.3", abs(math.exp(0.03 * 40) - 3.3) < 0.05, f"{math.exp(1.2):.2f}")
check("lag: e^{0.05*50} ~ 12", abs(math.exp(0.05 * 50) - 12) < 0.3, f"{math.exp(2.5):.2f}")
check("NSF DMS share of GDP ~ one part in a hundred thousand", 5e-6 < 248.4e6 / 28e12 < 2e-5, f"{248.4e6/28e12:.2e}")
# spark = smallest number of linearly dependent columns; krank = largest k with every k columns independent
from itertools import combinations
def spark_and_krank(X):
    ncol = X.shape[1]
    spark = ncol + 1
    for k in range(1, ncol + 1):
        if any(np.linalg.matrix_rank(X[:, list(cols)]) < k for cols in combinations(range(ncol), k)):
            spark = k; break
    krank = 0
    for k in range(1, ncol + 1):
        if all(np.linalg.matrix_rank(X[:, list(cols)]) == k for cols in combinations(range(ncol), k)):
            krank = k
        else:
            break
    return spark, krank
rng = np.random.default_rng(1)
cases = [rng.integers(-3, 4, size=(3, 5)).astype(float) for _ in range(20)]
cases.append(np.array([[1., 0., 1., 2.], [0., 1., 1., 3.], [0., 0., 0., 0.]]))   # planted dependencies
check("girth identity: spark(X) = krank(X) + 1 on 21 random and planted matrices",
      all(spark_and_krank(X)[0] == spark_and_krank(X)[1] + 1 for X in cases),
      "; ".join(f"{spark_and_krank(X)}" for X in cases[:4]))
check("professor relativity: 2.4/3.2 is a fall of a quarter", abs(1 - 2.4 / 3.2 - 0.25) < 1e-9)
check("IMU directory: 57,000 of 6.3bn is under one per hundred thousand", 57000 / 6.3e9 < 1e-5, f"{57000/6.3e9*1e5:.2f} per 100k")

print()
print(f"{len(FAILS)} failure(s)" if FAILS else "all checks passed")
raise SystemExit(1 if FAILS else 0)
