

# ================================================================ Electronic Devices (B4 I5 A4)
SCC = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "


def truth_table(fn):
    return [fn(a, b) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))]


NAND = lambda a, b: 1 - (a & b)
NOR = lambda a, b: 1 - (a | b)

# ---- Basic
q(ED, "p-n junction diode and rectifier", "Basic", "numerical",
  "A half-wave rectifier (a single junction diode in series with a load resistor) is fed from a 60 Hz AC supply. The "
  "number of current pulses through the load per second, i.e. the frequency of the rectified output, is:",
  *opt("60 Hz", ["120 Hz", "30 Hz", "zero, since the output is DC"], "B"),
  "Half-wave rectification: the diode conducts in only one half of each input cycle",
  "In each cycle of the input, the diode conducts during one half-cycle and blocks during the other, so the load "
  "receives one pulse per input cycle. The pulsating output therefore repeats 60 times a second.",
  ["One conducting half-cycle per input cycle", "Pulses per second = input frequency = 60 Hz"],
  why="120 Hz is the ripple frequency of a full-wave rectifier, which conducts in both halves. 30 Hz halves the "
      "frequency for no reason. The output is unidirectional but pulsating, not steady DC.",
  ncert=SCC + "application of junction diode as a rectifier", seconds=25, rc=True)

frac = 1.5e16 / 5e28
close(frac, 3e-13)
q(ED, "Semiconductors", "Basic", "numerical",
  "Pure silicon contains about 5 × 10²⁸ atoms per m³, and at room temperature its intrinsic carrier concentration is "
  "1.5 × 10¹⁶ m⁻³. The fraction of the silicon atoms that have released an electron into the conduction band is "
  "about:",
  *opt("3 × 10⁻¹³", ["3.3 × 10¹²", "1.5 × 10¹⁶", "6 × 10⁻¹³"], "D"),
  "Intrinsic semiconductor: n_e = n_h = n_i; each free electron comes from one broken covalent bond",
  "Each thermally generated free electron leaves one hole, so the number of atoms that have lost an electron per m³ "
  "is n_e = n_i. Dividing by the number of atoms per m³ gives the fraction, which is extremely small; this is why "
  "pure silicon conducts so poorly.",
  ["Fraction = n_i/N = 1.5 × 10¹⁶/5 × 10²⁸", "= 3 × 10⁻¹³"],
  why="3.3 × 10¹² is N/n_i, the inverse. 1.5 × 10¹⁶ is the carrier concentration itself, not a fraction. 6 × 10⁻¹³ "
      "counts the electrons and the holes as if each came from a different atom.",
  ncert=SCC + "intrinsic semiconductor", seconds=35, rc=True)

q(ED, "Semiconductors", "Basic", "direct",
  "An electric field is applied across a sample of pure silicon. The holes in its valence band move:",
  *opt("in the direction of the electric field, as positive charges would",
       ["opposite to the electric field, in the same direction as the free electrons",
        "at random, with no net drift, because holes are not real particles",
        "only if the sample has been doped with a trivalent impurity"], "A"),
  "Hole motion: a vacancy filled successively by neighbouring bound electrons behaves as a positive charge",
  "Bound electrons near a hole jump into it against the field direction, leaving a vacancy behind them. The vacancy "
  "therefore moves along the field, exactly as a positive charge would, and the hole current adds to the electron "
  "current.",
  ["Bound electrons move opposite to E (negative charge)", "The vacancy moves the other way → along E",
   "Holes act as positive carriers"],
  why="Free electrons move opposite to the field; holes move the other way. Although a hole is a vacancy, its motion "
      "is a real drift of charge. Pure silicon also has holes (thermally generated), not only doped silicon.",
  ncert=SCC + "intrinsic semiconductor", seconds=35)

q(ED, "Zener diode", "Basic", "statement_pair",
  sp("A Zener diode is made by heavily doping both its p- and n-sides, so that its depletion region is very thin.",
     "Because its depletion region is so thin, the electric field across the junction is very high (of the order of "
     "5 × 10⁶ V/m) even for a small reverse bias of about 5 V."),
  SP, sp_key(True, True),
  "Construction of the Zener diode",
  "Both statements are as described in NCERT. Heavy doping makes the depletion layer very thin (less than about "
  "10⁻⁶ m), so even a few volts of reverse bias produce an extremely high field, which can pull valence electrons "
  "out of their bonds and cause breakdown at a well-defined voltage.",
  ["I: heavy doping → thin depletion region → true", "II: thin region → very high field at small reverse bias → true"],
  why="Both statements are correct; neither has been altered.",
  ncert=SCC + "Zener diode", seconds=35)

# ---- Intermediate
q(ED, "p-n junction diode and rectifier", "Intermediate", "assertion_reason",
  ar("When a p-n junction is forward biased, a large current flows, carried mainly by the diffusion of majority "
     "carriers across the junction.",
     "Forward bias lowers the potential barrier at the junction, so that many more majority carriers have enough "
     "energy to diffuse across it."),
  AR, ar_key(True, True, True),
  "p-n junction under forward bias",
  "With forward bias the applied voltage opposes the built-in barrier, so the effective barrier height falls to "
  "V₀ − V. Majority carriers (holes from p, electrons from n) can then diffuse across in large numbers and become "
  "minority carriers on the other side, giving a large current that grows rapidly with V. R explains A.",
  ["A: forward current large, mainly diffusion of majority carriers → true",
   "R: barrier lowered → more carriers cross → true, and the cause of A"],
  why="R is the reason for the large diffusion current; it is not an unrelated property.",
  ncert=SCC + "semiconductor diode: p-n junction diode under forward bias", seconds=40)

q(ED, "p-n junction diode and rectifier", "Intermediate", "match_list",
  ml("Match each condition of a p-n junction (List-I) with its description (List-II).",
     ["No bias, in equilibrium", "Forward bias", "Reverse bias, below breakdown",
      "Reverse bias, at the breakdown voltage of a Zener diode"],
     ["No net current: the diffusion current is balanced by an equal and opposite drift current",
      "Barrier lowered and depletion region narrowed; a large current due mainly to majority carriers",
      "Barrier raised and depletion region widened; a small current due to minority carriers",
      "The current rises sharply while the voltage across the diode stays almost constant"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-II, B-I, C-III, D-IV", "A-I, B-III, C-II, D-IV", "A-I, B-II, C-IV, D-III"], "C"),
  "p-n junction: formation, forward bias, reverse bias and breakdown",
  "Without bias the junction settles into equilibrium in which diffusion and drift currents cancel. Forward bias "
  "reduces the barrier and the depletion width, giving a large majority-carrier current. Reverse bias raises the "
  "barrier and widens the depletion region; only minority carriers drift across, giving a small current. At the "
  "Zener breakdown voltage the reverse current increases sharply at an almost constant voltage.",
  ["A → I", "B → II", "C → III", "D → IV"],
  why="The other codes exchange the forward and reverse descriptions or give the breakdown behaviour to ordinary "
      "reverse bias.",
  ncert=SCC + "p-n junction formation; semiconductor diode; Zener diode", seconds=60)

truth = {"a": True, "b": True, "c": False, "d": True, "e": True}
q(ED, "Semiconductors", "Intermediate", "multi_statement",
  ms("Which of the following statements about doping and extrinsic semiconductors are correct?",
     ["An n-type semiconductor is electrically neutral as a whole.",
      "The dopant atoms should be of nearly the same size as the atoms of the pure semiconductor, so that they do not "
      "distort its crystal lattice.",
      "Pentavalent dopant atoms such as arsenic and phosphorus are called acceptors.",
      "In a p-type semiconductor, the number density of holes is much greater than that of free electrons.",
      "Trivalent dopants such as indium, boron and aluminium make silicon a p-type semiconductor."]),
  *mso(truth, "abde", ["abcd", "bde", "acde"], "B"),
  "Extrinsic semiconductors: donors (pentavalent) and acceptors (trivalent)",
  "Every free electron in n-type material is balanced by a positive donor ion, so the crystal stays neutral (a). "
  "NCERT notes that the dopant must not distort the lattice, so its atoms should be of nearly the same size (b). "
  "Pentavalent atoms donate an electron and are called donors, not acceptors (c false). In p-type material the "
  "acceptors create holes, so n_h ≫ n_e (d). In, B and Al are trivalent acceptors (e).",
  ["(a) true", "(b) true", "(c) false: pentavalent atoms are donors", "(d) true", "(e) true"],
  why="Options with (c) swap the names donor and acceptor; the options leaving out (a) or (e) miss correct "
      "statements.",
  ncert=SCC + "extrinsic semiconductor", seconds=60)

Y_i4 = truth_table(lambda a, b: NAND(a, b) | a)
assert Y_i4 == [1, 1, 1, 1]
q(ED, "Logic gates", "Intermediate", "direct",
  "Inputs A and B are fed to a NAND gate. The output of the NAND gate and the input A are then fed to an OR gate, "
  "whose output is Y. For the inputs (A, B) = (0, 0), (0, 1), (1, 0) and (1, 1), in that order, the outputs Y are:",
  *opt("1, 1, 1, 1", ["1, 1, 1, 0", "0, 1, 1, 1", "1, 0, 1, 1"], "D"),
  "Truth tables of NAND and OR gates",
  "The NAND output is 0 only for A = B = 1. Whenever the NAND output is 0, A is 1, so the OR gate still gives 1. In "
  "every other case the NAND output is 1 and the OR output is 1.",
  ["NAND: 1, 1, 1, 0", "A: 0, 0, 1, 1", "Y = NAND OR A: 1, 1, 1, 1"],
  shortcut="Y = (A·B)' + A = A' + B' + A = 1 always.",
  why="1, 1, 1, 0 is the NAND output alone. 0, 1, 1, 1 is A OR B. 1, 0, 1, 1 is A + B′, which would need "
      "the inverse of B, not the NAND output, at the OR gate.",
  ncert=SCC + "logic gates", seconds=50, rc=True)

I_z = F(20 - 5 - 7, 400)
assert I_z == F(20, 1000) and F(20 - 7, 400) == F(325, 10000) and F(20, 400) == F(50, 1000) and F(12, 400) == F(3, 100)
q(ED, "Zener diode", "Intermediate", "numerical",
  "Two Zener diodes, of breakdown voltages 5.0 V and 7.0 V, are connected in series with each other and with a "
  "400 Ω resistor across a 20 V DC supply. Both Zener diodes are reverse biased and operating in their breakdown "
  "regions. The current in the circuit is:",
  *opt("20 mA", ["32.5 mA", "50 mA", "30 mA"], "B"),
  "A Zener diode in breakdown keeps an (almost) constant voltage across itself",
  "With both Zeners in breakdown, the voltage across them together is 5.0 + 7.0 = 12 V. The rest of the supply "
  "voltage appears across the resistor, which fixes the current.",
  ["Voltage across the Zeners = 12 V", "Voltage across 400 Ω = 20 − 12 = 8 V", "I = 8/400 = 0.020 A = 20 mA"],
  why="32.5 mA subtracts only one Zener voltage. 50 mA ignores both Zener voltages. 30 mA divides the Zener voltage "
      "(12 V), instead of the resistor's voltage, by 400 Ω.",
  ncert=SCC + "Zener diode as a voltage regulator", seconds=50, rc=True)

# ---- Advanced
v_open = solve_network(3, [(0, 1, 1000), (1, 2, 2000)], {0: 6, 2: 0})
assert v_open[1] == 4 and v_open[1] > 3                        # diode would be forward biased
VM = F(3)
I_R1, I_R2 = (6 - VM) / 1000, VM / 2000
I_D = I_R1 - I_R2
assert I_R1 == F(3, 1000) and I_R2 == F(15, 10000) and I_D == F(15, 10000)
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "An ideal 6.0 V battery (negative terminal at the earth point G) is connected through a 1.0 kΩ resistor to a point "
  "M. From M a 2.0 kΩ resistor goes to G. An ideal diode has its anode at M and its cathode at the positive terminal "
  "of an ideal 3.0 V battery whose negative terminal is at G. The current through the diode is:",
  *opt("1.5 mA", ["zero", "2.0 mA", "3.0 mA"], "D"),
  "Ideal diode: test whether it is forward biased, then treat it as a short (forward) or an open circuit (reverse)",
  "Without the diode branch, M would be at 6 × 2/3 = 4.0 V, higher than the 3.0 V at the cathode, so the diode is "
  "forward biased and conducts. An ideal conducting diode has no voltage across it, so M is held at 3.0 V.",
  ["Test: V_M (diode removed) = 4.0 V > 3.0 V → diode conducts", "V_M = 3.0 V",
   "Current in 1.0 kΩ = (6 − 3)/1.0 kΩ = 3.0 mA; in 2.0 kΩ = 3/2.0 kΩ = 1.5 mA",
   "Diode current = 3.0 − 1.5 = 1.5 mA"],
  why="Zero assumes the diode is reverse biased; the test shows it is not. 2.0 mA is the current with the diode "
      "branch removed. 3.0 mA is the current in the 1.0 kΩ resistor, part of which goes through the 2.0 kΩ "
      "resistor.",
  ncert=SCC + "semiconductor diode", seconds=120, rc=True)

A_seq, B_seq = [1, 1, 0, 0, 1], [0, 1, 1, 0, 1]
seq = lambda fn: [fn(a, b) for a, b in zip(A_seq, B_seq)]
assert seq(lambda a, b: a | b) == [1, 1, 1, 0, 1] and seq(lambda a, b: a & b) == [0, 1, 0, 0, 1]
assert seq(NAND) == [1, 0, 1, 1, 0] and seq(NOR) == [0, 0, 0, 1, 0]
q(ED, "Logic gates", "Advanced", "match_list",
  ml("The two inputs of a gate take the following values in five successive time intervals: A = 1, 1, 0, 0, 1 and "
     "B = 0, 1, 1, 0, 1. Match each two-input gate in List-I with its output in these five intervals (List-II).",
     ["OR", "AND", "NAND", "NOR"],
     ["0, 1, 0, 0, 1", "1, 0, 1, 1, 0", "1, 1, 1, 0, 1", "0, 0, 0, 1, 0"]),
  *mlo("A-III, B-I, C-II, D-IV", ["A-I, B-III, C-IV, D-II", "A-III, B-I, C-IV, D-II", "A-II, B-I, C-III, D-IV"], "C"),
  "Truth tables of OR, AND, NAND and NOR gates",
  "Take the input pairs in turn: (1, 0), (1, 1), (0, 1), (0, 0), (1, 1). OR gives 1 unless both inputs are 0; AND "
  "gives 1 only when both are 1; NAND and NOR are the inverses of AND and OR respectively.",
  ["OR: 1, 1, 1, 0, 1 → III", "AND: 0, 1, 0, 0, 1 → I", "NAND (NOT AND): 1, 0, 1, 1, 0 → II",
   "NOR (NOT OR): 0, 0, 0, 1, 0 → IV"],
  why="The other codes swap OR with AND, or NAND with NOR, i.e. invert the wrong basic gate.",
  ncert=SCC + "logic gates", seconds=70, rc=True)

X = truth_table(NOR)
Y = [x & b for x, (a, b) in zip(X, ((0, 0), (0, 1), (1, 0), (1, 1)))]
Y_or = [x | b for x, (a, b) in zip(X, ((0, 0), (0, 1), (1, 0), (1, 1)))]
Y_e = [(a | b) & b for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))]
assert X == [1, 0, 0, 0] and Y == [0, 0, 0, 0] and Y_or == [1, 1, 0, 1] and Y_e == [0, 1, 0, 1]
truth = {"a": True, "b": True, "c": False, "d": False, "e": True}
q(ED, "Logic gates", "Advanced", "multi_statement",
  ms("Inputs A and B are fed to a NOR gate, whose output is X. X and the input B are then fed to an AND gate, whose "
     "output is Y. Which of the following statements are correct?",
     ["X = 1 only when A = 0 and B = 0.",
      "Y = 0 for every combination of the inputs.",
      "Y = 1 when A = 0 and B = 1.",
      "If the AND gate is replaced by an OR gate, the new output is 1 for every combination of the inputs.",
      "If the NOR gate is replaced by an OR gate (the AND gate kept), the new output Y is always equal to B."]),
  *mso(truth, "abe", ["abd", "ace", "be"], "A"),
  "Truth tables of NOR, AND and OR; Boolean simplification",
  "X = (A + B)' is 1 only for A = B = 0 (a). Then Y = X·B: when X = 1, B = 0, and when B = 1, X = 0, so Y is always 0 "
  "(b true, c false). With an OR gate instead, X + B gives 1, 1, 0, 1 for the four input pairs; it is 0 for A = 1, "
  "B = 0, so (d) is false. With an OR gate in place of the NOR, Y = (A + B)·B = B (e).",
  ["X: 1, 0, 0, 0 → (a) true", "Y = X·B: 0, 0, 0, 0 → (b) true, (c) false",
   "X + B: 1, 1, 0, 1 → (d) false", "(A + B)·B = B → (e) true"],
  why="Options with (c) or (d) contradict the truth tables; the option without (a) misses the defining property of "
      "the NOR gate.",
  ncert=SCC + "logic gates", seconds=100, rc=True)

ni_ratio = 2
assert ni_ratio ** 2 == 4
q(ED, "Semiconductors", "Advanced", "numerical",
  "A silicon sample is doped with donor atoms, all of which are ionised, the donor concentration being far larger "
  "than the intrinsic carrier concentration n_i. When the temperature of the sample is raised, n_i doubles, while "
  "the electron concentration remains practically equal to the donor concentration. The hole concentration in the "
  "sample becomes:",
  *opt("4 times its earlier value", ["2 times its earlier value", "unchanged", "1/4 of its earlier value"], "B"),
  "Mass-action law in thermal equilibrium: n_e n_h = n_i²",
  "In the n-type sample n_e ≈ N_D is fixed by the doping. The minority (hole) concentration is n_h = n_i²/n_e, so it "
  "varies as the square of n_i. This is why the reverse current of a junction diode, carried by minority carriers, "
  "rises steeply with temperature.",
  ["n_h = n_i²/N_D", "n_i → 2n_i, N_D unchanged → n_h → 4n_h"],
  why="'2 times' treats n_h as proportional to n_i. 'Unchanged' assumes the doping alone fixes the minority carriers. "
      "'1/4' inverts the dependence.",
  ncert=SCC + "extrinsic semiconductor", seconds=60, rc=True)
