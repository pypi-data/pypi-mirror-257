const {
  SvelteComponent: ot,
  assign: rt,
  create_slot: _t,
  detach: at,
  element: ct,
  get_all_dirty_from_scope: ut,
  get_slot_changes: dt,
  get_spread_update: mt,
  init: bt,
  insert: gt,
  safe_not_equal: ht,
  set_dynamic_element_data: ke,
  set_style: V,
  toggle_class: D,
  transition_in: Re,
  transition_out: Ue,
  update_slot_base: wt
} = window.__gradio__svelte__internal;
function kt(n) {
  let t, e, l;
  const i = (
    /*#slots*/
    n[18].default
  ), f = _t(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let s = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: e = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-1t38q2d"
    }
  ], r = {};
  for (let o = 0; o < s.length; o += 1)
    r = rt(r, s[o]);
  return {
    c() {
      t = ct(
        /*tag*/
        n[14]
      ), f && f.c(), ke(
        /*tag*/
        n[14]
      )(t, r), D(
        t,
        "hidden",
        /*visible*/
        n[10] === !1
      ), D(
        t,
        "padded",
        /*padding*/
        n[6]
      ), D(
        t,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), D(t, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), V(
        t,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), V(t, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), V(
        t,
        "border-style",
        /*variant*/
        n[4]
      ), V(
        t,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), V(
        t,
        "flex-grow",
        /*scale*/
        n[12]
      ), V(t, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), V(t, "border-width", "var(--block-border-width)");
    },
    m(o, _) {
      gt(o, t, _), f && f.m(t, null), l = !0;
    },
    p(o, _) {
      f && f.p && (!l || _ & /*$$scope*/
      131072) && wt(
        f,
        i,
        o,
        /*$$scope*/
        o[17],
        l ? dt(
          i,
          /*$$scope*/
          o[17],
          _,
          null
        ) : ut(
          /*$$scope*/
          o[17]
        ),
        null
      ), ke(
        /*tag*/
        o[14]
      )(t, r = mt(s, [
        (!l || _ & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!l || _ & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!l || _ & /*elem_classes*/
        8 && e !== (e = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-1t38q2d")) && { class: e }
      ])), D(
        t,
        "hidden",
        /*visible*/
        o[10] === !1
      ), D(
        t,
        "padded",
        /*padding*/
        o[6]
      ), D(
        t,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), D(t, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), _ & /*height*/
      1 && V(
        t,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), _ & /*width*/
      2 && V(t, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), _ & /*variant*/
      16 && V(
        t,
        "border-style",
        /*variant*/
        o[4]
      ), _ & /*allow_overflow*/
      2048 && V(
        t,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), _ & /*scale*/
      4096 && V(
        t,
        "flex-grow",
        /*scale*/
        o[12]
      ), _ & /*min_width*/
      8192 && V(t, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      l || (Re(f, o), l = !0);
    },
    o(o) {
      Ue(f, o), l = !1;
    },
    d(o) {
      o && at(t), f && f.d(o);
    }
  };
}
function pt(n) {
  let t, e = (
    /*tag*/
    n[14] && kt(n)
  );
  return {
    c() {
      e && e.c();
    },
    m(l, i) {
      e && e.m(l, i), t = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && e.p(l, i);
    },
    i(l) {
      t || (Re(e, l), t = !0);
    },
    o(l) {
      Ue(e, l), t = !1;
    },
    d(l) {
      e && e.d(l);
    }
  };
}
function yt(n, t, e) {
  let { $$slots: l = {}, $$scope: i } = t, { height: f = void 0 } = t, { width: s = void 0 } = t, { elem_id: r = "" } = t, { elem_classes: o = [] } = t, { variant: _ = "solid" } = t, { border_mode: a = "base" } = t, { padding: d = !0 } = t, { type: u = "normal" } = t, { test_id: w = void 0 } = t, { explicit_call: p = !1 } = t, { container: C = !0 } = t, { visible: F = !0 } = t, { allow_overflow: L = !0 } = t, { scale: q = null } = t, { min_width: c = 0 } = t, y = u === "fieldset" ? "fieldset" : "div";
  const S = (b) => {
    if (b !== void 0) {
      if (typeof b == "number")
        return b + "px";
      if (typeof b == "string")
        return b;
    }
  };
  return n.$$set = (b) => {
    "height" in b && e(0, f = b.height), "width" in b && e(1, s = b.width), "elem_id" in b && e(2, r = b.elem_id), "elem_classes" in b && e(3, o = b.elem_classes), "variant" in b && e(4, _ = b.variant), "border_mode" in b && e(5, a = b.border_mode), "padding" in b && e(6, d = b.padding), "type" in b && e(16, u = b.type), "test_id" in b && e(7, w = b.test_id), "explicit_call" in b && e(8, p = b.explicit_call), "container" in b && e(9, C = b.container), "visible" in b && e(10, F = b.visible), "allow_overflow" in b && e(11, L = b.allow_overflow), "scale" in b && e(12, q = b.scale), "min_width" in b && e(13, c = b.min_width), "$$scope" in b && e(17, i = b.$$scope);
  }, [
    f,
    s,
    r,
    o,
    _,
    a,
    d,
    w,
    p,
    C,
    F,
    L,
    q,
    c,
    y,
    S,
    u,
    i,
    l
  ];
}
class vt extends ot {
  constructor(t) {
    super(), bt(this, t, yt, pt, ht, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const qt = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], pe = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
qt.reduce(
  (n, { color: t, primary: e, secondary: l }) => ({
    ...n,
    [t]: {
      primary: pe[t][e],
      secondary: pe[t][l]
    }
  }),
  {}
);
function U(n) {
  let t = ["", "k", "M", "G", "T", "P", "E", "Z"], e = 0;
  for (; n > 1e3 && e < t.length - 1; )
    n /= 1e3, e++;
  let l = t[e];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function re() {
}
function Ft(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
const He = typeof window < "u";
let ye = He ? () => window.performance.now() : () => Date.now(), Je = He ? (n) => requestAnimationFrame(n) : re;
const H = /* @__PURE__ */ new Set();
function We(n) {
  H.forEach((t) => {
    t.c(n) || (H.delete(t), t.f());
  }), H.size !== 0 && Je(We);
}
function Ct(n) {
  let t;
  return H.size === 0 && Je(We), {
    promise: new Promise((e) => {
      H.add(t = { c: n, f: e });
    }),
    abort() {
      H.delete(t);
    }
  };
}
const R = [];
function Lt(n, t = re) {
  let e;
  const l = /* @__PURE__ */ new Set();
  function i(r) {
    if (Ft(n, r) && (n = r, e)) {
      const o = !R.length;
      for (const _ of l)
        _[1](), R.push(_, n);
      if (o) {
        for (let _ = 0; _ < R.length; _ += 2)
          R[_][0](R[_ + 1]);
        R.length = 0;
      }
    }
  }
  function f(r) {
    i(r(n));
  }
  function s(r, o = re) {
    const _ = [r, o];
    return l.add(_), l.size === 1 && (e = t(i, f) || re), r(n), () => {
      l.delete(_), l.size === 0 && e && (e(), e = null);
    };
  }
  return { set: i, update: f, subscribe: s };
}
function ve(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function de(n, t, e, l) {
  if (typeof e == "number" || ve(e)) {
    const i = l - e, f = (e - t) / (n.dt || 1 / 60), s = n.opts.stiffness * i, r = n.opts.damping * f, o = (s - r) * n.inv_mass, _ = (f + o) * n.dt;
    return Math.abs(_) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, ve(e) ? new Date(e.getTime() + _) : e + _);
  } else {
    if (Array.isArray(e))
      return e.map(
        (i, f) => de(n, t[f], e[f], l[f])
      );
    if (typeof e == "object") {
      const i = {};
      for (const f in e)
        i[f] = de(n, t[f], e[f], l[f]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof e} values`);
  }
}
function qe(n, t = {}) {
  const e = Lt(n), { stiffness: l = 0.15, damping: i = 0.8, precision: f = 0.01 } = t;
  let s, r, o, _ = n, a = n, d = 1, u = 0, w = !1;
  function p(F, L = {}) {
    a = F;
    const q = o = {};
    return n == null || L.hard || C.stiffness >= 1 && C.damping >= 1 ? (w = !0, s = ye(), _ = F, e.set(n = a), Promise.resolve()) : (L.soft && (u = 1 / ((L.soft === !0 ? 0.5 : +L.soft) * 60), d = 0), r || (s = ye(), w = !1, r = Ct((c) => {
      if (w)
        return w = !1, r = null, !1;
      d = Math.min(d + u, 1);
      const y = {
        inv_mass: d,
        opts: C,
        settled: !0,
        dt: (c - s) * 60 / 1e3
      }, S = de(y, _, n, a);
      return s = c, _ = n, e.set(n = S), y.settled && (r = null), !y.settled;
    })), new Promise((c) => {
      r.promise.then(() => {
        q === o && c();
      });
    }));
  }
  const C = {
    set: p,
    update: (F, L) => p(F(a, n), L),
    subscribe: e.subscribe,
    stiffness: l,
    damping: i,
    precision: f
  };
  return C;
}
const {
  SvelteComponent: Vt,
  append: P,
  attr: k,
  component_subscribe: Fe,
  detach: Mt,
  element: Nt,
  init: zt,
  insert: St,
  noop: Ce,
  safe_not_equal: Pt,
  set_style: se,
  svg_element: Z,
  toggle_class: Le
} = window.__gradio__svelte__internal, { onMount: Zt } = window.__gradio__svelte__internal;
function Tt(n) {
  let t, e, l, i, f, s, r, o, _, a, d, u;
  return {
    c() {
      t = Nt("div"), e = Z("svg"), l = Z("g"), i = Z("path"), f = Z("path"), s = Z("path"), r = Z("path"), o = Z("g"), _ = Z("path"), a = Z("path"), d = Z("path"), u = Z("path"), k(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), k(i, "fill", "#FF7C00"), k(i, "fill-opacity", "0.4"), k(i, "class", "svelte-43sxxs"), k(f, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), k(f, "fill", "#FF7C00"), k(f, "class", "svelte-43sxxs"), k(s, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), k(s, "fill", "#FF7C00"), k(s, "fill-opacity", "0.4"), k(s, "class", "svelte-43sxxs"), k(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), k(r, "fill", "#FF7C00"), k(r, "class", "svelte-43sxxs"), se(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), k(_, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), k(_, "fill", "#FF7C00"), k(_, "fill-opacity", "0.4"), k(_, "class", "svelte-43sxxs"), k(a, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), k(a, "fill", "#FF7C00"), k(a, "class", "svelte-43sxxs"), k(d, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), k(d, "fill", "#FF7C00"), k(d, "fill-opacity", "0.4"), k(d, "class", "svelte-43sxxs"), k(u, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), k(u, "fill", "#FF7C00"), k(u, "class", "svelte-43sxxs"), se(o, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), k(e, "viewBox", "-1200 -1200 3000 3000"), k(e, "fill", "none"), k(e, "xmlns", "http://www.w3.org/2000/svg"), k(e, "class", "svelte-43sxxs"), k(t, "class", "svelte-43sxxs"), Le(
        t,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(w, p) {
      St(w, t, p), P(t, e), P(e, l), P(l, i), P(l, f), P(l, s), P(l, r), P(e, o), P(o, _), P(o, a), P(o, d), P(o, u);
    },
    p(w, [p]) {
      p & /*$top*/
      2 && se(l, "transform", "translate(" + /*$top*/
      w[1][0] + "px, " + /*$top*/
      w[1][1] + "px)"), p & /*$bottom*/
      4 && se(o, "transform", "translate(" + /*$bottom*/
      w[2][0] + "px, " + /*$bottom*/
      w[2][1] + "px)"), p & /*margin*/
      1 && Le(
        t,
        "margin",
        /*margin*/
        w[0]
      );
    },
    i: Ce,
    o: Ce,
    d(w) {
      w && Mt(t);
    }
  };
}
function jt(n, t, e) {
  let l, i, { margin: f = !0 } = t;
  const s = qe([0, 0]);
  Fe(n, s, (u) => e(1, l = u));
  const r = qe([0, 0]);
  Fe(n, r, (u) => e(2, i = u));
  let o;
  async function _() {
    await Promise.all([s.set([125, 140]), r.set([-125, -140])]), await Promise.all([s.set([-125, 140]), r.set([125, -140])]), await Promise.all([s.set([-125, 0]), r.set([125, -0])]), await Promise.all([s.set([125, 0]), r.set([-125, 0])]);
  }
  async function a() {
    await _(), o || a();
  }
  async function d() {
    await Promise.all([s.set([125, 0]), r.set([-125, 0])]), a();
  }
  return Zt(() => (d(), () => o = !0)), n.$$set = (u) => {
    "margin" in u && e(0, f = u.margin);
  }, [f, l, i, s, r];
}
class Bt extends Vt {
  constructor(t) {
    super(), zt(this, t, jt, Tt, Pt, { margin: 0 });
  }
}
const {
  SvelteComponent: At,
  append: X,
  attr: T,
  binding_callbacks: Ve,
  check_outros: xe,
  create_component: Dt,
  create_slot: It,
  destroy_component: Et,
  destroy_each: $e,
  detach: g,
  element: B,
  empty: $,
  ensure_array_like: _e,
  get_all_dirty_from_scope: Qt,
  get_slot_changes: Xt,
  group_outros: et,
  init: Yt,
  insert: h,
  mount_component: Gt,
  noop: me,
  safe_not_equal: Kt,
  set_data: z,
  set_style: I,
  space: j,
  text: v,
  toggle_class: N,
  transition_in: W,
  transition_out: x,
  update_slot_base: Ot
} = window.__gradio__svelte__internal, { tick: Rt } = window.__gradio__svelte__internal, { onDestroy: Ut } = window.__gradio__svelte__internal, Ht = (n) => ({}), Me = (n) => ({});
function Ne(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l[40] = e, l;
}
function ze(n, t, e) {
  const l = n.slice();
  return l[38] = t[e], l;
}
function Jt(n) {
  let t, e = (
    /*i18n*/
    n[1]("common.error") + ""
  ), l, i, f;
  const s = (
    /*#slots*/
    n[29].error
  ), r = It(
    s,
    n,
    /*$$scope*/
    n[28],
    Me
  );
  return {
    c() {
      t = B("span"), l = v(e), i = j(), r && r.c(), T(t, "class", "error svelte-1txqlrd");
    },
    m(o, _) {
      h(o, t, _), X(t, l), h(o, i, _), r && r.m(o, _), f = !0;
    },
    p(o, _) {
      (!f || _[0] & /*i18n*/
      2) && e !== (e = /*i18n*/
      o[1]("common.error") + "") && z(l, e), r && r.p && (!f || _[0] & /*$$scope*/
      268435456) && Ot(
        r,
        s,
        o,
        /*$$scope*/
        o[28],
        f ? Xt(
          s,
          /*$$scope*/
          o[28],
          _,
          Ht
        ) : Qt(
          /*$$scope*/
          o[28]
        ),
        Me
      );
    },
    i(o) {
      f || (W(r, o), f = !0);
    },
    o(o) {
      x(r, o), f = !1;
    },
    d(o) {
      o && (g(t), g(i)), r && r.d(o);
    }
  };
}
function Wt(n) {
  let t, e, l, i, f, s, r, o, _, a = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && Se(n)
  );
  function d(c, y) {
    if (
      /*progress*/
      c[7]
    )
      return el;
    if (
      /*queue_position*/
      c[2] !== null && /*queue_size*/
      c[3] !== void 0 && /*queue_position*/
      c[2] >= 0
    )
      return $t;
    if (
      /*queue_position*/
      c[2] === 0
    )
      return xt;
  }
  let u = d(n), w = u && u(n), p = (
    /*timer*/
    n[5] && Te(n)
  );
  const C = [il, nl], F = [];
  function L(c, y) {
    return (
      /*last_progress_level*/
      c[15] != null ? 0 : (
        /*show_progress*/
        c[6] === "full" ? 1 : -1
      )
    );
  }
  ~(f = L(n)) && (s = F[f] = C[f](n));
  let q = !/*timer*/
  n[5] && Qe(n);
  return {
    c() {
      a && a.c(), t = j(), e = B("div"), w && w.c(), l = j(), p && p.c(), i = j(), s && s.c(), r = j(), q && q.c(), o = $(), T(e, "class", "progress-text svelte-1txqlrd"), N(
        e,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), N(
        e,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(c, y) {
      a && a.m(c, y), h(c, t, y), h(c, e, y), w && w.m(e, null), X(e, l), p && p.m(e, null), h(c, i, y), ~f && F[f].m(c, y), h(c, r, y), q && q.m(c, y), h(c, o, y), _ = !0;
    },
    p(c, y) {
      /*variant*/
      c[8] === "default" && /*show_eta_bar*/
      c[18] && /*show_progress*/
      c[6] === "full" ? a ? a.p(c, y) : (a = Se(c), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), u === (u = d(c)) && w ? w.p(c, y) : (w && w.d(1), w = u && u(c), w && (w.c(), w.m(e, l))), /*timer*/
      c[5] ? p ? p.p(c, y) : (p = Te(c), p.c(), p.m(e, null)) : p && (p.d(1), p = null), (!_ || y[0] & /*variant*/
      256) && N(
        e,
        "meta-text-center",
        /*variant*/
        c[8] === "center"
      ), (!_ || y[0] & /*variant*/
      256) && N(
        e,
        "meta-text",
        /*variant*/
        c[8] === "default"
      );
      let S = f;
      f = L(c), f === S ? ~f && F[f].p(c, y) : (s && (et(), x(F[S], 1, 1, () => {
        F[S] = null;
      }), xe()), ~f ? (s = F[f], s ? s.p(c, y) : (s = F[f] = C[f](c), s.c()), W(s, 1), s.m(r.parentNode, r)) : s = null), /*timer*/
      c[5] ? q && (q.d(1), q = null) : q ? q.p(c, y) : (q = Qe(c), q.c(), q.m(o.parentNode, o));
    },
    i(c) {
      _ || (W(s), _ = !0);
    },
    o(c) {
      x(s), _ = !1;
    },
    d(c) {
      c && (g(t), g(e), g(i), g(r), g(o)), a && a.d(c), w && w.d(), p && p.d(), ~f && F[f].d(c), q && q.d(c);
    }
  };
}
function Se(n) {
  let t, e = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      t = B("div"), T(t, "class", "eta-bar svelte-1txqlrd"), I(t, "transform", e);
    },
    m(l, i) {
      h(l, t, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && e !== (e = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && I(t, "transform", e);
    },
    d(l) {
      l && g(t);
    }
  };
}
function xt(n) {
  let t;
  return {
    c() {
      t = v("processing |");
    },
    m(e, l) {
      h(e, t, l);
    },
    p: me,
    d(e) {
      e && g(t);
    }
  };
}
function $t(n) {
  let t, e = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, f, s;
  return {
    c() {
      t = v("queue: "), l = v(e), i = v("/"), f = v(
        /*queue_size*/
        n[3]
      ), s = v(" |");
    },
    m(r, o) {
      h(r, t, o), h(r, l, o), h(r, i, o), h(r, f, o), h(r, s, o);
    },
    p(r, o) {
      o[0] & /*queue_position*/
      4 && e !== (e = /*queue_position*/
      r[2] + 1 + "") && z(l, e), o[0] & /*queue_size*/
      8 && z(
        f,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (g(t), g(l), g(i), g(f), g(s));
    }
  };
}
function el(n) {
  let t, e = _e(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < e.length; i += 1)
    l[i] = Ze(ze(n, e, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      t = $();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      h(i, t, f);
    },
    p(i, f) {
      if (f[0] & /*progress*/
      128) {
        e = _e(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < e.length; s += 1) {
          const r = ze(i, e, s);
          l[s] ? l[s].p(r, f) : (l[s] = Ze(r), l[s].c(), l[s].m(t.parentNode, t));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = e.length;
      }
    },
    d(i) {
      i && g(t), $e(l, i);
    }
  };
}
function Pe(n) {
  let t, e = (
    /*p*/
    n[38].unit + ""
  ), l, i, f = " ", s;
  function r(a, d) {
    return (
      /*p*/
      a[38].length != null ? ll : tl
    );
  }
  let o = r(n), _ = o(n);
  return {
    c() {
      _.c(), t = j(), l = v(e), i = v(" | "), s = v(f);
    },
    m(a, d) {
      _.m(a, d), h(a, t, d), h(a, l, d), h(a, i, d), h(a, s, d);
    },
    p(a, d) {
      o === (o = r(a)) && _ ? _.p(a, d) : (_.d(1), _ = o(a), _ && (_.c(), _.m(t.parentNode, t))), d[0] & /*progress*/
      128 && e !== (e = /*p*/
      a[38].unit + "") && z(l, e);
    },
    d(a) {
      a && (g(t), g(l), g(i), g(s)), _.d(a);
    }
  };
}
function tl(n) {
  let t = U(
    /*p*/
    n[38].index || 0
  ) + "", e;
  return {
    c() {
      e = v(t);
    },
    m(l, i) {
      h(l, e, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && t !== (t = U(
        /*p*/
        l[38].index || 0
      ) + "") && z(e, t);
    },
    d(l) {
      l && g(e);
    }
  };
}
function ll(n) {
  let t = U(
    /*p*/
    n[38].index || 0
  ) + "", e, l, i = U(
    /*p*/
    n[38].length
  ) + "", f;
  return {
    c() {
      e = v(t), l = v("/"), f = v(i);
    },
    m(s, r) {
      h(s, e, r), h(s, l, r), h(s, f, r);
    },
    p(s, r) {
      r[0] & /*progress*/
      128 && t !== (t = U(
        /*p*/
        s[38].index || 0
      ) + "") && z(e, t), r[0] & /*progress*/
      128 && i !== (i = U(
        /*p*/
        s[38].length
      ) + "") && z(f, i);
    },
    d(s) {
      s && (g(e), g(l), g(f));
    }
  };
}
function Ze(n) {
  let t, e = (
    /*p*/
    n[38].index != null && Pe(n)
  );
  return {
    c() {
      e && e.c(), t = $();
    },
    m(l, i) {
      e && e.m(l, i), h(l, t, i);
    },
    p(l, i) {
      /*p*/
      l[38].index != null ? e ? e.p(l, i) : (e = Pe(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && g(t), e && e.d(l);
    }
  };
}
function Te(n) {
  let t, e = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      t = v(
        /*formatted_timer*/
        n[20]
      ), l = v(e), i = v("s");
    },
    m(f, s) {
      h(f, t, s), h(f, l, s), h(f, i, s);
    },
    p(f, s) {
      s[0] & /*formatted_timer*/
      1048576 && z(
        t,
        /*formatted_timer*/
        f[20]
      ), s[0] & /*eta, formatted_eta*/
      524289 && e !== (e = /*eta*/
      f[0] ? `/${/*formatted_eta*/
      f[19]}` : "") && z(l, e);
    },
    d(f) {
      f && (g(t), g(l), g(i));
    }
  };
}
function nl(n) {
  let t, e;
  return t = new Bt({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Dt(t.$$.fragment);
    },
    m(l, i) {
      Gt(t, l, i), e = !0;
    },
    p(l, i) {
      const f = {};
      i[0] & /*variant*/
      256 && (f.margin = /*variant*/
      l[8] === "default"), t.$set(f);
    },
    i(l) {
      e || (W(t.$$.fragment, l), e = !0);
    },
    o(l) {
      x(t.$$.fragment, l), e = !1;
    },
    d(l) {
      Et(t, l);
    }
  };
}
function il(n) {
  let t, e, l, i, f, s = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && je(n)
  );
  return {
    c() {
      t = B("div"), e = B("div"), r && r.c(), l = j(), i = B("div"), f = B("div"), T(e, "class", "progress-level-inner svelte-1txqlrd"), T(f, "class", "progress-bar svelte-1txqlrd"), I(f, "width", s), T(i, "class", "progress-bar-wrap svelte-1txqlrd"), T(t, "class", "progress-level svelte-1txqlrd");
    },
    m(o, _) {
      h(o, t, _), X(t, e), r && r.m(e, null), X(t, l), X(t, i), X(i, f), n[30](f);
    },
    p(o, _) {
      /*progress*/
      o[7] != null ? r ? r.p(o, _) : (r = je(o), r.c(), r.m(e, null)) : r && (r.d(1), r = null), _[0] & /*last_progress_level*/
      32768 && s !== (s = `${/*last_progress_level*/
      o[15] * 100}%`) && I(f, "width", s);
    },
    i: me,
    o: me,
    d(o) {
      o && g(t), r && r.d(), n[30](null);
    }
  };
}
function je(n) {
  let t, e = _e(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < e.length; i += 1)
    l[i] = Ee(Ne(n, e, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      t = $();
    },
    m(i, f) {
      for (let s = 0; s < l.length; s += 1)
        l[s] && l[s].m(i, f);
      h(i, t, f);
    },
    p(i, f) {
      if (f[0] & /*progress_level, progress*/
      16512) {
        e = _e(
          /*progress*/
          i[7]
        );
        let s;
        for (s = 0; s < e.length; s += 1) {
          const r = Ne(i, e, s);
          l[s] ? l[s].p(r, f) : (l[s] = Ee(r), l[s].c(), l[s].m(t.parentNode, t));
        }
        for (; s < l.length; s += 1)
          l[s].d(1);
        l.length = e.length;
      }
    },
    d(i) {
      i && g(t), $e(l, i);
    }
  };
}
function Be(n) {
  let t, e, l, i, f = (
    /*i*/
    n[40] !== 0 && fl()
  ), s = (
    /*p*/
    n[38].desc != null && Ae(n)
  ), r = (
    /*p*/
    n[38].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null && De()
  ), o = (
    /*progress_level*/
    n[14] != null && Ie(n)
  );
  return {
    c() {
      f && f.c(), t = j(), s && s.c(), e = j(), r && r.c(), l = j(), o && o.c(), i = $();
    },
    m(_, a) {
      f && f.m(_, a), h(_, t, a), s && s.m(_, a), h(_, e, a), r && r.m(_, a), h(_, l, a), o && o.m(_, a), h(_, i, a);
    },
    p(_, a) {
      /*p*/
      _[38].desc != null ? s ? s.p(_, a) : (s = Ae(_), s.c(), s.m(e.parentNode, e)) : s && (s.d(1), s = null), /*p*/
      _[38].desc != null && /*progress_level*/
      _[14] && /*progress_level*/
      _[14][
        /*i*/
        _[40]
      ] != null ? r || (r = De(), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null), /*progress_level*/
      _[14] != null ? o ? o.p(_, a) : (o = Ie(_), o.c(), o.m(i.parentNode, i)) : o && (o.d(1), o = null);
    },
    d(_) {
      _ && (g(t), g(e), g(l), g(i)), f && f.d(_), s && s.d(_), r && r.d(_), o && o.d(_);
    }
  };
}
function fl(n) {
  let t;
  return {
    c() {
      t = v(" /");
    },
    m(e, l) {
      h(e, t, l);
    },
    d(e) {
      e && g(t);
    }
  };
}
function Ae(n) {
  let t = (
    /*p*/
    n[38].desc + ""
  ), e;
  return {
    c() {
      e = v(t);
    },
    m(l, i) {
      h(l, e, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && t !== (t = /*p*/
      l[38].desc + "") && z(e, t);
    },
    d(l) {
      l && g(e);
    }
  };
}
function De(n) {
  let t;
  return {
    c() {
      t = v("-");
    },
    m(e, l) {
      h(e, t, l);
    },
    d(e) {
      e && g(t);
    }
  };
}
function Ie(n) {
  let t = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[40]
  ] || 0)).toFixed(1) + "", e, l;
  return {
    c() {
      e = v(t), l = v("%");
    },
    m(i, f) {
      h(i, e, f), h(i, l, f);
    },
    p(i, f) {
      f[0] & /*progress_level*/
      16384 && t !== (t = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[40]
      ] || 0)).toFixed(1) + "") && z(e, t);
    },
    d(i) {
      i && (g(e), g(l));
    }
  };
}
function Ee(n) {
  let t, e = (
    /*p*/
    (n[38].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[40]
    ] != null) && Be(n)
  );
  return {
    c() {
      e && e.c(), t = $();
    },
    m(l, i) {
      e && e.m(l, i), h(l, t, i);
    },
    p(l, i) {
      /*p*/
      l[38].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[40]
      ] != null ? e ? e.p(l, i) : (e = Be(l), e.c(), e.m(t.parentNode, t)) : e && (e.d(1), e = null);
    },
    d(l) {
      l && g(t), e && e.d(l);
    }
  };
}
function Qe(n) {
  let t, e;
  return {
    c() {
      t = B("p"), e = v(
        /*loading_text*/
        n[9]
      ), T(t, "class", "loading svelte-1txqlrd");
    },
    m(l, i) {
      h(l, t, i), X(t, e);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && z(
        e,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && g(t);
    }
  };
}
function sl(n) {
  let t, e, l, i, f;
  const s = [Wt, Jt], r = [];
  function o(_, a) {
    return (
      /*status*/
      _[4] === "pending" ? 0 : (
        /*status*/
        _[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(e = o(n)) && (l = r[e] = s[e](n)), {
    c() {
      t = B("div"), l && l.c(), T(t, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1txqlrd"), N(t, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), N(
        t,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), N(
        t,
        "generating",
        /*status*/
        n[4] === "generating"
      ), N(
        t,
        "border",
        /*border*/
        n[12]
      ), I(
        t,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), I(
        t,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(_, a) {
      h(_, t, a), ~e && r[e].m(t, null), n[31](t), f = !0;
    },
    p(_, a) {
      let d = e;
      e = o(_), e === d ? ~e && r[e].p(_, a) : (l && (et(), x(r[d], 1, 1, () => {
        r[d] = null;
      }), xe()), ~e ? (l = r[e], l ? l.p(_, a) : (l = r[e] = s[e](_), l.c()), W(l, 1), l.m(t, null)) : l = null), (!f || a[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      _[8] + " " + /*show_progress*/
      _[6] + " svelte-1txqlrd")) && T(t, "class", i), (!f || a[0] & /*variant, show_progress, status, show_progress*/
      336) && N(t, "hide", !/*status*/
      _[4] || /*status*/
      _[4] === "complete" || /*show_progress*/
      _[6] === "hidden"), (!f || a[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && N(
        t,
        "translucent",
        /*variant*/
        _[8] === "center" && /*status*/
        (_[4] === "pending" || /*status*/
        _[4] === "error") || /*translucent*/
        _[11] || /*show_progress*/
        _[6] === "minimal"
      ), (!f || a[0] & /*variant, show_progress, status*/
      336) && N(
        t,
        "generating",
        /*status*/
        _[4] === "generating"
      ), (!f || a[0] & /*variant, show_progress, border*/
      4416) && N(
        t,
        "border",
        /*border*/
        _[12]
      ), a[0] & /*absolute*/
      1024 && I(
        t,
        "position",
        /*absolute*/
        _[10] ? "absolute" : "static"
      ), a[0] & /*absolute*/
      1024 && I(
        t,
        "padding",
        /*absolute*/
        _[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(_) {
      f || (W(l), f = !0);
    },
    o(_) {
      x(l), f = !1;
    },
    d(_) {
      _ && g(t), ~e && r[e].d(), n[31](null);
    }
  };
}
let oe = [], ue = !1;
async function ol(n, t = !0) {
  if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
    if (oe.push(n), !ue)
      ue = !0;
    else
      return;
    await Rt(), requestAnimationFrame(() => {
      let e = [0, 0];
      for (let l = 0; l < oe.length; l++) {
        const f = oe[l].getBoundingClientRect();
        (l === 0 || f.top + window.scrollY <= e[0]) && (e[0] = f.top + window.scrollY, e[1] = l);
      }
      window.scrollTo({ top: e[0] - 20, behavior: "smooth" }), ue = !1, oe = [];
    });
  }
}
function rl(n, t, e) {
  let l, { $$slots: i = {}, $$scope: f } = t, { i18n: s } = t, { eta: r = null } = t, { queue_position: o } = t, { queue_size: _ } = t, { status: a } = t, { scroll_to_output: d = !1 } = t, { timer: u = !0 } = t, { show_progress: w = "full" } = t, { message: p = null } = t, { progress: C = null } = t, { variant: F = "default" } = t, { loading_text: L = "Loading..." } = t, { absolute: q = !0 } = t, { translucent: c = !1 } = t, { border: y = !1 } = t, { autoscroll: S } = t, b, ee = !1, ie = 0, E = 0, K = null, O = null, be = 0, Q = null, te, A = null, ge = !0;
  const it = () => {
    e(0, r = e(26, K = e(19, fe = null))), e(24, ie = performance.now()), e(25, E = 0), ee = !0, he();
  };
  function he() {
    requestAnimationFrame(() => {
      e(25, E = (performance.now() - ie) / 1e3), ee && he();
    });
  }
  function we() {
    e(25, E = 0), e(0, r = e(26, K = e(19, fe = null))), ee && (ee = !1);
  }
  Ut(() => {
    ee && we();
  });
  let fe = null;
  function ft(m) {
    Ve[m ? "unshift" : "push"](() => {
      A = m, e(16, A), e(7, C), e(14, Q), e(15, te);
    });
  }
  function st(m) {
    Ve[m ? "unshift" : "push"](() => {
      b = m, e(13, b);
    });
  }
  return n.$$set = (m) => {
    "i18n" in m && e(1, s = m.i18n), "eta" in m && e(0, r = m.eta), "queue_position" in m && e(2, o = m.queue_position), "queue_size" in m && e(3, _ = m.queue_size), "status" in m && e(4, a = m.status), "scroll_to_output" in m && e(21, d = m.scroll_to_output), "timer" in m && e(5, u = m.timer), "show_progress" in m && e(6, w = m.show_progress), "message" in m && e(22, p = m.message), "progress" in m && e(7, C = m.progress), "variant" in m && e(8, F = m.variant), "loading_text" in m && e(9, L = m.loading_text), "absolute" in m && e(10, q = m.absolute), "translucent" in m && e(11, c = m.translucent), "border" in m && e(12, y = m.border), "autoscroll" in m && e(23, S = m.autoscroll), "$$scope" in m && e(28, f = m.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    218103809 && (r === null && e(0, r = K), r != null && K !== r && (e(27, O = (performance.now() - ie) / 1e3 + r), e(19, fe = O.toFixed(1)), e(26, K = r))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    167772160 && e(17, be = O === null || O <= 0 || !E ? null : Math.min(E / O, 1)), n.$$.dirty[0] & /*progress*/
    128 && C != null && e(18, ge = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (C != null ? e(14, Q = C.map((m) => {
      if (m.index != null && m.length != null)
        return m.index / m.length;
      if (m.progress != null)
        return m.progress;
    })) : e(14, Q = null), Q ? (e(15, te = Q[Q.length - 1]), A && (te === 0 ? e(16, A.style.transition = "0", A) : e(16, A.style.transition = "150ms", A))) : e(15, te = void 0)), n.$$.dirty[0] & /*status*/
    16 && (a === "pending" ? it() : we()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    10493968 && b && d && (a === "pending" || a === "complete") && ol(b, S), n.$$.dirty[0] & /*status, message*/
    4194320, n.$$.dirty[0] & /*timer_diff*/
    33554432 && e(20, l = E.toFixed(1));
  }, [
    r,
    s,
    o,
    _,
    a,
    u,
    w,
    C,
    F,
    L,
    q,
    c,
    y,
    b,
    Q,
    te,
    A,
    be,
    ge,
    fe,
    l,
    d,
    p,
    S,
    ie,
    E,
    K,
    O,
    f,
    i,
    ft,
    st
  ];
}
class _l extends At {
  constructor(t) {
    super(), Yt(
      this,
      t,
      rl,
      sl,
      Kt,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 21,
        timer: 5,
        show_progress: 6,
        message: 22,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 23
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: al,
  append: le,
  assign: cl,
  attr: M,
  check_outros: ul,
  create_component: tt,
  destroy_component: lt,
  destroy_each: dl,
  detach: Y,
  element: J,
  empty: ml,
  ensure_array_like: Xe,
  get_spread_object: bl,
  get_spread_update: gl,
  group_outros: hl,
  init: wl,
  insert: G,
  mount_component: nt,
  noop: kl,
  safe_not_equal: pl,
  set_data: yl,
  space: ae,
  src_url_equal: Ye,
  text: vl,
  transition_in: ne,
  transition_out: ce
} = window.__gradio__svelte__internal;
function Ge(n, t, e) {
  const l = n.slice();
  return l[9] = t[e].link, l[10] = t[e].hostname, l;
}
function Ke(n) {
  let t, e;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[7].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[7].i18n
    ) },
    /*loading_status*/
    n[6]
  ];
  let i = {};
  for (let f = 0; f < l.length; f += 1)
    i = cl(i, l[f]);
  return t = new _l({ props: i }), {
    c() {
      tt(t.$$.fragment);
    },
    m(f, s) {
      nt(t, f, s), e = !0;
    },
    p(f, s) {
      const r = s & /*gradio, loading_status*/
      192 ? gl(l, [
        s & /*gradio*/
        128 && { autoscroll: (
          /*gradio*/
          f[7].autoscroll
        ) },
        s & /*gradio*/
        128 && { i18n: (
          /*gradio*/
          f[7].i18n
        ) },
        s & /*loading_status*/
        64 && bl(
          /*loading_status*/
          f[6]
        )
      ]) : {};
      t.$set(r);
    },
    i(f) {
      e || (ne(t.$$.fragment, f), e = !0);
    },
    o(f) {
      ce(t.$$.fragment, f), e = !1;
    },
    d(f) {
      lt(t, f);
    }
  };
}
function ql(n) {
  let t, e, l, i = Xe(
    /*value*/
    n[8]
  ), f = [];
  for (let s = 0; s < i.length; s += 1)
    f[s] = Oe(Ge(n, i, s));
  return {
    c() {
      t = J("div"), t.textContent = "Quellen:", e = ae();
      for (let s = 0; s < f.length; s += 1)
        f[s].c();
      l = ml(), M(t, "class", "text-gray-400 svelte-hkkokf");
    },
    m(s, r) {
      G(s, t, r), G(s, e, r);
      for (let o = 0; o < f.length; o += 1)
        f[o] && f[o].m(s, r);
      G(s, l, r);
    },
    p(s, r) {
      if (r & /*value*/
      256) {
        i = Xe(
          /*value*/
          s[8]
        );
        let o;
        for (o = 0; o < i.length; o += 1) {
          const _ = Ge(s, i, o);
          f[o] ? f[o].p(_, r) : (f[o] = Oe(_), f[o].c(), f[o].m(l.parentNode, l));
        }
        for (; o < f.length; o += 1)
          f[o].d(1);
        f.length = i.length;
      }
    },
    d(s) {
      s && (Y(t), Y(e), Y(l)), dl(f, s);
    }
  };
}
function Fl(n) {
  let t;
  return {
    c() {
      t = J("div"), t.textContent = "Keine Quellen gefunden.", M(t, "class", "text-gray-400 svelte-hkkokf");
    },
    m(e, l) {
      G(e, t, l);
    },
    p: kl,
    d(e) {
      e && Y(t);
    }
  };
}
function Oe(n) {
  let t, e, l, i, f, s, r = (
    /*hostname*/
    n[10].replace(/^www\./, "") + ""
  ), o, _, a;
  return {
    c() {
      t = J("a"), e = J("img"), f = ae(), s = J("div"), o = vl(r), _ = ae(), M(e, "class", "h-3.5 w-3.5 rounded svelte-hkkokf"), Ye(e.src, l = "https://www.google.com/s2/favicons?sz=64&domain_url=" + /*hostname*/
      n[10]) || M(e, "src", l), M(e, "alt", i = /*hostname*/
      n[10].replace(/^www\./, "") + " favicon"), M(s, "class", "svelte-hkkokf"), M(t, "class", "flex items-center gap-2 whitespace-nowrap rounded-lg border bg-white px-2 py-1.5 leading-none hover:border-gray-300 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-gray-700 svelte-hkkokf"), M(t, "href", a = /*link*/
      n[9]), M(t, "target", "_blank");
    },
    m(d, u) {
      G(d, t, u), le(t, e), le(t, f), le(t, s), le(s, o), le(t, _);
    },
    p(d, u) {
      u & /*value*/
      256 && !Ye(e.src, l = "https://www.google.com/s2/favicons?sz=64&domain_url=" + /*hostname*/
      d[10]) && M(e, "src", l), u & /*value*/
      256 && i !== (i = /*hostname*/
      d[10].replace(/^www\./, "") + " favicon") && M(e, "alt", i), u & /*value*/
      256 && r !== (r = /*hostname*/
      d[10].replace(/^www\./, "") + "") && yl(o, r), u & /*value*/
      256 && a !== (a = /*link*/
      d[9]) && M(t, "href", a);
    },
    d(d) {
      d && Y(t);
    }
  };
}
function Cl(n) {
  let t, e, l, i = (
    /*loading_status*/
    n[6] && Ke(n)
  );
  function f(o, _) {
    return (
      /*value*/
      o[8] === void 0 || /*value*/
      o[8].length === 0 ? Fl : ql
    );
  }
  let s = f(n), r = s(n);
  return {
    c() {
      i && i.c(), t = ae(), e = J("div"), r.c(), M(e, "class", "mt-4 flex flex-wrap items-center gap-x-2 gap-y-1.5 text-sm svelte-hkkokf");
    },
    m(o, _) {
      i && i.m(o, _), G(o, t, _), G(o, e, _), r.m(e, null), l = !0;
    },
    p(o, _) {
      /*loading_status*/
      o[6] ? i ? (i.p(o, _), _ & /*loading_status*/
      64 && ne(i, 1)) : (i = Ke(o), i.c(), ne(i, 1), i.m(t.parentNode, t)) : i && (hl(), ce(i, 1, 1, () => {
        i = null;
      }), ul()), s === (s = f(o)) && r ? r.p(o, _) : (r.d(1), r = s(o), r && (r.c(), r.m(e, null)));
    },
    i(o) {
      l || (ne(i), l = !0);
    },
    o(o) {
      ce(i), l = !1;
    },
    d(o) {
      o && (Y(t), Y(e)), i && i.d(o), r.d();
    }
  };
}
function Ll(n) {
  let t, e;
  return t = new vt({
    props: {
      visible: (
        /*visible*/
        n[2]
      ),
      elem_id: (
        /*elem_id*/
        n[0]
      ),
      elem_classes: (
        /*elem_classes*/
        n[1]
      ),
      container: (
        /*container*/
        n[3]
      ),
      scale: (
        /*scale*/
        n[4]
      ),
      min_width: (
        /*min_width*/
        n[5]
      ),
      $$slots: { default: [Cl] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      tt(t.$$.fragment);
    },
    m(l, i) {
      nt(t, l, i), e = !0;
    },
    p(l, [i]) {
      const f = {};
      i & /*visible*/
      4 && (f.visible = /*visible*/
      l[2]), i & /*elem_id*/
      1 && (f.elem_id = /*elem_id*/
      l[0]), i & /*elem_classes*/
      2 && (f.elem_classes = /*elem_classes*/
      l[1]), i & /*container*/
      8 && (f.container = /*container*/
      l[3]), i & /*scale*/
      16 && (f.scale = /*scale*/
      l[4]), i & /*min_width*/
      32 && (f.min_width = /*min_width*/
      l[5]), i & /*$$scope, value, gradio, loading_status*/
      8640 && (f.$$scope = { dirty: i, ctx: l }), t.$set(f);
    },
    i(l) {
      e || (ne(t.$$.fragment, l), e = !0);
    },
    o(l) {
      ce(t.$$.fragment, l), e = !1;
    },
    d(l) {
      lt(t, l);
    }
  };
}
function Vl(n, t, e) {
  let { elem_id: l = "" } = t, { elem_classes: i = [] } = t, { visible: f = !0 } = t, { container: s = !0 } = t, { scale: r = null } = t, { min_width: o = void 0 } = t, { loading_status: _ } = t, { gradio: a } = t, { value: d } = t;
  return n.$$set = (u) => {
    "elem_id" in u && e(0, l = u.elem_id), "elem_classes" in u && e(1, i = u.elem_classes), "visible" in u && e(2, f = u.visible), "container" in u && e(3, s = u.container), "scale" in u && e(4, r = u.scale), "min_width" in u && e(5, o = u.min_width), "loading_status" in u && e(6, _ = u.loading_status), "gradio" in u && e(7, a = u.gradio), "value" in u && e(8, d = u.value);
  }, [
    l,
    i,
    f,
    s,
    r,
    o,
    _,
    a,
    d
  ];
}
class Ml extends al {
  constructor(t) {
    super(), wl(this, t, Vl, Ll, pl, {
      elem_id: 0,
      elem_classes: 1,
      visible: 2,
      container: 3,
      scale: 4,
      min_width: 5,
      loading_status: 6,
      gradio: 7,
      value: 8
    });
  }
}
export {
  Ml as default
};
