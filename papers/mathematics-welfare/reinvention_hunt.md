# Hunting reinventions with a model, and being hunted

Two exercises run on 12 September 2026 with Claude (Fable 5.1) agents, at the author's request,
after the nine-case test recorded in `reinvention_test.md`.

1. Five agents, one per field, scanned 2024–2026 arXiv listings for a method presented as new that
   exists under another name elsewhere. Each finding was then given to an independent verifier
   agent told to break it: fetch the recent paper and read its reference list, locate the prior
   source, redo the algebra, and return confirmed, weakened, or rejected with quoted evidence.
2. Three agents did the same to the author's own papers, and two verifiers checked those.

The distinction the verifiers enforced, and that this record keeps: "presented as new" and "never
recognized as old" are different accusations. Where a paper inherits a construction from its own
lineage without claiming it, the second applies, not the first.

## Outside findings, 2024–2026

| # | Recent paper | Prior result | Relationship | Cites prior? | Verdict |
|---|---|---|---|---|---|
| 1 | Muon optimizer (Jordan et al. blog 2024; "Muon is Scalable", arXiv 2502.16982) | Stochastic spectral descent, Carlson, Cevher, Carin (AISTATS 2015; NeurIPS 2015): polar factor of the gradient as steepest descent under the spectral norm | Identical update direction; Muon applies it to momentum via Newton–Schulz (itself Kovarik 1970, Björck–Bowie 1971) | Scaling paper: no. Blog: credit added July 2025, seven months after posting (Wayback) | Confirmed, high |
| 2 | Kolmogorov–Arnold Networks (Liu et al., arXiv 2404.19756) | Kolmogorov Spline Network, Igelnik and Parikh, IEEE TNN 2003: learnable splines on both layers | Depth-2 KAN is the KSN; depth and tooling are new | Igelnik–Parikh absent; but a 2013 chapter about the KSN is cited in a list of eight without comment | Weakened |
| 3 | GRPO (DeepSeekMath, arXiv 2402.03300) | REINFORCE with leave-one-out baseline (Williams 1992; Kool, van Hoof, Welling 2019) | Advantage with std removed equals G/(G−1) times RLOO, exact; full objective adds clipping and KL | No; "REINFORCE" occurs zero times | Confirmed, high |
| 4 | Bias-corrected participation ratio (Chun et al., arXiv 2509.26560) | Sphericity U-statistics, Glasser 1961; Chen, Zhang, Zhong JASA 2010; Li–Chen 2012 | Row-sampling estimator term for term the 1, −2, 1 construction; the two-way row-and-column version is the paper's own | No statistics paper in ~60 references | Confirmed for the row component, weakened in scope |
| 5 | Paired-strata variance estimator (Bai, Huang, Romano, Shaikh, Tabord-Meehan, arXiv 2503.10851) | Collapsed-strata estimator, Hansen, Hurwitz, Madow 1953; Cochran 1977 | Identical statistic and identical bias formula, from the paper's own eq. 11 | Cochran cited for other theorems; "collaps" nowhere in the paper | Confirmed, high |
| 6 | Change points by mixed-integer programming (Prokhorov et al., arXiv 2408.05665) | Exact dynamic programming: Auger–Lawrence 1989, Jackson et al. 2005, Killick et al. 2012 PELT, Bai–Perron 2003 | Same additive-segment-cost objective; MIO is a slower exact solver | Bai–Perron cited only for information criteria; no DP, PELT, or Yao | Confirmed, high |
| 7 | Cauchy-kernel correntropy UKF (Nguyen, Zhao, Hu, arXiv 2509.01163) | Geman–McClure loss, 1985 | Maximizing 1/(1+e²/σ) is minimizing e²/(σ+e²); IRLS weight identical | No robust-statistics source; kernel inherited from a 2020 paper | Confirmed on the mathematics; the lineage, not this paper, is the reinventor |
| 8 | Least lncosh adaptive filter (Zhao, Abebe, Peng, arXiv 2606.01233) | Holland–Welsch 1977 "logistic" M-estimator, ψ = tanh; in MATLAB robustfit | Identical up to scale; cost inherited from a 2023 paper | No | Confirmed, same caveat |
| 9 | νPI Lagrange-multiplier controller (Sohrabi et al., ICML 2024, arXiv 2406.04558) | Augmented Lagrangian, Hestenes 1969, Powell 1969, Rockafellar 1973; PI reading in Wang and Elia CDC 2011 | With smoothing off, primal iterates identical to gradient descent-ascent on the augmented Lagrangian; verified algebraically | "Method of multipliers ... outside the scope"; "augmented" absent; the group's 2026 follow-up calls the identity "previously unknown" and also omits Wang–Elia | Confirmed, high |
| 10 | Risk-sensitive control as Rényi minimization (Kataoka et al., arXiv 2609.07045) | van den Broek, Wiegerinck, Kappen UAI 2010; Boué–Dupuis 1998 duality | Same model class; parameter map is the 2010 temperature relation rearranged | None of the three in 19 references | Confirmed, high |
| 11 | Hoeffding regime-change warning (Egger and Vestal, arXiv 2512.08851) | Hoeffding-bound drift detectors, Frías-Blanco et al. TKDE 2015; ADWIN; CUSUM | Known-reference special case of HDDM_A | Nine references, none from drift detection or sequential testing | Confirmed |
| 12 | Generalized population synchrony on the circle (Motta et al., arXiv 2406.15987) | Intrinsic circular variance; Hotz–Huckemann 2015 (sample means at polygon vertices, linear time); McKilliam et al. 2012 | Proposition 8's antipodal-cut algorithm, with a looser count than the prior | 68 references, none from circular statistics | Confirmed |

Tally: twelve findings, eleven confirmed, one weakened, none rejected. Every field produced at
least one. The pattern is the one the nine historical reinventions record: a construction arrives in
a field, is named there, and the field's reference list contains nothing from where it came.

## The author's own papers

The same hunt, pointed at home.microprediction.org, with the same verification.

| # | Paper | Prior result | Relationship | Verdict |
|---|---|---|---|---|
| 1 | skaters (JSS): trunk weight recursion | Dynamic Model Averaging, Raftery, Kárný, Ettler 2010 | In logs, DMA with α = γ plus tempering and a rent; DMA also proves what a footnote argues informally | Confirmed, high (skaters #218) |
| 2 | skaters (JSS) §11.6: the sandwich | Berkowitz 2001 (Gaussian AR(1) on the probit of the PIT) | Exact for that inner model; section cites nothing | Confirmed, high (skaters #219) |
| 3 | Platform 2022, point-cloud 2026: near-the-pin | Johnstone 2007 parimutuel Kelly rule, not proper; Kilgour–Gerchak 2004 proper alternative | Antecedent and parallel; discrete pool versus continuous density | Confirmed on citations (home #5) |
| 4 | Covariance Inflation 2025 | Weighted matrix geometric mean, Pusz–Woronowicz 1975, Kubo–Ando 1980; Ledoit–Wolf 2004 constant-correlation target | Identical; and the claim that variances are preserved is false away from the endpoints, closed form given | Confirmed (home #6); LW attribution weakened |
| 5 | Trading Illiquid Goods 2022 | Guéant 2017 δ* = p + Λ/(−Λ′); Ho–Stoll 1981 | Identical up to notation | Confirmed, high (home #7) |
| 6 | Herd Immunity Convexity Adjustments 2020 | Karev / Vaupel–Yashin MGF identity; Novozhilov 2008 exact threshold | Identical growth identity; threshold related | Confirmed (home #8); priority dating weakened |
| 7 | Horse Race Problem 2021 §1.7 | Lo and Bacon-Shone discount model 1992/1995 | Identical; wrong Lo–Bacon-Shone paper cited, with a misprinted year | Confirmed (winning #39) |
| 8 | Two Sides of Schur Damping: γ* | Thompson 1968 (exact); Vasicek 1973 (form only, needs zero prior mean); paper says James–Stein and Ledoit–Wolf | γ* = t²/(1+t²) exactly; James–Stein and Ledoit–Wolf match to first order only; "Wiener" is exact | Confirmed; Vasicek weakened (precise #70) |
| 9 | Two Sides; SCA: the damping pair | Gaussian conditioning on a sibling observed with proportional nugget ((1−γ)/γ)D; response Vecchia, Datta et al. 2016 | Exact; and the hedged residual has variance A − (2γ−γ²)BD⁻¹Bᵀ, not S(γ), which the paper implies but never writes | Confirmed, high (precise #71) |
| 10 | SCA: hierarchical minimum variance | Tola, Lillo, Gallegati, Mantegna 2008 (Markowitz on hierarchically filtered covariance); NCO 2019 | A different construction: the matrix is filtered and then optimized, with no sub-block recursion, so it does not bear on the SCA claim | Not a reinvention; kept as a related-work citation (precise #72) |
| 11 | Two Sides: the two readings; block pseudo-likelihood | Johnson 1960, Ederington 1979; Stein, Chi, Welty 2004 for the block form | Citation gap; Vecchia attribution incomplete; with c = all other blocks the product is Besag's pseudo-likelihood, not a factorization | Confirmed (precise #73) |

Tally on the author's side: eleven findings, ten confirmed, three weakened in part, one reclassified on the author's review from reinvention to related work worth citing.

Cleared by the hunters on the author's side: Harville, Plackett–Luce, Henery, Stern, Vovk's
conformal transducers and predictive distributions, and the 2026 contests paper's literature
coverage, which was found thorough after its twenty-five rounds of model-assisted search.

Issues were filed on the author's repositories for each finding, each carrying the verifier's
verdict and evidence.
