"""Stage 1: base meshes and proportions for Tobi and Amara.

Bodies and clothes are grown from joint graphs with the Skin modifier (clean quad tubes), then one
level of subdivision. Heads are shaped quad-spheres; eyes, brows and mouth are separate small meshes
(face rig shape keys are added in stage 3); hair, outfit and props are separate, clearly named meshes.
Output: blender/work/stage1.blend
"""
import sys, pathlib, math, random
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *
from mathutils.bvhtree import BVHTree

def skin_object(name, coll, nodes, edges, root=0, subsurf=1, smooth=0.25):
    """nodes: list of (pos, (rx, ry)); edges: index pairs. Returns an applied quad mesh object."""
    me = bpy.data.meshes.new(name + "_src"); me.from_pydata([n[0] for n in nodes], edges, [])
    o = new_obj(name + "_src", me, coll)
    sk = o.modifiers.new("skin", "SKIN"); sk.branch_smoothing = smooth; sk.use_smooth_shade = True
    # every connected piece needs its own root, or the Skin modifier skips it
    parent = list(range(len(nodes)))
    def find(i):
        while parent[i] != i: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for a, b in edges: parent[find(a)] = find(b)
    roots = {}
    for i in [root] + list(range(len(nodes))): roots.setdefault(find(i), i)
    for i, (p, r) in enumerate(nodes):
        d = me.skin_vertices[0].data[i]; d.radius = r; d.use_root = i in roots.values()
    if subsurf:
        ss = o.modifiers.new("ss", "SUBSURF"); ss.levels = ss.render_levels = subsurf
    dg = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(dg)
    out = bpy.data.meshes.new_from_object(ev); out.name = name
    bpy.data.objects.remove(o); bpy.data.meshes.remove(me)
    ob = new_obj(name, out, coll)
    for p in ob.data.polygons: p.use_smooth = True
    return ob

class Graph:
    def __init__(self): self.nodes, self.edges, self.idx = [], [], {}
    def add(self, key, pos, r):
        self.idx[key] = len(self.nodes); self.nodes.append((tuple(pos), r)); return self
    def link(self, *keys):
        for a, b in zip(keys, keys[1:]): self.edges.append((self.idx[a], self.idx[b]))
        return self

def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

def body_graph(name):
    c = CHARS[name]; J = joints(name); k = c["height"] / 1.8; t = c["torso"]; a = c["arm"]
    g = Graph(); R = lambda x, y=None: (x * k, (y if y is not None else x) * k)
    g.add("pelvis", J["pelvis"], R(0.115 * (1.06 if name == "amara" else 1), 0.088))
    g.add("spine1", J["spine1"], R(0.118 * t, 0.086)).add("spine2", J["spine2"], R(0.124 * t, 0.088))
    g.add("spine3", J["spine3"], R(0.140 * t, 0.092)).add("neck", J["neck"], R(0.048)).add("head", J["head"], R(0.044))
    g.link("pelvis", "spine1", "spine2", "spine3", "neck", "head")
    for s, f in (("L", lambda p: p), ("R", mirror)):
        g.add("clav" + s, f(J["clav"]), R(0.052)).add("sh" + s, f(J["shoulder"]), R(0.050 * a))
        g.add("el" + s, f(J["elbow"]), R(0.039 * a)).add("wr" + s, f(J["wrist"]), R(0.029 * a, 0.024 * a))
        g.add("palm" + s, f(J["palm"]), R(0.031 * a, 0.015 * a))
        g.link("neck", "clav" + s, "sh" + s, "el" + s, "wr" + s, "palm" + s)
        for fg in ("thumb", "index", "middle", "ring", "pinky"):
            rr = 0.0095 if fg == "thumb" else (0.0072 if fg == "pinky" else 0.0082)
            for i in range(4):
                g.add(f"{fg}{i}{s}", f(J[f"{fg}_{i}"]), R(rr * a * (1 - 0.12 * i)))
            g.link("wr" + s if fg == "thumb" else "palm" + s, *[f"{fg}{i}{s}" for i in range(4)])
        g.add("hip" + s, f(J["hipj"]), R(0.062 * (1.05 if name == "amara" else 1)))
        g.add("knee" + s, f(J["knee"]), R(0.050)).add("ankle" + s, f(J["ankle"]), R(0.034))
        g.add("ball" + s, f(J["ball"]), R(0.036, 0.020)).add("toe" + s, f(J["toe"]), R(0.030, 0.016))
        g.link("pelvis", "hip" + s, "knee" + s, "ankle" + s, "ball" + s, "toe" + s)
    return g

def outfit_graphs(name):
    """Shirt, trousers and shoes as skin graphs; returns list of (graph, material keys, part)."""
    c = CHARS[name]; J = joints(name); H = c["height"]; k = H / 1.8; t = c["torso"]
    R = lambda x, y=None: (x * k, (y if y is not None else x) * k)
    parts = []
    # shirt
    g = Graph()
    if name == "tobi":   # oversized tee, sleeves to just above the elbow
        g.add("hem", (0, 0.005, 0.458 * H), R(0.205, 0.128)).add("pelvis", J["pelvis"], R(0.188, 0.124))
        g.add("s1", J["spine1"], R(0.160, 0.118)).add("s2", J["spine2"], R(0.166, 0.120)).add("s3", J["spine3"], R(0.178, 0.122))
        g.add("collar", (0, -0.002, 0.762 * H), R(0.062)).link("hem", "pelvis", "s1", "s2", "s3", "collar")
        for s, f in (("L", lambda p: p), ("R", mirror)):
            g.add("cl" + s, f(J["clav"]), R(0.072)).add("sh" + s, f(J["shoulder"]), R(0.074))
            g.add("sl" + s, f(lerp(J["shoulder"], J["elbow"], 0.78)), R(0.060)).link("collar", "cl" + s, "sh" + s, "sl" + s)
    else:                # button-up shirt, sleeves to the wrist with a rolled cuff
        g.add("hem", (0, 0.005, 0.466 * H), R(0.200, 0.126)).add("pelvis", J["pelvis"], R(0.172, 0.118))
        g.add("s1", J["spine1"], R(0.134 * t / 0.9, 0.102)).add("s2", J["spine2"], R(0.140 * t / 0.9, 0.104)).add("s3", J["spine3"], R(0.150 * t / 0.9, 0.104))
        g.add("collar", (0, -0.002, 0.768 * H), R(0.060)).link("hem", "pelvis", "s1", "s2", "s3", "collar")
        for s, f in (("L", lambda p: p), ("R", mirror)):
            g.add("cl" + s, f(J["clav"]), R(0.060)).add("sh" + s, f(J["shoulder"]), R(0.056))
            g.add("el" + s, f(J["elbow"]), R(0.044)).add("cf" + s, f(lerp(J["elbow"], J["wrist"], 0.80)), R(0.042))
            g.link("collar", "cl" + s, "sh" + s, "el" + s, "cf" + s)
    parts.append((g, "shirt"))
    # trousers
    g = Graph(); wide = 1.0 if name == "tobi" else 1.06
    g.add("waist", (0, 0.004, 0.552 * H), R(0.156 if name == "tobi" else 0.164, 0.116)).add("pelvis", J["pelvis"], R(0.168, 0.122))
    g.link("waist", "pelvis")
    for s, f in (("L", lambda p: p), ("R", mirror)):
        g.add("hip" + s, f(J["hipj"]), R(0.104 * wide)).add("knee" + s, f(J["knee"]), R(0.078 * wide))
        hem = lerp(J["ankle"], J["knee"], 0.10 if name == "tobi" else 0.07)
        g.add("hem" + s, f(hem), R(0.072 if name == "tobi" else 0.078)).link("pelvis", "hip" + s, "knee" + s, "hem" + s)
    parts.append((g, "trousers"))
    # shoes
    g = Graph()
    for s, f in (("L", lambda p: p), ("R", mirror)):
        x = J["ankle"][0]
        if name == "tobi":   # chunky white sneakers
            g.add("a" + s, f((x, 0.018, 0.058)), R(0.052, 0.050)).add("b" + s, f((x, -0.095, 0.036)), R(0.056, 0.036))
            g.add("t" + s, f((x, -0.158, 0.034)), R(0.046, 0.032))
        else:                # dark flats
            g.add("a" + s, f((x, 0.014, 0.034)), R(0.040, 0.028)).add("b" + s, f((x, -0.086, 0.024)), R(0.042, 0.022))
            g.add("t" + s, f((x, -0.140, 0.022)), R(0.034, 0.020))
        g.link("a" + s, "b" + s, "t" + s)
    parts.append((g, "shoes"))
    return parts

def quad_sphere(cuts=7):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=2.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=cuts, use_grid_fill=True)
    for v in bm.verts: v.co = v.co.normalized()
    return bm

def head_mesh(name):
    c = CHARS[name]; hd = c["head"]; w, d, h, jaw = hd["w"], hd["d"], hd["h"], hd["jaw"]
    bm = quad_sphere(9)   # 9 cuts: smoother skull silhouette, keeps each character inside the 8k-15k triangle target
    for v in bm.verts:
        x, y, z = v.co
        sx = 1 - jaw * max(0, -z) ** 1.6          # narrower jaw
        sy = 1 - 0.18 * max(0, -z) ** 2           # chin a little forward but slimmer
        v.co = Vector((x * w / 2 * sx, y * d / 2 * sy, z * h / 2))
        if y < -0.8 and abs(x) < 0.16 and -0.25 < z < 0.08:   # nose bump
            v.co.y -= 0.012 * (1 - abs(x) / 0.16) * (1 - abs(z + 0.08) / 0.17)
        if z < -0.55 and y < -0.3:                # chin
            v.co.y -= 0.01 * (-(z + 0.55) / 0.45)
    # ears
    for s in (1, -1):
        e = quad_sphere(2)
        for v in e.verts: v.co = Vector((v.co.x * 0.014 + s * w / 2 * 0.97, v.co.y * 0.026 + 0.004, v.co.z * 0.040 - 0.004))
        tmp = bpy.data.meshes.new("tmp"); e.to_mesh(tmp); e.free(); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
    return bm

def head_center(name):
    c = CHARS[name]; J = joints(name); return Vector(J["head"]) + Vector((0, -0.006, c["head"]["h"] * 0.47))

def surface_y(bvh, x, z, y_front=-1.0):
    hit = bvh.ray_cast(Vector((x, y_front, z)), Vector((0, 1, 0)))
    return hit[0].y if hit[0] else None

def build(name, coll):
    c = CHARS[name]; H = c["height"]; J = joints(name); out = {}
    g = body_graph(name); body = skin_object(f"{name}_body", coll, g.nodes, g.edges, root=g.idx["pelvis"])
    set_mats(body, [c["skin"]]); out["body"] = body
    # head
    bm = head_mesh(name); hc = head_center(name)
    for v in bm.verts: v.co += hc
    head = from_bmesh(f"{name}_head", bm, coll); set_mats(head, [c["skin"]])
    for p in head.data.polygons: p.use_smooth = True
    out["head"] = head
    hbvh = BVHTree.FromObject(head, bpy.context.evaluated_depsgraph_get())
    hd = c["head"]
    # eyes (white + iris), brows, mouth: separate meshes placed on the face surface
    ex, ez = 0.043 * hd["w"] / 0.18, hc.z + 0.004
    bm = bmesh.new()
    for s in (1, -1):
        sy = surface_y(hbvh, s * ex, ez)
        w_ = quad_sphere(3)
        for v in w_.verts: v.co = Vector((v.co.x * 0.018 + s * ex, v.co.y * 0.0085 + sy, v.co.z * 0.021 + ez))
        tmp = bpy.data.meshes.new("t"); w_.to_mesh(tmp); w_.free(); n0 = len(bm.faces); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
        bm.faces.ensure_lookup_table()
        for f in bm.faces[n0:]: f.material_index = 0
        ir = bmesh.ops.create_circle(bm, cap_ends=True, segments=12, radius=0.0105)
        for v in ir["verts"]:
            v.co = Vector((v.co.x + s * ex + s * -0.002, sy - 0.0098, v.co.y * 1.1 + ez - 0.001))
        for f in {f for v in ir["verts"] for f in v.link_faces}:
            f.material_index = 1
            if f.normal.y > 0: f.normal_flip()
    for f in bm.faces: f.material_index = 1 if len(f.verts) > 4 else 0   # irises are the 12-sided discs
    eyes = from_bmesh(f"{name}_eyes", bm, coll, ["eye_white", "iris"]); out["eyes"] = eyes
    bm = bmesh.new()
    for s in (1, -1):
        r = bmesh.ops.create_cube(bm, size=1.0)
        for v in r["verts"]:
            x0 = v.co.x * 0.036 + s * ex; zz = ez + 0.036 + 0.006 * (1 - (abs(v.co.x * 2)) ** 2) * (1 if name == "amara" else 0.6)
            sy = surface_y(hbvh, x0, zz) or (hc.y - hd["d"] / 2)
            v.co = Vector((x0, sy - 0.003 + v.co.y * 0.006, zz + v.co.z * (0.0085 if name == "tobi" else 0.0065)))
    brows = from_bmesh(f"{name}_brows", bm, coll, ["brow"]); out["brows"] = brows
    # mouth: a lens-shaped grid hugging the face (neutral: closed, slight smile)
    bm = bmesh.new(); nx, mw, mz = 9, 0.054 if name == "tobi" else 0.046, hc.z - 0.066 * hd["h"] / 0.245
    rows = []
    for j in range(3):
        row = []
        for i in range(nx):
            u = i / (nx - 1) * 2 - 1; th = 0.0035 * (1 - u * u)
            zz = mz + (j - 1) * th + 0.006 * u * u
            xx = u * mw / 2; sy = surface_y(hbvh, xx, zz)
            row.append(bm.verts.new((xx, sy - 0.0025, zz)))
        rows.append(row)
    for j in range(2):
        for i in range(nx - 1):
            bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
    mouth = from_bmesh(f"{name}_mouth", bm, coll, ["mouth" if name == "tobi" else "lip_amara"]); out["mouth"] = mouth
    # hair: a cap over the skull plus character detail
    bm = head_mesh(name)
    for f in list(bm.faces):
        cz = sum((v.co.z for v in f.verts)) / len(f.verts); cy = sum((v.co.y for v in f.verts)) / len(f.verts)
        cx = sum((v.co.x for v in f.verts)) / len(f.verts)
        line = 0.05 if cy < -0.03 else -0.04   # higher hairline at the front
        if name == "amara" and cy < -0.03: line = 0.062
        if abs(cx) > hd["w"] / 2 * 0.9 and abs(cz) < 0.03: line = 10  # keep ears clear
        if cz < line: bm.faces.remove(f)
    for v in list(bm.verts):
        if not v.link_faces: bm.verts.remove(v)
    for v in bm.verts: v.co = v.co * 1.055 + hc
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.012)
    rnd = random.Random(1 if name == "tobi" else 2)
    if name == "tobi":   # short twists
        for i in range(26):
            ph = math.acos(1 - rnd.random() * 0.75); th = rnd.random() * math.tau
            n = Vector((math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th), math.cos(ph)))
            if n.y < -0.55: continue
            base = hc + Vector((n.x * hd["w"] / 2 * 1.05, n.y * hd["d"] / 2 * 1.05, n.z * hd["h"] / 2 * 1.05))
            r = bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.012, radius2=0.006, depth=0.055 + rnd.random() * 0.03)
            m = (n + Vector((rnd.uniform(-.3, .3), rnd.uniform(-.2, .3), 0))).normalized().to_track_quat("Z", "Y").to_matrix().to_4x4()
            for v in r["verts"]: v.co = base + (m @ (v.co + Vector((0, 0, 0.025))))
    else:                # bun at the back, low on her right, and braid ridges
        bun = hc + Vector((-0.035, hd["d"] / 2 * 0.95, -0.025))
        b = quad_sphere(3)
        for v in b.verts: v.co = bun + Vector((v.co.x * 0.062, v.co.y * 0.055, v.co.z * 0.058))
        tmp = bpy.data.meshes.new("t"); b.to_mesh(tmp); b.free(); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
    hair = from_bmesh(f"{name}_hair", bm, coll, ["hair"])
    for p in hair.data.polygons: p.use_smooth = True
    out["hair"] = hair
    # outfit: shirt + trousers + shoes in one mesh, with material slots
    objs = []
    for gr, part in outfit_graphs(name):
        objs.append((skin_object(f"{name}_{part}", coll, gr.nodes, gr.edges, root=0), part))
    keys = {"tobi": ["lime", "trouser_tobi", "white", "sole", "charcoal"], "amara": ["offwhite", "olive", "ink", "ink", "ink"]}[name]
    bm = bmesh.new()
    for o, part in objs:
        n0 = len(bm.faces); bm.from_mesh(o.data); bm.faces.ensure_lookup_table()
        for f in bm.faces[n0:]:
            ctr = f.calc_center_median(); nrm = f.normal
            if part == "shirt":
                f.material_index = 0
                if name == "amara" and nrm.y < -0.3 and abs(ctr.x) < 0.032 and 0.60 * H < ctr.z < 0.77 * H: f.material_index = 4  # dark tee showing
            elif part == "trousers": f.material_index = 1
            else: f.material_index = 3 if nrm.z < -0.55 or ctr.z < 0.012 else 2
        bpy.data.objects.remove(o)
    outfit = from_bmesh(f"{name}_outfit", bm, coll, keys)
    for p in outfit.data.polygons: p.use_smooth = True
    out["outfit"] = outfit
    obvh = BVHTree.FromObject(outfit, bpy.context.evaluated_depsgraph_get())
    # delete body faces that sit fully inside the clothes: fewer triangles, nothing poking through
    bm = bmesh.new(); bm.from_mesh(body.data); gone = []
    for f in bm.faces:
        inside = True
        for v in f.verts:
            loc, nrm, _, dist = obvh.find_nearest(v.co)
            if loc is None or (v.co - loc).dot(nrm) > -0.006: inside = False; break
        if inside: gone.append(f)
    bmesh.ops.delete(bm, geom=gone, context="FACES"); bm.to_mesh(body.data); bm.free()
    # props
    def add_box(bm, size, center, rot=None, bevel=0.0):
        r = bmesh.ops.create_cube(bm, size=1.0)
        for v in r["verts"]:
            p = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
            if rot: p = rot @ p
            v.co = p + Vector(center)
        return r
    pin_z = 0.705 * H; px = 0.055 if name == "tobi" else 0.062
    py = surface_y(obvh, px, pin_z) or -0.12
    bm = bmesh.new(); leaf = quad_sphere(2)
    for v in leaf.verts: v.co = Vector((v.co.x * 0.013 + px, v.co.y * 0.004 + py - 0.004, v.co.z * 0.021 + pin_z))
    tmp = bpy.data.meshes.new("t"); leaf.to_mesh(tmp); leaf.free(); bm.from_mesh(tmp); bpy.data.meshes.remove(tmp)
    pin = from_bmesh(f"{name}_pin", bm, coll, ["leaf"]); out["pin"] = pin
    if name == "tobi":
        # bandana: elliptical band round the forehead, with a knot and tails at the back
        bm = bmesh.new(); seg = 32; rows = []
        for j in range(4):
            row = []
            for i in range(seg):
                a = i / seg * math.tau; zz = hc.z + hd["h"] * 0.20 + (j - 1.5) * 0.013 + 0.012 * math.cos(a) * -0.6
                rr = 1.075 + 0.012 * (1 - abs(j - 1.5) / 1.5)
                row.append(bm.verts.new((hc.x + math.sin(a) * hd["w"] / 2 * rr, hc.y - math.cos(a) * hd["d"] / 2 * rr, zz)))
            rows.append(row)
        for j in range(3):
            for i in range(seg):
                bm.faces.new((rows[j][i], rows[j][(i + 1) % seg], rows[j + 1][(i + 1) % seg], rows[j + 1][i]))
        bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.006)
        knot = hc + Vector((0.055, hd["d"] / 2 * 1.02, hd["h"] * 0.18))
        add_box(bm, (0.03, 0.025, 0.03), knot)
        for k2, ang in ((0, 0.5), (1, -0.2)):
            rot = Matrix.Rotation(ang, 3, "Y") @ Matrix.Rotation(0.6, 3, "X")
            add_box(bm, (0.032, 0.008, 0.07), knot + Vector((0.015 * k2, 0.02, -0.045)), rot)
        band = from_bmesh("tobi_bandana", bm, coll, ["lime"]); out["bandana"] = band
        # phone in the right hand, bag at the left hip, strap from the right shoulder
        palm = Vector(mirror(J["palm"])); armdir = (Vector(mirror(J["palm"])) - Vector(mirror(J["wrist"]))).normalized()
        rot = armdir.to_track_quat("Z", "Y").to_matrix()
        bm = bmesh.new(); add_box(bm, (0.075, 0.009, 0.15), palm + Vector((0.0, -0.025, 0.0)), rot)
        phone = from_bmesh("tobi_phone", bm, coll, ["ink"]); out["phone"] = phone
        bagc = Vector((0.13, (surface_y(obvh, 0.13, 0.565 * H) or -0.12) - 0.035, 0.565 * H))
        bm = bmesh.new(); add_box(bm, (0.20, 0.07, 0.115), bagc, Matrix.Rotation(-0.25, 3, "Y"))
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=0.02, segments=2, affect="EDGES")
        pts = [Vector((-0.12, 0.02, 0.795 * H)), Vector((-0.09, -0.08, 0.77 * H))]
        for t0 in (0.25, 0.5, 0.75):
            x0 = -0.08 + (0.20) * t0; z0 = 0.75 * H - (0.75 * H - 0.6 * H) * t0
            pts.append(Vector((x0, (surface_y(obvh, x0, z0) or -0.12) - 0.008, z0)))
        pts.append(bagc + Vector((-0.08, 0, 0.05)))
        # strap as a flat tube along the points
        prev = None
        for i in range(len(pts) - 1):
            a0, b0 = pts[i], pts[i + 1]; dvec = (b0 - a0); L = dvec.length
            rot = dvec.normalized().to_track_quat("Z", "Y").to_matrix()
            add_box(bm, (0.032, 0.006, L + 0.01), (a0 + b0) / 2, rot)
        bag = from_bmesh("tobi_bag", bm, coll, ["ink"]); out["bag"] = bag
    else:
        # round glasses
        bm = bmesh.new(); gy = None
        for s in (1, -1):
            sy = surface_y(hbvh, s * ex, ez) - 0.016; gy = sy
            r = bmesh.ops.create_circle(bm, cap_ends=False, segments=16, radius=0.031)
            ring = r["verts"]
            outer = [bm.verts.new((v.co.x * 1.0 + s * ex, sy, v.co.y + ez)) for v in ring]
            inner = [bm.verts.new((v.co.x * 0.86 + s * ex, sy, v.co.y * 0.86 + ez)) for v in ring]
            for v in ring: bm.verts.remove(v)
            for i in range(16):
                bm.faces.new((outer[i], outer[(i + 1) % 16], inner[(i + 1) % 16], inner[i]))
            add_box(bm, (0.004, (hd["d"] * 0.55), 0.005), (s * (ex + 0.031), sy + hd["d"] * 0.27, ez + 0.006))
        add_box(bm, (0.026, 0.004, 0.004), (0, gy, ez + 0.012))
        bmesh.ops.solidify(bm, geom=[f for f in bm.faces if len(f.verts) == 4 and abs(f.normal.y) > 0.9], thickness=0.004)
        glasses = from_bmesh("amara_glasses", bm, coll, ["ink"]); out["glasses"] = glasses
        # lanyard: a lime band from the neck to a V on the chest
        bm = bmesh.new()
        tip = Vector((0.0, (surface_y(obvh, 0.0, 0.625 * H) or -0.11) - 0.006, 0.625 * H))
        for s in (1, -1):
            pts = [Vector((s * 0.052, 0.01, 0.775 * H)), Vector((s * 0.058, -0.06, 0.755 * H))]
            for t0 in (0.35, 0.7):
                x0 = s * 0.05 * (1 - t0); z0 = 0.74 * H - (0.74 * H - 0.625 * H) * t0
                pts.append(Vector((x0, (surface_y(obvh, x0, z0) or -0.11) - 0.006, z0)))
            pts.append(tip)
            for i in range(len(pts) - 1):
                a0, b0 = pts[i], pts[i + 1]; dvec = b0 - a0
                add_box(bm, (0.012, 0.003, dvec.length + 0.006), (a0 + b0) / 2, dvec.normalized().to_track_quat("Z", "Y").to_matrix())
        lan = from_bmesh("amara_lanyard", bm, coll, ["lime"]); out["lanyard"] = lan
        # tablet in the left hand
        palm = Vector(J["palm"]); armdir = (Vector(J["palm"]) - Vector(J["wrist"])).normalized()
        rot = armdir.to_track_quat("Z", "Y").to_matrix() @ Matrix.Rotation(math.radians(90), 3, "Z")
        bm = bmesh.new(); add_box(bm, (0.20, 0.010, 0.145), palm + Vector((0.035, -0.035, 0.03)), rot)
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=0.006, segments=1, affect="EDGES")
        bm.faces.ensure_lookup_table()
        for f in bm.faces:
            f.material_index = 1 if (f.normal.y < -0.9 and f.calc_area() > 0.015) else 0
        tab = from_bmesh("amara_tablet", bm, coll, ["ink", "screen"]); out["tablet"] = tab
    return out

def main():
    sc = reset(); report = {}
    for name in ("tobi", "amara"):
        coll = bpy.data.collections.new(name.capitalize()); sc.collection.children.link(coll)
        grp = bpy.data.objects.new(f"{name}_grp", None); coll.objects.link(grp)
        parts = build(name, coll)
        for o in parts.values(): o.parent = grp
        grp.location.x = CHARS[name]["offset_x"]
        report[name] = {k: tri_count(o) for k, o in parts.items()}
        report[name]["TOTAL"] = sum(report[name].values())
    save(WORK / "stage1.blend")
    for n, r in report.items(): print(n, r)

if __name__ == "__main__":
    main()
