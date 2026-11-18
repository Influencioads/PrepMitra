

# =====================================================================================================================
# Oscillations and Waves (B5 I5 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

assert close(4 * 5 / 2, 10)
add(T, "SHM equation and phase", "Basic", "numerical",
    "A particle executes simple harmonic motion with an amplitude of 5 cm and a period of 2 s. Its average speed "
    "over one complete oscillation is:",
    place("10 cm/s", ["Zero", "5π cm/s", "5 cm/s"], "B"),
    "Distance covered in one period of SHM",
    "In one complete oscillation the particle goes from the mean position to one extreme, back, to the other "
    "extreme and back: a distance of 4A. Average speed = total distance / time.",
    ["Distance in one period = 4A = 20 cm", "Average speed = 20 cm / 2 s = 10 cm/s"],
    why="Zero is the average VELOCITY over a period (the displacement is zero); 5π cm/s is the maximum speed Aω; "
        "5 cm/s counts only 2A per period.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion", seconds=30, recomputed=True)

assert close(math.pi / 2 - math.pi / 6, math.pi / 3)
add(T, "SHM equation and phase", "Basic", "numerical",
    "Two particles execute simple harmonic motions given by x₁ = A sin(ωt + π/6) and x₂ = A cos ωt along the same "
    "line. The phase difference between the two motions is:",
    place("π/3", ["π/6", "2π/3", "π/2"], "D"),
    "Comparing phases: writing cosine as a sine",
    "To compare phases, write both motions with the same function: A cos ωt = A sin(ωt + π/2). The phase "
    "difference is then the difference of the phase constants.",
    ["x₂ = A sin(ωt + π/2)", "Δφ = π/2 − π/6 = π/3 (x₂ leads x₁)"],
    why="π/6 compares cos ωt with sin ωt as if they were in phase; 2π/3 adds the phase constants; π/2 is the "
        "difference between sine and cosine alone, ignoring the π/6.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (phase)", seconds=30, recomputed=True)

assert close(2 * 0.20 * 500, 200)
add(T, "Superposition and standing waves", "Basic", "numerical",
    "In a stationary wave set up on a stretched string at a frequency of 500 Hz, adjacent nodes are 20 cm apart. The "
    "speed of the travelling waves on the string is:",
    place("200 m/s", ["100 m/s", "400 m/s", "20 m/s"], "B"),
    "Node spacing in a stationary wave",
    "Adjacent nodes in a stationary wave are half a wavelength apart, so λ = 2 × 20 cm = 0.40 m. The speed of the "
    "travelling waves is v = fλ.",
    ["λ/2 = 0.20 m → λ = 0.40 m", "v = fλ = 500 × 0.40 = 200 m/s"],
    why="100 m/s takes the node spacing as a whole wavelength; 400 m/s takes it as a quarter wavelength (the "
        "node-to-antinode distance); 20 m/s converts 20 cm wrongly to 0.02 m.",
    ncert="Class 11 Physics, 'Waves', reflection of waves (standing waves and normal modes)", seconds=30,
    recomputed=True)

add(T, "SHM equation and phase", "Basic", "direct",
    "Which of the following motions is periodic but NOT oscillatory?",
    place("A particle moving uniformly along a circle",
          ["The bob of a simple pendulum swinging through a small angle",
           "A block oscillating on a horizontal spring", "A prong of a vibrating tuning fork"], "C"),
    "Periodic and oscillatory motion",
    "NCERT: every oscillatory motion is periodic, but not every periodic motion is oscillatory. Uniform circular "
    "motion repeats itself after a fixed time, but the particle does not move to and fro about a mean position.",
    ["Periodic → repeats after a fixed interval", "Oscillatory → to-and-fro about a mean position",
     "Uniform circular motion: periodic, not oscillatory"],
    why="A pendulum bob, a block on a spring and a tuning-fork prong all move to and fro about a mean position, so "
        "their motions are both periodic and oscillatory.",
    ncert="Class 11 Physics, 'Oscillations', periodic and oscillatory motions", seconds=20)

add(T, "Progressive waves and wave speed", "Basic", "statement_pair",
    SP_STEM.format(
        s1="When a transverse wave passes from a light string into a heavier string joined to it, under the same "
           "tension, its frequency stays the same while its speed and wavelength decrease.",
        s2="In a sound wave travelling through air, a compression is a region where the density and the pressure "
           "of the air are higher than normal."),
    sp("A"),
    "Wave speed, frequency and wavelength; compressions",
    "The frequency of a wave is set by the source and does not change at a boundary. The speed on a string is "
    "√(T/μ), so a larger μ means a smaller speed, and λ = v/f is smaller too: Statement I is true. In a longitudinal "
    "wave, compressions are regions of higher density and pressure, rarefactions of lower: Statement II is true.",
    ["Statement I: f fixed, v = √(T/μ) falls as μ rises, λ = v/f falls → true",
     "Statement II: compression = higher density and pressure → true"],
    why="Both statements are true.",
    ncert="Class 11 Physics, 'Waves', speed of a travelling wave; transverse and longitudinal waves", seconds=40)

t_eq = 2.0 / 8
assert close(math.sin(2 * math.pi / 2.0 * t_eq), 1 / math.sqrt(2))
add(T, "Energy in SHM", "Intermediate", "numerical",
    "A particle starts from its mean position at t = 0 and executes simple harmonic motion with a period of 2 s. The "
    "earliest time at which its kinetic energy equals its potential energy is:",
    place("0.25 s", ["0.5 s", "0.125 s", "0.33 s"], "B"),
    "Energy sharing in SHM and the corresponding time",
    "K = U when each is half the total energy: ½kx² = ¼kA², so x = A/√2. With x = A sin(2πt/T), this first happens "
    "at 2πt/T = π/4, i.e. t = T/8.",
    ["K = U → x = A/√2", "sin(2πt/T) = 1/√2 → 2πt/T = π/4", "t = T/8 = 2/8 = 0.25 s"],
    why="0.5 s (T/4) is the time to reach the extreme position; 0.125 s (T/16) halves the phase angle; 0.33 s (T/6) "
        "is the time to reach x = A/2, where K = 3U.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=60, recomputed=True)

f_B = 256 - 6
assert abs((f_B + 2) - 256) == 4 and abs((256 + 6 + 2) - 256) == 8
add(T, "Organ pipes and beats", "Intermediate", "numerical",
    "Tuning fork P of frequency 256 Hz and tuning fork Q produce 6 beats per second when sounded together. When the "
    "prongs of Q are filed slightly, the two forks produce 4 beats per second. The frequency of Q before filing "
    "was:",
    place("250 Hz", ["262 Hz", "252 Hz", "260 Hz"], "C"),
    "Beats, and the effect of filing a tuning fork",
    "Beat frequency = |f_P − f_Q|, so f_Q is 250 Hz or 262 Hz. Filing the prongs makes them lighter, which RAISES "
    "the frequency of the fork. If f_Q were 262 Hz, raising it would increase the beat frequency; since the beats "
    "fall to 4 per second, f_Q must have been 250 Hz (raised to 252 Hz).",
    ["f_Q = 256 ± 6 = 250 Hz or 262 Hz", "Filing → f_Q increases",
     "250 → 252 Hz gives 4 beats/s (matches); 262 → higher gives more than 6 beats/s",
     "f_Q = 250 Hz"],
    why="262 Hz assumes filing lowers the frequency (that is the effect of loading with wax); 252 Hz is the "
        "frequency after filing; 260 Hz uses the second beat count with the wrong sign.",
    ncert="Class 11 Physics, 'Waves', beats", seconds=60, recomputed=True)

n_h = 2 * 1.5 * 500 / 300
assert close(n_h, 5) and int(round(n_h)) + 1 == 6
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "A string 1.5 m long is fixed at both ends. Transverse waves travel on it at 300 m/s. When it vibrates in a "
    "normal mode of frequency 500 Hz, the number of nodes on it, including the two fixed ends, is:",
    place("6", ["5", "4", "10"], "B"),
    "Normal modes of a string fixed at both ends",
    "The normal modes have L = nλ/2, i.e. fₙ = nv/(2L). The nth mode has n loops, and therefore n + 1 nodes "
    "counting the two ends.",
    ["λ = v/f = 300/500 = 0.6 m", "n = 2L/λ = 3/0.6 = 5 (fifth harmonic, 5 loops)", "Nodes = n + 1 = 6"],
    why="5 is the number of loops (antinodes), not nodes; 4 leaves out both ends; 10 counts the number of half "
        "wavelengths in a doubled length.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=60, recomputed=True)

add(T, "Energy in SHM", "Intermediate", "match_list",
    match_stem("For a particle executing simple harmonic motion about x = 0 between x = −A and x = +A, match "
               "List-I (graph) with List-II (its shape).",
               ["Velocity v against displacement x", "Acceleration a against displacement x",
                "Potential energy U against displacement x", "Total mechanical energy E against displacement x"],
               ["A horizontal straight line", "An ellipse",
                "A straight line through the origin with a negative slope",
                "A parabola opening upward with its minimum at x = 0"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
                   {"A": "IV", "B": "III", "C": "II", "D": "I"}], "D"),
    "Graphs of SHM quantities against displacement",
    "v = ±ω√(A² − x²) gives v²/(ωA)² + x²/A² = 1, an ellipse. a = −ω²x is a straight line of negative slope through "
    "the origin. U = ½kx² is a parabola with its minimum at the mean position. E = ½kA² is the same at every x.",
    ["A: v² + ω²x² = ω²A² → ellipse (II)", "B: a = −ω²x → straight line, negative slope (III)",
     "C: U = ½kx² → upward parabola (IV)", "D: E = ½kA² constant → horizontal line (I)"],
    why="The wrong codes swap the velocity graph with the acceleration graph, or the potential energy with the "
        "total energy.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in SHM; energy in SHM", seconds=60)

add(T, "SHM equation and phase", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="For a particle executing simple harmonic motion, the speed is greatest at the extreme positions.",
        r="At the extreme positions of simple harmonic motion, the restoring force and the acceleration have their "
          "greatest magnitudes."),
    ar("D"),
    "Speed and acceleration in SHM",
    "v = ω√(A² − x²) is zero at the extremes (x = ±A) and greatest at the mean position, so A is false. "
    "a = −ω²x has its greatest magnitude ω²A at the extremes, so R is true.",
    ["A: at x = ±A, v = 0 → speed least, not greatest → false", "R: |a| = ω²|x| greatest at |x| = A → true"],
    why="A is false, so options A, B and C are wrong. A large acceleration does not mean a large speed: at the "
        "extremes the particle is momentarily at rest.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=40)

ratio_A = (3 / 4) / math.sqrt(3 / 4)
assert close(ratio_A, math.sqrt(3) / 2)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A block of mass 3 kg attached to a light horizontal spring oscillates on a smooth floor with amplitude A. Just as "
    "the block passes through its mean position, a lump of putty of mass 1 kg is dropped vertically onto it and "
    "sticks. The new amplitude of oscillation is:",
    place("(√3/2)A", ["(3/4)A", "A", "(9/16)A"], "B"),
    "SHM combined with conservation of momentum",
    "The putty has no horizontal velocity, so horizontal momentum is conserved: the speed at the mean position drops "
    "from v₀ = Aω to 3v₀/4. The angular frequency also changes, to ω' = √(k/4) = ω√(3/4). The new amplitude is the "
    "new maximum speed divided by ω'.",
    ["3v₀ = 4v' → v' = (3/4)Aω", "ω' = ω√(3/4)", "A' = v'/ω' = (3/4)A/√(3/4) = (√3/2)A"],
    shortcut="A' = A√(M/(M + m)) when mass is added at the mean position.",
    why="(3/4)A divides by the old ω, forgetting that the mass change also changes ω; A assumes the amplitude is "
        "unaffected; (9/16)A squares the velocity ratio.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring; 'Laws of Motion', conservation of "
          "momentum", seconds=120, recomputed=True)

ts = [i / 1000 * 2 * math.pi for i in range(1001)]
sep = max(abs(math.sin(t) - math.sin(t + math.pi / 3)) for t in ts)
assert close(sep, 1.0, rel=1e-4)
add(T, "SHM equation and phase", "Advanced", "numerical",
    "Two particles execute simple harmonic motions x₁ = A sin ωt and x₂ = A sin(ωt + π/3) along the same straight "
    "line, about the same mean position. The maximum distance between the two particles during the motion is:",
    place("A", ["2A", "√3 A", "A/2"], "C"),
    "Superposing two SHMs of the same frequency",
    "Their separation is x₂ − x₁ = A[sin(ωt + π/3) − sin ωt] = 2A cos(ωt + π/6) sin(π/6) = A cos(ωt + π/6). It is "
    "itself simple harmonic with amplitude 2A sin(Δφ/2) = A.",
    ["x₂ − x₁ = 2A sin(π/6) cos(ωt + π/6)", "= A cos(ωt + π/6)", "Maximum |x₂ − x₁| = A"],
    shortcut="Maximum separation = 2A sin(Δφ/2).",
    why="2A would need opposite phase (Δφ = π); √3 A uses 2A cos(Δφ/2), the amplitude of the SUM x₁ + x₂; A/2 "
        "uses A sin(Δφ/2) without the factor 2.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (phase)", seconds=110, recomputed=True)

assert close(2 * math.pi * math.sqrt(1 / math.pi ** 2), 2) and close(2 * math.pi * math.sqrt(4 / math.pi ** 2), 4)
truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Spring and pendulum oscillations", "Advanced", "multi_statement",
    multi("A simple pendulum of length 1 m, at a place where g = π² m/s², is pulled aside through 4° and released. "
          "Which of the following statements are correct?",
          ["Its period is 2 s.",
           "If it were released from 2° instead, its period would still be very nearly 2 s.",
           "As the bob passes through the mean position, the tension in the string is equal to the weight of the bob.",
           "If the length were made 4 m, the period would become 4 s.",
           "If the mass of the bob were doubled, the period would become √2 times as long."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(a), (d) and (e) only",
                                    "(b), (c) and (e) only"], "A"),
    "Simple pendulum: period, and tension at the mean position",
    "For small angles T = 2π√(L/g), independent of amplitude and of the mass of the bob. At the mean position the "
    "bob is moving along a circular arc with speed v, so the string must supply a net upward force mv²/L: "
    "T − mg = mv²/L, and the tension exceeds the weight.",
    ["(a) T = 2π√(1/π²) = 2 s, true", "(b) small angles → T independent of amplitude, true",
     "(c) T = mg + mv²/L > mg, since v ≠ 0 at the mean position → false", "(d) T ∝ √L → 2 × 2 = 4 s, true",
     "(e) T does not depend on mass → false"],
    why="(c) treats the moving bob as if it were hanging at rest, forgetting the centripetal force mv²/L; (e) wrongly brings in the mass, which cancels "
        "in the restoring-force equation.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=100, recomputed=True)

k_, w_ = 5 * math.pi, 200 * math.pi
assert close(2 * math.pi / k_, 0.4) and close(w_ / (2 * math.pi), 100) and close(w_ / k_, 40)
assert all(close(math.sin(k_ * x), 0, rel=0) or abs(math.sin(k_ * x)) < 1e-9 for x in (0, 0.2, 0.4))
truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Superposition and standing waves", "Advanced", "multi_statement",
    multi("A stationary wave on a string is described by y = 0.04 sin(5πx) cos(200πt), where x and y are in metres "
          "and t in seconds. Which of the following statements are correct?",
          ["The wavelength of the component travelling waves is 0.4 m.",
           "The frequency of oscillation of the particles is 100 Hz.",
           "The speed of each component travelling wave is 0.025 m/s.",
           "The amplitude of each component travelling wave is 0.04 m.",
           "There are nodes at x = 0, x = 0.2 m and x = 0.4 m."]),
    place("(a), (b) and (e) only", ["(a), (b), (d) and (e) only", "(b), (c) and (e) only",
                                    "(a), (c) and (d) only"], "B"),
    "Reading a stationary-wave equation",
    "y = 2a sin kx cos ωt is the superposition of two waves of amplitude a travelling in opposite directions. Here "
    "k = 5π m⁻¹ and ω = 200π rad/s. Nodes are where sin kx = 0.",
    ["(a) λ = 2π/k = 0.4 m, true", "(b) f = ω/2π = 100 Hz, true",
     "(c) v = ω/k = 40 m/s, not 0.025 m/s (that is k/ω) → false",
     "(d) 2a = 0.04 m → each wave has a = 0.02 m → false", "(e) sin 5πx = 0 at x = 0, 0.2, 0.4 m, true"],
    why="(c) inverts ω/k; (d) takes the amplitude at an antinode, 2a, as the amplitude of each component wave.",
    ncert="Class 11 Physics, 'Waves', reflection of waves (standing waves and normal modes)", seconds=110,
    recomputed=True)
