

# ================================================================ Optics (B6 I9 A6)
ROC = NC + "'Ray Optics and Optical Instruments', "
WOC = NC + "'Wave Optics', "


def lens_v(u, f):
    """Thin lens, Cartesian convention: 1/v − 1/u = 1/f."""
    return 1 / (1 / F(f) + 1 / F(u))


def mirror_v(u, f):
    """Spherical mirror, Cartesian convention: 1/v + 1/u = 1/f."""
    return 1 / (1 / F(f) - 1 / F(u))


# ---- Basic
assert 2 * 10 == 20
q(OPT, "Mirrors", "Basic", "numerical",
  "A ray of light falls on a plane mirror. Keeping the incident ray fixed, the mirror is rotated through 10° about an "
  "axis lying in its plane and perpendicular to the plane of incidence. The reflected ray turns through:",
  *opt("20°", ["10°", "5°", "40°"], "A"),
  "Laws of reflection: angle of incidence = angle of reflection, both measured from the normal",
  "Rotating the mirror through θ rotates its normal through θ. The angle of incidence therefore changes by θ, and so "
  "does the angle of reflection; the angle between the incident and reflected rays (2i) changes by 2θ. Since the "
  "incident ray is fixed, the reflected ray turns through 2θ.",
  ["Normal turns through 10°", "i changes by 10°, so 2i changes by 20°", "Reflected ray turns through 20°"],
  why="10° is the rotation of the mirror (and of its normal), not of the reflected ray. 5° halves instead of "
      "doubling. 40° doubles twice.",
  ncert=ROC + "reflection of light by spherical mirrors (laws of reflection)", seconds=30, rc=True)

f_b = 1 / F(4) * 100          # cm
v_b = lens_v(-50, f_b)
assert f_b == 25 and v_b == 50 and v_b / -50 == -1
assert 1 / (F(4) + 2) * 100 == F(50, 3)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A thin lens has a power of +4 D. An object is placed on its principal axis 50 cm in front of it. The image is "
  "formed:",
  *opt("50 cm behind the lens; real, inverted and of the same size as the object",
       ["about 16.7 cm behind the lens; real, inverted and diminished",
        "50 cm in front of the lens; virtual, erect and of the same size",
        "25 cm behind the lens, at its focus"], "C"),
  "Power P = 1/f (f in metres); thin lens formula 1/v − 1/u = 1/f",
  "A power of +4 D means a converging lens of focal length 1/4 m = 25 cm. The object at 50 cm is at 2f, so the image "
  "is at 2f on the other side, real, inverted and of the same size.",
  ["f = 1/P = 0.25 m = 25 cm", "1/v = 1/25 + 1/(−50) = 1/50 → v = +50 cm", "m = v/u = 50/(−50) = −1"],
  why="16.7 cm adds 1/50 to 1/25 instead of subtracting (sign error for u). The virtual-image option gets the sign "
      "of v wrong. 25 cm is where the image of a very distant object would form.",
  ncert=ROC + "power of a lens; thin lens formula", seconds=40, rc=True)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "A point source of light is placed at the principal focus of a thin convex lens, on its axis. The wavefront of the "
  "light emerging from the lens is:",
  *opt("plane", ["spherical, diverging from the focus on the other side", "spherical, converging to a point",
                 "cylindrical"], "D"),
  "Wavefronts and rays: rays are normal to the wavefront",
  "Light from a point source at the focus of a convex lens emerges as a parallel beam. Rays of a parallel beam are "
  "all perpendicular to a plane, so the emerging wavefront is plane.",
  ["Source at F → emergent rays parallel to the axis", "Parallel rays ↔ plane wavefront"],
  why="A spherical wavefront (diverging or converging) would need the rays to spread out from, or meet at, a point. "
      "A cylindrical wavefront comes from a line source, not a point source.",
  ncert=WOC + "Huygens' principle", seconds=30)

q(OPT, "Optical instruments", "Basic", "assertion_reason",
  ar("The final image seen through an astronomical (refracting) telescope is inverted with respect to the object.",
     "The objective forms a real, inverted image of the distant object, and the eyepiece, acting as a simple "
     "magnifier, forms an enlarged virtual image of that intermediate image without inverting it again."),
  AR, ar_key(True, True, True),
  "Image formation in an astronomical telescope",
  "The objective, a converging lens, forms a real inverted image of the distant object at its focus. The eyepiece "
  "views this image as a magnifying glass: a simple magnifier gives an erect (non-inverted) virtual image of what it "
  "views. So the single inversion by the objective remains in the final image. R is the reason for A.",
  ["Objective: real, inverted image", "Eyepiece: virtual, erect image of that image", "Net: inverted → R explains A"],
  why="R explains A directly; it is not a separate fact about telescopes.",
  ncert=ROC + "optical instruments: telescope", seconds=40)

q(OPT, "Mirrors", "Basic", "statement_pair",
  sp("The laws of reflection hold at every point of a curved mirror, the normal at the point of incidence being "
     "along the radius of curvature through that point.",
     "The mirror formula 1/v + 1/u = 1/f applies only to concave mirrors; a convex mirror needs a different "
     "formula."),
  SP, sp_key(True, False),
  "Reflection by spherical mirrors; mirror equation with the Cartesian sign convention",
  "NCERT states that the laws of reflection are true for any reflecting surface, plane or curved; for a spherical "
  "mirror the normal is along the radius. So Statement I is true. With the Cartesian sign convention the same "
  "mirror equation applies to both concave and convex mirrors (f is negative for a concave mirror and positive for "
  "a convex one), so Statement II is false.",
  ["I: true", "II: one formula for both mirrors, with signs → false"],
  why="Statement II forgets that the sign convention lets a single equation cover both kinds of mirror.",
  ncert=ROC + "the mirror equation", seconds=35)

lam_b = 600e-9
pd4 = (2 * 4 - 1) / 2 * lam_b
close(pd4, 2.1e-6)
q(OPT, "Huygens' principle and interference", "Basic", "numerical",
  "In a Young's double-slit experiment with light of wavelength 600 nm, the path difference between the waves "
  "reaching the fourth dark fringe (counted from the central bright fringe, on one side) from the two slits is:",
  *opt("2.1 µm", ["2.4 µm", "2.7 µm", "1.8 µm"], "B"),
  "Dark fringe: path difference = (2n − 1)λ/2, n = 1, 2, 3, ...",
  "The first dark fringe has a path difference λ/2, the second 3λ/2, the third 5λ/2 and the fourth 7λ/2.",
  ["Fourth dark fringe: Δ = 7λ/2 = 3.5λ", "Δ = 3.5 × 600 nm = 2100 nm = 2.1 µm"],
  why="2.4 µm (4λ) is the path difference for the fourth bright fringe. 2.7 µm (9λ/2) is for the fifth dark "
      "fringe. 1.8 µm (3λ) is for the third bright fringe.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=35, rc=True)

# ---- Intermediate
fc = F(20)
x_obj = 40
assert fc / (fc + x_obj) == F(1, 3) and fc / 60 == F(1, 3)
v_c = mirror_v(-x_obj, fc)
assert v_c == F(40, 3) and -v_c / -x_obj == F(1, 3)
assert mirror_v(-80, -20) == F(-80, 3) and -mirror_v(-80, -20) / -80 == F(-1, 3)
q(OPT, "Mirrors", "Intermediate", "numerical",
  "A convex mirror has a radius of curvature of 40 cm. For a real object on its axis, the image formed is one-third "
  "the size of the object. The distance of the object from the mirror is:",
  *opt("40 cm", ["60 cm", "20 cm", "80 cm"], "D"),
  "Mirror equation and magnification m = −v/u = f/(f − u)",
  "With the Cartesian convention f = +20 cm for the convex mirror and u = −x. The image of a real object in a "
  "convex mirror is virtual and erect, so m = +1/3.",
  ["m = f/(f − u) = 20/(20 + x) = 1/3", "20 + x = 60 → x = 40 cm",
   "Check: 1/v = 1/20 + 1/40 → v = +13.3 cm; m = −v/u = 13.3/40 = 1/3"],
  why="60 cm uses m = f/u. 20 cm puts the object at the focal length. 80 cm treats the mirror as concave (f = −20 cm) "
      "giving a real inverted image of one-third size.",
  ncert=ROC + "the mirror equation; magnification", seconds=60, rc=True)

i_p = deg(math.asin(math.sqrt(2) * math.sin(rad(30))))
close(i_p, 45)
close(deg(math.asin(0.5 / math.sqrt(2))), 20.7, 1e-2)
q(OPT, "Prism", "Intermediate", "numerical",
  "A ray of light falls on one refracting face of a prism of refracting angle 30°, made of glass of refractive index "
  "√2, and emerges from the second refracting face along its normal. The angle of incidence on the first face is:",
  *opt("45°", ["30°", "about 21°", "60°"], "B"),
  "Refraction through a prism: r₁ + r₂ = A; Snell's law at each face",
  "The ray leaves the second face along the normal, so the angle of refraction inside at the second face is r₂ = 0. "
  "Then r₁ = A − r₂ = 30°, and Snell's law at the first face gives the angle of incidence.",
  ["r₂ = 0 → r₁ = A = 30°", "sin i = √2 sin 30° = 1/√2", "i = 45° (deviation = i + 0 − A = 15°)"],
  why="30° takes the angle inside the glass (r₁) as the angle of incidence. 'About 21°' divides by √2 instead of "
      "multiplying (sin i = sin 30°/√2). 60° is just 2A.",
  ncert=ROC + "refraction through a prism", seconds=60, rc=True)

t_s, n_s, lam_s = 6e-6, 1.5, 600e-9
N_shift = (n_s - 1) * t_s / lam_s
close(N_shift, 5)
close(n_s * t_s / lam_s, 15)
q(OPT, "Huygens' principle and interference", "Intermediate", "numerical",
  "In a Young's double-slit experiment with light of wavelength 600 nm, one of the slits is covered by a thin "
  "transparent sheet of thickness 6.0 µm and refractive index 1.5. The interference pattern on the screen shifts "
  "through:",
  *opt("5 fringes, towards the side of the covered slit",
       ["5 fringes, away from the side of the covered slit", "15 fringes, towards the side of the covered slit",
        "10 fringes, towards the side of the covered slit"], "C"),
  "Optical path: a thickness t of a medium of refractive index n adds (n − 1)t to the path compared with air",
  "Light through the covered slit gains an extra optical path (n − 1)t. The central bright fringe, where the two "
  "optical paths are equal, moves to a point that is geometrically nearer the covered slit, so the whole pattern "
  "shifts towards that side. Each fringe width of shift corresponds to a path change of one wavelength.",
  ["Extra optical path = (1.5 − 1) × 6.0 µm = 3.0 µm", "Number of fringes = 3.0 µm / 0.60 µm = 5",
   "Shift is towards the covered slit"],
  why="'Away from the covered slit' reverses the direction: the extra path through the sheet must be compensated by "
      "a shorter geometrical path from that slit. 15 fringes uses nt instead of (n − 1)t. 10 fringes uses t alone.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=75, rc=True)

thetas = [k * math.pi / 180 for k in range(0, 91)]
I_mid = [0.5 * math.cos(t) ** 2 * math.sin(t) ** 2 for t in thetas]
best = max(range(91), key=lambda k: I_mid[k])
assert best == 45 and math.isclose(I_mid[45], 1 / 8)
q(OPT, "Polarisation", "Intermediate", "numerical",
  "Unpolarised light of intensity I₀ falls on two ideal polaroids whose pass axes are crossed (at 90°), so that no "
  "light emerges. A third ideal polaroid is inserted between them, and its pass axis is turned in its own plane. "
  "The greatest intensity of light that can now emerge from the last polaroid, and the angle between the pass axes "
  "of the first and the middle polaroid when this happens, are:",
  *opt("I₀/8, at 45°", ["I₀/4, at 45°", "I₀/2, at 0°", "I₀/2, at 45°"], "D"),
  "Malus's law I = I' cos²θ; unpolarised light loses half its intensity at the first polaroid",
  "After the first polaroid the intensity is I₀/2. If the middle polaroid's axis makes θ with the first, the "
  "intensity after it is (I₀/2)cos²θ, and after the last (axis at 90° − θ to the middle one) it is "
  "(I₀/2)cos²θ sin²θ = (I₀/8) sin²2θ.",
  ["I = (I₀/2) cos²θ sin²θ = (I₀/8) sin²2θ", "Maximum when sin 2θ = 1, i.e. θ = 45°", "I_max = I₀/8"],
  why="I₀/4 forgets that unpolarised light is halved by the first polaroid. At 0° the middle polaroid is parallel "
      "to the first and crossed with the last, so nothing emerges, not I₀/2. I₀/2 at 45° ignores the losses at the "
      "second and third polaroids.",
  ncert=WOC + "polarisation", seconds=80, rc=True)

C_w = deg(math.asin(3 / 4))
close(C_w, 48.6, 1e-2)
q(OPT, "Total internal reflection", "Intermediate", "direct",
  "A fish looks up from some depth below the calm surface of a pond (refractive index of water 4/3). Light from the "
  "entire sky above the water reaches the fish's eye only from within a cone whose axis is vertical. The "
  "semi-vertical angle of this cone is about:",
  *opt("49°, the critical angle for water", ["41°, the complement of the critical angle",
                                             "37°", "90°, since light arrives from the whole sky"], "B"),
  "Refraction at a plane surface; critical angle sin C = 1/n",
  "Light from the sky enters the water at angles of incidence from 0° to almost 90° (grazing). By Snell's law the "
  "largest angle of refraction, for grazing incidence, is the critical angle C with sin C = 1/n = 3/4. So all the "
  "light from the sky reaches the fish within a cone of semi-vertical angle C ≈ 49°; outside it the fish sees light "
  "totally reflected from below the surface.",
  ["Grazing incidence (90°) → angle of refraction = C", "sin C = 3/4 → C ≈ 48.6° ≈ 49°"],
  why="41° is 90° − C, the angle measured from the surface rather than from the vertical. 37° is sin⁻¹(3/5), not "
      "related to n = 4/3. The sky is compressed into the cone by refraction; it does not fill the hemisphere as "
      "seen from under water.",
  ncert=ROC + "total internal reflection", seconds=60, rc=True)

q(OPT, "Refraction and lenses", "Intermediate", "assertion_reason",
  ar("A ray of light passing through the optical centre of a thin lens emerges without deviation.",
     "Near the optical centre the two surfaces of a thin lens are parallel to each other, so this part of the lens "
     "acts like a thin parallel-sided glass slab."),
  AR, ar_key(True, True, True),
  "The optical centre of a thin lens",
  "A parallel-sided slab does not change the direction of a ray; it only shifts it sideways, and the shift is "
  "negligible for a thin slab. At the optical centre the tangent planes to the two lens surfaces are parallel, so "
  "the lens behaves there like such a slab. R explains A.",
  ["A: ray through the optical centre is undeviated → true", "R: faces parallel near the centre → slab → true",
   "R explains A"],
  why="R is the reason for A, not an unrelated property of lenses.",
  ncert=ROC + "refraction by a lens", seconds=40)

q(OPT, "Total internal reflection", "Intermediate", "statement_pair",
  sp("Optical fibres are extensively used to transmit audio and video signals over long distances.",
     "Bundles of optical fibres used as light pipes allow doctors to examine internal organs such as the "
     "oesophagus, stomach and intestines."),
  SP, sp_key(True, True),
  "Applications of total internal reflection: optical fibres",
  "Both are uses of optical fibres described in NCERT. In each fibre, light is guided by repeated total internal "
  "reflection at the core–cladding boundary, so it can be carried round bends with little loss.",
  ["I: signal transmission → true", "II: light pipes for viewing internal organs → true"],
  why="Both statements are NCERT applications of optical fibres; neither is false.",
  ncert=ROC + "total internal reflection: optical fibres", seconds=30)

I_of = lambda frac: 4 * math.cos(math.pi * frac) ** 2      # Δ = frac × λ, I in units of I₀
close(I_of(0), 4)
close(I_of(1 / 6), 3)
close(I_of(1 / 4), 2)
assert abs(I_of(1 / 2)) < 1e-12
q(OPT, "Huygens' principle and interference", "Intermediate", "match_list",
  ml("In a Young's double-slit experiment the waves from the two slits reach the screen with equal intensities, each "
     "I₀. Match the path difference at a point of the screen (List-I) with the resultant intensity there (List-II).",
     ["0", "λ/6", "λ/4", "λ/2"],
     ["2I₀", "zero", "4I₀", "3I₀"]),
  *mlo("A-III, B-IV, C-I, D-II", ["A-III, B-I, C-IV, D-II", "A-I, B-IV, C-III, D-II", "A-III, B-II, C-I, D-IV"], "D"),
  "Resultant intensity I = 4I₀ cos²(φ/2) with phase difference φ = 2πΔ/λ",
  "A path difference Δ gives a phase difference φ = 2πΔ/λ, and for equal intensities the resultant is "
  "4I₀ cos²(φ/2) = 4I₀ cos²(πΔ/λ).",
  ["Δ = 0: 4I₀ cos² 0 = 4I₀", "Δ = λ/6: 4I₀ cos²(30°) = 3I₀", "Δ = λ/4: 4I₀ cos²(45°) = 2I₀",
   "Δ = λ/2: 4I₀ cos²(90°) = 0"],
  why="Swapping λ/6 and λ/4 confuses cos² 30° (3/4) with cos² 45° (1/2). Treating the maximum as 2I₀ adds "
      "intensities instead of amplitudes.",
  ncert=WOC + "coherent and incoherent addition of waves", seconds=70, rc=True)

truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(OPT, "Huygens' principle and interference", "Intermediate", "multi_statement",
  ms("A Young's double-slit experiment is set up in air with monochromatic light. Each of the following changes is "
     "made separately, everything else being unchanged. Which of the following statements are correct?",
     ["Moving the screen farther from the slits increases the fringe width.",
      "Using light of shorter wavelength decreases the fringe width.",
      "Increasing the separation between the slits increases the fringe width.",
      "Covering one slit completely makes the interference fringes disappear; only the broad diffraction pattern "
      "of the other slit remains.",
      "Immersing the whole apparatus in water increases the fringe width."]),
  *mso(truth, "abd", ["abc", "bde", "ade"], "C"),
  "Fringe width β = λD/d; interference needs two coherent sources",
  "β = λD/d increases with D (a true), decreases with λ (b true) and decreases as d increases (c false). In water the "
  "wavelength becomes λ/n, so β decreases (e false). With one slit covered there is only one source, so there can be "
  "no two-source interference; the single slit gives its own diffraction pattern (d true).",
  ["(a) β ∝ D → true", "(b) β ∝ λ → true", "(c) β ∝ 1/d → false", "(d) true", "(e) λ → λ/n → β decreases → false"],
  why="Options with (c) or (e) reverse the dependence of β on d or on the medium.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=70)

# ---- Advanced
f1 = F(20)                                  # equiconvex, n = 1.5, R = 20 cm
f2 = -F(20) / (F(4, 3) - 1)                 # plano-concave water lens, R = 20 cm
Fc = 1 / (1 / f1 + 1 / f2)
assert f2 == -60 and Fc == 30 and 1 / (1 / f1 + 1 / F(60)) == 15
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin equiconvex lens of glass (refractive index 1.5), each face of radius of curvature 20 cm, rests on a "
  "horizontal plane mirror. A little water (refractive index 4/3) is put between the lens and the mirror, so that it "
  "forms a thin layer bounded by the lower face of the lens and the flat mirror. Looking down along the axis, a pin "
  "held above the lens coincides with its own image (no parallax) when the pin is at a height h above the lens. The "
  "value of h is:",
  *opt("30 cm", ["15 cm", "20 cm", "60 cm"], "C"),
  "Lens maker's formula; lenses in contact; image coincides with the object when the light returns along its path",
  "The pin coincides with its image when the rays, after passing through the glass lens and the water layer, strike "
  "the mirror normally and retrace their path; that is when the pin is at the focus of the combination (glass lens + "
  "water lens). The water layer is a plano-concave lens with one face of radius 20 cm.",
  ["Glass lens: 1/f₁ = (1.5 − 1)(2/20) → f₁ = 20 cm",
   "Water lens: 1/f₂ = (4/3 − 1)(−1/20) → f₂ = −60 cm",
   "1/F = 1/20 − 1/60 = 1/30 → F = 30 cm = h"],
  why="15 cm adds the powers as if the water layer were converging. 20 cm ignores the water layer. 60 cm is the "
      "magnitude of the focal length of the water lens alone.",
  ncert=ROC + "lens maker's formula; combination of thin lenses in contact", seconds=140, rc=True)

v_near, v_far = mirror_v(-30, -20), mirror_v(-40, -20)
v_mid = mirror_v(-35, -20)
assert v_near == -60 and v_far == -40 and abs(v_near - v_far) == 20
assert (v_near / 30) ** 2 * 10 == 40 and round(float((v_mid / 35) ** 2 * 10), 1) == 17.8
q(OPT, "Mirrors", "Advanced", "numerical",
  "A thin rod 10 cm long lies along the principal axis of a concave mirror of focal length 20 cm, its nearer end "
  "being 30 cm from the pole and its farther end 40 cm from the pole. The length of the image of the rod is:",
  *opt("20 cm", ["40 cm", "10 cm", "about 17.8 cm"], "A"),
  "Mirror equation applied to each end of an extended object along the axis",
  "For an object along the axis the magnification is not the same at every point, so find the image of each end "
  "separately. The end at 40 cm (= 2f, the centre of curvature) images onto itself.",
  ["Near end: 1/v = −1/20 + 1/30 → v = −60 cm", "Far end: 1/v = −1/20 + 1/40 → v = −40 cm",
   "Image length = 60 − 40 = 20 cm"],
  why="40 cm uses m² × 10 cm with m = 2, the magnification at the near end only. 10 cm assumes the image is the same "
      "length. 17.8 cm uses m² with the magnification at the middle of the rod; that approximation is valid only for "
      "a very short object.",
  ncert=ROC + "the mirror equation", seconds=120, rc=True)

h_eye, depth, n_w = F(30), F(40), F(4, 3)
app_mirror = h_eye + depth / n_w
assert app_mirror == 60 and 2 * app_mirror == 120 and 2 * (h_eye + depth) == 140 and 2 * h_eye + depth == 100
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A tank contains water (refractive index 4/3) 40 cm deep, and a plane mirror lies flat on its bottom. A person "
  "looks vertically down at the mirror, his eye being 30 cm above the water surface. Using the near-normal "
  "(paraxial) approximation, the distance from his eye at which he sees the image of his own eye is:",
  *opt("120 cm", ["140 cm", "60 cm", "100 cm"], "B"),
  "Apparent depth (real depth/n) for near-normal viewing; image in a plane mirror",
  "Seen from the air, the mirror on the bottom appears raised to an apparent depth of 40/(4/3) = 30 cm below the "
  "surface, i.e. 60 cm below the eye. The light travels down and back up through the same water, so the eye sees "
  "itself as in a plane mirror placed at this apparent position: the image lies as far behind the apparent mirror "
  "as the eye is in front of it.",
  ["Apparent depth of mirror = 40 × 3/4 = 30 cm", "Eye to apparent mirror = 30 + 30 = 60 cm",
   "Image of eye is 60 cm behind it → 120 cm from the eye"],
  why="140 cm ignores refraction and doubles the actual distance 70 cm. 60 cm is the distance to the apparent "
      "mirror, not to the image. 100 cm applies the refraction correction to neither water path.",
  ncert=ROC + "refraction (real and apparent depth)", seconds=120, rc=True)

v1, v2 = lens_v(-30, 20), F(80)
f_conc = 1 / (1 / v2 - 1 / v1)
assert v1 == 60 and f_conc == -240
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin convex lens of focal length 20 cm forms a sharp image of an object, placed 30 cm in front of it, on a "
  "screen. A thin concave lens is now placed in contact with the convex lens, and the screen has to be moved 20 cm "
  "farther from the lenses to obtain a sharp image again (the object stays where it was). The focal length of the "
  "concave lens is:",
  *opt("−240 cm", ["−20 cm", "+240 cm", "about −34 cm"], "C"),
  "Thin lens formula; lenses in contact: 1/F = 1/f₁ + 1/f₂",
  "First the convex lens alone: the image is at v = 60 cm. With the concave lens added, the image is at 80 cm. For the "
  "same object distance, 1/v − 1/u = 1/F, so the change in 1/v equals the power added by the concave lens.",
  ["Convex lens alone: 1/v = 1/20 − 1/30 → v = 60 cm", "Combination: v' = 80 cm",
   "1/f₂ = 1/v' − 1/v = 1/80 − 1/60 = −1/240 → f₂ = −240 cm"],
  why="−20 cm takes the shift of the screen as the focal length. +240 cm gets the sign wrong; adding a converging lens "
      "would bring the image closer. About −34 cm adds 1/80 and 1/60.",
  ncert=ROC + "combination of thin lenses in contact", seconds=110, rc=True)

nn = math.sqrt(3)
ib = deg(math.atan(nn))
close(ib, 60)
close(90 - ib, 30)
close(deg(math.asin(1 / nn)), 35.26)
close((nn - 1) * 6, 4.39)
q(OPT, "Polarisation", "Advanced", "match_list",
  ml("A transparent material has refractive index √3 (about 1.73) and is used in air. Match each quantity in List-I "
     "with its value in List-II.",
     ["Angle of incidence (in air) at which the reflected light is completely plane polarised",
      "Angle of refraction (in the material) for light incident at that angle",
      "Critical angle for light going from the material into air",
      "Deviation produced by a thin prism of this material with a refracting angle of 6°"],
     ["30°", "60°", "about 35°", "about 4.4°"]),
  *mlo("A-II, B-I, C-III, D-IV", ["A-I, B-II, C-III, D-IV", "A-II, B-I, C-IV, D-III", "A-III, B-I, C-II, D-IV"], "B"),
  "Brewster's law tan i_B = n; reflected and refracted rays perpendicular at i_B; sin C = 1/n; thin prism δ = (n − 1)A",
  "tan i_B = √3 gives i_B = 60°. At Brewster's angle the reflected and refracted rays are perpendicular, so the "
  "angle of refraction is 90° − 60° = 30°. sin C = 1/√3 gives C ≈ 35.3°. A thin prism deviates light by "
  "(n − 1)A = 0.732 × 6° ≈ 4.4°.",
  ["A → 60° (II)", "B → 30° (I)", "C → about 35° (III)", "D → about 4.4° (IV)"],
  why="Swapping A and B confuses the Brewster angle with the refraction angle. The other codes mix up the critical "
      "angle with the prism deviation.",
  ncert=WOC + "polarisation by reflection; " + "Ray Optics: critical angle, refraction through a prism", seconds=100,
  rc=True)

us = [-60, -40, -30]
vs = [lens_v(u, 20) for u in us]
ms_ = [v / u for v, u in zip(vs, us)]
assert vs == [30, 40, 60] and ms_ == [F(-1, 2), -1, -2]
assert (ms_[0] ** 2 < 1) and (ms_[2] ** 2 > 1)          # image slower at 60 cm, faster at 30 cm
truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(OPT, "Refraction and lenses", "Advanced", "multi_statement",
  ms("An object is moved steadily along the principal axis of a thin convex lens of focal length 20 cm, from a "
     "distance of 60 cm to a distance of 30 cm from the lens. During this motion, which of the following statements "
     "are correct?",
     ["The image moves away from the lens, from 30 cm to 60 cm behind it.",
      "The image grows from half the size of the object to twice its size.",
      "The image stays real and inverted.",
      "Throughout the motion, the image moves more slowly than the object.",
      "When the object is 40 cm from the lens, the image is of the same size as the object."]),
  *mso(truth, "abce", ["abcd", "ace", "bcde"], "A"),
  "Thin lens formula; magnification; speed of the image along the axis = m² × speed of the object",
  "With f = 20 cm: u = −60 gives v = 30 cm (m = −½), u = −40 gives v = 40 cm (m = −1) and u = −30 gives v = 60 cm "
  "(m = −2). The object stays beyond f, so the image is real and inverted throughout. Differentiating the lens "
  "formula gives (image speed) = m² × (object speed): slower than the object while |m| < 1 (object beyond 2f) but "
  "faster once |m| > 1 (object between f and 2f), so (d) is false.",
  ["(a) v: 30 → 60 cm → true", "(b) |m|: ½ → 2 → true", "(c) object beyond f → real, inverted → true",
   "(d) speed ratio m²: ¼ → 4 → false", "(e) u = 2f → |m| = 1 → true"],
  why="Options with (d) ignore that the image speeds up once the magnification exceeds 1; the options leaving out "
      "(a) or (b) miss changes that follow directly from the lens formula.",
  ncert=ROC + "thin lens formula; magnification", seconds=110, rc=True)
