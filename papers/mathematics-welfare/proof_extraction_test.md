# Two long proofs, put to a model

Method. Each paper was given to a fresh instance of Claude (Fable 5.1), 12 September 2026, with
web access to arXiv, and the instruction: read the paper (not a secondary summary), extract ONE
idea that a strong non-specialist could follow and that is new in the paper; give a toy case;
propose one use outside the field, marked speculative if it is; and state which sections were
read and which parts of the idea were inherited. Reports verbatim below, lightly trimmed of
preamble.

---

## 1. Wang and Zahl, "Volume estimates for unions of convex sets, and the Kakeya set conjecture in three dimensions", arXiv 2502.17655

**What I read.** Sections 1 (Introduction through 1.7), 2 (proof sketch), and 4.1–4.2 (Proposition 4.6 and its proof) of v1, from the PDF text. Tao's Feb 2025 blog post as a cross-check; everything below is sourced to the paper itself.

**The idea: "Factoring convex sets", Proposition 4.6 (Section 4.2).** Take any finite family U of congruent convex bodies (thin tubes) in the unit ball. The proposition says you can throw away a small fraction and cover the rest by a family W of larger congruent convex containers such that (a) the containers are sparse: no convex region holds more containers than its volume allows (Katz–Tao Convex Wolff axioms, error ≈ 1); (b) inside each container the tubes are packed at the maximal density the whole family ever achieves; (c) inside each container the tubes are evenly spread (Frostman Convex Wolff axioms, error ≈ 1).

Why it is the crux: the authors' earlier "Sticky Kakeya" theorem handled tube families that look self-similar across scales. The unresolved case is where intermediate-scale tubes cluster heavily while fine tubes inside them are sparse. Proposition 4.6 manufactures the missing intermediate objects from scratch, with exactly the two properties (sparse upward, dense and even downward) needed to run induction on scale. The paper says outright: "A key new idea of our paper is a structure theorem that finds a set W of convex sets…" (Section 1.5). The proof is elementary: greedily pick the densest container, remove its contents, repeat; then dyadically pigeonhole container shapes and prune a bipartite incidence graph (Lemma 4.7).

**Toy version.** N points in the unit square, "tubes" = tiny discs. You can keep a constant fraction and cover those by congruent ellipses so that every ellipse holds about the same number of points, that number equals roughly (max point density anywhere) × (ellipse area), the ellipses are spread out, and inside each ellipse no sub-region holds a disproportionate share. Example: 100 dense clusters of 100 points each; the proposition returns the 100 cluster shapes as W.

**Outside connection (speculative).** Density-based clustering (DBSCAN-style) lacks a guarantee that found clusters are simultaneously internally uniform and mutually non-clustered at every convex scale. Proposition 4.6 is such a guarantee, in any dimension for any convex shape class, with a greedy algorithm. It resembles a regularity lemma for point-set geometry and might inform multi-resolution sampling or hierarchical codes.

**Honesty.** Statement, proof outline, and "key new idea" characterisation are from the paper. Ingredients are older: Frostman Convex Wolff axioms (Wang–Zahl 2024, arXiv 2401.12337), Katz–Tao-type non-concentration (Wolff 1995; Katz–Tao), grains (Guth 2014). Proposition 4.6 itself, and the multiplicity split µ ≈ µ_fine · µ_coarse (eq. 1.10), appear genuinely new here.

---

## 2. Baek, "Optimality of Gerver's Sofa", arXiv 2411.19826

**What I read.** The PDF directly: all of Chapter 1 (Sections 1.1–1.8, the paper's own overview), Section 6.1, and Section 6.5. Not read in detail: Chapters 2–5, 6.2–6.4, 7, 8.

**The idea: the injectivity condition (Theorem 1.7.1, abridged; full form Definition 6.1.2 / Theorem 6.1.1).** Sit in the sofa's frame and watch the hallway rotate around it. The hallway's inner corner traces a curve x(t), t in [0, π/2] (Romik's rotation path). The condition says the corner's x-coordinate strictly decreases: the path never loops back on itself and is a Jordan arc.

Why it is the crux: the paper says the obstacle to global optimality is that "there is no manageable formula of the area α(x)" in terms of x; every derivation of Gerver's sofa (Gerver, Romik, Deng) assumed a shape first. Injectivity lets Baek carve a region R ⊇ S with the "one core, two tails" shape of Gerver's niche, compute its area Q by Green's theorem, and show Q is a concave quadratic functional on triples of convex bodies (via Brunn–Minkowski and Mamikon's theorem), so Romik's local optimality of G becomes global.

How it is proved: Romik's balancing ODE (1.8) holds only where the hallway touches the sofa at three points. Baek replaces it with a one-sided inequality (1.9), later Theorem 6.4.3, which holds for any maximum sofa regardless of contact, rewrites it in "arm lengths" as f'(t) ≥ m_0(g(t)) (Theorem 6.5.1), and bootstraps.

**Toy version (Section 6.5).** Let m_0(x) = x − max(|x−1|, (|x−1|+1)/2), increasing, with m_0 ≥ −1 and m_0(y) > 0 for y > 2/3. Given f(0) = 1, f' ≥ m_0(g), and the mirror bound for g, define F f(x) = 1 + ∫_0^x m_0(f(π/2−u)) du, f_0 = 0, f_{n+1} = max(f_n, F f_n). Then f_1 = max(0, 1−x); each step lifts the floor by 1/12 (Lemma 6.5.3); f_10 > 2/3; f_11 > 1 (Lemma 6.5.5). Since x'(t) = −(f−1)u_t + (g−1)v_t, f, g > 1 is exactly injectivity. A Picard/Grönwall-style exercise with a reflected argument.

**Outside connection (speculative).** Piano-mover motion planning: an obstacle corner's trajectory in the robot frame is the same object as x(t). A proven no-self-loop condition on such contact trajectories would let swept or clearance areas be written by Green's theorem and turn shape-versus-path optimization into a concave program over support functions, as here.

**Honesty.** Everything above is from the paper's text. Not new: the balancing argument (Gerver 1992, gap repaired here), the ODE (1.8) (Romik 2018), and injectivity as an assumption, which Remark 6.1.1 says Romik already assumed in weak form for G. New in this paper: the inequality (1.9)/(1.10), the iteration proving injectivity for every maximum sofa, and the concave upper bound Q it enables.
