# The nine reinventions, put to a model

Method. Each of the nine cases in the paper's "Nine reinventions" section was put to a fresh
instance of Claude (Fable 5.1), 12 September 2026, as a practitioner inside one vocabulary would
ask it, with no mention of the other literature, with tools and web search disabled, and a
150-word limit. Scored a hit if the answer names the other literature(s) and states the
relationship. Nine of nine were hits. Prompts and answers verbatim below.

Caveat. The nine identifications are all documented somewhere the model has read, so this tests
whether a model *carries* a known identification across a vocabulary boundary on request, not
whether it can make a new one. The second test needs an uncatalogued pair.

---

## 1. Spark (asked as a compressed-sensing researcher)

**Prompt.** I work in compressed sensing. For a sensing matrix X we use the quantity called the spark, the smallest number of columns of X that are linearly dependent. Is this quantity known under any other names in other fields of mathematics or engineering, and if so, what exactly is the relationship (state any identity precisely)?

**Answer.** Yes, it appears under several names. (1) Matroid theory, girth: the columns of X define a linear (vector) matroid; its circuits are the minimal dependent column sets; spark(X) = girth of that matroid. (2) Coding theory, minimum distance: for a linear code with parity-check matrix H, d_min = smallest number of linearly dependent columns of H, so spark(X) = min{‖v‖₀ : Xv = 0, v ≠ 0}. (3) Kruskal rank (Kruskal 1977): krank(X) = largest k such that every k columns are linearly independent; identity spark(X) = krank(X) + 1. Also spark(X) ≤ rank(X) + 1, and uniqueness of sparse solutions holds when ‖v‖₀ < spark(X)/2.

## 2. BCJR (asked as a coding theorist)

**Prompt.** I work on error-correcting codes. We decode convolutional codes with the BCJR algorithm, a forward-backward recursion over a trellis that computes a posteriori symbol probabilities. Does this procedure correspond to anything known under other names in other fields, and if so, what is the exact correspondence?

**Answer.** Yes. BCJR is exactly the forward-backward (Baum–Welch E-step, "smoothing") algorithm for hidden Markov models, and more generally the sum-product algorithm on a chain-structured factor graph. Trellis states ↔ HMM hidden states; branches ↔ transitions with input priors; channel likelihoods ↔ emission probabilities; α, β, γ ↔ the forward variable, backward variable, and transition-times-emission factor; a posteriori symbol probabilities ↔ posterior marginals over transitions. Kalman smoothing is the linear-Gaussian analogue; Viterbi is the max-product variant; log-MAP is the log-domain form.

## 3. Backpropagation (asked as a neural-network practitioner)

**Prompt.** I train neural networks. We compute gradients with backpropagation. Is this procedure known under other names in other fields, and when and where was the same idea published before its use in neural networks? Be specific about fields and dates.

**Answer.** Yes. Backpropagation is an instance of reverse-mode automatic differentiation, and the same idea surfaced independently: control theory (Kelley 1960, Bryson 1961, Dreyfus 1962; Bryson and Ho 1969 as the adjoint method); numerical analysis (Linnainmaa's 1970 thesis, published 1976 in BIT); physics and engineering as adjoint sensitivity analysis (Cacuci 1981) and the adjoint state method in geophysics. Application to neural networks: Werbos 1974; popularized by Rumelhart, Hinton and Williams 1986.

## 4. Mixture fitting (asked as someone fitting Gaussian mixtures)

**Prompt.** I fit Gaussian mixture models by alternately assigning responsibilities to components and re-estimating component parameters. Is this a special case of some more general procedure, and had that procedure appeared under other names or in other problems before being stated generally? Be specific.

**Answer.** Yes, the EM algorithm (Dempster, Laird and Rubin 1977): responsibilities are the E-step, re-estimation the M-step. Earlier special cases they unified: Hartley 1958 and Healy and Westmacott 1956 (missing values in designs); Baum et al. 1970 (Baum–Welch for HMMs, with a monotonicity proof); Sundberg 1974, 1976 (exponential-family incomplete data); Orchard and Woodbury 1972 (missing information principle); Day 1969 and Hasselblad 1966, 1969 (mixture fitting); Ceppellini, Siniscalco and Smith 1955 (gene frequencies); Newcomb 1886. The hard-assignment variant is k-means.

## 5. Heredity (asked as a biometrician)

**Prompt.** I am a biometrician studying continuously varying traits with correlation and regression among relatives. Colleagues who study discrete Mendelian factors say our results contradict theirs. Is there a mathematical model under which both descriptions are correct, and who first stated it?

**Answer.** Yes. The infinitesimal (polygenic) model: a continuous trait that is the sum of small additive contributions from many independent Mendelian loci, plus environment, is approximately normal, and the correlations between relatives follow from Mendelian inheritance. First stated by R. A. Fisher in 1918, "The Correlation between Relatives on the Supposition of Mendelian Inheritance", which also partitioned variance into additive, dominance and environmental components. Yule had gestured toward it in 1902 and 1906.

## 6. Raking (asked as a survey statistician)

**Prompt.** I do survey statistics. We adjust sample weights by raking: alternately rescaling rows and columns of a weight table so the margins match known population totals. Is this iteration known under other names in other fields, and what is the common mathematical description?

**Answer.** Yes. It is iterative proportional fitting, the Deming–Stephan algorithm (1940), RAS in input-output balancing, and the Sinkhorn or Sinkhorn–Knopp algorithm (1964), now central to entropic optimal transport (Cuturi 2013); also alternating scaling, matrix scaling, biproportional fitting. Common description: find diagonal D₁, D₂ with D₁AD₂ having the target margins; equivalently, minimize KL divergence from A subject to the margins (an I-projection); the alternating scaling is coordinate ascent on the dual, converging geometrically in Hilbert's projective metric; in statistics it fits the log-linear model of independence plus margins.

## 7. Filter banks (asked as a DSP engineer)

**Prompt.** I am a digital signal processing engineer working with two-channel perfect-reconstruction filter banks and quadrature-mirror filters. Do these correspond to objects studied under other names in mathematics or computer vision, and what is the exact correspondence?

**Answer.** Yes. Iterated on the lowpass branch, a two-channel PR bank is exactly the discrete wavelet transform (Mallat's multiresolution analysis). An orthogonal bank with lowpass h and highpass g (conjugate quadrature filters) yields the scaling function via the refinement equation φ(t) = √2 Σ h[n] φ(2t−n) and the wavelet ψ likewise, provided the cascade converges (Daubechies, Cohen). Orthogonal banks ↔ orthonormal wavelets; biorthogonal banks (CDF 5/3, 9/7 in JPEG2000) ↔ biorthogonal wavelets; lifting ↔ polyphase factorization. Caveat: strict Croisier–Esteban–Galand QMF gives FIR perfect reconstruction only for Haar. In vision the Burt–Adelson Laplacian pyramid is the oversampled analogue; in CAGD the refinement equation is a subdivision scheme.

## 8. Kriging (asked as a geostatistician)

**Prompt.** I am a geostatistician. I interpolate ore grades with ordinary kriging using a fitted variogram. Is kriging equivalent to any method used in other fields under a different name, and in what precise sense are they the same or different?

**Answer.** Yes. Ordinary kriging is the best linear unbiased predictor under a second-order stationary or intrinsic random field with known covariance or variogram. Under a Gaussian assumption it coincides with the posterior mean of Gaussian-process regression, with kriging variance equal to posterior variance; ordinary kriging corresponds to a GP with an unknown constant mean integrated out under a flat prior. It is also the Wiener–Kolmogorov filter on a spatial index, and the spatial analogue of generalized least squares. Differences are in practice: variograms fitted by moments, hyperparameters by marginal likelihood; frequentist versus Bayesian readings of the uncertainty.

## 9. Spectral factorization (asked as a control engineer)

**Prompt.** I work in control engineering. I need to factor a matrix polynomial that is positive semidefinite on the unit circle as P(z) = Q(z)^* Q(z) with Q stable (spectral factorization). Is this result known under other names in other fields, and which fields developed it separately?

**Answer.** Yes, one of the most independently rediscovered results in applied mathematics. Mathematics: the Fejér–Riesz theorem (1915–16), matrix version Rosenblum (1968), general case via Hardy spaces (Helson and Lowdenslager). Time series: the Wold decomposition and Kolmogorov–Szegő, Wiener's prediction theory, Wiener–Masani (1957). Signal processing and circuit synthesis: minimum-phase factorization, Youla (1961), Darlington synthesis. Control: Kalman, Anderson, Youla, Wilson, tied to Riccati equations and the KYP lemma. Operator theory: inner-outer factorization (Beurling, Sz.-Nagy–Foias).
