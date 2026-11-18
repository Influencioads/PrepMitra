

def solve3(rows, rhs):
    """Solve a 3x3 linear system exactly (Fractions) by Cramer's rule."""
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    rows = [[F(x) for x in r] for r in rows]
    d = det(rows)
    out = []
    for i in range(3):
        m = [r[:] for r in rows]
        for j in range(3):
            m[j][i] = F(rhs[j])
        out.append(det(m) / d)
    return out


# =====================================================================================================================
# Physics and Measurement (B2 I3 A2)
# =====================================================================================================================
T = "Physics and Measurement"

add(T, "Units and SI system", "Basic", "direct",
    "The SI unit of solid angle is:",
    place("Steradian", ["Radian", "Degree", "Candela"], "B"),
    "Supplementary units: radian and steradian",
    "In the SI system the plane angle is measured in radian (rad) and the solid angle in steradian (sr). A solid "
    "angle is the ratio of the intercepted area on a sphere to the square of its radius, so like the plane angle it "
    "is dimensionless but has a named unit.",
    ["Plane angle dθ = ds/r → radian", "Solid angle dΩ = dA/r² → steradian"],
    why="The radian and the degree are units of plane angle, not solid angle. The candela is the SI base unit of "
        "luminous intensity.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units (radian and steradian)",
    seconds=20)

assert close(0.05 / 2.50 * 100, 2.0)
add(T, "Errors in measurement", "Basic", "numerical",
    "Repeated measurements of the period of a pendulum give a mean value of 2.50 s and a mean absolute error of "
    "0.05 s. The percentage error in the measured period is:",
    place("2%", ["0.02%", "5%", "0.2%"], "C"),
    "Relative and percentage error",
    "The relative error is the mean absolute error divided by the mean value; multiplying by 100 gives the "
    "percentage error.",
    ["δa = Δa_mean / a_mean = 0.05 / 2.50 = 0.02", "Percentage error = 0.02 × 100 = 2%"],
    why="0.02% forgets to multiply by 100 correctly (it treats 0.02 itself as a percentage); 5% writes the absolute "
        "error 0.05 as 5%; 0.2% misplaces the decimal point.",
    ncert="Class 11 Physics, 'Units and Measurement', errors in measurement (relative and percentage error)",
    seconds=30, recomputed=True)

# centripetal force: F = m^x v^y r^z ; m [M], v [L T^-1], r [L], F [M L T^-2]
x_, y_, z_ = solve3([[1, 0, 0], [0, 1, 1], [0, -1, 0]], [1, 1, -2])
assert (x_, y_, z_) == (1, 2, -1)
add(T, "Dimensional analysis", "Intermediate", "numerical",
    "The force F needed to keep a body moving uniformly in a circle is assumed to depend only on its mass m, its "
    "speed v and the radius r of the circle, as F ∝ mˣ vʸ rᶻ. By the method of dimensions, the values of x, y and z "
    "are respectively:",
    place("1, 2 and −1", ["1, 1 and −1", "1, 2 and 1", "1, −2 and 1"], "D"),
    "Deducing a relation by the method of dimensions",
    "Equate the powers of M, L and T on the two sides. With m = [M], v = [L T⁻¹] and r = [L], the force "
    "[M L T⁻²] requires x = 1, y = 2 and z = −1, i.e. F ∝ mv²/r (the dimensionless constant, here 1, cannot be "
    "found this way).",
    ["[M L T⁻²] = [M]ˣ [L T⁻¹]ʸ [L]ᶻ", "M: x = 1", "T: −y = −2 → y = 2", "L: y + z = 1 → z = −1"],
    why="(1, 1, −1) gives [M T⁻¹], not a force; (1, 2, 1) gives [M L³ T⁻²]; (1, −2, 1) gives [M L⁻¹ T²].",
    ncert="Class 11 Physics, 'Units and Measurement', deducing relations among physical quantities", seconds=60,
    recomputed=True)

ML2 = {"Moment of inertia": dims(1, 2, 0), "Angular momentum": dims(1, 2, -1), "Torque": dims(1, 2, -2),
       "Power": dims(1, 2, -3)}
assert ML2["Angular momentum"] == dmul(dims(1, 0, 0), dims(0, 1, -1), dims(0, 1, 0))     # m v r
assert ML2["Torque"] == dmul(dims(1, 1, -2), dims(0, 1, 0))                               # F r
assert ML2["Power"] == dmul(dims(1, 1, -2), dims(0, 1, -1))                               # F v
add(T, "Dimensional analysis", "Intermediate", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its dimensional formula).",
               ["Moment of inertia", "Angular momentum", "Torque", "Power"],
               ["[M L² T⁻²]", "[M L² T⁻³]", "[M L² T⁰]", "[M L² T⁻¹]"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"),
    "Dimensional formulae of rotational quantities",
    "All four quantities contain M L²; they differ only in the power of time. Moment of inertia is mr² → [M L²]; "
    "angular momentum is mvr → [M L² T⁻¹]; torque is force × distance → [M L² T⁻²]; power is force × velocity → "
    "[M L² T⁻³].",
    ["I = mr² → [M L² T⁰] (III)", "L = mvr → [M L² T⁻¹] (IV)", "τ = rF → [M L² T⁻²] (I)",
     "P = Fv → [M L² T⁻³] (II)"],
    shortcut="Each time derivative adds one T⁻¹: I → L (= Iω) → τ (= dL/dt); power = τω adds one more T⁻¹.",
    why="The other codes swap neighbouring powers of T: angular momentum with torque, moment of inertia with angular "
        "momentum, or torque with power.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional formulae", seconds=60)

add(T, "Least count and significant figures", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When a measured value is written in scientific notation, a × 10ᵇ, the power of ten does not affect the "
           "number of significant figures.",
        s2="According to the rules given in NCERT, a length written as 12300 cm (without a decimal point) has five "
           "significant figures."),
    sp("C"),
    "Rules for counting significant figures",
    "In scientific notation all the significant digits appear in a; the factor 10ᵇ only fixes the order of "
    "magnitude, so Statement I is true. NCERT states that trailing zeros in a number without a decimal point are "
    "not significant: 123 m = 12300 cm = 123000 mm has three significant figures, so Statement II is false.",
    ["Statement I: 10ᵇ is irrelevant to significant figures → true",
     "Statement II: 12300 (no decimal point) → trailing zeros not significant → 3 significant figures → false"],
    why="Statement II would be true only if the number were written 12300. (with a decimal point) or as 1.2300 × 10⁴.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures", seconds=45)

# deep-water waves: v = g^x lam^y rho^z ; g [L T^-2], lam [L], rho [M L^-3], v [L T^-1]
x_, y_, z_ = solve3([[0, 0, 1], [1, 1, -3], [-2, 0, 0]], [0, 1, -1])
assert (x_, y_, z_) == (F(1, 2), F(1, 2), 0)
assert close(4 ** float(y_) * 2 ** float(z_), 2.0)
add(T, "Dimensional analysis", "Advanced", "numerical",
    "The speed v of waves on the surface of deep water is assumed to depend only on the acceleration due to "
    "gravity g, the wavelength λ of the waves and the density ρ of the liquid. Using the method of dimensions, if "
    "the wavelength is made 4 times and the water is replaced by a liquid of twice the density, the wave speed "
    "becomes:",
    place("2 times", ["√2 times", "4 times", "2√2 times"], "D"),
    "Method of dimensions: a variable whose exponent comes out zero",
    "Writing v ∝ gˣ λʸ ρᶻ and equating the powers of M, L and T gives z = 0: density is the only quantity with "
    "mass in it, so it cannot appear. Then x = y = 1/2, so v ∝ √(gλ), independent of the density.",
    ["[L T⁻¹] = [L T⁻²]ˣ [L]ʸ [M L⁻³]ᶻ", "M: z = 0", "T: −2x = −1 → x = 1/2", "L: x + y − 3z = 1 → y = 1/2",
     "v'/v = √4 = 2 (the change of density has no effect)"],
    shortcut="A quantity is the only one containing a base dimension (here ρ with M) → its exponent must be zero.",
    why="√2 times wrongly keeps ρ^(−1/2), giving √4/√2; 4 times forgets the square root; 2√2 times takes "
        "v ∝ √(gλρ).",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional analysis and its applications", seconds=110,
    recomputed=True)

P_ = 2 * (12.5 + 4.2)
dP = 2 * (0.1 + 0.1)
assert close(P_, 33.4) and close(dP, 0.4) and round(dP / P_ * 100, 1) == 1.2
assert round((0.1 / 12.5 + 0.1 / 4.2) * 100, 1) == 3.2
add(T, "Errors in measurement", "Advanced", "numerical",
    "The length and breadth of a rectangular plate are measured as l = (12.5 ± 0.1) cm and b = (4.2 ± 0.1) cm. "
    "The perimeter of the plate with its maximum absolute error, and the corresponding percentage error "
    "(to one decimal place), are:",
    place("(33.4 ± 0.4) cm; 1.2%", ["(33.4 ± 0.2) cm; 0.6%", "(33.4 ± 0.4) cm; 3.2%", "(33.4 ± 0.8) cm; 2.4%"], "B"),
    "Combination of errors in a sum",
    "For a sum the absolute errors add. The perimeter is P = 2(l + b), so ΔP = 2(Δl + Δb). The percentage error is "
    "then ΔP/P × 100; relative errors are added only for products and quotients, not for sums.",
    ["P = 2(12.5 + 4.2) = 33.4 cm", "ΔP = 2(0.1 + 0.1) = 0.4 cm", "Percentage error = 0.4/33.4 × 100 ≈ 1.2%"],
    why="(33.4 ± 0.2) cm forgets the factor 2 in P = 2(l + b); 3.2% adds the relative errors of l and b as if P were "
        "a product; (33.4 ± 0.8) cm counts the error of each of the four sides twice.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors (error of a sum)", seconds=80,
    recomputed=True)
