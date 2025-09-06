# app.py
import streamlit as st
import random
import textwrap

st.set_page_config(page_title="CSS Shape Generator — Amna", layout="wide")

def hex_to_rgba(hex_color: str, alpha: float = 1.0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def build_background_style(use_gradient, bg_color, g1, g2, direction):
    if use_gradient:
        if direction == "radial":
            return f"background: radial-gradient(circle, {g1}, {g2});"
        return f"background: linear-gradient({direction}, {g1}, {g2});"
    else:
        return f"background-color: {bg_color};"

def build_border_css(top, right, bottom, left, style, color):
    return (
        f"border-top: {top}px {style} {color};"
        f"border-right: {right}px {style} {color};"
        f"border-bottom: {bottom}px {style} {color};"
        f"border-left: {left}px {style} {color};"
    )

def build_clip_path(shape, polygon_points):
    if shape == "default (none)":
        return ""
    if shape == "circle":
        return "clip-path: circle(50% at 50% 50%);"
    if shape == "ellipse":
        return "clip-path: ellipse(50% 35% at 50% 50%);"
    if shape == "triangle":
        return "clip-path: polygon(50% 0%, 0% 100%, 100% 100%);"
    if shape == "polygon (custom)":
        return f"clip-path: polygon({polygon_points});"
    return ""

def generate_css(props):
    radius = f"border-radius: {props['tl']}px {props['tr']}px {props['br']}px {props['bl']}px;"
    bg = build_background_style(props['use_gradient'], props['bg_color'], props['g1'], props['g2'], props['g_dir'])
    border = build_border_css(props['b_top'], props['b_right'], props['b_bottom'], props['b_left'], props['b_style'], props['b_color'])
    shadow = props['shadow_css']
    transform = f"transform: rotate({props['rotate']}deg) skew({props['skew_x']}deg, {props['skew_y']}deg) scale({props['scale']});"
    clip = build_clip_path(props['shape'], props['polygon_points'])
    size_w = f"{props['width']}{props['unit']}"
    size_h = f"{props['height']}{props['unit']}"
    css = textwrap.dedent(f"""
    .shape-preview {{
      width: {size_w};
      height: {size_h};
      {bg}
      {radius}
      {border}
      {shadow}
      {transform}
      {clip}
      margin: 20px auto;
      display: block;
    }}
    """).strip()
    return css

# --- Sidebar: Presets & Randomize ------------------------------------------------
st.sidebar.title("Controls")
if "seed" not in st.session_state:
    st.session_state.seed = 0

preset = st.sidebar.selectbox("Presets", ["None", "Rounded Card", "Pill / Badge", "Perfect Circle", "Triangle", "Soft Card (shadow)"])
if st.sidebar.button("Randomize"):
    # produce random values (stored in session_state so UI updates)
    st.session_state.seed += 1
    st.session_state._random = {
        "bg_color": random_color(),
        "g1": random_color(),
        "g2": random_color(),
        "b_color": random_color(),
        "width": random.randint(80, 360),
        "height": random.randint(80, 360),
        "tl": random.randint(0, 100),
        "tr": random.randint(0, 100),
        "br": random.randint(0, 100),
        "bl": random.randint(0, 100),
        "b_top": random.randint(0, 8),
        "b_right": random.randint(0, 8),
        "b_bottom": random.randint(0, 8),
        "b_left": random.randint(0, 8),
        "rotate": random.randint(0, 360),
        "skew_x": random.randint(-20, 20),
        "skew_y": random.randint(-20, 20),
        "scale": round(random.uniform(0.5, 1.5), 2)
    }

# --- Main layout ------------------------------------------------
st.write("Use the controls to the left to design a shape. Preview updates live. Export CSS or copy to clipboard.")

col_preview, col_controls = st.columns([1, 1.2])

# --- Defaults / initial values (use random overrides if present) -----------------
rand = st.session_state.get("_random", {})
def rget(k, default):
    return rand.get(k, default)

with col_controls:
    st.header("Shape Properties")

    # Basic size + units
    size_col1, size_col2 = st.columns([2,1])
    with size_col1:
        width = st.number_input("Width", min_value=10, max_value=2000, value=int(rget("width", 150)))
        height = st.number_input("Height", min_value=10, max_value=2000, value=int(rget("height", 150)))
    with size_col2:
        unit = st.selectbox("Unit", ["px", "%", "vw", "vh"], index=0)

    # Background
    st.subheader("Background")
    use_gradient = st.checkbox("Use gradient", value=False)
    if use_gradient:
        g1 = st.color_picker("Gradient color 1", rget("g1", "#FF6B6B"))
        g2 = st.color_picker("Gradient color 2", rget("g2", "#5568FF"))
        g_dir = st.selectbox("Direction", ["to right", "to left", "to bottom", "to top", "radial"], index=0)
        bg_color = "#00000000"  # not used when gradient on
    else:
        bg_color = st.color_picker("Background color", rget("bg_color", "#654FEF"))
        g1 = g2 = g_dir = None

    # Borders & radius grouped
    with st.expander("Borders & Radius", expanded=True):
        colb1, colb2 = st.columns(2)
        with colb1:
            b_top = st.slider("Top border (px)", 0, 40, int(rget("b_top", 1)))
            b_right = st.slider("Right border (px)", 0, 40, int(rget("b_right", 1)))
            b_bottom = st.slider("Bottom border (px)", 0, 40, int(rget("b_bottom", 1)))
            b_left = st.slider("Left border (px)", 0, 40, int(rget("b_left", 1)))
        with colb2:
            b_style = st.selectbox("Border style", ["solid", "dotted", "dashed", "double", "groove", "ridge"], index=0)
            b_color = st.color_picker("Border color", rget("b_color", "#222222"))

        tcol, rcol = st.columns(2)
        with tcol:
            tl = st.slider("Top-left radius (px)", 0, 200, int(rget("tl", 10)))
            tr = st.slider("Top-right radius (px)", 0, 200, int(rget("tr", 10)))
        with rcol:
            bl = st.slider("Bottom-left radius (px)", 0, 200, int(rget("bl", 10)))
            br = st.slider("Bottom-right radius (px)", 0, 200, int(rget("br", 10)))

    # Shadows
    with st.expander("Shadow (box-shadow)", expanded=False):
        use_shadow = st.checkbox("Enable shadow", value=True)
        if use_shadow:
            sh_h = st.slider("Horizontal offset", -100, 100, 8)
            sh_v = st.slider("Vertical offset", -100, 100, 12)
            sh_blur = st.slider("Blur radius", 0, 200, 30)
            sh_spread = st.slider("Spread", -50, 50, 0)
            sh_color = st.color_picker("Shadow color", "#000000")
            sh_alpha = st.slider("Shadow opacity", 0.0, 1.0, 0.18)
            shadow_css = f"box-shadow: {sh_h}px {sh_v}px {sh_blur}px {sh_spread}px {hex_to_rgba(sh_color, sh_alpha)};"
        else:
            shadow_css = ""

    # Transform controls
    with st.expander("Transforms", expanded=False):
        rotate = st.slider("Rotate (deg)", -360, 360, int(rget("rotate", 0)))
        skew_x = st.slider("Skew X (deg)", -60, 60, int(rget("skew_x", 0)))
        skew_y = st.slider("Skew Y (deg)", -60, 60, int(rget("skew_y", 0)))
        scale = st.slider("Scale", 0.1, 3.0, float(rget("scale", 1.0)), step=0.05)

    # Clip-path / shape
    st.subheader("Shape Type (clip-path)")
    shape = st.selectbox("Choose shape", ["default (none)", "circle", "ellipse", "triangle", "polygon (custom)"])
    polygon_points = ""
    if shape == "polygon (custom)":
        polygon_points = st.text_input("Polygon points (CSS list)", "50% 0%, 0% 100%, 100% 100%")

    # Preset application
    if preset != "None" and st.button("Apply Preset"):
        if preset == "Rounded Card":
            tl = tr = br = bl = 12
            use_shadow = True
            shadow_css = f"box-shadow: 6px 8px 24px {hex_to_rgba('#000000', 0.12)};"
            width, height, unit = 360, 220, "px"
            bg_color = "#ffffff"
        elif preset == "Pill / Badge":
            tl = tr = br = bl = 999
            width, height, unit = 220, 48, "px"
            bg_color = "#ff8a65"
            b_top = b_right = b_bottom = b_left = 0
        elif preset == "Perfect Circle":
            shape = "circle"
            width = height = 180
            unit = "px"
        elif preset == "Triangle":
            shape = "triangle"
            width, height, unit = 200, 160, "px"
            tl = tr = br = bl = 0
        elif preset == "Soft Card (shadow)":
            width, height, unit = 340, 200, "px"
            tl = tr = br = bl = 14
            shadow_css = f"box-shadow: 0px 18px 40px {hex_to_rgba('#000000', 0.12)};"
            bg_color = "#ffffff"
        # Note: presets are applied locally; user can further tweak

# Collect props
props = {
    "width": width,
    "height": height,
    "unit": unit,
    "use_gradient": use_gradient,
    "bg_color": bg_color,
    "g1": g1,
    "g2": g2,
    "g_dir": g_dir,
    "b_top": b_top,
    "b_right": b_right,
    "b_bottom": b_bottom,
    "b_left": b_left,
    "b_style": b_style,
    "b_color": b_color,
    "tl": tl,
    "tr": tr,
    "br": br,
    "bl": bl,
    "shadow_css": shadow_css,
    "rotate": rotate,
    "skew_x": skew_x,
    "skew_y": skew_y,
    "scale": scale,
    "shape": shape,
    "polygon_points": polygon_points,
}

# --- Preview & CSS display -------------------------------------------------------
with col_preview:
    st.header("Live Preview")
    css = generate_css(props)

    # Build small HTML preview that isolates the shape
    preview_html = f"""
    <div style="padding:20px; display:flex; justify-content:center; align-items:center;">
      <div class="shape-preview"></div>
    </div>
    <style>
    {css}
    /* ensure preview background contrasts */
    .stApp {{ background: linear-gradient(180deg, #f7f8fb, #ffffff); }}
    </style>
    """

    st.components.v1.html(preview_html, height=420, scrolling=True)

    st.subheader("Generated CSS")
    st.code(css, language="css")

    # Copy to clipboard button using a tiny HTML/JS component
    copy_html = f"""
    <button id="copyBtn">Copy CSS</button>
    <script>
      const css = `{css.replace('`', '\\`')}`;
      const btn = document.getElementById("copyBtn");
      btn.onclick = () => navigator.clipboard.writeText(css).then(()=>{{
         btn.textContent = 'Copied!';
         setTimeout(()=> btn.textContent = 'Copy CSS', 1200);
      }});
    </script>
    """
    st.components.v1.html(copy_html, height=50)

    # Download button
    st.download_button("Download CSS file", css, file_name="shape.css", mime="text/css")

    st.markdown("---")
    st.caption("Tip: toggle 'Use gradient' or try 'polygon (custom)' to create triangles and custom shapes with clip-path. Use small scale/rotate values for subtle effects.")

# --- Footer / small help ---------------------------------------------------------
st.markdown("""
#### Quick tips
- Use `clip-path` (polygon) to make any custom shape. Example polygon points for a diamond: `50% 0%, 100% 50%, 50% 100%, 0% 50%`.
- When using `radial` gradient, the CSS uses `radial-gradient(...)`.
- Export the CSS and paste into your project. The preview class is `.shape-preview`.
""")
