/* Interactive part viewer for the CAD downloads page (fabrication/cad-downloads.md).
 *
 * <model-viewer id="dh-viewer"> (Google model-viewer 3.5) shows assets/viewer/robot.glb:
 * one mesh per occurrence of every component of the Fusion model, in the Fusion appearance
 * colours, each with its own glTF material. Material names are the mesh ids:
 *   "<part_id>#<n>"          a part with a site part_id (machined or printed)
 *   "vendor:<file_name>#<n>" a purchased part, <file_name> as in tree.csv
 *   "context"                optional grey backdrop (older scenes), never selectable
 *
 * assets/viewer/parts.json (tools/build_viewer.py) is read at run time:
 *   parts:   { part_id:   [ {node, path, center:[x,y,z] m, radius m}, ... ] }
 *   vendor:  { file_name: [ {node, path, center, radius}, ... ] }
 *            (an object with a `meshes` list plus name/appearance/material/mass_g/bbox is accepted too)
 *   info:    { part_id: {desc, kind, qty, material, mass_g, bbox:[x,y,z]},
 *              "vendor:<file_name>": {name, appearance, material, mass_g, bbox} }
 *   axes:    { x:[x,y,z], y:[...], z:[...] }   arrow tips, metres, glTF (model-viewer) frame
 *   modules: { file_name: {name, path, depth, qty, mass_g, children} }  or a list with `file`
 * A mesh belongs to a module when its `path` equals the module path or starts with it + "+".
 * Optional, from tools/ (the data lane):
 *   assets/viewer/vendor-map.json  { file_name: {part_id, bom_file, description, qty_in_model, via} }
 *            (page, mpn, vendor, vendor_url are shown when a map carries them)
 *   assets/viewer/downloads.json   { part_id_or_file_name: [ {label, href}, ... ] }  hrefs docs-root relative
 *
 *   Preview button / click or Enter on a row  -> the target turns red, the camera frames it
 *   Download button                           -> the file downloads (the row also previews)
 *   hover or focus a row                      -> the target turns amber
 *   click a component on the model            -> info box (facts, module chain, downloads),
 *                                                the page scrolls to its row when it has one
 * Every other colour is the material's own baseColorFactor, remembered at load and restored.
 *
 * model-viewer 3.5 API used (packages/model-viewer/src/features/scene-graph.ts,
 * scene-graph/material.ts, scene-graph/pbr-metallic-roughness.ts, annotation.ts, controls.ts):
 *   mv.loaded, mv.model.materials[].name          name = glTF material name
 *   material.pbrMetallicRoughness.baseColorFactor  [r, g, b, a], linear (copied as the original)
 *   material.pbrMetallicRoughness.setBaseColorFactor("#rrggbb" | [r, g, b, a])
 *       a CSS string is converted sRGB -> linear; an array is taken as linear, so the
 *       remembered array restores the exact original
 *   mv.materialFromPoint(clientX, clientY)        Material | null; null before load
 *   mv.positionAndNormalFromPoint(clientX, clientY)   {position: {x, y, z}} | null
 *   mv.getCameraOrbit() -> {theta, phi, radius}   radians, radians, metres
 *   mv.cameraTarget = "Xm Ym Zm" | "auto auto auto";  mv.cameraOrbit = "Arad Brad Rm"
 *   mv.updateHotspot({name, position})            moves a <button slot="hotspot-…"> child
 *   material.setAlphaMode("BLEND" | "OPAQUE")     fallback only, see below
 *
 * The public scene graph exposes materials only, so hiding a part and the x-ray ghost go
 * through the three.js scene behind the element. Checked in the 3.5.0 bundle
 * (cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.js, line numbers from it;
 * the site loads model-viewer.min.js, which keeps Symbol("scene") and every name used here):
 *   mv[Symbol("scene")]      own property of the element, `this[$scene] = new ModelScene(…)`
 *                            in the constructor (l. 60339 `const $scene = Symbol('scene')`,
 *                            l. 60438); ModelScene extends the three.js Scene (l. 59340)
 *   scene.queueRender()      l. 59414, marks the scene dirty; the renderer's animation loop
 *                            (l. 56533) draws the next frame — called after every change here
 *   scene.hitFromPoint()     l. 59989: raycaster.intersectObject(scene, true), then the first
 *                            hit with `hit.object.visible && !hit.object.userData.noHit`;
 *                            mv.materialFromPoint (l. 58669) and positionAndNormalFromPoint
 *                            (l. 60000) are built on it
 *   three.js intersect()     l. 38817: an object is raycast only when
 *                            `object.layers.test(raycaster.layers)`, both masks layer 0
 * Hiding therefore sets `mesh.layers.set(1)` (the camera draws layer 0 only, and the raycaster
 * tests layer 0 only, so a hidden mesh is neither drawn nor picked: a click where it was selects
 * the part behind it) plus `mesh.visible = false`, which the hitFromPoint filter honours as well.
 * Restoring is layers.set(0) and visible = true.
 * Meshes are matched by MATERIAL name, not by object name: GLTFLoader renames nodes and meshes
 * (PropertyBinding.sanitizeNodeName drops "[ ] . : /", l. 36673, and numbers duplicates, l. 44082),
 * while the material keeps the glTF name as written (l. 44067). tools/glb_tools.py gives node,
 * mesh and material of an occurrence the same name, so material.name is the mesh id.
 * X-ray ghost of the selection: one clone per selected mesh (mesh.clone() shares the geometry)
 * with its own cloned material — color RED, transparent = true, opacity GHOST_ALPHA,
 * depthWrite = false, depthTest = true, depthFunc = GreaterDepth, renderOrder 1000, a no-op
 * raycast() and userData.noHit, added to mesh.parent so it carries the same transform, removed
 * from its parent and material-disposed on deselect, on hide and on "Show all". GreaterDepth is
 * the three.js constant 6 (l. 61; 5 is GreaterEqualDepth), so the ghost is drawn only where the
 * part is behind other geometry, and the directly visible surface keeps the solid red.
 * Without the scene (symbol gone in a future model-viewer), parts are hidden by a transparent
 * material instead, ghosts are skipped, and a console.warn says hidden parts still block clicks.
 */
(function () {
  "use strict";

  // Same values as the legend swatches .dh-sw-* in stylesheets/extra.css.
  const RED = "#d91f14";         // selected
  const EYE_OFF = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M2 5.3 3.3 4l16.7 16.7-1.3 1.3-3-3A11 11 0 0 1 12 20C7 20 2.7 16.9 1 12.5c.8-1.9 2-3.6 3.5-4.9L2 5.3m9.9 2.3.6 0A4.5 4.5 0 0 1 16.4 12c0 .2 0 .4-.1.6l-4.4-4.4c.1-.2 0-.6 0-.6M12 5c5 0 9.3 3.1 11 7.5a12 12 0 0 1-3.5 4.7l-1.4-1.4A9.9 9.9 0 0 0 20.8 12.5 9.8 9.8 0 0 0 12 7c-.9 0-1.8.1-2.6.4L7.8 5.8C9.1 5.3 10.5 5 12 5Z"/></svg>';
  const EYE_ON = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M12 9a3 3 0 0 1 3 3 3 3 0 0 1-3 3 3 3 0 0 1-3-3 3 3 0 0 1 3-3m0-4.5c5 0 9.3 3.1 11 7.5-1.7 4.4-6 7.5-11 7.5S2.7 16.4 1 12c1.7-4.4 6-7.5 11-7.5M3.2 12a9.8 9.8 0 0 0 17.6 0 9.8 9.8 0 0 0-17.6 0Z"/></svg>';
  const AMBER = "#f2a61a";       // hovered or focused row (the row hover colour)
  const DRAG_PX = 6;             // pointer travel beyond which a click was an orbit drag
  const MIN_RADIUS_M = 0.35;     // never closer than this when framing a target
  const FRAME_FACTOR = 4.5;      // camera distance = bounding-sphere radius x this
  const SAME_SURFACE_M = 0.002;  // a part this close behind the backdrop is the surface that was clicked
  const GHOST_ALPHA = 0.35;      // x-ray clone of the selection, drawn where it is occluded
  const GHOST_ORDER = 1000;      // the ghosts are drawn after the model
  const GREATER_DEPTH = 6;       // three.js GreaterDepth: keep only fragments behind the depth buffer
  const AXES = ["x", "y", "z"];
  // docs/data/<csv> -> the page that lists it (vendor-map.json gives `bom_file`; `page` overrides).
  const BOM_PAGES = {
    "actuators.csv": "bom/actuators.md", "electronics.csv": "bom/electronics.md",
    "cables-connectors.csv": "bom/cables-and-connectors.md", "fasteners.csv": "bom/fasteners-and-hardware.md",
    "cnc-parts.csv": "bom/cnc-parts.md", "printed-parts.csv": "bom/printed-parts.md",
  };
  // files/<kind>/<id>[_revNN].<ext>[.zip]; <id> may contain dots ("humanoid_2.1_latest") and "~2".
  const FILE_RE = /files\/(step|print|drawings|plates|assembly|modules|vendor)\/([^/]+?)(?:_rev\d+)?\.(?:step|stp|stl|3mf|pdf|f3z|f3d|zip)(?:\.zip)?$/i;

  const ICON_PREVIEW = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6m0-6a1 1 0 0 1 1 1v1.07A8 8 0 0 1 19.93 11H21a1 1 0 1 1 0 2h-1.07A8 8 0 0 1 13 19.93V21a1 1 0 1 1-2 0v-1.07A8 8 0 0 1 4.07 13H3a1 1 0 1 1 0-2h1.07A8 8 0 0 1 11 4.07V3a1 1 0 0 1 1-1m0 4a6 6 0 1 0 0 12 6 6 0 0 0 0-12Z"/></svg>';
  const ICON_DOWNLOAD = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M5 20h14v-2H5v2M19 9h-4V3H9v6H5l7 7 7-7Z"/></svg>';

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }

  // {kind, id} of a download link, or null when the href is not a files/ download.
  function fileRef(href) {
    const m = FILE_RE.exec(href || "");
    if (!m) return null;
    let id = m[2];
    try { id = decodeURIComponent(id); } catch (err) { /* keep the raw name */ }
    return { kind: m[1].toLowerCase(), id };
  }

  function meshesOf(v) {
    return Array.isArray(v) ? v : (v && (v.meshes || v.nodes)) || [];
  }

  function num(v) {
    const n = parseFloat(v);
    return Number.isFinite(n) ? n : null;
  }
  function fmt(v) {
    const n = num(v);
    return n === null ? String(v) : String(Math.round(n * 10) / 10);
  }
  function bboxOf(info) {
    if (!info) return null;
    if (Array.isArray(info.bbox) && info.bbox.length === 3) return info.bbox;
    const b = AXES.map((a) => info["bbox_" + a + "_mm"]);
    return b.every((v) => v !== undefined && v !== null && v !== "") ? b : null;
  }
  function inModule(path, mod) {
    return path === mod.path || path.startsWith(mod.path + "+");
  }

  // Sphere that holds every mesh of a target (left and right, all four plates, a whole module).
  function frameOf(meshes) {
    const n = meshes.length, c = [0, 0, 0];
    meshes.forEach((m) => { for (let i = 0; i < 3; i++) c[i] += m.center[i] / n; });
    const r = Math.max(...meshes.map((m) => Math.hypot(m.center[0] - c[0], m.center[1] - c[1], m.center[2] - c[2]) + m.radius));
    return { center: c, radius: r };
  }

  // parts.json in whichever of the accepted shapes -> Maps and a module list with their meshes.
  function normalize(raw) {
    const d = { parts: new Map(), vendor: new Map(), info: raw.info || {}, axes: raw.axes || null, modules: [] };
    Object.keys(raw.parts || {}).forEach((id) => d.parts.set(id, meshesOf(raw.parts[id])));
    Object.keys(raw.vendor || {}).forEach((id) => d.vendor.set(id, meshesOf(raw.vendor[id])));
    const all = [];
    d.parts.forEach((ms) => ms.forEach((m) => all.push(m)));
    d.vendor.forEach((ms) => ms.forEach((m) => all.push(m)));
    const mods = raw.modules || [];
    const list = Array.isArray(mods) ? mods : Object.keys(mods).map((k) => Object.assign({ file: k }, mods[k]));
    list.forEach((m) => {
      if (!m || !m.path) return;
      const file = String(m.file || m.file_name || m.id || "").replace(/\.(step|stp)$/i, "");
      if (!file) return;
      const meshes = all.filter((x) => x.path && inModule(x.path, m));
      d.modules.push({
        file, name: m.name || m.fusion_name || file, path: m.path,
        depth: m.depth != null && m.depth !== "" ? Number(m.depth) : m.path.split("+").length,
        qty: m.qty, mass_g: m.mass_g, children: m.children, meshes,
      });
    });
    d.modules.sort((a, b) => a.depth - b.depth || a.path.localeCompare(b.path));
    d.moduleByFile = new Map(d.modules.map((m) => [m.file, m]));
    d.vendorInfo = (file) => {
      const info = raw.info || {};
      if (info["vendor:" + file]) return info["vendor:" + file];
      if (raw.vendor && raw.vendor[file] && !Array.isArray(raw.vendor[file])) return raw.vendor[file];
      return info[file] || {};
    };
    return d;
  }

  async function init() {
    const mv = document.getElementById("dh-viewer");
    if (!mv || mv.dataset.ready) return;   // not the CAD page, or already wired
    mv.dataset.ready = "1";
    const box = document.getElementById("dh-viewer-info");
    const reset = document.getElementById("dh-viewer-reset");
    // Eye button (hide / show the selected target) and "Show hidden (N)", next to "Show all".
    const eye = document.createElement("button");
    eye.type = "button"; eye.className = "md-button dh-eye"; eye.disabled = true;
    eye.innerHTML = EYE_OFF + "<span>Hide selected</span>";
    const unhide = document.createElement("button");
    unhide.type = "button"; unhide.className = "md-button dh-unhide"; unhide.hidden = true;
    reset.after(eye, unhide);
    const base = mv.dataset.base || "";
    const homeOrbit = mv.getAttribute("camera-orbit") || "auto auto auto";

    async function getJson(name, required) {
      try {
        const r = await fetch(base + "assets/viewer/" + name);
        if (!r.ok) throw new Error("HTTP " + r.status);
        return await r.json();
      } catch (err) {
        if (required) throw err;
        console.info("dh-viewer: " + name + " not available, continuing without it");
        return null;
      }
    }
    let data;
    try {
      const [raw, vendorMap, downloads] = await Promise.all([
        getJson("parts.json", true), getJson("vendor-map.json", false), getJson("downloads.json", false)]);
      data = normalize(raw);
      data.vendorMap = vendorMap || {};
      data.downloads = downloads || {};
    } catch (err) {
      console.warn("dh-viewer: parts.json unavailable, file rows stay plain", err);
      return;
    }

    // ---- targets: a part, a purchased part, a module or the whole robot ----------------
    const targets = new Map();   // "part:<id>" | "vendor:<file>" | "module:<file>" | "robot" -> target
    function target(kind, id) {
      const key = kind === "robot" ? "robot" : kind + ":" + id;
      if (targets.has(key)) return targets.get(key);
      let t = null;
      if (kind === "part" && data.parts.has(id)) t = { meshes: data.parts.get(id) };
      else if (kind === "vendor" && data.vendor.has(id)) t = { meshes: data.vendor.get(id) };
      else if (kind === "module" && data.moduleByFile.has(id)) {
        const m = data.moduleByFile.get(id);
        t = { meshes: m.meshes, module: m };
      } else if (kind === "robot") t = { meshes: [] };
      if (!t) return null;
      Object.assign(t, { key, kind, id: kind === "robot" ? "robot" : id, rows: [],
                         nodes: new Set(t.meshes.map((m) => m.node)) });
      targets.set(key, t);
      return t;
    }
    // A file row's target from its download link: the id is tried as a part, a purchased
    // part and a module (the folder decides the order); whole-robot files preview the robot.
    function targetForRef(ref) {
      if (!ref) return null;
      const order = ref.kind === "modules" ? ["module", "part", "vendor"]
                  : ref.kind === "vendor" ? ["vendor", "part", "module"] : ["part", "vendor", "module"];
      for (const k of order) {
        const t = target(k, ref.id);
        if (t) return t;
      }
      return ref.kind === "assembly" || ref.kind === "drawings" ? target("robot") : null;
    }
    function targetForNode(name) {
      const id = name.replace(/#\d+$/, "");
      return id.startsWith("vendor:") ? target("vendor", id.slice(7)) : target("part", id);
    }

    // ---- file rows: every table row on the page with a files/ download link ------------
    document.querySelectorAll(".md-typeset table tr").forEach((tr) => {
      const links = Array.from(tr.querySelectorAll("a[href]")).filter((a) => fileRef(a.getAttribute("href")));
      let t = null;
      for (const a of links) {
        t = targetForRef(fileRef(a.getAttribute("href")));
        if (t) break;
      }
      if (!t) return;
      tr.dataset.target = t.key;
      tr.classList.add("dh-part-row");
      tr.tabIndex = 0;
      tr.title = "Show on the robot";
      t.rows.push(tr);
      // The file link becomes a Download button; it still downloads on click (no preventDefault).
      links.forEach((a) => {
        a.classList.add("dh-dl");
        a.title = "Download " + a.textContent.trim();
        if (!a.querySelector("svg")) a.insertAdjacentHTML("afterbegin", ICON_DOWNLOAD);
      });
      // Preview: an explicit button in the first cell, in front of the row's content.
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "dh-preview";
      btn.title = "Show on the robot";
      btn.innerHTML = ICON_PREVIEW + "<span>Preview</span>";
      btn.addEventListener("click", (ev) => { ev.stopPropagation(); select(t, true); });
      const cell = tr.querySelector("td");
      if (cell) cell.insertBefore(btn, cell.firstChild);

      tr.addEventListener("mouseenter", () => hover(t, true));
      tr.addEventListener("mouseleave", () => hover(t, false));
      tr.addEventListener("focus", () => hover(t, true));
      tr.addEventListener("blur", () => hover(t, false));
      tr.addEventListener("click", () => select(t, true));   // a click on the link downloads as well
      tr.addEventListener("keydown", (ev) => {
        if (ev.key !== "Enter" && ev.key !== " ") return;
        if (ev.target.closest("a, button")) return;   // Enter on the link downloads, on the button previews
        ev.preventDefault();
        select(t, true);
      });
    });

    // ---- model colours: originals remembered at load, amber on hover, red when selected --
    let materials = null;   // glTF material name -> Material, once the model has loaded
    let originals = null;   // glTF material name -> [r, g, b, a] as loaded (linear)
    const hovered = new Set();   // targets under the pointer or focused
    let selected = null;
    let current = new Map();     // node -> colour string it is painted with right now

    function setColor(node, color) {
      const m = materials.get(node);
      if (!m) return;
      if (color) m.pbrMetallicRoughness.setBaseColorFactor(color);
      else if (originals.has(node)) m.pbrMetallicRoughness.setBaseColorFactor(originals.get(node));
    }
    // Only the nodes whose colour changes are touched: leaving nodes go back to their original.
    function repaint() {
      if (!materials) return;
      const want = new Map();
      hovered.forEach((t) => t.nodes.forEach((n) => { if (!hidden.has(n)) want.set(n, AMBER); }));
      if (selected) selected.nodes.forEach((n) => { if (!hidden.has(n)) want.set(n, RED); });   // selection wins over hover
      current.forEach((c, n) => { if (!want.has(n)) setColor(n, null); });
      want.forEach((c, n) => { if (current.get(n) !== c) setColor(n, c); });
      current = want;
    }
    function hover(t, on) {
      if (on) hovered.add(t); else hovered.delete(t);
      repaint();
    }
    // ---- three.js access: hide meshes (Fusion's eye) and x-ray the selection -------------
    // model-viewer keeps its ModelScene under Symbol(scene). Hidden meshes move to render
    // layer 1: the camera draws layer 0 only and the raycaster behind materialFromPoint tests
    // object.layers, so a hidden part neither shows nor blocks clicks. The x-ray ghost is a
    // clone of each selected mesh with a translucent red MeshStandardMaterial whose depthFunc
    // is GreaterDepth (6): it is drawn only where the part lies behind other geometry.
    function threeScene() {
      const sym = Object.getOwnPropertySymbols(mv).find((s) => s.description === "scene");
      const scene = sym && mv[sym];
      return scene && typeof scene.traverse === "function" ? scene : null;
    }
    let meshMap = null;   // node name -> three.js Mesh
    function meshOf(node) {
      if (!meshMap) {
        const scene = threeScene();
        if (!scene) return null;
        meshMap = new Map();
        scene.traverse((o) => { if (o.isMesh && o.name) meshMap.set(o.name, o); });
      }
      return meshMap.get(node) || null;
    }
    function rerender() {
      const scene = threeScene();
      if (scene && typeof scene.queueRender === "function") scene.queueRender();
    }
    const hidden = new Set();      // node names hidden with the eye button
    const ghosts = new Map();      // node name -> ghost mesh
    function updateEye() {
      const t = selected;
      const allHidden = t && t.nodes.size > 0 && Array.from(t.nodes).every((n) => hidden.has(n));
      eye.disabled = !t || !t.nodes.size || !threeScene();
      eye.innerHTML = (allHidden ? EYE_ON : EYE_OFF) + `<span>${allHidden ? "Show selected" : "Hide selected"}</span>`;
      eye.setAttribute("aria-label", allHidden ? "Show the selected part again" : "Hide the selected part");
      unhide.hidden = hidden.size === 0;
      unhide.textContent = `Show hidden (${hidden.size})`;
      unhide.setAttribute("aria-label", `Show the ${hidden.size} hidden parts again`);
    }
    function setHidden(nodes, on) {
      nodes.forEach((n) => {
        const m = meshOf(n);
        if (!m) return;
        m.layers.set(on ? 1 : 0);
        if (on) hidden.add(n); else hidden.delete(n);
      });
      refreshGhosts();
      repaint();
      updateEye();
      rerender();
    }
    function clearGhosts() {
      ghosts.forEach((g) => { if (g.parent) g.parent.remove(g); g.material.dispose(); });
      ghosts.clear();
    }
    function refreshGhosts() {
      clearGhosts();
      if (!selected) return;
      selected.nodes.forEach((n) => {
        if (hidden.has(n)) return;
        const m = meshOf(n);
        if (!m || !m.parent || !m.material) return;
        const g = m.clone();
        const mat = m.material.clone();
        mat.color.set(RED);          // three.js Color.set takes the CSS hex string
        mat.transparent = true;
        mat.opacity = GHOST_ALPHA;
        mat.depthWrite = false;
        mat.depthTest = true;
        mat.depthFunc = GREATER_DEPTH;   // only the occluded fragments pass
        mat.metalness = 0; mat.roughness = 1;
        g.material = mat;
        g.renderOrder = GHOST_ORDER;
        g.raycast = () => {};       // never picked
        g.name = "ghost:" + n;
        m.parent.add(g);
        ghosts.set(n, g);
      });
      rerender();
    }

    function bindModel() {
      if (materials || !mv.model) return;
      meshMap = null;
      materials = new Map();
      originals = new Map();
      mv.model.materials.forEach((m) => {
        materials.set(m.name, m);
        try { originals.set(m.name, Array.from(m.pbrMetallicRoughness.baseColorFactor)); } catch (err) { /* no colour to restore */ }
      });
      pushBackdropBack();
      repaint();
      placeAxes();
    }
    // Older scenes carry a "context" backdrop whose faces coincide with the part faces; a depth
    // offset on its three.js material draws the parts on top instead of z-fighting with it.
    function pushBackdropBack() {
      const mesh = backdropMesh();
      [].concat(mesh ? mesh.material : []).forEach((m) => {
        m.polygonOffset = true; m.polygonOffsetFactor = 1; m.polygonOffsetUnits = 1; m.needsUpdate = true;
      });
    }
    mv.addEventListener("load", bindModel);
    if (mv.loaded) bindModel();   // the model finished while parts.json was still in flight
    mv.addEventListener("error", () => {
      box.textContent = "The 3D model did not load. Reload the page.";
      box.hidden = false;
    });

    // ---- axis labels: hotspots moved to the arrow tips given by parts.json --------------
    function placeAxes() {
      AXES.forEach((a) => {
        const el = mv.querySelector('[slot="hotspot-' + a + '"]');
        if (!el) return;
        let tip = data.axes && data.axes[a];
        if (tip && !Array.isArray(tip)) tip = tip.tip || tip.position || tip.end || null;
        if (!tip || tip.length < 3 || tip.slice(0, 3).some((v) => !Number.isFinite(Number(v)))) {
          el.classList.remove("dh-axis-on");
          return;
        }
        const pos = tip.slice(0, 3).map((v) => Number(v) + "m").join(" ");
        el.dataset.position = pos;
        if (typeof mv.updateHotspot === "function") mv.updateHotspot({ name: "hotspot-" + a, position: pos });
        el.classList.add("dh-axis-on");
      });
    }
    placeAxes();

    // ---- info box -----------------------------------------------------------------------
    function resolveHref(h) {
      return /^(?:[a-z][a-z0-9+.-]*:|\/|\.\.?\/)/i.test(h) ? h : base + h;
    }
    function pageHref(page) {
      if (!page) return null;
      if (/^(?:[a-z][a-z0-9+.-]*:|\/)/i.test(page)) return page;
      const i = page.indexOf("#"), hash = i >= 0 ? page.slice(i) : "", p = i >= 0 ? page.slice(0, i) : page;
      let path = p.replace(/\.md$/i, "/").replace(/(^|\/)index\/$/, "$1");
      if (path && !path.endsWith("/")) path += "/";
      return base + path + hash;
    }
    function dlHtml(href, label) {
      return `<a class="dh-dl" href="${esc(href)}" download>${ICON_DOWNLOAD}${esc(label)}</a>`;
    }
    // Download buttons for a target: its rows' links on this page, then downloads.json.
    function downloadsFor(keys, rows, limit) {
      const seen = new Set(), out = [];
      const add = (href, label) => {
        let abs = href;
        try { abs = new URL(href, location.href).href; } catch (err) { /* keep as given */ }
        if (seen.has(abs) || (limit && out.length >= limit)) return;
        seen.add(abs);
        out.push(dlHtml(href, label));
      };
      (rows || []).forEach((tr) => tr.querySelectorAll("a.dh-dl").forEach((a) => add(a.getAttribute("href"), a.textContent.trim())));
      keys.forEach((k) => (k && data.downloads[k] || []).forEach((d) => {
        if (d && d.href) add(resolveHref(d.href), d.label || d.href.split("/").pop());
      }));
      return out;
    }
    // "In: Lower body › Left leg › Knee module", each a preview chip with its STEP download.
    function chainHtml(path, skipPath) {
      const chain = data.modules.filter((m) => inModule(path, m) && m.path !== skipPath);
      if (!chain.length) return "";
      return "In: " + chain.map((m) => {
        const t = target("module", m.file);
        const dl = downloadsFor([m.file], t ? t.rows : [], 1);
        return `<button type="button" class="dh-chip" data-target="module:${esc(m.file)}" title="Show this module">${esc(m.name)}</button>` +
               (dl.length ? " " + dl[0] : "");
      }).join(" › ");
    }
    function chainsHtml(meshes, skipPath) {
      const seen = new Set(), out = [];
      meshes.forEach((m) => {
        const h = m.path ? chainHtml(m.path, skipPath) : "";
        if (h && !seen.has(h)) { seen.add(h); out.push(h); }
      });
      return out.slice(0, 3);
    }
    function facts(info) {
      const bbox = bboxOf(info);
      return [info.appearance, info.material && info.material !== info.appearance ? info.material : "",
              info.mass_g !== undefined && info.mass_g !== "" ? `CAD mass ${fmt(info.mass_g)} g` : "",
              bbox ? `CAD size ${bbox.map(fmt).join(" × ")} mm` : ""].filter(Boolean);
    }
    function infoHtml(t) {
      const lines = [];
      if (t.kind === "part") {
        const info = data.info[t.id] || {};
        // BOM quantity; the count on the model is added only when it differs (both values shown).
        lines.push([`<strong><code>${esc(t.id)}</code></strong>`, info.qty ? `Qty ${esc(info.qty)}` : "",
                    String(t.meshes.length) === String(info.qty) ? "" : `${t.meshes.length} on the model`].filter(Boolean).join(" · "));
        if (info.desc) lines.push(esc(info.desc));
        // Mass and size are CAD values from the Fusion model (part-properties.csv), not measured.
        const f = [info.kind].concat(facts(info)).filter(Boolean);
        if (f.length) lines.push(esc(f.join(" · ")));
        const dl = downloadsFor([t.id], t.rows);
        lines.push(dl.length ? dl.join(" ") : "No file on this page.");
        lines.push(...chainsHtml(t.meshes));
      } else if (t.kind === "vendor") {
        const vi = data.vendorInfo(t.id), vm = data.vendorMap[t.id];
        const name = vi.name || vi.fusion_name || t.id;
        lines.push([`<strong>${esc(name)}</strong>`, "Purchased part",
                    t.meshes.length > 1 ? `${t.meshes.length} on the model` : ""].filter(Boolean).join(" · "));
        const f = facts(vi);
        if (f.length) lines.push(esc(f.join(" · ")));
        if (vm) {
          const bits = [vm.description ? esc(vm.description) : "", vm.mpn ? `MPN ${esc(vm.mpn)}` : "",
                        vm.vendor ? (vm.vendor_url ? `<a href="${esc(vm.vendor_url)}" target="_blank" rel="noopener">${esc(vm.vendor)}</a>` : esc(vm.vendor)) : "",
                        num(vm.qty_in_model) > 1 ? `×${esc(vm.qty_in_model)} on the robot` : ""];
          // The parts-list page: `page` when given, else the page that renders the BOM CSV.
          const page = pageHref(vm.page || BOM_PAGES[String(vm.bom_file || "").toLowerCase()] || "");
          if (vm.part_id) bits.push(page ? `<a href="${esc(page)}">Parts list: <code>${esc(vm.part_id)}</code></a>` : `Parts list: <code>${esc(vm.part_id)}</code>`);
          lines.push(bits.filter(Boolean).join(" · "));
        } else {
          lines.push('<strong class="dh-missing">Purchased part — not in the parts list yet</strong>');
        }
        const dl = downloadsFor([t.id, vm && vm.part_id], t.rows);
        lines.push(dl.length ? dl.join(" ") : "No STEP on this page.");
        lines.push(...chainsHtml(t.meshes));
      } else if (t.kind === "module") {
        const m = t.module;
        const kids = data.modules.filter((x) => x !== m && inModule(x.path, m)).length;
        lines.push([`<strong>${esc(m.name)}</strong>`, "Module", num(m.depth) !== null ? `depth ${esc(m.depth)}` : "",
                    num(m.qty) > 1 ? `×${esc(m.qty)} on the robot` : ""].filter(Boolean).join(" · "));
        const f = [m.mass_g !== undefined && m.mass_g !== "" ? `CAD mass ${fmt(m.mass_g)} g` : "",
                   `${t.meshes.length} components on the model`, kids ? `${kids} sub-modules` : ""].filter(Boolean);
        lines.push(esc(f.join(" · ")));
        const dl = downloadsFor([m.file], t.rows);
        lines.push(dl.length ? dl.join(" ") : "No file on this page.");
        const parents = chainHtml(m.path, m.path);
        if (parents) lines.push(parents);
      } else {
        lines.push("<strong>Whole robot</strong> · every component of the Fusion model");
        const dl = downloadsFor(["robot", "assembly"], t.rows);
        lines.push(dl.length ? dl.join(" ") : "No file on this page.");
      }
      return lines.join("<br>");
    }
    box.addEventListener("click", (ev) => {
      const chip = ev.target.closest("[data-target]");
      if (!chip) return;
      const t = targets.get(chip.dataset.target);
      if (t) select(t, true);
    });

    // ---- selection ------------------------------------------------------------------
    function frame(t) {
      if (typeof mv.getCameraOrbit !== "function") return;
      if (t.kind === "robot" || !t.meshes.length) {
        mv.cameraTarget = "auto auto auto";
        mv.cameraOrbit = homeOrbit;
        return;
      }
      const f = frameOf(t.meshes), o = mv.getCameraOrbit();
      mv.cameraTarget = `${f.center[0]}m ${f.center[1]}m ${f.center[2]}m`;
      mv.cameraOrbit = `${o.theta}rad ${o.phi}rad ${Math.max(MIN_RADIUS_M, f.radius * FRAME_FACTOR)}m`;
    }
    function select(t, moveCamera) {
      if (!t) return;
      selected = t;
      repaint();
      if (moveCamera) frame(t);
      document.querySelectorAll(".dh-part-row.dh-selected").forEach((tr) => tr.classList.remove("dh-selected"));
      t.rows.forEach((tr) => tr.classList.add("dh-selected"));
      box.innerHTML = infoHtml(t);
      box.hidden = false;
      refreshGhosts();
      updateEye();
    }
    eye.addEventListener("click", () => {
      if (!selected || !selected.nodes.size) return;
      const allHidden = Array.from(selected.nodes).every((n) => hidden.has(n));
      setHidden(Array.from(selected.nodes), !allHidden);
    });
    unhide.addEventListener("click", () => setHidden(Array.from(hidden), false));

    // ---- clicks on the model ----------------------------------------------------------
    // With a backdrop (older scenes) a part's surface and the backdrop's coincide, and on
    // that tie the raycast returns the backdrop, which comes first in the scene. When the
    // backdrop is hit, hide it for a second query and take the part right behind it if its
    // surface is within SAME_SURFACE_M of the first hit. The backdrop's three.js mesh is
    // reached through model-viewer's own `scene` symbol; without it, the first hit is used.
    function backdropMesh() {
      const sym = Object.getOwnPropertySymbols(mv).find((s) => s.description === "scene");
      const scene = sym && mv[sym];
      let mesh = null;
      if (scene && typeof scene.traverse === "function") {
        scene.traverse((o) => { if (!mesh && o.isMesh && o.material && o.material.name === "context") mesh = o; });
      }
      return mesh;
    }
    function pickMaterial(x, y) {
      const first = mv.materialFromPoint(x, y);   // client pixels; null off the model
      if (!first || first.name !== "context" || typeof mv.positionAndNormalFromPoint !== "function") return first;
      const mesh = backdropMesh();
      if (!mesh) return first;
      const front = mv.positionAndNormalFromPoint(x, y);
      let behind = null, hit = null;
      mesh.visible = false;
      try {
        behind = mv.materialFromPoint(x, y);
        hit = behind && mv.positionAndNormalFromPoint(x, y);
      } finally {
        mesh.visible = true;
      }
      if (!front || !hit) return first;
      const p = front.position, q = hit.position;
      return Math.hypot(p.x - q.x, p.y - q.y, p.z - q.z) < SAME_SURFACE_M ? behind : first;
    }

    // An orbit drag also ends with a click event on the element; only a still pointer selects.
    let down = null;
    mv.addEventListener("pointerdown", (ev) => { down = [ev.clientX, ev.clientY]; });
    mv.addEventListener("click", (ev) => {
      if (ev.target.closest && ev.target.closest("[slot^='hotspot']")) return;   // an axis label
      const moved = down && Math.hypot(ev.clientX - down[0], ev.clientY - down[1]) > DRAG_PX;
      down = null;
      if (moved || !materials || typeof mv.materialFromPoint !== "function") return;
      const m = pickMaterial(ev.clientX, ev.clientY);
      if (!m || !m.name || m.name === "context") return;
      const t = targetForNode(m.name);
      if (!t) return;
      select(t, false);
      const tr = t.rows[0];
      if (!tr) return;
      tr.scrollIntoView({ behavior: "smooth", block: "center" });
      tr.focus({ preventScroll: true });
      tr.classList.add("dh-flash");
      setTimeout(() => tr.classList.remove("dh-flash"), 1600);
    });

    reset.addEventListener("click", () => {
      selected = null;
      clearGhosts();
      if (hidden.size) setHidden(Array.from(hidden), false);
      repaint();
      updateEye();
      mv.cameraTarget = "auto auto auto";
      mv.cameraOrbit = homeOrbit;
      document.querySelectorAll(".dh-part-row.dh-selected").forEach((tr) => tr.classList.remove("dh-selected"));
      box.hidden = true;
    });
  }

  // Material for MkDocs defines document$ on every page (it emits after DOMContentLoaded,
  // and again on each page change when navigation.instant is on). init() is idempotent.
  if (typeof document$ !== "undefined") document$.subscribe(() => { init(); });
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => { init(); });
  else init();
})();
