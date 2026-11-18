

# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

assert close(0.6 / 0.8, 0.75)
add(T, "Friction", "Basic", "numerical",
    "A block placed on a plank begins to slide down when one end of the plank is slowly raised until the plank "
    "makes an angle of 37° with the horizontal (sin 37° = 0.6, cos 37° = 0.8). The coefficient of static friction "
    "between the block and the plank is:",
    place("0.75", ["0.6", "0.8", "1.33"], "C"),
    "Angle of repose",
    "At the angle of repose θᵣ the component of weight along the incline just equals the limiting static "
    "friction: mg sin θᵣ = μₛ mg cos θᵣ, so μₛ = tan θᵣ.",
    ["μₛ = tan 37° = sin 37°/cos 37°", "= 0.6/0.8 = 0.75"],
    why="0.6 is sin 37° and 0.8 is cos 37°, not their ratio; 1.33 is cot 37°, the ratio taken upside down.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (angle of repose)", seconds=30, recomputed=True)

assert close(1000 * 10 ** 2 / 50, 2000)
add(T, "Circular motion: level and banked roads", "Basic", "numerical",
    "A car of mass 1000 kg takes a turn of radius 50 m on a level (unbanked) road at a steady speed of 10 m/s. The "
    "magnitude of the frictional force exerted by the road on the car is:",
    place("2000 N", ["200 N", "20000 N", "10000 N"], "D"),
    "Friction as the centripetal force on a level road",
    "On a level road the only horizontal force on the car is static friction, so it alone supplies the "
    "centripetal force mv²/r. It need not be the limiting value μₛN.",
    ["f = mv²/r", "= 1000 × 100/50 = 2000 N"],
    why="200 N uses mv/r (speed not squared); 20000 N uses mv²/r with r = 5 m; 10000 N is the weight mg, which "
        "would be μN with μ = 1.",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion (car on a level road)", seconds=30, recomputed=True)

a_ = g * math.sin(math.radians(30))
assert close(math.sqrt(2 * a_ * 10), 10.0)
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A block is released from rest on a smooth plane inclined at 30° to the horizontal. Taking g = 10 m/s², its "
    "speed after it has slid 10 m along the incline is:",
    place("10 m/s", ["10√3 m/s", "10√2 m/s", "5 m/s"], "A"),
    "Motion on a smooth inclined plane",
    "On a smooth incline the only force along the plane is the component of weight mg sin θ, so the block "
    "accelerates uniformly at g sin θ along the incline.",
    ["a = g sin 30° = 5 m/s²", "v² = 2as = 2 × 5 × 10 = 100", "v = 10 m/s"],
    why="10√3 m/s uses g cos θ as the acceleration; 10√2 m/s uses the full g (free fall through 10 m); 5 m/s gives "
        "the acceleration value instead of the speed.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law", seconds=35, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "direct",
    "Which of the following is NOT a contact force?",
    place("The gravitational force between the Earth and the Moon",
          ["The frictional force between a block and the floor", "The normal reaction of a table on a book",
           "The tension in a string pulling a block"], "B"),
    "Contact and non-contact forces",
    "Friction, the normal reaction and the tension in a string act only when bodies touch. Gravitational (and "
    "magnetic) forces act across a distance, without contact.",
    ["Friction, normal force, tension → contact forces", "Gravitation → acts at a distance"],
    why="The other three forces all need physical contact between the bodies concerned.",
    ncert="Class 11 Physics, 'Laws of Motion', introduction (contact and non-contact forces)", seconds=20)

# blocks 1, 2, 3 kg in a line, 12 N pulls the 3 kg block
a_ = 12 / (1 + 2 + 3)
assert close(a_, 2) and close((1 + 2) * a_, 6) and close(1 * a_, 2)
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "Three blocks of masses 1 kg, 2 kg and 3 kg lie in a line on a smooth horizontal table, in that order, joined "
    "by two light horizontal strings (1 kg to 2 kg, and 2 kg to 3 kg). A horizontal force of 12 N pulls the 3 kg "
    "block away from the others. The tension in the string joining the 2 kg and 3 kg blocks is:",
    place("6 N", ["2 N", "10 N", "4 N"], "A"),
    "Connected bodies: tension from the free-body diagram of the trailing part",
    "All three blocks have the same acceleration. The string between the 2 kg and 3 kg blocks pulls the 1 kg and "
    "2 kg blocks together, so its tension equals their combined mass times the acceleration.",
    ["a = 12/(1 + 2 + 3) = 2 m/s²", "T = (1 + 2) × 2 = 6 N"],
    why="2 N is the tension in the other string (1 kg × 2 m/s²); 10 N subtracts only the 1 kg block's share from "
        "12 N; 4 N uses the 2 kg block alone.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law and the dynamics of connected bodies",
    seconds=55, recomputed=True)

a_ = 0.5 * g
assert close(10 ** 2 / (2 * a_), 10.0)
add(T, "Friction", "Intermediate", "numerical",
    "A block slides onto a rough horizontal floor with a speed of 10 m/s. The coefficient of kinetic friction "
    "between the block and the floor is 0.5. Taking g = 10 m/s², the distance it slides before coming to rest is:",
    place("10 m", ["20 m", "5 m", "2 m"], "C"),
    "Retardation due to kinetic friction",
    "The only horizontal force is kinetic friction μₖmg, so the retardation is μₖg, independent of the mass.",
    ["a = μₖg = 0.5 × 10 = 5 m/s²", "s = u²/(2a) = 100/10 = 10 m"],
    why="20 m forgets the 2 in u²/(2a); 5 m is the value of the retardation; 2 m is the stopping time "
        "(u/a = 2 s) written as a distance.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (kinetic friction)", seconds=40, recomputed=True)

px, py = 2 * 3, 1 * 6
assert close(math.hypot(px, py) / 3, 2 * math.sqrt(2))
add(T, "Conservation of linear momentum", "Intermediate", "numerical",
    "On a smooth horizontal surface, a ball of mass 2 kg moving due east at 3 m/s collides with a ball of mass "
    "1 kg moving due north at 6 m/s. The balls stick together. The speed of the combined body just after the "
    "collision is:",
    place("2√2 m/s", ["4 m/s", "6√2 m/s", "2 m/s"], "B"),
    "Conservation of momentum in two dimensions",
    "With no external horizontal force, the total momentum is conserved as a vector. Conserve each component "
    "separately and combine.",
    ["East: 2 × 3 = 6 kg m/s; North: 1 × 6 = 6 kg m/s", "Total p = √(6² + 6²) = 6√2 kg m/s",
     "v = 6√2/3 = 2√2 m/s, directed north-east"],
    why="4 m/s adds the two momenta as scalars (12/3); 6√2 m/s is the magnitude of the total momentum, not divided "
        "by the total mass; 2 m/s is only one component of the final velocity.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=50, recomputed=True)

assert (0, 2 * 4, 2 * 3 ** 2 / 2, 6) == (0, 8, 9, 6)
add(T, "Newton's laws and impulse", "Intermediate", "match_list",
    match_stem("A body of mass 2 kg moves as described in List-I (SI units). Match List-I with List-II "
               "(magnitude of the net force on the body).",
               ["It moves with a constant velocity v = (3î + 4ĵ) m/s",
                "Its position along a straight line is x = 2t²",
                "It moves uniformly on a circle of radius 2 m with a speed of 3 m/s",
                "Its linear momentum along a straight line is p = 6t"],
               ["9 N", "Zero", "6 N", "8 N"]),
    match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                  [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "II", "B": "IV", "C": "III", "D": "I"}], "D"),
    "Net force from the state of motion",
    "Newton's second law: F = dp/dt = ma. Constant velocity means zero net force; in uniform circular motion the "
    "net force is mv²/r.",
    ["A: a = 0 → F = 0 (II)", "B: a = d²x/dt² = 4 m/s² → F = 8 N (IV)", "C: F = mv²/r = 2 × 9/2 = 9 N (I)",
     "D: F = dp/dt = 6 N (III)"],
    why="The wrong codes give x = 2t² the value 6 N (taking a = 2t² differentiated once) or swap the circular-"
        "motion and momentum cases.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law", seconds=70, recomputed=True)

add(T, "Newton's laws and impulse", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Newton's second law is a local relation: the force at a point at a certain instant determines the "
           "acceleration at that point at that instant, independent of the history of motion.",
        s2="A stone is dropped from the window of a train that is accelerating along a level track. Just after its "
           "release, the stone has the train's horizontal acceleration in addition to the acceleration g "
           "(neglect air resistance)."),
    sp("C"),
    "Second law as a local relation",
    "Statement I is NCERT's description of the second law. For the stone: once it leaves the hand, no horizontal "
    "force acts on it (air resistance neglected), so by this local relation its acceleration is g, vertically "
    "downward, at once. It keeps the train's horizontal velocity at the instant of release, but not the train's "
    "acceleration. So Statement II is false.",
    ["Statement I: acceleration depends only on the force at that instant → true",
     "Statement II: after release, horizontal force = 0 → horizontal acceleration = 0 → false"],
    why="Statement II confuses velocity, which the stone keeps, with acceleration, which depends only on the "
        "force acting at that instant.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=50)

cos_t = (13 ** 2 - 7 ** 2 - 8 ** 2) / (2 * 7 * 8)
assert close(cos_t, 0.5) and close(math.degrees(math.acos(cos_t)), 60)
add(T, "Equilibrium of concurrent forces", "Advanced", "numerical",
    "Three concurrent forces of magnitudes 7 N, 8 N and 13 N keep a particle in equilibrium. The angle between the "
    "directions of the 7 N and the 8 N forces is:",
    place("60°", ["120°", "90°", "30°"], "B"),
    "Equilibrium of three concurrent forces",
    "In equilibrium the 13 N force is equal and opposite to the resultant of the other two, so the resultant of the "
    "7 N and 8 N forces has magnitude 13 N. Use R² = A² + B² + 2AB cos θ.",
    ["169 = 49 + 64 + 2(7)(8) cos θ", "cos θ = 56/112 = 1/2", "θ = 60°"],
    why="120° is the interior angle of the triangle of forces (180° − 60°), not the angle between the force "
        "directions; 90° assumes the forces form a right angle; 30° results from using sin θ for cos θ.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=75, recomputed=True)

theta = math.radians(45)
mu = math.tan(theta) * (1 - 1 / 2 ** 2)
assert close(mu, 0.75)
a_s, a_r = g * math.sin(theta), g * (math.sin(theta) - mu * math.cos(theta))
assert close(math.sqrt(2 * 1 / a_r) / math.sqrt(2 * 1 / a_s), 2.0)
add(T, "Friction", "Advanced", "numerical",
    "A block takes twice as long to slide from rest down a rough plane inclined at 45° as it would take to slide "
    "the same distance from rest down a smooth plane of the same inclination. The coefficient of kinetic friction "
    "between the block and the rough plane is:",
    place("0.75", ["0.5", "0.25", "1.33"], "A"),
    "Motion on a rough incline compared with a smooth one",
    "From rest, s = ½at², so for the same distance t ∝ 1/√a. Twice the time means one quarter of the "
    "acceleration. On the rough plane a = g(sin θ − μ cos θ); on the smooth plane a = g sin θ.",
    ["t_rough/t_smooth = 2 → a_smooth/a_rough = 4", "sin θ − μ cos θ = (sin θ)/4",
     "μ = (3/4) tan θ = 0.75 at θ = 45°"],
    shortcut="μ = tan θ (1 − 1/n²) when the time is n times as long.",
    why="0.5 takes t ∝ 1/a (forgetting the square root); 0.25 writes μ = tan θ/n²; 1.33 inverts the ratio 3/4.",
    ncert="Class 11 Physics, 'Laws of Motion', friction on an inclined plane", seconds=110, recomputed=True)

add(T, "Circular motion: level and banked roads", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="When a car turns sharply to the left, a passenger sitting on the right side is pressed against the "
          "right-hand door.",
        r="The passenger's body tends to keep moving in a straight line because of inertia, so the car turns "
          "towards the left under the passenger until the door pushes on the passenger and supplies the "
          "centripetal force needed to turn."),
    ar("A"),
    "Inertia of direction and the centripetal force",
    "Seen from the ground, no force pushes the passenger outward. Her body tends to continue in its original "
    "straight line (first law); the car turns left beneath her, so the right-hand door moves into her, and the "
    "door's push towards the centre of the turn supplies the centripetal force. This is exactly why she is pressed "
    "against the door.",
    ["A: true, a familiar observation", "R: true, it is the first-law explanation", "R explains A → option A"],
    why="R is the explanation, not a separate fact, so B is wrong; both statements are true, so C and D are wrong. "
        "The common wrong idea is an outward 'centrifugal' force, which R correctly avoids.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first law of motion", seconds=50)

a_ = (20 - 0.2 * 5 * g) / 5
N12 = 3 * a_ + 0.2 * 3 * g
N_alt = 2 * a_ + 0.2 * 2 * g
assert close(a_, 2) and close(N12, 12) and close(N_alt, 8) and close(2 * a_, 4) and close(0.2 * 3 * g, 6)
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Friction", "Advanced", "multi_statement",
    multi("Blocks of masses 2 kg and 3 kg are placed in contact on a rough horizontal floor. The coefficient of "
          "kinetic friction between each block and the floor is 0.2. A horizontal force of 20 N is applied to the "
          "2 kg block, pushing both blocks along together. Take g = 10 m/s². Which of the following statements "
          "are correct?",
          ["The acceleration of the blocks is 2 m/s².",
           "The 2 kg block pushes the 3 kg block with a force of 12 N.",
           "If the same 20 N force were instead applied to the 3 kg block, pushing the blocks the other way, the "
           "contact force between them would be 8 N.",
           "The net force on the 2 kg block is 8 N.",
           "The friction force on the 3 kg block is 10 N."]),
    place("(a), (b) and (c) only", ["(a), (b) and (d) only", "(a), (c) and (e) only",
                                    "(b), (d) and (e) only"], "D"),
    "Connected bodies with friction: free-body diagrams",
    "Total friction = 0.2 × 50 = 10 N, so the common acceleration is (20 − 10)/5 = 2 m/s². The contact force on "
    "the leading block must accelerate it and overcome its own friction.",
    ["(a) a = (20 − 10)/5 = 2 m/s², true", "(b) N = 3(2) + 0.2(30) = 6 + 6 = 12 N, true",
     "(c) N' = 2(2) + 0.2(20) = 4 + 4 = 8 N, true", "(d) net force on 2 kg = 2 × 2 = 4 N, not 8 N → false",
     "(e) friction on 3 kg = 0.2 × 30 = 6 N; 10 N is the total friction on both → false"],
    why="(d) confuses the net force with the contact force on the other block; (e) uses the total friction on both "
        "blocks for one of them.",
    ncert="Class 11 Physics, 'Laws of Motion', friction and the dynamics of connected bodies", seconds=120,
    recomputed=True)
