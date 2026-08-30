#!/usr/bin/env python3
"""
Generates docs/fields-data.js, docs/fields/<slug>.html, and docs/ledger.html
from the FIELDS survey data below. Run from repo root: python3 scripts/build_site.py

This is the single source of truth for the 34-field MSC (~1959-60) pure-math
survey. map.html and timeline.html load docs/fields-data.js at runtime rather
than embedding their own copies of this data.
"""
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")
FIELDS_DIR = os.path.join(DOCS, "fields")

CLUSTERS = {
    "numtheory": {"label": "Number theory & algebraic geometry", "color": "#2980b9"},
    "algebra":   {"label": "Algebra",                            "color": "#8e44ad"},
    "geometry":  {"label": "Geometry",                           "color": "#16a085"},
    "topology":  {"label": "Topology",                           "color": "#d68910"},
    "logic":     {"label": "Logic & foundations",                "color": "#c0392b"},
    "analysis":  {"label": "Analysis & probability",             "color": "#27ae60"},
}

# verdict codes:
#  a  = named, dated dismissal on record; later applied
#  b  = never dismissed by anyone; quietly (or immediately) useful
#  d  = no major real-world application well-documented today (the honest "null" case)
#  x  = mixed / doesn't fit cleanly; explained in note

FIELDS = [
    dict(slug="mathematical-logic", msc="03", name="Mathematical logic & foundations",
         cluster="logic",
         one_liner="Model theory, proof theory, recursion theory: formal systems, provability, computability.",
         founded=dict(year=1879, event="Frege's Begriffsschrift, the first fully formal logical system"),
         dismissed=dict(kind="hostile", who="Henri Poincaré", year=1905,
             quote="La Logique reste donc stérile, à moins d'être fécondée par l'intuition (“Logic remains sterile unless fertilized by intuition”); after Russell's paradox: “Logistic is no longer sterile — it engenders the antinomy.”",
             source="Poincaré, essays collected in *Science et méthode*, c. 1905–06 (primary French text).",
             note="Aimed at the Peano–Russell logicist program specifically, not at the later technical subfields (model theory, recursion theory) that didn't exist yet.",
             confidence="medium-high"),
         applications=[
             dict(name="Model checking", year=1981, note="Clarke, Emerson & Sifakis — 2007 Turing Award; industry-standard hardware/protocol verification.", url="https://en.wikipedia.org/wiki/Model_checking"),
             dict(name="Formally verified software (seL4)", year=2009, note="Curry–Howard-based proof assistants; seL4's machine-checked correctness proof is deployed in Qualcomm chipsets and DARPA's HACMS drone program.", url="https://en.wikipedia.org/wiki/L4_microkernel_family#seL4"),
         ],
         verdict="a", gap_basis="founding (1879) to first real-world technique (model checking, 1981)", gap_years=102,
         confidence="medium-high"),

    dict(slug="set-theory", msc="04", name="Set theory",
         cluster="logic",
         one_liner="Cantor's theory of infinite sets — and the standard foundational language modern mathematics is written in.",
         founded=dict(year=1874, event="Cantor's first paper on the uncountability of the reals"),
         dismissed=None,
         dismissed_note="The famous “set theory is a disease” line usually pinned on Poincaré is documented as apocryphal (Jeremy Gray, *The Mathematical Intelligencer*, 1991). Kronecker's attacks on Cantor (“corrupter of youth”) target set theory's *legitimacy* — whether actual infinities exist at all — not its *utility*.",
         applications=[],
         applications_note="Split by what “application” means. Elementary set theory is enabling infrastructure for essentially all of modern mathematics: functions are sets of ordered pairs, spaces are sets with structure, probability spaces are sets equipped with σ-algebras and measures. That's a real transmission mechanism, just an indirect one — it doesn't put set-theoretic notation into a GPS receiver, it puts a foundational language under the mathematician who writes the receiver's equations. Application of mathematics is not the same thing as its notation appearing in the final result. The narrower, genuinely open question is whether the *distinctive* machinery of research set theory — forcing, measurable and large cardinals, independence results, inner models, none of which ordinary mathematics actually needs — has any application outside mathematics. There, the answer is still no. Descriptive set theory comes closest (Borel equivalence relations have been used to establish measurable equilibria in Bayesian and stochastic games), but it sits close enough to analysis and topology that it isn't a clean vindication of forcing or large-cardinal set theory specifically. Turing's 1936 reuse of Cantor's diagonalization is a reuse of a *proof technique*, not an application of transfinite set theory itself.",
         verdict="d", gap_basis=None, gap_years=None,
         note="Cantor began in 1874; Cohen's forcing is from 1963. This may simply be a field sitting inside its own waiting period, the same one every other field on this page eventually left.",
         confidence="medium"),

    dict(slug="combinatorics", msc="05", name="Combinatorics",
         cluster="logic",
         one_liner="Counting, arrangement and structure of discrete sets: enumeration, graph theory, design theory.",
         founded=dict(year=1900, event="No single founding event — ancient roots (Pascal's triangle, Euler's Königsberg bridges); became a systematically organized field with Fisher's design theory in the 1920s", low_confidence=True),
         dismissed=None,
         dismissed_note="Retrospectives repeat only a vague, unattributed folk memory that combinatorics was “unserious” mid-century, with no named person or exact quote. One narrow, dated anecdote: Mittag-Leffler shelved 18th-century “combinatorial school” texts under a library label “Dekadenter” (decadent) — targets one obsolete pre-1900 formalist tradition, not the modern field.",
         applications=[
             dict(name="Design of experiments", year=1925, note="R. A. Fisher's combinatorial design theory underlies randomized agricultural and clinical-trial methodology.", url="https://en.wikipedia.org/wiki/Design_of_experiments"),
             dict(name="Reed–Solomon codes", year=1960, note="Enumerative/finite combinatorics underlying error-correcting codes; Voyager, CDs, QR codes.", url="https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction"),
         ],
         verdict="b", gap_basis="no meaningful gap — organized and applied at roughly the same time", gap_years=None,
         confidence="medium"),

    dict(slug="boolean-algebra", msc="06/08", name="Order, lattices & Boolean algebra",
         cluster="logic",
         one_liner="Boole's algebra of logic: propositions manipulated as 0/1 algebraic quantities.",
         founded=dict(year=1854, event="Boole's An Investigation of the Laws of Thought"),
         dismissed=None,
         dismissed_note="Not dismissed, and not actually obscure. Boole's algebra spawned an active 19th-century logic tradition (Jevons, Peirce, Schröder), and Charles Sanders Peirce reportedly sketched an electrical-relay reading of logical operations decades before Shannon. What changed in 1937 wasn't the first hint that Boolean algebra could touch circuits — it was Shannon supplying the first systematic engineering theory showing it could design arbitrary switching circuits, turning a live logical tradition into a design method.",
         applications=[
             dict(name="Digital circuit design", year=1937, note="Claude Shannon's MIT master's thesis proved Boolean algebra maps exactly onto relay/switching circuits — the theoretical foundation of all digital computing.", url="https://en.wikipedia.org/wiki/A_Symbolic_Analysis_of_Relay_and_Switching_Circuits"),
         ],
         verdict="b", gap_basis="founding (1854) to Shannon's thesis (1937)", gap_years=83,
         confidence="high"),

    dict(slug="number-theory", msc="11", name="Number theory",
         cluster="numtheory",
         one_liner="The study of integers, primes, and modular arithmetic.",
         founded=dict(year=1801, event="Gauss's Disquisitiones Arithmeticae"),
         dismissed=dict(kind="hedged", who="G. H. Hardy", year=1915,
             quote="“The Theory of Numbers has always been regarded as one of the most obviously useless branches of Pure Mathematics” (1915 lecture, delivered with sustained irony per the annotated edition); echoed, with explicit hedges (“at present at any rate,” “Time may change all this”), in *A Mathematician's Apology* (1940).",
             source="Hardy, *A Mathematician's Apology*, CUP 1940, §21/§25/§28 (primary text, quoted directly).",
             note="Hardy's case wasn't purely empirical: he also argued serious mathematics is justified as art, independent of use, and he explicitly allowed that time might prove him wrong about the applications. He was too pessimistic about scope and timescale — that's the real story, not a flat, unhedged prediction.",
             confidence="high"),
         applications=[
             dict(name="RSA cryptography", year=1977, note="Rivest–Shamir–Adleman; publicly circulated 1977, the canonical paper appeared in Communications of the ACM in 1978. Security rests on the difficulty of factoring large primes.", url="https://dl.acm.org/doi/10.1145/359340.359342"),
         ],
         verdict="a", gap_basis="founding (1801) to RSA (1977)", gap_years=176,
         confidence="high"),

    dict(slug="galois-theory", msc="12", name="Field theory & Galois theory",
         cluster="algebra",
         one_liner="Which polynomial equations are solvable by radicals — and the finite-field arithmetic this required.",
         founded=dict(year=1830, event="Galois's “Sur la théorie des nombres,” developing finite-field arithmetic — published in his lifetime, in the Bulletin des sciences mathématiques, without much incident"),
         dismissed=None,
         dismissed_note="No dismissal attaches to this specific paper. A separate, related work fared worse: Galois's 1831 memoir on solvability of equations by radicals was rejected by Siméon Poisson for the Paris Academy (“neither sufficiently clear nor sufficiently developed to allow us to judge its rigour”) and published only posthumously in 1846. That memoir became foundational to group theory through Serret, Betti, and Jordan across the rest of the 19th century — actively developed, not shelved — but its influence runs through group theory broadly, not through the specific finite-field arithmetic that Reed–Solomon codes use. The two papers are often run together; they shouldn't be.",
         applications=[
             dict(name="Reed–Solomon codes", year=1960, note="Finite-field (“Galois field”) arithmetic. Voyager's telemetry, CDs, QR codes.", url="https://en.wikipedia.org/wiki/Reed%E2%80%93Solomon_error_correction"),
         ],
         verdict="b", gap_basis="founding (1830) to Reed–Solomon (1960)", gap_years=130,
         confidence="medium"),

    dict(slug="commutative-algebra", msc="13", name="Commutative rings & algebras",
         cluster="algebra",
         one_liner="Ideal theory: rings, ideals, modules — the algebraic foundation of algebraic geometry.",
         founded=dict(year=1871, event="Dedekind's ideal theory"),
         dismissed=None,
         dismissed_note="Krull's ideal theory (1920s–30s) was, per MacTutor, “quickly recognised as a decisive advance.”",
         applications=[
             dict(name="McEliece cryptosystem", year=1978, note="Uses algebraic-geometry (Goppa) codes built on this machinery.", url="https://en.wikipedia.org/wiki/McEliece_cryptosystem"),
             dict(name="NIST post-quantum standards", year=2024, note="Ring-LWE (2012) underlies CRYSTALS-Kyber/Dilithium, finalized as FIPS 203/204.", url="https://csrc.nist.gov/pubs/fips/203/final"),
         ],
         verdict="b", gap_basis="founding (1871) to first cryptographic use (1978)", gap_years=107,
         confidence="medium-high"),

    dict(slug="algebraic-geometry", msc="14", name="Algebraic geometry",
         cluster="numtheory",
         one_liner="Solution sets of polynomial systems — varieties, and in the modern language, schemes.",
         founded=dict(year=1830, event="Abel & Jacobi's elliptic-integral theory, the ancestor of elliptic curves (classical algebraic geometry itself traces further back, to 17th-century curve classification)"),
         dismissed=dict(kind="self-description", who="Koblitz, Menezes & Vanstone (retrospective)", year=2008,
             quote="“Research into number theoretic questions concerning elliptic curves was originally pursued mainly for aesthetic reasons.”",
             source="Koblitz et al., IACR ePrint 2008/390.",
             note="A 2008/2011 retrospective characterization by ECC's own historians, not a contemporaneous 19th-century dismissal. No credible dismissal of algebraic geometry more broadly — including the ultra-abstract Grothendieck/scheme-theoretic reformulation of the 1950s–60s — was found.",
             confidence="medium"),
         applications=[
             dict(name="Elliptic-curve cryptography", year=1985, note="Koblitz & Miller, independently. Bitcoin, TLS, Signal.", url="https://en.wikipedia.org/wiki/Elliptic-curve_cryptography"),
         ],
         verdict="x", gap_basis="founding (1830) to ECC (1985) — for the elliptic-curve sub-story only", gap_years=155,
         note="Mixed field: the elliptic-curve story is a strong case, but the broader, more abstract core of algebraic geometry (schemes, sheaf cohomology) has no well-documented application outside pure mathematics — its most-cited physics connection (Calabi–Yau manifolds in string theory) doesn't clear the real-world bar, since string theory is experimentally unconfirmed.",
         confidence="medium"),

    dict(slug="matrix-theory", msc="15", name="Linear & multilinear algebra; matrix theory",
         cluster="algebra",
         one_liner="Matrices, vector spaces, linear transformations, tensors.",
         founded=dict(year=1858, event="Cayley's A Memoir on the Theory of Matrices"),
         dismissed=None,
         dismissed_note="The famous line calling matrix algebra “an algebra of no conceivable use” is unattested in the standard scholarly history (Higham 2008) and looks apocryphal. A genuine, different Hardy quote exists: *A Mathematician's Apology* (1940) notes “no one foresaw the applications of matrices and groups… to modern physics” — a retrospective note that applications were unforeseen, not a claim they'd never come.",
         applications=[
             dict(name="Matrix mechanics", year=1925, note="Heisenberg, formalized by Born & Jordan — one formulation of quantum mechanics.", url="https://en.wikipedia.org/wiki/Matrix_mechanics"),
             dict(name="Google PageRank", year=1998, note="The principal eigenvector of the web link matrix.", url="https://en.wikipedia.org/wiki/PageRank"),
         ],
         verdict="b", gap_basis="founding (1858) to matrix mechanics (1925)", gap_years=67,
         confidence="high"),

    dict(slug="quaternions", msc="16", name="Associative rings & algebras (quaternions)",
         cluster="algebra",
         one_liner="Hamilton's four-dimensional extension of complex numbers.",
         founded=dict(year=1843, event="Hamilton's discovery of quaternions"),
         dismissed=dict(kind="hostile", who="Lord Kelvin (William Thomson)", year=1892,
             quote="“Quaternions came from Hamilton after his really good work had been done, and though beautifully ingenious, have been an unmixed evil to those who have touched them in any way.”",
             source="Letter to Robert Baldwin Hayward, 1892; standard citation Silvanus Thompson's 1910 biography of Kelvin.",
             note="By the 1890s quaternions had genuinely lost ground to Gibbs's and Heaviside's vector calculus.", confidence="high"),
         applications=[
             dict(name="3D computer graphics (SLERP)", year=1985, note="Ken Shoemake's quaternion interpolation, SIGGRAPH. Standard in every game engine since.", url="https://en.wikipedia.org/wiki/Slerp"),
             dict(name="Gimbal-lock-free attitude control", year=1985, note="Fixes the exact failure Apollo 11's inertial platform hit in 1969.", url="https://en.wikipedia.org/wiki/Gimbal_lock"),
         ],
         verdict="a", gap_basis="founding (1843) to graphics/aerospace adoption (1985)", gap_years=142,
         confidence="high"),

    dict(slug="lie-algebras", msc="17", name="Lie algebras & nonassociative algebra",
         cluster="algebra",
         one_liner="The linearization of continuous symmetry: vector spaces with a bracket [x,y].",
         founded=dict(year=1874, event="Sophus Lie's foundational work"),
         dismissed=None,
         dismissed_note="Complaints targeted comprehension difficulty (“Lie's clumsy formalism… rendered his theories obscure”), not value — Lie himself confidently predicted future recognition.",
         applications=[
             dict(name="The Eightfold Way", year=1961, note="Gell-Mann & Ne'eman's su(3) representation theory organized hadrons and predicted the Ω⁻ baryon, confirmed at Brookhaven in 1964.", url="https://en.wikipedia.org/wiki/Eightfold_way_(physics)"),
         ],
         verdict="b", gap_basis="founding (1874) to the Eightfold Way (1961)", gap_years=87,
         confidence="medium-high"),

    dict(slug="category-theory", msc="18", name="Category theory & homological algebra",
         cluster="algebra",
         one_liner="Objects, morphisms, and composition — the structural patterns common to all of mathematics.",
         founded=dict(year=1945, event="Eilenberg & Mac Lane's General Theory of Natural Equivalences"),
         dismissed=dict(kind="self-label", who="attributed to Norman Steenrod", year=1945,
             quote="“Abstract nonsense” — an affectionate in-joke, not a hostile dismissal.",
             source="Attribution via Rotman (Bull. AMS 33:4, 1996) and McLarty (Br. J. Philos. Sci. 41, 1990); no primary quote from Steenrod himself has surfaced.",
             note="Coined by, and popular among, its own early practitioners — the opposite of an outside attack.",
             confidence="medium"),
         applications=[
             dict(name="Monads in functional programming", year=1989, note="Moggi applies category-theoretic monads to programming-language semantics; standardized as Haskell's I/O mechanism by 1996.", url="https://en.wikipedia.org/wiki/Monad_(functional_programming)"),
         ],
         verdict="a", gap_basis="founding (1945) to Moggi's monads (1989)", gap_years=44,
         confidence="medium"),

    dict(slug="k-theory", msc="19", name="K-theory",
         cluster="algebra",
         one_liner="Vector bundles (or their algebraic analogues) classified via stable-isomorphism groups.",
         founded=dict(year=1957, event="Grothendieck's algebraic K-theory (K₀); topological K-theory follows with Atiyah–Hirzebruch, 1959–61 — right at the 1960 boundary"),
         dismissed=None,
         dismissed_note="No credible dismissal found.",
         applications=[
             dict(name="Classification of topological phases of matter", year=2009, note="Kitaev's K-theory classification of topological insulators and superconductors, later sharpened via KR-theory for the Z₂ invariants of time-reversal-invariant topological insulators, and extended to numerical K-theory for nonlinear topological materials (2023), motivated partly by photonic devices such as topological lasers and frequency combs. Experimentally real (HgTe wells, Bi₂Se₃) and an active, named use of K-theory as the classification language — not just borrowed vocabulary.", url="https://en.wikipedia.org/wiki/Topological_insulator"),
         ],
         verdict="s", gap_basis="founding (1957) to the topological-insulator classification (2009)", gap_years=52,
         note="Working physicists often compute a Chern number or Z₂ invariant without saying “K-theory” — but that's not a good reason to say K-theory has no application, any more than compiled arithmetic disqualifies calculus. It is real and scientifically important, but not yet mass-market infrastructure: commercial/technological importance remains emergent. D-branes in string theory, the other commonly cited tie, still doesn't clear this bar — string theory is experimentally unconfirmed.",
         confidence="medium"),

    dict(slug="group-theory", msc="20/22", name="Group theory & Lie groups",
         cluster="algebra",
         one_liner="The algebra of symmetry, and its continuous (Lie) generalization.",
         founded=dict(year=1854, event="Cayley's abstract definition of a group"),
         dismissed=None,
         dismissed_note="Weaker than it's often told. Burnside's 1897 preface to *Theory of Groups of Finite Order* explains an omission — given the results then known to him, he found it hard to name a result more directly reached via linear-transformation groups than via substitution groups — which is a narrow, time-qualified editorial judgment, not a forecast that the topic would never produce anything. Scholarship also cautions he may not even have meant Frobenius's brand-new representation theory: the relevant Frobenius paper connecting character theory to linear substitutions appears to have followed Burnside's preface within the same year. By the 1911 second edition, new results had changed Burnside's assessment. Separately, physicists in the late 1920s coined “Gruppenpest” (the group-plague) for group-representation methods arriving in quantum mechanics, commonly traced to Paul Ehrenfest's circle in Leiden (1928) — but Ehrenfest himself did not reject the theory and ran seminars on it; the episode was a mix of enthusiasm, skepticism, fashion, and pedagogical frustration, not a clean dismissal.",
         applications=[
             dict(name="Crystallography", year=1891, note="Fedorov & Schoenflies's 230 space groups classify every possible crystal structure.", url="https://en.wikipedia.org/wiki/Space_group"),
             dict(name="Quantum mechanics", year=1928, note="Wigner, Weyl, Hund apply group representation theory to QM, amid the mixed reception nicknamed “Gruppenpest.”", url="https://en.wikipedia.org/wiki/Standard_Model"),
             dict(name="The Standard Model", year=1973, note="Gauge symmetry, SU(3)×SU(2)×U(1), is representation theory.", url="https://en.wikipedia.org/wiki/Standard_Model"),
         ],
         verdict="b", gap_basis="founding (1854) to crystallography (1891)", gap_years=37,
         confidence="medium"),

    dict(slug="measure-theory", msc="26/28", name="Real analysis & measure theory",
         cluster="analysis",
         one_liner="Lebesgue's rigorous theory of measure and integration.",
         founded=dict(year=1902, event="Lebesgue's thesis on integration"),
         dismissed=None,
         dismissed_note="Real controversy existed (Borel's constructivist objections, du Bois-Reymond's rigor arguments) but concerned legitimacy, not usefulness.",
         applications=[
             dict(name="Axiomatic probability theory", year=1933, note="Kolmogorov's Grundbegriffe — the now-universal measure-theoretic foundation of probability.", url="https://en.wikipedia.org/wiki/Probability_axioms"),
         ],
         verdict="b", gap_basis="founding (1902) to Kolmogorov's axiomatization (1933)", gap_years=31,
         confidence="medium-high"),

    dict(slug="complex-analysis", msc="30", name="Complex analysis",
         cluster="analysis",
         one_liner="Holomorphic functions of a complex variable: Cauchy's theorem, residues, conformal mapping.",
         founded=dict(year=1825, event="Cauchy's integral theorem"),
         dismissed=None,
         dismissed_note="Cardano's “as subtle as it is useless” (1545) and Descartes coining “imaginary” (1637) as an insult both target *complex numbers*, roughly two centuries before complex analysis existed as a field — conflating the two would misattribute the dismissal.",
         applications=[
             dict(name="AC circuit analysis", year=1893, note="Charles Steinmetz's complex-impedance/phasor method for electrical engineering.", url="https://en.wikipedia.org/wiki/Charles_Proteus_Steinmetz"),
         ],
         verdict="b", gap_basis="founding (1825) to Steinmetz (1893)", gap_years=68,
         confidence="medium"),

    dict(slug="potential-theory", msc="31", name="Potential theory",
         cluster="analysis",
         one_liner="Harmonic functions — solutions of Laplace's equation.",
         founded=dict(year=1828, event="Green's essay on electricity and magnetism"),
         dismissed=None,
         dismissed_note="Born directly from physics (Newtonian gravitation, electrostatics) and never abstracted away from application before being taken seriously. One aside: Green's own 1828 essay was neglected (51 subscribers) until Kelvin rediscovered it in the 1840s — obscurity, not a “useless” verdict.",
         applications=[
             dict(name="Electrostatics & gravitational modeling", year=1828, note="Applied essentially from the moment of its rigorous formulation.", url="https://en.wikipedia.org/wiki/Potential_theory"),
         ],
         verdict="b", gap_basis="applied from inception — no meaningful gap", gap_years=0,
         confidence="medium"),

    dict(slug="several-complex-variables", msc="32", name="Several complex variables",
         cluster="analysis",
         one_liner="Holomorphic functions of two or more complex variables — genuinely new obstructions appear.",
         founded=dict(year=1906, event="Hartogs's extension phenomenon"),
         dismissed=None,
         dismissed_note="No credible dismissal found.",
         applications=[
             dict(name="Multidimensional systems engineering", year=1975, note="Stability of m-D digital filters is governed by domain-of-holomorphy conditions with no 1-D analogue. Bose's Applied Multidimensional Systems Theory documents functions and polynomials of several complex variables underlying image processing, multidimensional control, iterative learning control, network synthesis, geophysical signal processing, and multidimensional convolutional coding — genuinely several-variable phenomena, not just notation borrowed from one-variable theory, since stability, realization, and interpolation behave differently once there's more than one complex variable. A related literature connects multidimensional robust control with multivariable Nevanlinna–Pick interpolation and H^∞ theory.", url="https://en.wikipedia.org/wiki/Multidimensional_filter_design"),
         ],
         verdict="s", gap_basis="founding (1906) to multidimensional filter/control theory (1975)", gap_years=69,
         note="Definitely applied, but niche: not RSA or GPS. “No major application” is defensible only under a narrow reading of “major” as “visible in mass-market infrastructure” — “no known application” would be false. String theory's Calabi–Yau connection and twistor theory also use this machinery but don't clear the real-world bar on their own (unconfirmed physics). This entry's specific citations (Bose's textbook, the robust-control/Nevanlinna–Pick literature) rest on a single secondary characterization rather than the primary literature, so confidence here is lower than elsewhere on the Ledger.",
         confidence="medium"),

    dict(slug="special-functions", msc="33", name="Special functions",
         cluster="analysis",
         one_liner="Bessel, hypergeometric, and elliptic functions — named solutions of specific differential equations.",
         founded=dict(year=1732, event="Daniel Bernoulli's work on the hanging chain (an early Bessel-type equation)"),
         dismissed=None,
         dismissed_note="The Gauss “supreme uselessness” line sometimes attached here is about number theory, a different field, and is itself apocryphal (Hardy says so in the *Apology*). Bessel functions, hypergeometric series, and elliptic integrals were all motivated by concrete physical problems (pendulums, planetary perturbation, arc length) from the start.",
         applications=[
             dict(name="Elliptic-curve cryptography", year=1985, note="Abel & Jacobi's abstract elliptic-function theory (1827) sat as pure mathematics for 158 years before ECC — the one genuinely delayed pocket in an otherwise immediately-applied field.", url="https://en.wikipedia.org/wiki/Elliptic-curve_cryptography"),
         ],
         verdict="x", gap_basis="Abel's elliptic functions (1827) to ECC (1985) — the field's one delayed sub-story; Bessel/hypergeometric functions were applied from birth", gap_years=158,
         confidence="medium"),

    dict(slug="ordinary-differential-equations", msc="34", name="Ordinary differential equations",
         cluster="analysis",
         one_liner="Equations relating a function of one variable to its derivatives.",
         founded=dict(year=1687, event="Newton's Principia"),
         dismissed=None,
         dismissed_note="Tied to mechanics and orbital motion from inception. Confidence on the absence of a dismissal is lower here than elsewhere on the Ledger.",
         applications=[
             dict(name="Orbital mechanics", year=1687, note="Newton derives Kepler's laws in the same work that founds the field.", url="https://en.wikipedia.org/wiki/Ordinary_differential_equation"),
         ],
         verdict="b", gap_basis="applied from inception — no meaningful gap", gap_years=0,
         confidence="low-medium"),

    dict(slug="partial-differential-equations", msc="35", name="Partial differential equations",
         cluster="analysis",
         one_liner="Equations involving unknown functions of several variables and their partial derivatives.",
         founded=dict(year=1747, event="d'Alembert's wave equation"),
         dismissed=None,
         dismissed_note="Born from 18th/19th-century physics. The one documented case is neglect, not dismissal: Courant's 1943 piecewise-linear variational method went unrecognized for over a decade until independently rediscovered by structural engineers (1954–56).",
         applications=[
             dict(name="Finite element method", year=1956, note="Argyris, Turner, Clough, Martin & Topp's engineering rediscovery of Courant's 1943 method — standard in structural, aerospace and civil simulation.", url="https://en.wikipedia.org/wiki/Finite_element_method"),
         ],
         verdict="b", gap_basis="applied from inception for the classical theory; Sobolev's 1938 abstract reformulation to FEM engineering deployment (1956) is an 18-year pocket", gap_years=0,
         confidence="medium-high"),

    dict(slug="dynamical-systems", msc="37", name="Dynamical systems & ergodic theory",
         cluster="analysis",
         one_liner="Poincaré's qualitative theory of the three-body problem: deterministic systems can be unpredictable.",
         founded=dict(year=1890, event="Poincaré's corrected prize memoir on the three-body problem"),
         dismissed=None,
         dismissed_note="No named dismissal, but treated as a narrow celestial-mechanics curiosity by nearly everyone — obscure enough that Stephen Smale rediscovered the same ideas independently in the late 1950s.",
         applications=[
             dict(name="Chaos theory & weather-forecast limits", year=1963, note="Lorenz independently rediscovers sensitive dependence on initial conditions in a weather model — founds the modern predictability-limit theory.", url="https://en.wikipedia.org/wiki/Chaos_theory"),
         ],
         verdict="b", gap_basis="founding (1890) to Lorenz (1963)", gap_years=73,
         confidence="high"),

    dict(slug="summability-theory", msc="40/41", name="Classical analysis: series & summability",
         cluster="analysis",
         one_liner="Summing divergent series by generalized methods (Cesàro, Abel, Borel).",
         founded=dict(year=1899, event="Borel's rigorous summation method (the axiomatized theory MSC classifies)"),
         dismissed=dict(kind="hostile", who="Niels Henrik Abel; separately, Gösta Mittag-Leffler quoting Weierstrass", year=1826,
             quote="“Divergent series are in general something fatal… you can get whatever result you want when you use them” (Abel, letter to Holmboe, 1826). Separately, Borel's 1899 method was rebuffed with “The Master [Weierstrass] forbids it.”",
             source="Abel's *Oeuvres complètes*; Wikipedia's “Borel summation” article for the Mittag-Leffler line.",
             note="Abel's 1826 complaint targets pre-rigorous, ad hoc use of divergent series 73 years before the axiomatized theory MSC 40/41 actually covers — the dismissal predates the field's formal founding.",
             confidence="medium"),
         applications=[
             dict(name="Critical exponents in condensed matter", year=1977, note="Le Guillou & Zinn-Justin's Borel–Padé resummation of the renormalization-group ε-expansion, tested against real 3D Ising/O(N) experiments.", url="https://en.wikipedia.org/wiki/Renormalization_group"),
         ],
         verdict="a", gap_basis="rigorous founding (1899) to the condensed-matter application (1977)", gap_years=78,
         confidence="medium"),

    dict(slug="fourier-analysis", msc="42", name="Fourier analysis",
         cluster="analysis",
         one_liner="Representing functions as sums of sines and cosines.",
         founded=dict(year=1822, event="Fourier's Théorie analytique de la chaleur"),
         dismissed=None,
         dismissed_note="The 1807 Paris Academy committee (Lagrange, Laplace, Monge, Lacroix) objected to representing arbitrary functions as trigonometric series on *rigor* grounds, not utility — the underlying problem (heat conduction) was never in question.",
         applications=[
             dict(name="Tide-predicting machine", year=1872, note="Kelvin's harmonic analysis of tidal constituents — an early, concrete engineering application.", url="https://en.wikipedia.org/wiki/Tide-predicting_machine"),
         ],
         verdict="b", gap_basis="founding (1822) to Kelvin's tide predictor (1872)", gap_years=50,
         confidence="medium-high"),

    dict(slug="abstract-harmonic-analysis", msc="43", name="Abstract harmonic analysis",
         cluster="analysis",
         one_liner="Fourier analysis generalized to representation theory on locally compact groups (Pontryagin duality).",
         founded=dict(year=1934, event="Pontryagin duality"),
         dismissed=None,
         dismissed_note="No credible dismissal found.",
         applications=[
             dict(name="Fast SO(3) Fourier transforms", year=2000, note="Harmonic analysis on SO(3), built from irreducible representations and Wigner D-matrices — compact-group harmonic analysis, not ordinary scalar Fourier analysis. Fast SO(3) transforms are an active numerical topic, used in computational structural biology to calculate rigid-body rotational correlations of three-dimensional objects.", url="https://en.wikipedia.org/wiki/Wigner_D-matrix"),
         ],
         verdict="s", gap_basis="founding (1934) to fast SO(3) transform methods (~2000)", gap_years=66,
         note="The AMS itself describes commutative and noncommutative harmonic analysis as feeding applications in signal processing, multiplexing, cosmology, and astrophysics. Calling this “just generalized Fourier analysis” is a fair description, not a disqualification — that's what abstract harmonic analysis is; excluding an application because it manifests as a Fourier transform on a non-Euclidean group comes close to excluding its applications by definition. No mass-market application has yet been identified where the group-theoretic machinery is unmistakably indispensable, which is why this stays “specialized” rather than “infrastructure.” The SO(3)-transform and AMS characterizations here rest on a single secondary characterization rather than the primary literature, so confidence is lower than elsewhere on the Ledger.",
         confidence="medium"),

    dict(slug="integral-equations", msc="44/45", name="Integral transforms & integral equations",
         cluster="analysis",
         one_liner="Laplace-type transforms and the Fredholm/Volterra theory of integral equations.",
         founded=dict(year=1880, event="Heaviside's operational calculus"),
         dismissed=dict(kind="rigor-rejection", who="William Burnside (Royal Society referee) & Peter Guthrie Tait", year=1893,
             quote="Burnside rejected a Heaviside paper for “irredeemable inadequacies in proof”; Tait attacked his methods in *Nature*.",
             source="MacTutor History of Mathematics.",
             note="A rigor critique, not a usefulness one — Heaviside's methods were already solving real telegraphy problems while under attack; the rigorous justification (Bromwich) came only in the 1910s. A reversed pattern: applied first, proved later.",
             confidence="medium"),
         applications=[
             dict(name="Feedback amplifier design", year=1927, note="Bode/Nyquist/Black at Bell Labs codify Laplace-transform methods for circuit and control engineering.", url="https://en.wikipedia.org/wiki/Hendrik_Wade_Bode"),
             dict(name="Actuarial calculations", year=1904, note="Fredholm himself applied his own integral equations at Skandia insurance.", url="https://en.wikipedia.org/wiki/Fredholm_integral_equation"),
         ],
         verdict="b", gap_basis="Heaviside's methods were used by engineers before they were proved rigorous — applied essentially immediately", gap_years=0,
         confidence="medium-high"),

    dict(slug="functional-analysis", msc="46/47", name="Functional analysis & operator theory",
         cluster="analysis",
         one_liner="Infinite-dimensional vector spaces, studied for their own analytic properties.",
         founded=dict(year=1904, event="Hilbert's papers on integral equations"),
         dismissed=dict(kind="hostile", who="David Hilbert (on his own work)", year=1904,
             quote="“I developed my theory of infinitely many variables from purely mathematical interests, and even called it ‘spectral analysis’ without any presentiment that it would later find application to the actual spectrum of physics.”",
             source="Widely attributed via Lynn Steen, *American Mathematical Monthly* 80(4), 1973; primary provenance unconfirmed.",
             note=None, confidence="medium"),
         applications=[
             dict(name="Quantum mechanics", year=1932, note="Von Neumann's Mathematical Foundations of Quantum Mechanics — quantum states are vectors in Hilbert space.", url="https://en.wikipedia.org/wiki/Mathematical_formulation_of_quantum_mechanics"),
         ],
         verdict="a", gap_basis="founding (1904) to von Neumann (1932)", gap_years=28,
         confidence="medium-high"),

    dict(slug="calculus-of-variations", msc="49", name="Calculus of variations & optimal control",
         cluster="analysis",
         one_liner="Extremizing functionals — and, later, optimally steering dynamical systems over time.",
         founded=dict(year=1696, event="Johann Bernoulli's brachistochrone challenge"),
         dismissed=None,
         dismissed_note="True in none of the three eras checked: classical Bernoulli/Euler/Lagrange, the 20th-century functional-analytic “direct method” reformulation, and Pontryagin/Bellman-era optimal control.",
         applications=[
             dict(name="Rocket trajectory optimization", year=1956, note="Pontryagin's maximum principle, created explicitly for this purpose.", url="https://en.wikipedia.org/wiki/Pontryagin%27s_maximum_principle"),
         ],
         verdict="b", gap_basis="applied from inception in every era — no meaningful gap", gap_years=0,
         confidence="medium-high"),

    dict(slug="discrete-geometry", msc="51/52", name="Geometry: classical, convex & discrete",
         cluster="geometry",
         one_liner="Packings, polytopes, lattice arrangements — the Kepler conjecture on stacking spheres.",
         founded=dict(year=1611, event="Kepler's sphere-packing conjecture, posed after Raleigh asked Harriot about stacking cannonballs — a genuinely practical origin"),
         dismissed=None,
         dismissed_note="Despite the field's long unresolved-curiosity reputation.",
         applications=[
             dict(name="Coding theory (Leech lattice)", year=1965, note="Ties to the binary Golay code, used in Voyager's deep-space communication.", url="https://en.wikipedia.org/wiki/Leech_lattice"),
             dict(name="Lattice-based post-quantum cryptography", year=2005, note="Regev's LWE and NTRU underlie NIST's finalized post-quantum standards.", url="https://en.wikipedia.org/wiki/Lattice-based_cryptography"),
         ],
         verdict="x", gap_basis="a practical 1611 origin, then centuries of pure dormancy, before an unrelated application (coding theory) emerged", gap_years=354,
         note="Doesn't fit the clean categories: never dismissed, and the eventual application is strong — but it arrived only after a genuinely multi-century gap, not “early.”",
         confidence="high"),

    dict(slug="differential-geometry", msc="53", name="Differential geometry",
         cluster="geometry",
         one_liner="Non-Euclidean and Riemannian geometry: the mathematics of curved space.",
         founded=dict(year=1854, event="Riemann's habilitation lecture on the geometry of curved manifolds"),
         dismissed=dict(kind="anticipated-hostility", who="Carl Friedrich Gauss", year=1829,
             quote="“It may take very long before I make public my investigations on this issue… for I fear the clamor of the Boeotians.”",
             source="Letter to Bessel, 1829.",
             note="A different failure mode from Hardy's or Kelvin's: Gauss valued this mathematics highly and wasn't calling it useless — he feared hostile reception from unsympathetic contemporaries (“Boeotians,” a classical slur for the intellectually dull), not that the work lacked value. The field was nonetheless widely regarded as a logical exercise with no physical relevance until the 1860s–70s.",
             confidence="high"),
         applications=[
             dict(name="General Relativity", year=1915, note="Einstein. Requires Riemann's geometry of curved manifolds as its literal language.", url="https://en.wikipedia.org/wiki/General_relativity"),
             dict(name="GPS", year=1977, note="Uncorrected relativistic clock drift ⇒ roughly 10km/day position error — confirmed on the NTS-2 satellite.", url="https://en.wikipedia.org/wiki/Error_analysis_for_the_Global_Positioning_System"),
         ],
         verdict="a", gap_basis="founding (1854) to General Relativity (1915)", gap_years=61,
         confidence="high"),

    dict(slug="general-topology", msc="54", name="General topology",
         cluster="topology",
         one_liner="Point-set topology: the abstract study of continuity, compactness, and convergence.",
         founded=dict(year=1914, event="Hausdorff's Grundzüge der Mengenlehre"),
         dismissed=None,
         dismissed_note="This entry is a lower-confidence synthesis rather than a sourced claim; treat with appropriate caution. Constructivist/intuitionist objections (Brouwer) concerned foundations, not utility.",
         applications=[
             dict(name="General equilibrium economics", year=1954, note="Arrow & Debreu's existence proof uses Kakutani's 1941 fixed-point theorem, built on compactness (Tychonoff).", url="https://en.wikipedia.org/wiki/Arrow%E2%80%93Debreu_model"),
         ],
         verdict="b", gap_basis="founding (1914) to Arrow–Debreu (1954)", gap_years=40,
         confidence="low-medium"),

    dict(slug="algebraic-topology", msc="55", name="Algebraic topology",
         cluster="topology",
         one_liner="Topological spaces studied via algebraic invariants: homology, cohomology.",
         founded=dict(year=1895, event="Poincaré's Analysis Situs"),
         dismissed=None,
         dismissed_note="Topology's founding self-understanding — discarding exactly the distances and coordinates data analysis depends on — is a fair characterization of the field's design, not a quote from a named critic.",
         applications=[
             dict(name="Topological data analysis", year=2002, note="Edelsbrunner–Letscher–Zomorodian's persistent-homology algorithm.", url="https://en.wikipedia.org/wiki/Topological_data_analysis"),
             dict(name="Breast-cancer subtype discovery", year=2011, note="Nicolau–Levine–Carlsson, PNAS — 295 tumors as points in 24,479 dimensions.", url="https://doi.org/10.1073/pnas.1102826108"),
         ],
         verdict="b", gap_basis="founding (1895) to persistent homology (2002)", gap_years=107,
         confidence="medium-high"),

    dict(slug="knot-theory", msc="57/58", name="Manifolds & low-dimensional topology (knot theory)",
         cluster="topology",
         one_liner="Kelvin's wrong theory that atoms were knotted vortices accelerated a mathematical field that already existed.",
         founded=dict(year=1847, event="Johann Benedict Listing's Vorstudien zur Topologie, with earlier linking-number work by Gauss (1833) — knot theory predates Kelvin by two decades"),
         dismissed=dict(kind="wrong-physics", who="Lord Kelvin", year=1867,
             quote="Proposed atoms were knotted vortices in the luminiferous aether — completely wrong physics, abandoned within decades.",
             source="Kelvin, “On Vortex Atoms,” Proc. Royal Society of Edinburgh, 1867.",
             note="Kelvin's theory didn't originate knot theory — Gauss and Listing got there first — but it accelerated and systematized it, motivating Tait's exhaustive tabulation of knots once the physics collapsed.",
             confidence="high"),
         applications=[
             dict(name="DNA topology", year=1990, note="Topoisomerases manage DNA knotting and supercoiling (Sumners et al.).", url="https://en.wikipedia.org/wiki/Topoisomerase"),
             dict(name="Topological quantum computing", year=1997, note="Kitaev's proposal to use anyons — particles that braid like knots.", url="https://en.wikipedia.org/wiki/Topological_quantum_computer"),
         ],
         verdict="a", gap_basis="founding (1847) to DNA topology (1990)", gap_years=143,
         confidence="high"),

    dict(slug="probability-theory", msc="60", name="Probability theory",
         cluster="analysis",
         one_liner="The mathematics of randomness, later axiomatized via measure theory.",
         founded=dict(year=1654, event="Pascal & Fermat's correspondence on gambling problems"),
         dismissed=None,
         dismissed_note="Not at any level of abstraction, including Kolmogorov's 1933 measure-theoretic axiomatization, which “became the mostly undisputed axiomatic basis” essentially immediately. Invented to solve a practical problem and never stopped being applied.",
         applications=[
             dict(name="Actuarial science & statistical mechanics", year=1654, note="Applied from the field's origin.", url="https://en.wikipedia.org/wiki/Probability_theory"),
             dict(name="Black–Scholes options pricing", year=1973, note="Itô calculus, built on measure-theoretic probability, underlies modern derivatives markets.", url="https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model"),
         ],
         verdict="b", gap_basis="applied from inception — the clean control case: never even a candidate for the myth", gap_years=0,
         confidence="high"),
]

VERDICT_LABELS = {
    "a": "Named dismissal, later applied",
    "b": "Never dismissed, applied anyway",
    "s": "Real application, but specialized — not mass-market infrastructure",
    "d": "No external application documented",
    "x": "Mixed / doesn't fit cleanly",
}


def slugify_check():
    slugs = [f["slug"] for f in FIELDS]
    assert len(slugs) == len(set(slugs)), "duplicate slugs"


def write_fields_data_js():
    payload = []
    for f in FIELDS:
        payload.append(f)
    js = "// Generated by scripts/build_site.py — do not hand-edit.\n"
    js += "const CLUSTERS = " + json.dumps(CLUSTERS, indent=2) + ";\n"
    js += "const VERDICT_LABELS = " + json.dumps(VERDICT_LABELS, indent=2) + ";\n"
    js += "const FIELDS = " + json.dumps(payload, indent=2, ensure_ascii=False) + ";\n"
    with open(os.path.join(DOCS, "fields-data.js"), "w") as fh:
        fh.write(js)


NAV = """  <header class="site-header">
    <div class="nav-inner">
      <a class="brand" href="{root}index.html">pure</a>
      <nav>
        <a href="{root}intro.html">Methodology</a>
        <span class="menu" tabindex="0">
          <span class="menu-label">Explore</span>
          <span class="drop">
            <span class="drop-panel">
              <a href="{root}ledger.html">The Ledger</a>
              <a href="{root}map.html">Map</a>
              <a href="{root}timeline.html">Timeline</a>
              <a href="{root}survival.html">Survival</a>
            </span>
          </span>
        </span>
        <a href="{root}abstraction.html">Abstraction</a>
        <a href="{root}sources.html">Sources</a>
        <a href="https://github.com/microprediction/pure">GitHub</a>
      </nav>
    </div>
  </header>
"""


def esc(s):
    if s is None:
        return ""
    return s


_ENTITY_NAMES = ("amp|lt|gt|quot|apos|mdash|ndash|rsquo|lsquo|rdquo|ldquo|hellip|rarr|larr|"
                 "middot|sect|eacute|egrave|ouml|uuml|auml|ntilde|times|sim|infin|le|ge|ne|"
                 "deg|copy|reg|trade|oacute|iacute|aacute|uacute|ograve|agrave|ecirc|acirc|"
                 "ocirc|ucirc|icirc|ccedil")
_BARE_AMP = re.compile(r"&(?!#\d+;)(?!(?:" + _ENTITY_NAMES + r");)")
_SCRIPT_BLOCK = re.compile(r"<script>.*?</script>", re.S)


def escape_amp_outside_scripts(html):
    """Escape bare & to &amp; everywhere except inside inline <script> blocks
    (script content is raw text to the HTML parser; entity-escaping it there
    would corrupt JS operators like && and any literal-& string data)."""
    parts = []
    last = 0
    for m in _SCRIPT_BLOCK.finditer(html):
        parts.append(_BARE_AMP.sub("&amp;", html[last:m.start()]))
        parts.append(m.group(0))
        last = m.end()
    parts.append(_BARE_AMP.sub("&amp;", html[last:]))
    return "".join(parts)


def md(s):
    """Minimal markdown->HTML: *word* becomes <em>word</em>."""
    if s is None:
        return ""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)


def render_field_page(f):
    root = "../"
    dismissed_html = ""
    if f.get("dismissed"):
        d = f["dismissed"]
        who = d.get("who", "")
        year = d.get("year", "")
        quote = md(d.get("quote", ""))
        source = md(d.get("source", ""))
        note = md(d.get("note"))
        dismissed_html = f"""
    <h2>The claim</h2>
    <div class="dismissal">
      <span class="who">{who}</span>, {year}: {quote}
    </div>
    <p class="confidence">Source: {source}</p>
"""
        if note:
            dismissed_html += f"    <p class=\"muted\">{note}</p>\n"
    else:
        note = md(f.get("dismissed_note", "No dismissal on record."))
        dismissed_html = f"""
    <h2>The claim</h2>
    <p class="muted"><strong>No credible dismissal found.</strong> {note}</p>
"""

    apps = f.get("applications") or []
    if apps:
        app_html = "\n    <h2>What happened</h2>\n"
        for a in apps:
            url = a.get("url")
            name_html = f'<a href="{url}">{a["name"]}</a>' if url else a["name"]
            app_html += f"""    <div class="application">
      <strong>{name_html}</strong> ({a["year"]}) &mdash; {md(a["note"])}
    </div>
"""
    else:
        app_html = f"""
    <h2>What happened</h2>
    <p class="muted"><strong>No major real-world application is well-documented today.</strong> {md(f.get("applications_note", ""))}</p>
"""

    gap = f.get("gap_years")
    gap_badge = ""
    if gap is not None:
        gap_badge = f'<span class="gap-badge">{gap} years &mdash; {md(esc(f.get("gap_basis")))}</span>'
    elif f.get("gap_basis"):
        gap_badge = f'<span class="gap-badge">{md(esc(f.get("gap_basis")))}</span>'
    gap_para = f"    <p>{gap_badge}</p>\n" if gap_badge else ""

    extra_note = md(f.get("note"))
    extra_html = f'<p class="muted">{extra_note}</p>' if extra_note else ""

    founded = f["founded"]
    founded_flag = " <span class=\"confidence\">(approximate)</span>" if founded.get("low_confidence") else ""

    verdict_label = VERDICT_LABELS[f["verdict"]]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Pure: {f["name"]}</title>
  <meta name="description" content="{f["one_liner"]}">
  <link rel="stylesheet" href="{root}style.css" />
</head>
<body>
{NAV.format(root=root)}
  <main>
    <p class="pagenav"><a href="{root}ledger.html">&larr; The Ledger</a></p>
    <span class="field-tag">MSC {f["msc"]} &middot; {CLUSTERS[f["cluster"]]["label"]}</span>
    <h1>{f["name"]}</h1>
    <p class="subtitle">{f["one_liner"]}</p>

    <p><strong>Founded:</strong> {founded["year"]} &mdash; {md(founded["event"])}{founded_flag}</p>
{dismissed_html}{app_html}
{gap_para}    <p class="verdict"><strong>Verdict:</strong> {verdict_label}.</p>
    {extra_html}
    <p class="confidence">Confidence: {f["confidence"]}.</p>
  </main>

  <footer>
    Part of the <a href="{root}ledger.html">34-field survey</a> &mdash;
    <a href="https://github.com/microprediction/pure">microprediction/pure</a>.
  </footer>
</body>
</html>
"""
    return html


def write_field_pages():
    for f in FIELDS:
        html = escape_amp_outside_scripts(render_field_page(f))
        path = os.path.join(FIELDS_DIR, f["slug"] + ".html")
        with open(path, "w") as fh:
            fh.write(html)


def compute_stats():
    n = len(FIELDS)
    by_verdict = {}
    for f in FIELDS:
        by_verdict.setdefault(f["verdict"], []).append(f)
    gaps = [f["gap_years"] for f in FIELDS if f.get("gap_years") not in (None,)]
    avg_gap = sum(gaps) / len(gaps) if gaps else 0
    return dict(
        total=n,
        dismissed_applied=len(by_verdict.get("a", [])),
        never_dismissed_applied=len(by_verdict.get("b", [])),
        specialized=len(by_verdict.get("s", [])),
        no_application=len(by_verdict.get("d", [])),
        mixed=len(by_verdict.get("x", [])),
        avg_gap=round(avg_gap),
        min_gap=min(gaps) if gaps else None,
        max_gap=max(gaps) if gaps else None,
    )


def render_ledger():
    stats = compute_stats()
    rows = []
    for f in sorted(FIELDS, key=lambda f: f["msc"]):
        dismissed_str = "Yes" if f.get("dismissed") else "No"
        if f["verdict"] == "s":
            app_str = "Yes (specialized)"
        elif f["verdict"] == "d":
            app_str = "Thin/speculative" if f.get("applications") else "No"
        else:
            app_str = "Yes" if f.get("applications") else "No"
        gap = f.get("gap_years")
        gap_str = f"{gap}" if gap is not None else "&mdash;"
        url = f"./fields/{f['slug']}.html"
        rows.append(f"""        <tr data-verdict="{f['verdict']}" data-gap="{gap if gap is not None else -1}">
          <td>{f['msc']}</td>
          <td><a href="{url}">{f['name']}</a></td>
          <td>{dismissed_str}</td>
          <td>{app_str}</td>
          <td>{gap_str}</td>
          <td>{VERDICT_LABELS[f['verdict']]}</td>
        </tr>""")
    rows_html = "\n".join(rows)

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Pure: The Ledger</title>
  <meta name="description" content="A full survey of {stats['total']} pure-math fields from the 1959 Mathematics Subject Classification: which were ever declared useless, and what each one became.">
  <link rel="stylesheet" href="./style.css" />
  <style>
    table.impl th {{ cursor: pointer; user-select: none; }}
    table.impl th:hover {{ color: var(--ink); }}
    table.impl th.sort-asc::after {{ content: " \\25B2"; }}
    table.impl th.sort-desc::after {{ content: " \\25BC"; }}
    .filters {{ display: flex; gap: 8px; flex-wrap: wrap; margin: 14px 0; }}
    .filters button {{ font-size: 0.85rem; padding: 5px 12px; border-radius: 14px; border: 1px solid var(--border);
      background: #fff; cursor: pointer; color: var(--muted); }}
    .filters button.active {{ background: var(--ink); color: #fff; border-color: var(--ink); }}
  </style>
</head>
<body>
{NAV.format(root="./")}
  <main>
    <p class="pagenav"><a href="./index.html">&larr; Home</a></p>
    <h1>The Ledger</h1>
    <p class="subtitle">Every pure-math field in the 1959 Mathematics Subject Classification that counts as “pure” and was established by 1960 &mdash; all {stats['total']} of them, not just the ones with a good story.</p>

    <div class="scoreboard">
      <div class="stat"><div class="n">{stats['total']}</div><div class="label">fields surveyed</div></div>
      <div class="stat"><div class="n">{stats['dismissed_applied']}</div><div class="label">named dismissal, later applied</div></div>
      <div class="stat"><div class="n">{stats['never_dismissed_applied']}</div><div class="label">never dismissed, applied anyway</div></div>
      <div class="stat"><div class="n">{stats['specialized']}</div><div class="label">real application, but specialized</div></div>
      <div class="stat"><div class="n zero">{stats['no_application']}</div><div class="label">no external application documented</div></div>
    </div>

    <p>
      Click a column header to sort. Filter by verdict below. Every row links to that field's own page:
      the exact founding date, the dismissal quote (or its absence, stated plainly), the application (or its
      absence, stated plainly), and a confidence grade. Full citations are on the
      <a href="./sources.html">Sources</a> page.
    </p>

    <div class="filters" id="filters">
      <button data-filter="all" class="active">All ({stats['total']})</button>
      <button data-filter="a">Named dismissal, later applied ({stats['dismissed_applied']})</button>
      <button data-filter="b">Never dismissed, applied anyway ({stats['never_dismissed_applied']})</button>
      <button data-filter="s">Real application, but specialized ({stats['specialized']})</button>
      <button data-filter="d">No external application documented ({stats['no_application']})</button>
      <button data-filter="x">Mixed ({stats['mixed']})</button>
    </div>

    <div class="table-wrap">
      <table class="impl" id="ledger-table">
        <thead>
          <tr>
            <th data-key="msc">MSC</th>
            <th data-key="name">Field</th>
            <th data-key="dismissed">Dismissed?</th>
            <th data-key="applied">Applied?</th>
            <th data-key="gap">Gap (yrs)</th>
            <th data-key="verdict">Verdict</th>
          </tr>
        </thead>
        <tbody>
{rows_html}
        </tbody>
      </table>
    </div>
    <p class="hint muted">&ldquo;Gap&rdquo; is years from founding to first documented real-world application, not from any dismissal &mdash; several fields were never dismissed at all.</p>

    <div class="next-steps">
      <h2>Continue to</h2>
      <ul>
        <li><a href="./map.html">Map</a> &mdash; every field and application above, as a graph, with the surprising cross-field convergences.</li>
        <li><a href="./timeline.html">Timeline</a> &mdash; the same fields laid out by year.</li>
        <li><a href="./survival.html">Survival</a> &mdash; time-to-application as a right-censored survival curve.</li>
        <li><a href="./holdouts.html">The Holdouts</a> &mdash; the four fields where the application search came back thin or empty.</li>
        <li><a href="./sources.html">Sources</a> &mdash; full citations.</li>
      </ul>
    </div>
  </main>

  <footer>
    Corrections and additional fields welcome &mdash; file an issue on
    <a href="https://github.com/microprediction/pure">microprediction/pure</a>.
  </footer>

<script>
const table = document.getElementById('ledger-table');
const tbody = table.querySelector('tbody');
let sortKey = null, sortDir = 1;
document.querySelectorAll('#ledger-table th').forEach((th, i) => {{
  th.addEventListener('click', () => {{
    const key = th.dataset.key;
    sortDir = (sortKey === key) ? -sortDir : 1;
    sortKey = key;
    document.querySelectorAll('#ledger-table th').forEach(h => h.classList.remove('sort-asc','sort-desc'));
    th.classList.add(sortDir === 1 ? 'sort-asc' : 'sort-desc');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    rows.sort((a, b) => {{
      const va = a.children[i].textContent.trim(), vb = b.children[i].textContent.trim();
      const na = parseFloat(va), nb = parseFloat(vb);
      if (!isNaN(na) && !isNaN(nb)) return (na - nb) * sortDir;
      return va.localeCompare(vb) * sortDir;
    }});
    rows.forEach(r => tbody.appendChild(r));
  }});
}});
document.querySelectorAll('#filters button').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('#filters button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const f = btn.dataset.filter;
    tbody.querySelectorAll('tr').forEach(tr => {{
      tr.style.display = (f === 'all' || tr.dataset.verdict === f) ? '' : 'none';
    }});
  }});
}});
</script>
</body>
</html>
"""
    with open(os.path.join(DOCS, "ledger.html"), "w") as fh:
        fh.write(escape_amp_outside_scripts(html))
    return stats


def render_sources():
    sections = []
    for f in sorted(FIELDS, key=lambda f: f["msc"]):
        items = []
        if f.get("dismissed"):
            items.append(f"<li>{md(f['dismissed'].get('source',''))}</li>")
        for a in (f.get("applications") or []):
            if a.get("url"):
                items.append(f"<li>{a['name']} ({a['year']}): <a href=\"{a['url']}\">{a['url']}</a></li>")
        if not items:
            continue
        sections.append(f"""    <h3>{f['name']} (MSC {f['msc']})</h3>
    <ul>
{chr(10).join('      '+i for i in items)}
    </ul>""")
    body = "\n".join(sections)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Pure: Sources</title>
  <meta name="description" content="Full citations for every dismissal quote and every application claim across all 34 surveyed fields.">
  <link rel="stylesheet" href="./style.css" />
</head>
<body>
{NAV.format(root="./")}
  <main class="bib">
    <p class="pagenav"><a href="./index.html">&larr; Home</a></p>
    <h1>Sources</h1>
    <p class="subtitle">Every dismissal and every application, field by field.</p>
    <p>
      Links and citations, in one place, matched to <a href="./ledger.html">each field's own page</a>.
    </p>
{body}
    <div class="next-steps">
      <h2>See something wrong?</h2>
      <p>
        Tighten a citation, correct a date, or supply the missing provenance for a medium-confidence
        quote: open an issue or a PR on <a href="https://github.com/microprediction/pure">microprediction/pure</a>.
      </p>
    </div>
  </main>
  <footer>
    Corrections and additional fields welcome &mdash; file an issue on
    <a href="https://github.com/microprediction/pure">microprediction/pure</a>.
  </footer>
</body>
</html>
"""
    with open(os.path.join(DOCS, "sources.html"), "w") as fh:
        fh.write(escape_amp_outside_scripts(html))


if __name__ == "__main__":
    slugify_check()
    write_fields_data_js()
    write_field_pages()
    stats = render_ledger()
    render_sources()
    print(json.dumps(stats, indent=2))
    print(f"Wrote fields-data.js, {len(FIELDS)} field pages, and ledger.html")
