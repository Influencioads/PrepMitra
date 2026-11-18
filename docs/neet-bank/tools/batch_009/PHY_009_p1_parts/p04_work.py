

# =====================================================================================================================
# Work, Energy and Power (B4 I5 A4)
# =====================================================================================================================
T = "Work, Energy and Power"

assert close(0.5 * 2 * (3 ** 2 + 4 ** 2), 25)
add(T, "Work-energy theorem", "Basic", "numerical",
    "A body of mass 2 kg moves with a velocity v = (3î + 4ĵ) m/s. Its kinetic energy is:",
    place("25 J", ["49 J", "50 J", "5 J"], "B"),
    "Kinetic energy from a velocity vector",
    "Kinetic energy depends on the square of the speed, v² = v·v = vₓ² + v_y². It is a scalar.",
    ["v² = 3² + 4² = 25 m²/s²", "K = ½ × 2 × 25 = 25 J"],
    why="49 J squares the sum of the components, (3 + 4)²; 50 J forgets the ½; 5 J is the speed in m/s.",
    ncert="Class 11 Physics, 'Work, Energy and Power', kinetic energy", seconds=25, recomputed=True)

assert close(2 * g * 5, 100)
add(T, "Work-energy theorem", "Basic", "numerical",
    "A ball of mass 2 kg is dropped from rest from a height of 5 m. Taking g = 10 m/s² and neglecting air "
    "resistance, its kinetic energy just before it strikes the ground is:",
    place("100 J", ["10 J", "50 J", "200 J"], "C"),
    "Work done by gravity equals the gain in kinetic energy",
    "The only force doing work is gravity, which does work mgh on the ball as it falls through h. By the "
    "work-energy theorem this equals the gain in kinetic energy.",
    ["W_gravity = mgh = 2 × 10 × 5 = 100 J", "K = 0 + 100 = 100 J"],
    why="10 J is the speed (10 m/s) written as an energy; 50 J halves mgh; 200 J doubles it.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=25, recomputed=True)

assert close(math.sqrt(g * 2.5), 5.0)
add(T, "Motion in a vertical circle", "Basic", "numerical",
    "A small stone tied to a light string 2.5 m long is whirled in a vertical circle. Taking g = 10 m/s², the least "
    "speed it must have at the highest point for the string to remain taut there is:",
    place("5 m/s", ["5√5 m/s", "25 m/s", "5√2 m/s"], "A"),
    "Critical speed at the top of a vertical circle",
    "At the highest point both gravity and the tension point towards the centre: T + mg = mv²/L. The string just "
    "stays taut when T = 0, so v² = gL.",
    ["T + mg = mv²/L with T = 0", "v = √(gL) = √25 = 5 m/s"],
    why="5√5 m/s is √(5gL), the least speed needed at the LOWEST point; 25 m/s is gL without the square root; "
        "5√2 m/s is √(2gL), the speed gained in falling through L, which is not the condition here.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=30, recomputed=True)

add(T, "Spring potential energy", "Basic", "direct",
    "A block attached to an ideal spring is pulled slowly from the spring's natural length to an extension x and "
    "then allowed to return slowly to the natural length. The total work done by the spring force over this whole "
    "cycle is:",
    place("Zero", ["½kx²", "−½kx²", "kx²"], "D"),
    "Spring force is conservative",
    "The spring force is conservative: the work it does depends only on the initial and final positions. While "
    "stretching it does −½kx², while returning it does +½kx², so the total over a closed cycle is zero.",
    ["Stretching: W = −½kx²", "Returning: W = +½kx²", "Total over the cycle = 0"],
    why="½kx² and −½kx² are the work in only one half of the cycle; kx² adds the magnitudes of the two halves.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=25)

t_ = 3.0
v_ = t_ ** 2          # a = 2t / 1 kg  ->  v = t^2
assert close(2 * t_ * v_, 54)
add(T, "Power", "Intermediate", "numerical",
    "A body of mass 1 kg, initially at rest, is acted on by a single force F = 2t along a straight line, where F is "
    "in newtons and t in seconds. The instantaneous power delivered by the force at t = 3 s is:",
    place("54 W", ["18 W", "27 W", "6 W"], "C"),
    "Instantaneous power P = Fv",
    "First find the velocity at t = 3 s by integrating the acceleration, then multiply by the force at that "
    "instant.",
    ["a = F/m = 2t → v = ∫₀ᵗ 2t dt = t²", "At t = 3 s: F = 6 N, v = 9 m/s", "P = Fv = 6 × 9 = 54 W"],
    why="18 W takes v = at = 6 × 3, treating the acceleration as constant; 27 W uses the average force 3 N; 6 W "
        "gives the force alone.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=60, recomputed=True)

assert close(5 / 0.5, 10)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "A small block is released from rest at a height of 5 m on a smooth curved track. At the bottom the track "
    "becomes horizontal and rough, with coefficient of kinetic friction 0.5. The distance the block slides along "
    "the rough part before stopping is:",
    place("10 m", ["5 m", "2.5 m", "20 m"], "B"),
    "Work-energy theorem with gravity and friction",
    "Over the whole motion the block starts and ends at rest, so the work done by gravity (mgh) and by friction "
    "(−μmgd) add up to zero. The smooth curved part does no frictional work, and the normal force does no work.",
    ["mgh − μmgd = 0", "d = h/μ = 5/0.5 = 10 m"],
    shortcut="d = h/μ; the mass and g cancel.",
    why="5 m equates d to h; 2.5 m multiplies h by μ instead of dividing; 20 m finds v² = 2gh = 100 m²/s² at the "
        "bottom and then forgets the 2 in d = v²/(2μg).",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=50, recomputed=True)

assert close(0.5 * 800 * 20 ** 2 / 10, 16000)
assert close(800 * 2 * 20, 32000) and close(0.5 * 800 * 10 ** 2 / 10, 4000)
add(T, "Power", "Intermediate", "numerical",
    "A car of mass 800 kg accelerates uniformly from rest to 20 m/s in 10 s along a level road. Neglecting friction "
    "and air resistance, the average power delivered to the car in these 10 s is:",
    place("16 kW", ["32 kW", "4 kW", "160 kW"], "D"),
    "Average power as work done divided by time",
    "The work done on the car equals its gain in kinetic energy. Average power is this work divided by the time. "
    "With uniform acceleration the instantaneous power rises steadily, so its final value is twice the average.",
    ["W = ½mv² = ½ × 800 × 400 = 160 kJ", "P_avg = 160 kJ / 10 s = 16 kW"],
    why="32 kW is the instantaneous power at the end (F = 1600 N times 20 m/s); 4 kW puts the average speed 10 m/s "
        "into ½mv²; 160 kW is the work in kJ, not divided by 10 s.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=50, recomputed=True)

add(T, "Work by constant and variable force", "Intermediate", "match_list",
    match_stem("A body moves along a straight line (the x-axis). Match List-I (feature of a graph) with List-II "
               "(the quantity it gives).",
               ["Area under the force–position (F–x) graph between two positions",
                "Slope of the kinetic energy–position (K–x) graph",
                "Negative of the slope of the potential energy–position (U–x) graph of a conservative force",
                "Slope of the kinetic energy–time (K–t) graph"],
               ["Power delivered by the net force", "The conservative force at that position",
                "Net force on the body along the x-axis", "Work done by the force between those positions"]),
    match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                  [{"A": "IV", "B": "I", "C": "II", "D": "III"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "IV", "B": "III", "C": "I", "D": "II"}], "A"),
    "Graphical meaning of work, force and power",
    "Work is ∫F dx, the area under F–x. By the work-energy theorem dK = F_net dx, so dK/dx = F_net and "
    "dK/dt = F_net·v, the power of the net force. For a conservative force F = −dU/dx.",
    ["A: W = ∫F dx → area (IV)", "B: dK/dx = F_net (III)", "C: −dU/dx = F (II)", "D: dK/dt = F_net v = P (I)"],
    why="The wrong codes swap the slope against position (a force) with the slope against time (a power), or the "
        "net force with the conservative force.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work done by a variable force; the concept of potential "
          "energy; power", seconds=70)

add(T, "Work-energy theorem", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The potential energy of a body can have a negative value.",
        s2="When only conservative forces do work on a body, its total mechanical energy remains constant, although "
           "its kinetic energy may change."),
    sp("A"),
    "Potential energy and conservation of mechanical energy",
    "Potential energy is defined only up to an additive constant: it is measured from a chosen zero, and below "
    "that reference (for example a body below the chosen ground level, or gravitational potential energy taken "
    "zero at infinity) it is negative. So Statement I is true. With only conservative forces, K + U is constant; K "
    "and U can each change as one is converted into the other. So Statement II is true.",
    ["Statement I: U depends on the reference level → can be negative → true",
     "Statement II: conservative forces → K + U = constant, K may vary → true"],
    why="Only the difference of potential energy is physically fixed, not its sign; and conservation of mechanical "
        "energy does not mean that the kinetic energy stays constant.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the concept of potential energy; conservation of mechanical "
          "energy", seconds=45)

x_ = 2 * g / 200
W_g = 2 * g * x_
U_s = 0.5 * 200 * x_ ** 2
assert close(x_, 0.1) and close(W_g, 2) and close(U_s, 1) and close(U_s - W_g, -1)
add(T, "Spring potential energy", "Advanced", "numerical",
    "A block of mass 2 kg is attached to the lower end of a light vertical spring of spring constant 200 N/m whose "
    "upper end is fixed. Starting with the spring at its natural length, the block is lowered slowly by hand until "
    "it hangs at rest in equilibrium. Taking g = 10 m/s², the work done by the hand on the block is:",
    place("−1 J", ["+1 J", "−2 J", "Zero"], "C"),
    "Work-energy theorem with gravity, spring and an applied force",
    "The block starts and ends at rest, so the total work done on it is zero. Gravity does +mgx; the spring does "
    "−½kx²; the hand, holding the block back, does the rest (negative work).",
    ["Equilibrium extension x = mg/k = 20/200 = 0.1 m", "W_gravity = mgx = 2 J; W_spring = −½kx² = −1 J",
     "W_hand = 0 − (2 − 1) = −1 J"],
    shortcut="Lowered slowly to equilibrium, the spring stores only half of the gravitational PE lost; the hand "
             "takes the other half.",
    why="+1 J has the wrong sign: the hand pushes up while the block moves down; −2 J ignores the spring; zero "
        "assumes gravity and the spring do equal and opposite work.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring; the work-energy theorem",
    seconds=110, recomputed=True)

L_ = 0.4
v_low = math.sqrt(5 * g * L_)
u_b = v_low * (0.05 + 0.95) / 0.05
assert close(v_low, 2 * math.sqrt(5)) and close(u_b, 40 * math.sqrt(5))
add(T, "Motion in a vertical circle", "Advanced", "numerical",
    "A wooden block of mass 0.95 kg hangs at rest from a light inextensible string 0.4 m long. A bullet of mass "
    "50 g moving horizontally strikes the block and gets embedded in it. Taking g = 10 m/s², the least speed of the "
    "bullet for which the block (with the bullet) just completes a vertical circle is:",
    place("40√5 m/s", ["40√2 m/s", "40 m/s", "2√5 m/s"], "B"),
    "Momentum conservation in the impact, then energy conservation in the vertical circle",
    "During the brief impact, momentum is conserved (kinetic energy is not). Just after the impact the block must "
    "have at least √(5gL) at the lowest point to go round the circle on a string.",
    ["Needed speed of block after impact: V = √(5gL) = √20 = 2√5 m/s",
     "Momentum: 0.05u = (0.05 + 0.95)V", "u = 20 × 2√5 = 40√5 m/s"],
    why="40√2 m/s uses √(2gL), which only raises the block to the level of the support; 40 m/s uses √(4gL), the "
        "condition for a light rod; 2√5 m/s is the block's speed, not the bullet's.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle; collisions", seconds=120,
    recomputed=True)

add(T, "Work by constant and variable force", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="The tension in the string of a swinging simple pendulum does no work on the bob.",
        r="The tension in the string of a swinging simple pendulum has the same magnitude at every point of the "
          "swing."),
    ar("C"),
    "Work done by a force perpendicular to the displacement",
    "The bob moves along an arc of a circle centred on the point of support, so its displacement at every instant "
    "is along the tangent, perpendicular to the string. The tension is along the string, so T·dr = 0 and the "
    "tension does no work: A is true. The tension is not constant: it must supply mv²/L plus the radial component "
    "of weight, T = mg cos θ + mv²/L, which is largest at the lowest point. So R is false.",
    ["A: tension ⊥ displacement → W = 0 → true", "R: T = mg cos θ + mv²/L varies with θ and v → false"],
    why="R is false, so options A and B are wrong; A is true, so D is wrong. The work is zero because of the "
        "direction of the tension, whatever its magnitude.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product and work", seconds=50)

k_, m_, u_ = 100, 1, 2
xmax = math.sqrt(m_ * u_ ** 2 / k_)
assert close(xmax, 0.2) and close(k_ * xmax, 20)
assert close(math.sqrt((0.5 * m_ * u_ ** 2 - 0.5 * k_ * 0.1 ** 2) * 2 / m_), math.sqrt(3))
truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Spring potential energy", "Advanced", "multi_statement",
    multi("A block of mass 1 kg moving at 2 m/s on a smooth horizontal surface strikes the free end of a light "
          "horizontal spring of spring constant 100 N/m, whose other end is fixed to a wall. Which of the following "
          "statements are correct?",
          ["The greatest force exerted by the spring on the block is 20 N.",
           "When the compression is 0.1 m, the speed of the block is √3 m/s.",
           "While the spring is being compressed, the spring force does +2 J of work on the block.",
           "The block leaves the spring with a speed of 2 m/s, moving away from the wall.",
           "Over the whole interaction, the net work done by the spring force on the block is +2 J."]),
    place("(a), (b) and (d) only", ["(a), (c) and (d) only", "(b), (c) and (e) only",
                                    "(a), (b), (d) and (e) only"], "D"),
    "Conservation of energy with an ideal spring",
    "All the kinetic energy (2 J) is stored at maximum compression, ½kx_m² = 2 J, so x_m = 0.2 m. The spring force "
    "opposes the block while it compresses (negative work) and pushes it back while it extends (positive work).",
    ["(a) x_m = √(2 × 2/100) = 0.2 m → F_max = kx_m = 20 N, true",
     "(b) ½v² = 2 − ½(100)(0.01) = 1.5 → v = √3 m/s, true",
     "(c) compression: W = −2 J, not +2 J → false", "(d) energy conserved → leaves at 2 m/s, reversed, true",
     "(e) net work = ΔK = 0 (speed unchanged) → false"],
    why="(c) has the wrong sign; (e) forgets that the block leaves with the same speed it came in with, so the net "
        "work is zero.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=110,
    recomputed=True)
