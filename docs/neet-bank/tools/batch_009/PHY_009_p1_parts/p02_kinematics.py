

def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    return math.sqrt(sum(x * x for x in a))


# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"

a_ = (20 ** 2 - 10 ** 2) / (2 * 75)
assert close(a_, 2.0)
add(T, "Motion in a straight line", "Basic", "numerical",
    "A car moving along a straight road with uniform acceleration increases its speed from 10 m/s to 20 m/s while "
    "covering a distance of 75 m. Its acceleration is:",
    place("2 m/s²", ["4 m/s²", "0.13 m/s²", "3.3 m/s²"], "A"),
    "Equation of motion v² = u² + 2as",
    "When the distance, not the time, is given, use the third equation of uniformly accelerated motion, "
    "v² = u² + 2as.",
    ["a = (v² − u²)/(2s)", "a = (400 − 100)/(2 × 75) = 300/150 = 2 m/s²"],
    why="4 m/s² forgets the 2 in 2as; 0.13 m/s² divides the change in speed by the distance (10/75); 3.3 m/s² adds "
        "the squares of the speeds instead of subtracting them (500/150).",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=35, recomputed=True)

assert close(4 * 5 * math.sin(math.radians(30)), 10.0)
add(T, "Vectors", "Basic", "numerical",
    "Two vectors of magnitudes 4 units and 5 units are inclined to each other at 30°. The magnitude of their vector "
    "(cross) product is:",
    place("10 units", ["10√3 units", "20 units", "9 units"], "C"),
    "Magnitude of the vector product",
    "|A × B| = AB sin θ, where θ is the angle between the vectors.",
    ["|A × B| = 4 × 5 × sin 30°", "= 20 × 1/2 = 10 units"],
    why="10√3 uses cos 30° (the scalar product); 20 takes sin θ = 1; 9 simply adds the magnitudes.",
    ncert="Class 11 Physics, 'Motion in a Plane' and 'System of Particles and Rotational Motion', vector product",
    seconds=25, recomputed=True)

assert close(30 ** 2 / g, 90.0)
add(T, "Projectile motion", "Basic", "numerical",
    "A ball can be thrown from level ground with a speed of 30 m/s in any direction. Taking g = 10 m/s² and "
    "neglecting air resistance, the greatest horizontal distance it can be thrown along the ground is:",
    place("90 m", ["45 m", "180 m", "45√2 m"], "B"),
    "Maximum horizontal range",
    "The range R = u² sin 2θ / g is greatest when sin 2θ = 1, i.e. θ = 45°, so R_max = u²/g.",
    ["R_max = u²/g", "= 900/10 = 90 m"],
    why="45 m is u²/(2g), the greatest height for a vertical throw; 180 m is 2u²/g; 45√2 m uses sin θ = sin 45° "
        "in place of sin 2θ = sin 90°.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion (horizontal range)", seconds=25,
    recomputed=True)

add(T, "Vectors", "Basic", "direct",
    "A vector A is multiplied by the real number −2. The resulting vector:",
    place("Has magnitude 2|A| and points opposite to A",
          ["Has magnitude 2|A| and points along A", "Has magnitude |A|/2 and points opposite to A",
           "Is a scalar of value −2|A|"], "D"),
    "Multiplication of a vector by a real number",
    "Multiplying a vector by a real number λ gives a vector of magnitude |λ| times the original. If λ is negative, "
    "the direction is reversed.",
    ["|−2A| = 2|A|", "λ < 0 → direction reversed"],
    why="A negative multiplier reverses the direction, so 'along A' is wrong; the magnitude is multiplied by 2, not "
        "divided; and a vector multiplied by a scalar is still a vector.",
    ncert="Class 11 Physics, 'Motion in a Plane', multiplication of vectors by real numbers", seconds=20)

# v = 6t - 3t^2, x(0) = 0 -> x = 3t^2 - t^3 ; v = 0 at t = 2
t_rest = 2.0
assert close(6 * t_rest - 3 * t_rest ** 2, 0.0)
assert close(3 * t_rest ** 2 - t_rest ** 3, 4.0)
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A particle starts from the origin at t = 0 and moves along the x-axis with velocity v = 6t − 3t², where v is "
    "in m/s and t in seconds. Its position at the instant (after t = 0) when it comes momentarily to rest is:",
    place("4 m", ["12 m", "2 m", "6 m"], "B"),
    "Position from velocity by integration",
    "Set v = 0 to find the instant of rest, then integrate the velocity from t = 0 to get the position, using "
    "x = 0 at t = 0.",
    ["v = 0 → 6t − 3t² = 0 → t = 2 s", "x = ∫₀ᵗ (6t − 3t²) dt = 3t² − t³", "x(2) = 12 − 8 = 4 m"],
    why="12 m keeps only the 3t² term; 2 m gives the time, not the position; 6 m multiplies the greatest speed "
        "(3 m/s, at t = 1 s) by the whole 2 s, as if the speed were constant.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and kinematic relations",
    seconds=60, recomputed=True)

uy = g * (2 * math.sqrt(3)) / 2
assert close(math.degrees(math.atan2(uy, 10)), 60.0)
add(T, "Projectile motion", "Intermediate", "numerical",
    "A projectile launched from level ground has a speed of 10 m/s at the highest point of its path and a time of "
    "flight of 2√3 s. Taking g = 10 m/s² and neglecting air resistance, its angle of projection above the "
    "horizontal is:",
    place("60°", ["30°", "45°", "tan⁻¹(2√3)"], "A"),
    "Horizontal and vertical components of a projectile's velocity",
    "At the highest point only the horizontal component u cos θ remains, so u cos θ = 10 m/s. The time of flight "
    "T = 2u sin θ / g gives the vertical component u sin θ = gT/2.",
    ["u cos θ = 10 m/s", "u sin θ = gT/2 = 10 × 2√3/2 = 10√3 m/s", "tan θ = √3 → θ = 60°"],
    why="30° swaps the two components; 45° assumes the components are equal; tan⁻¹(2√3) uses u sin θ = gT, "
        "forgetting that the rise takes only half the flight time.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=60, recomputed=True)

t_meet = 40 / 20
assert close(t_meet, 2.0) and close(20 * t_meet - 0.5 * g * t_meet ** 2, 40 - 0.5 * g * t_meet ** 2)
add(T, "Relative velocity", "Intermediate", "numerical",
    "At the same instant, ball P is thrown vertically upward from the ground with a speed of 20 m/s, and ball Q is "
    "released from rest at a height of 40 m vertically above P's starting point. Taking g = 10 m/s² and neglecting "
    "air resistance, the two balls meet after:",
    place("2 s", ["4 s", "2√2 s", "1 s"], "D"),
    "Relative motion of two bodies with the same acceleration",
    "Both balls have the same acceleration g, so the acceleration of one relative to the other is zero. Relative "
    "to Q, ball P moves upward at a constant 20 m/s, and it must close a gap of 40 m.",
    ["Relative acceleration = g − g = 0", "Relative speed = 20 − 0 = 20 m/s", "t = 40/20 = 2 s",
     "Check: P at 20(2) − 5(4) = 20 m; Q at 40 − 5(4) = 20 m"],
    shortcut="Same acceleration → treat the gap as closing at the constant relative speed.",
    why="4 s is P's time of flight; 2√2 s is the time Q alone would take to fall 40 m; 1 s halves the correct time "
        "by adding the two speeds wrongly (40/40).",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity", seconds=60, recomputed=True)

add(T, "Graphs of motion", "Intermediate", "match_list",
    match_stem("The position x of a particle moving along the x-axis is given by each relation in List-I (x in "
               "metres, t in seconds, t ≥ 0). Match List-I with the description of the motion in List-II.",
               ["x = 5", "x = 3t", "x = 2t²", "x = 4t − t²"],
               ["Constant acceleration opposite to the initial velocity; the particle stops at t = 2 s and then "
                "moves back", "Constant non-zero velocity, zero acceleration",
                "At rest", "Starts from rest with constant acceleration along +x"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "C"),
    "Reading velocity and acceleration from x(t)",
    "Differentiate each relation once for the velocity and twice for the acceleration.",
    ["x = 5: v = 0, a = 0 → at rest (III)", "x = 3t: v = 3 m/s, a = 0 → uniform velocity (II)",
     "x = 2t²: v = 4t (0 at t = 0), a = 4 m/s² → from rest with constant acceleration (IV)",
     "x = 4t − t²: v = 4 − 2t, a = −2 m/s² → stops at t = 2 s and returns (I)"],
    why="The wrong codes confuse a constant position (rest) with a constant velocity, or exchange the two "
        "accelerated motions, which differ in the sign of the acceleration relative to the initial velocity.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', position-time graphs and kinematic relations",
    seconds=70)

add(T, "Vectors", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A particle moving in a plane with a constant acceleration must always move along a parabolic path.",
        s2="For a particle moving in a plane with a constant acceleration a, its position vector at time t is "
           "r = r₀ + v₀t + ½at², where r₀ and v₀ are its position and velocity at t = 0."),
    sp("D"),
    "Motion in a plane with constant acceleration",
    "The vector relation r = r₀ + v₀t + ½at² holds for any constant acceleration, so Statement II is true. The "
    "path is a parabola only when v₀ is not parallel to a; if v₀ is zero or parallel (or antiparallel) to a, the "
    "particle moves along a straight line. So Statement I is false.",
    ["Statement II: integrate a = constant twice → r = r₀ + v₀t + ½at² → true",
     "Statement I: v₀ ∥ a (e.g. a ball thrown straight up) → straight-line path → false"],
    why="Statement I ignores the special case of initial velocity along the acceleration, such as vertical "
        "throws under gravity.",
    ncert="Class 11 Physics, 'Motion in a Plane', motion in a plane with constant acceleration", seconds=50)

# velocity 45 deg above horizontal at t = 1 s and 45 deg below at t = 3 s
uy = (g * 1 + g * 3) / 2
ux = uy - g * 1
assert close(uy, 20) and close(ux, 10) and close(-(uy - g * 3), ux)
assert close(uy / ux, 2.0)
add(T, "Projectile motion", "Advanced", "numerical",
    "A ball is projected from level ground. Its velocity is directed at 45° above the horizontal at t = 1 s and at "
    "45° below the horizontal at t = 3 s. Taking g = 10 m/s² and neglecting air resistance, the angle of projection "
    "above the horizontal is:",
    place("tan⁻¹(2)", ["45°", "tan⁻¹(1/2)", "60°"], "C"),
    "Components of projectile velocity at two instants",
    "The horizontal component u_x is constant and the vertical component falls as u_y − gt. At 45° above, "
    "u_y − g(1) = u_x; at 45° below, u_y − g(3) = −u_x. Solving gives both components.",
    ["u_y − 10 = u_x", "u_y − 30 = −u_x", "Adding: 2u_y = 40 → u_y = 20 m/s, so u_x = 10 m/s",
     "tan θ = u_y/u_x = 2 → θ = tan⁻¹(2)"],
    shortcut="By symmetry the highest point is midway, at t = 2 s, so u_y = 2g = 20 m/s; then u_x = u_y − g(1).",
    why="45° assumes the launch direction equals the direction at t = 1 s; tan⁻¹(1/2) inverts the ratio of "
        "components; 60° would need u_y/u_x = √3.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=110, recomputed=True)

Pd, Qd = (3, 1, -2), (1, -3, 4)
assert cross(Pd, Qd) == (-2, -14, -10)
assert close(0.5 * norm(cross(Pd, Qd)), 5 * math.sqrt(3))
add(T, "Vectors", "Advanced", "numerical",
    "The two diagonals of a parallelogram are represented by the vectors P = 3î + ĵ − 2k̂ and Q = î − 3ĵ + 4k̂. "
    "The area of the parallelogram is:",
    place("5√3 square units", ["10√3 square units", "20√3 square units", "(5√3)/2 square units"], "B"),
    "Area of a parallelogram from its diagonals",
    "If the sides are a and b, the diagonals are P = a + b and Q = a − b (or b − a). Then P × Q = −2(a × b) in "
    "magnitude 2|a × b|, so the area |a × b| equals ½|P × Q|.",
    ["P × Q = î(1·4 − (−2)(−3)) − ĵ(3·4 − (−2)·1) + k̂(3·(−3) − 1·1) = −2î − 14ĵ − 10k̂",
     "|P × Q| = √(4 + 196 + 100) = √300 = 10√3", "Area = ½|P × Q| = 5√3 square units"],
    why="10√3 uses |P × Q| directly, as if P and Q were the sides; 20√3 doubles instead of halving; (5√3)/2 "
        "halves twice, mixing up the area of a triangle with that of the parallelogram.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', vector product of two vectors",
    seconds=120, recomputed=True)

add(T, "Vectors", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="If two non-parallel vectors A and B have equal magnitudes, the vectors (A + B) and (A − B) are "
          "perpendicular to each other.",
        r="(A + B) · (A − B) = A² − B², where A and B are the magnitudes of the two vectors."),
    ar("A"),
    "Scalar product and perpendicularity",
    "Expanding the scalar product, (A + B)·(A − B) = A·A − A·B + B·A − B·B = A² − B², because the scalar product "
    "is commutative. When A = B this is zero, and a zero scalar product of two non-zero vectors means they are "
    "perpendicular. So R is exactly the reason for A.",
    ["(A + B)·(A − B) = A² − B² (R true)", "A = B → product = 0 → (A + B) ⊥ (A − B) (A true)",
     "R directly gives A → option A"],
    why="R is not a separate fact: setting A = B in R is the whole proof of A, so B is wrong; both statements are "
        "true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product", seconds=60)

add(T, "Motion in a straight line", "Advanced", "multi_statement",
    multi("A ball is thrown vertically upward from the ground with a speed of 20 m/s. Taking g = 10 m/s² and "
          "neglecting air resistance, which of the following statements are correct?",
          ["It rises to a maximum height of 20 m.",
           "At t = 3 s, it is 15 m above the ground.",
           "The distance it travels in the first 3 s is 25 m.",
           "At t = 3 s, its velocity is 10 m/s directed upward.",
           "Its average velocity over the first 4 s is zero."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(a), (c) and (e) only",
                                         "(b), (c), (d) and (e) only"], "D"),
    "Vertical motion under gravity: displacement versus distance",
    "The ball rises for u/g = 2 s to a height u²/2g = 20 m and is back on the ground at 2u/g = 4 s. After 2 s it "
    "falls, so its velocity at 3 s is downward.",
    ["(a) H = 400/20 = 20 m, true", "(b) y(3) = 20(3) − 5(9) = 15 m, true",
     "(c) 20 m up in 2 s, then 5 m down in the next 1 s → 25 m, true",
     "(d) v(3) = 20 − 30 = −10 m/s → 10 m/s downward, false", "(e) y(4) = 80 − 80 = 0 → average velocity 0, true"],
    why="(d) has the right speed but the wrong direction: after the highest point (t = 2 s) the ball moves down. "
        "Every option without (c) or including (d) is wrong.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=100, recomputed=True)
