

# ================================================================ Current Electricity (B5 I7 A5)
CEC = NC + "'Current Electricity', "

# ---- Basic
R_b = F(220 ** 2, 100)
assert R_b == 484 and F(220, 100) == F(22, 10) and 220 * 100 == 22000 and round(100 / 220, 2) == 0.45
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "An electric bulb is rated 100 W, 220 V. Treating its resistance as constant, the resistance of its filament when "
  "it is working at its rated voltage is:",
  *opt("484 Ω", ["2.2 Ω", "0.45 Ω", "22 kΩ"], "C"),
  "Electrical power P = V²/R",
  "At its rated voltage the bulb draws its rated power, so R = V²/P.",
  ["R = V²/P = (220 V)² / 100 W", "R = 48400/100 = 484 Ω"],
  why="2.2 Ω is V/P, which has no physical meaning here. 0.45 is P/V, the current in amperes, not a resistance. "
      "22 kΩ multiplies V by P.",
  ncert=CEC + "electrical energy, power", seconds=30, rc=True)

I_tot = F(6)
I4 = I_tot * 2 / (2 + 4)
assert I4 == 2 and I_tot * 4 / 6 == 4 and I_tot / 2 == 3
q(CE, "Combination of resistors", "Basic", "numerical",
  "A current of 6 A enters a parallel combination of a 2 Ω resistor and a 4 Ω resistor. The current through the "
  "4 Ω resistor is:",
  *opt("2 A", ["4 A", "3 A", "6 A"], "A"),
  "In a parallel combination the potential difference is the same, so the current divides in inverse proportion to "
  "the resistances",
  "The equivalent resistance is 2 × 4/(2 + 4) = 4/3 Ω, so the common potential difference is 6 A × 4/3 Ω = 8 V.",
  ["Common PD = 6 × (4/3) = 8 V", "Current in 4 Ω = 8/4 = 2 A (and 4 A in the 2 Ω resistor)"],
  shortcut="I₄ = I × R₂/(R₂ + R₄) = 6 × 2/6 = 2 A.",
  why="4 A is the current in the 2 Ω resistor (the larger share goes through the smaller resistance). 3 A assumes "
      "an equal split. 6 A treats the resistors as if they were in series.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=30, rc=True)

assert F(2) / F(1, 2) == 4
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "The current through a metal wire is doubled, and at the same time the wire is replaced by another wire of the "
  "same metal (at the same temperature) with half the cross-sectional area. The drift speed of the free electrons "
  "becomes:",
  *opt("4 times the original value", ["2 times the original value", "the same as before", "1/4 of the original value"],
       "D"),
  "I = n e A v_d, so v_d = I/(n e A)",
  "The number density n of free electrons is a property of the metal and does not change. The drift speed is "
  "proportional to I and inversely proportional to A.",
  ["v_d ∝ I/A", "New v_d ∝ (2I)/(A/2) = 4 × (I/A)"],
  why="'2 times' accounts for the doubled current but not the smaller area. 'The same' assumes the two changes "
      "cancel. '1/4' inverts the dependence on both I and A.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=30, rc=True)

q(CE, "Drift velocity and Ohm's law", "Basic", "assertion_reason",
  ar("Although the drift speed of the free electrons in a copper wire is only of the order of 1 mm/s, a wire of "
     "cross-sectional area 1 mm² can carry a current of several amperes.",
     "The number density of free electrons in a metal such as copper is very large, of the order of 10²⁸ to 10²⁹ "
     "per cubic metre."),
  AR, ar_key(True, True, True),
  "Current in terms of drift speed: I = n e A v_d",
  "The current through a cross-section is the charge carried across it per second, n e A v_d. With n ≈ 8.5 × 10²⁸ "
  "m⁻³, e = 1.6 × 10⁻¹⁹ C, A = 10⁻⁶ m² and v_d = 10⁻³ m/s, I ≈ 14 A. A tiny drift speed still gives a sizeable "
  "current only because n is enormous, so R explains A.",
  ["A: true", "R: true", "I = n e A v_d: small v_d is compensated by very large n → R explains A"],
  why="R is not a separate property: the large n is exactly what makes the current large in spite of the small "
      "drift speed.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=40)

q(CE, "Resistivity and temperature", "Basic", "statement_pair",
  sp("The resistivity of a metal wire at a given temperature increases if the wire is made longer.",
     "The SI unit of conductance, the reciprocal of resistance, is the siemens (S), with 1 S = 1 Ω⁻¹."),
  SP, sp_key(False, True),
  "Resistance depends on dimensions; resistivity is a property of the material",
  "R = ρl/A depends on the length and area, but ρ depends only on the material and its temperature, so Statement I "
  "is false. Conductance G = 1/R is measured in siemens, 1 S = 1 Ω⁻¹, so Statement II is true.",
  ["I: a longer wire has more resistance, not more resistivity → false", "II: G = 1/R, unit S = Ω⁻¹ → true"],
  why="Statement I confuses resistance with resistivity.",
  ncert=CEC + "Ohm's law; resistivity", seconds=35)

# ---- Intermediate
assert F(3, 1) / F(1, 3) == 9
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "Three identical bulbs, connected in series across a supply of constant voltage, together consume a power P. "
  "Treating the resistance of each bulb as constant, the total power they consume when they are connected in "
  "parallel across the same supply is:",
  *opt("9P", ["3P", "P/9", "P"], "B"),
  "For a fixed supply voltage, total power = V²/R_eq",
  "In series the equivalent resistance is 3R; in parallel it is R/3, which is 9 times smaller. With V fixed, power is "
  "inversely proportional to the equivalent resistance.",
  ["Series: P = V²/(3R)", "Parallel: P' = V²/(R/3) = 3V²/R", "P'/P = 9 → P' = 9P"],
  why="3P compares the parallel combination with a single bulb's resistance R. P/9 inverts the ratio. P assumes the "
      "arrangement does not matter.",
  ncert=CEC + "electrical energy, power", seconds=45, rc=True)

R_side = F(18, 3)
R_path = R_side + R_side / 2
assert R_path == 9 and R_path / 2 == F(9, 2) and R_side * 2 * R_side / (3 * R_side) == 4
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "A uniform wire of resistance 18 Ω is bent into the shape of an equilateral triangle ABC, its ends being joined. "
  "The resistance between the corner A and the midpoint M of the opposite side BC is:",
  *opt("4.5 Ω", ["9 Ω", "4 Ω", "6 Ω"], "D"),
  "Resistance proportional to length; parallel combination",
  "Each side is 6 Ω, and half a side is 3 Ω. From A to M there are two identical paths: A → B → M and A → C → M, each "
  "of 6 + 3 = 9 Ω. These two paths are in parallel.",
  ["Each side 6 Ω; BM = MC = 3 Ω", "Each path A→B→M or A→C→M = 9 Ω", "Two 9 Ω paths in parallel = 4.5 Ω"],
  why="9 Ω takes only one of the two paths. 4 Ω is the resistance between two corners (6 Ω in parallel with 12 Ω). "
      "6 Ω is just the resistance of one side.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=60, rc=True)

lx, ly = F(1), F(2)
assert (lx ** 2) / (ly ** 2) == F(1, 4) and lx / ly == F(1, 2)
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "Two wires X and Y are made of the same metal and have the same mass. The length of Y is twice that of X. The two "
  "wires are connected in series across a battery. The ratio of the heat produced per second in X to that in Y is:",
  *opt("1 : 4", ["1 : 2", "4 : 1", "1 : 8"], "B"),
  "R = ρl/A, with equal mass (equal volume) fixing A = volume/l; in series, heat ∝ R",
  "Same metal and same mass means the same volume V. The cross-sectional area is A = V/l, so R = ρl/A = ρl²/V, "
  "i.e. R ∝ l². In series the same current flows through both, so the heat per second I²R is proportional to R.",
  ["R ∝ l² at fixed volume", "R_X : R_Y = 1² : 2² = 1 : 4", "Series: heat ∝ R → 1 : 4"],
  why="1 : 2 uses R ∝ l and forgets that the longer wire is also thinner. 4 : 1 is the ratio for a parallel "
      "connection, where heat ∝ 1/R. 1 : 8 cubes the length ratio.",
  ncert=CEC + "resistivity of various materials; electrical energy, power", seconds=60, rc=True)

eps, r_ = 6, 1
assert eps - 0 == 6 and eps - eps / (r_ + 2) * r_ == 4 and eps + 2 * r_ == 8
q(CE, "Cells, emf and internal resistance", "Intermediate", "match_list",
  ml("A cell has emf 6 V and internal resistance 1 Ω. Match each situation in List-I with the potential difference "
     "between the terminals of the cell in List-II.",
     ["No current is drawn from the cell (open circuit)",
      "The terminals are joined directly by a thick wire of negligible resistance",
      "A 2 Ω resistor is connected across the terminals",
      "The cell is being charged by an external source, the charging current being 2 A"],
     ["8 V", "0 V", "6 V", "4 V"]),
  *mlo("A-III, B-II, C-IV, D-I", ["A-III, B-IV, C-II, D-I", "A-I, B-II, C-IV, D-III", "A-III, B-II, C-I, D-IV"], "B"),
  "Terminal potential difference V = ε − Ir while discharging and V = ε + Ir while charging",
  "Open circuit: no current, so V = ε = 6 V. Short circuit: the terminals are at the same potential, V = 0 (the "
  "current ε/r = 6 A makes Ir = ε). With 2 Ω: I = 6/3 = 2 A and V = 6 − 2 × 1 = 4 V. While charging, the current "
  "enters the positive terminal and V = ε + Ir = 6 + 2 = 8 V.",
  ["A → 6 V (III)", "B → 0 V (II)", "C → 4 V (IV)", "D → 8 V (I)"],
  why="The other codes either give the charging case ε − Ir (4 V), or give the short-circuited cell its emf, "
      "although its terminals are joined by a wire of negligible resistance.",
  ncert=CEC + "cells, emf, internal resistance", seconds=60)

I_ = F(1)
P4, P6, P12 = 4 * I_ ** 2, 6 * (I_ * 12 / 18) ** 2, 12 * (I_ * 6 / 18) ** 2
assert P4 == 4 and P6 == F(8, 3) and P12 == F(4, 3) and max(P4, P6, P12) == P4
q(CE, "Combination of resistors", "Intermediate", "direct",
  "A 4 Ω resistor is connected in series with a parallel combination of a 6 Ω resistor and a 12 Ω resistor, and the "
  "arrangement is connected across a battery. In which resistor is heat produced at the greatest rate?",
  *opt("The 4 Ω resistor", ["The 6 Ω resistor", "The 12 Ω resistor",
                             "The 6 Ω and 12 Ω resistors equally, since they have the same potential difference"], "A"),
  "Heat produced per second = I²R; current division in a parallel combination",
  "Let the current through the 4 Ω resistor be I. It divides in inverse ratio of the resistances: 2I/3 through "
  "6 Ω and I/3 through 12 Ω. The heating rates are 4I², 6(2I/3)² = 8I²/3 and 12(I/3)² = 4I²/3.",
  ["4 Ω: 4I²", "6 Ω: 6 × 4I²/9 = 2.67 I²", "12 Ω: 12 × I²/9 = 1.33 I²", "Largest: the 4 Ω resistor"],
  why="The 6 Ω resistor gets more heat than the 12 Ω one (same V, so heat ∝ 1/R), but still less than the 4 Ω "
      "resistor, which carries the full current. The 12 Ω resistor gets the least. Equal potential difference does "
      "not mean equal heat when the resistances differ.",
  ncert=CEC + "electrical energy, power", seconds=60, rc=True)

q(CE, "Cells, emf and internal resistance", "Intermediate", "assertion_reason",
  ar("A voltmeter of very high resistance connected directly across the terminals of a cell reads very nearly the "
     "emf of the cell.",
     "Such a voltmeter draws a negligible current, so the potential drop across the internal resistance of the cell "
     "is negligible."),
  AR, ar_key(True, True, True),
  "Terminal voltage V = ε − Ir",
  "The terminal voltage differs from the emf by the drop Ir across the internal resistance. A voltmeter of very high "
  "resistance R_V draws a current ε/(R_V + r), which is tiny, so Ir is tiny and the reading is almost ε. R gives the "
  "reason for A.",
  ["V = ε − Ir", "I ≈ 0 for a very high resistance voltmeter → V ≈ ε", "R explains A"],
  why="R is the direct reason for A; it is not an unrelated statement.",
  ncert=CEC + "cells, emf, internal resistance", seconds=40)

R0, R100, Rt = F(50), F(70), F(61)
alpha = (R100 - R0) / (R0 * 100)
t_ = (Rt - R0) / (R0 * alpha)
assert alpha == F(4, 1000) and t_ == 55
assert round(float(Rt / R100 * 100)) == 87 and Rt / R0 * 100 == 122
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "The resistance of a metal wire is 50 Ω at 0 °C and 70 Ω at 100 °C. Assuming that the resistance varies linearly "
  "with temperature, the temperature at which its resistance is 61 Ω is:",
  *opt("55 °C", ["87 °C", "122 °C", "45 °C"], "D"),
  "R_t = R₀(1 + αt) for a linear variation",
  "The resistance rises by 20 Ω over 100 °C, i.e. 0.2 Ω per °C. A rise of 11 Ω above the 0 °C value therefore needs "
  "55 °C.",
  ["α = (70 − 50)/(50 × 100) = 4 × 10⁻³ °C⁻¹", "61 = 50(1 + 4 × 10⁻³ t)", "t = 11/(50 × 4 × 10⁻³) = 55 °C"],
  shortcut="t = 100 × (61 − 50)/(70 − 50) = 55 °C.",
  why="87 °C takes R/R₁₀₀ × 100. 122 °C takes R/R₀ × 100. 45 °C measures the 11 Ω step down from 100 °C instead of "
      "up from 0 °C.",
  ncert=CEC + "temperature dependence of resistivity", seconds=50, rc=True)

# ---- Advanced
wheel = [(0, i, 5) for i in range(1, 7)] + [(i, i % 6 + 1, 5) for i in range(1, 7)]
R_opp = equivalent_resistance(7, wheel, 1, 4)
assert R_opp == 4
assert F(15, 2) == F(15 * 15, 30) and F(10 * F(15, 2), 10 + F(15, 2)) == F(30, 7)
q(CE, "Kirchhoff's laws", "Advanced", "numerical",
  "Twelve identical resistors, each of 5 Ω, form a wheel: six of them make the sides of a regular hexagon (the rim) "
  "and the other six join each corner of the hexagon to its centre O (the spokes). The equivalent resistance "
  "between two diametrically opposite corners of the hexagon is:",
  *opt("4 Ω", ["7.5 Ω", "30/7 Ω ≈ 4.3 Ω", "10 Ω"], "B"),
  "Symmetry of a network and Kirchhoff's junction rule",
  "Hold corner 1 at potential V and the opposite corner 4 at 0. By symmetry the centre O is at V/2, corners 2 and 6 "
  "(next to 1) are at a common potential x, and corners 3 and 5 are at V − x. Apply the junction rule at corner 2, "
  "which is joined to 1, to 3 and to O.",
  ["At corner 2: (V − x) + ((V − x) − x) + (V/2 − x) = 0 → x = 5V/8",
   "Current leaving corner 1 (each resistor 5 Ω): [2(V − 5V/8) + (V − V/2)]/5 = (5V/4)/5 = V/4",
   "R_eq = V ÷ (V/4) = 4 Ω"],
  why="7.5 Ω uses only the two rim paths (15 Ω each, in parallel). 30/7 Ω adds the 10 Ω spoke path through O in "
      "parallel with the rim but ignores the spokes to the other corners, which carry current. 10 Ω uses the spoke "
      "path alone.",
  seconds=150, rc=True)

X_ = F(10) * 50 / 50
Y_ = F(10) * 60 / 40
Pxy = X_ * Y_ / (X_ + Y_)
l_ = 100 * Pxy / (Pxy + 10)
assert X_ == 10 and Y_ == 15 and Pxy == 6 and l_ == F(75, 2)
assert round(float(100 * 25 / 35), 1) == 71.4
q(CE, "Wheatstone and metre bridge", "Advanced", "numerical",
  "In a metre bridge with a 10 Ω standard resistor in the right gap, the null point is 50.0 cm from the left end "
  "when a resistor X is in the left gap, and 60.0 cm from the left end when X is replaced by a resistor Y. When X and "
  "Y are connected in parallel and placed together in the left gap (10 Ω still in the right gap), the null point "
  "will be at a distance from the left end of:",
  *opt("37.5 cm", ["71.4 cm", "55.0 cm", "62.5 cm"], "C"),
  "Metre bridge balance: X/R = l/(100 − l)",
  "The two separate balances give X and Y; their parallel combination is then balanced against the same 10 Ω.",
  ["X = 10 × 50/50 = 10 Ω", "Y = 10 × 60/40 = 15 Ω", "X ∥ Y = 10 × 15/25 = 6 Ω",
   "6/10 = l/(100 − l) → l = 37.5 cm"],
  why="71.4 cm uses X and Y in series (25 Ω). 55.0 cm simply averages the two balance lengths. 62.5 cm is the "
      "correct balance length measured from the wrong (right-hand) end.",
  ncert=CEC + "Wheatstone bridge", seconds=110, rc=True)

R_wire = F(9) * 3 ** 2
piece = R_wire / 3
assert R_wire == 81 and piece == 27 and piece / 3 == 9
assert F(9, 3) / 3 == 1 and (F(9) * 3 / 3) / 3 == 3
q(CE, "Resistivity and temperature", "Advanced", "numerical",
  "A uniform wire of resistance 9 Ω is stretched uniformly to three times its original length, its volume and "
  "resistivity remaining unchanged. It is then cut into three pieces of equal length, and the three pieces are "
  "connected in parallel. The resistance of the combination is:",
  *opt("9 Ω", ["1 Ω", "27 Ω", "3 Ω"], "A"),
  "R = ρl/A with volume constant gives R ∝ l²; identical resistors in parallel",
  "Stretching to three times the length at constant volume reduces the area to one third, so the resistance becomes "
  "3² = 9 times larger. Each third of the stretched wire then has one third of that resistance, and three equal "
  "resistors in parallel give one third of one piece.",
  ["Stretched: R = 9 × 3² = 81 Ω", "Each piece: 81/3 = 27 Ω", "Three 27 Ω pieces in parallel: 27/3 = 9 Ω"],
  why="1 Ω ignores the stretching (pieces of 3 Ω in parallel). 27 Ω is the resistance of one piece. 3 Ω uses R ∝ l "
      "for the stretching, forgetting that the area also decreases.",
  ncert=CEC + "Ohm's law; resistivity", seconds=80, rc=True)

truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(CE, "Wheatstone and metre bridge", "Advanced", "multi_statement",
  ms("In a Wheatstone bridge, resistors P and Q form one branch and R and S the other; both branches are connected "
     "across a cell of emf ε and internal resistance r, and a galvanometer joins the P–Q junction to the R–S "
     "junction. The bridge is balanced. Which of the following statements are correct?",
     ["No current flows through the galvanometer.",
      "The balance condition P/Q = R/S does not depend on the emf of the cell.",
      "The balance condition does not depend on the resistance of the galvanometer.",
      "The balance condition depends on the internal resistance of the cell.",
      "If the galvanometer is replaced by a resistor of any value, the currents through P, Q, R and S do not "
      "change."]),
  *mso(truth, "abce", ["abc", "abde", "bce"], "D"),
  "Balanced Wheatstone bridge: the two junctions are at the same potential",
  "At balance the P–Q and R–S junctions are at the same potential, so no current flows through anything connected "
  "between them, whatever its resistance. Hence (a) and (e). The condition P/Q = R/S comes from the ratios of the "
  "resistances alone; ε, r and the galvanometer resistance change only the size of the currents, not whether the "
  "bridge balances. So (b) and (c) are true and (d) is false.",
  ["(a) true", "(b) true", "(c) true", "(d) false: r affects the currents, not the balance", "(e) true: no PD across "
   "the junctions, so no current in any element joining them"],
  why="Options with (d) wrongly make the balance depend on the cell; the option without (e) misses that a balanced "
      "bridge passes no current between the junctions whatever element joins them; the option without (a) misses "
      "the defining property of balance.",
  ncert=CEC + "Wheatstone bridge", seconds=80)

n_c, e_c, r_c = 4, F(3, 2), F(1, 4)
I_ring = n_c * e_c / (n_c * r_c)
assert I_ring == 6 and e_c - I_ring * r_c == 0 and n_c * e_c / r_c == 24
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "Four identical cells, each of emf 1.5 V and internal resistance 0.25 Ω, are connected in series to form a closed "
  "ring (the positive terminal of each joined to the negative terminal of the next), with nothing else in the "
  "circuit. The current in the ring and the reading of an ideal voltmeter connected across the terminals of any "
  "one cell are, respectively:",
  *opt("6 A and 0 V", ["6 A and 1.5 V", "24 A and 0 V", "zero and 1.5 V"], "C"),
  "Current in a closed loop of cells; terminal voltage V = ε − Ir",
  "Round the ring the emfs add to 6 V and the internal resistances to 1 Ω, so the current is 6 A. For each cell the "
  "drop across its internal resistance is Ir = 6 × 0.25 = 1.5 V, exactly its emf, so its terminal voltage is zero.",
  ["Total emf = 4 × 1.5 = 6 V; total resistance = 4 × 0.25 = 1 Ω", "I = 6/1 = 6 A",
   "Terminal voltage of each cell = 1.5 − 6 × 0.25 = 0 V"],
  shortcut="By symmetry all four terminals of the ring must be at the same potential, so every voltmeter reads zero.",
  why="1.5 V is the emf, which a voltmeter would read only if no current flowed. 24 A divides the total emf by the "
      "internal resistance of one cell. 'Zero' current wrongly assumes the cells cancel; they all push current the "
      "same way round the ring.",
  ncert=CEC + "cells in series and in parallel", seconds=80, rc=True)
