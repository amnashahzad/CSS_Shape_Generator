# CSS Shape Generator — Amna

A clean, user-friendly Streamlit app to design and export CSS shapes visually. Build cards, badges, circles, triangles and custom clip-path shapes, tweak borders, shadows, transforms and gradients — then copy or download the ready-to-use CSS.

---

## Features

* Live visual preview of your shape
* Backgrounds: solid color, linear gradients and radial gradients
* Individual border controls (top/right/bottom/left) and multiple border styles
* Per-corner border-radius controls
* Box-shadow with RGBA opacity
* Transforms: rotate, skew, scale
* Clip-path shapes: circle, ellipse, triangle and custom polygon points
* Unit support: `px`, `%`, `vw`, `vh`
* Presets (Rounded Card, Pill / Badge, Perfect Circle, Triangle, Soft Card)
* Randomize button that updates control values
* Copy-to-clipboard and "Download CSS" options
* Clean, exportable CSS class `.shape-preview` ready to paste into any project

---

## Quick demo

After running the app you will see a live preview and generated CSS like:

```css
.shape-preview {
  width: 180px;
  height: 180px;
  background: linear-gradient(to right, #FF6B6B, #5568FF);
  border-radius: 12px 12px 12px 12px;
  border-top: 1px solid #222222;
  border-right: 1px solid #222222;
  border-bottom: 1px solid #222222;
  border-left: 1px solid #222222;
  box-shadow: 6px 8px 24px 0px rgba(0,0,0,0.12);
  transform: rotate(0deg) skew(0deg, 0deg) scale(1);
  margin: 20px auto;
  display: block;
}
```

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/<your-username>/css-shape-generator.git
cd css-shape-generator
```

2. Create a Python virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` should minimally include:

```
streamlit>=1.0
```

(If the repo includes other helper packages, list them here.)

4. Run the app:

```bash
streamlit run app.py
```

---

## Usage

* Open the app in your browser (Streamlit prints the local URL).
* Use the controls panel to the left to:

  * Set size and unit.
  * Choose a background (solid or gradient).
  * Adjust each border side, style and color.
  * Tweak corner radii individually.
  * Configure shadow offsets, blur, spread and opacity.
  * Apply transforms (rotate / skew / scale).
  * Select a clip-path shape or enter a custom polygon.
* Click **Copy CSS** to copy the generated CSS to your clipboard or **Download CSS** to save a `.css` file.
* Use presets or press **Randomize** to explore variations quickly.

---

## Presets

Built-in presets include:

* **Rounded Card** — subtle radii and shadow for UI cards
* **Pill / Badge** — rounded pill shape for badges or chips
* **Perfect Circle** — circle that preserves aspect ratio
* **Triangle** — triangle via clip-path polygon
* **Soft Card (shadow)** — shadow-forward card for modern UIs

---

## Examples & Tips

* Diamond shape polygon: `50% 0%, 100% 50%, 50% 100%, 0% 50%`
* Star/hexagon: use `polygon(...)` with the correct vertex list (can be generated externally and pasted)
* For responsive shapes, try `%`, `vw`, or `vh` units instead of `px`
* For softer shadows, use low opacity (e.g. `0.08—0.18`) and larger blur values

---

## Customization & Extending

This project is intentionally small and easy to extend:

* Add more clip-path templates (star, hexagon) in the `build_clip_path` logic.
* Add SVG export for shapes that need exact vectors.
* Add a gallery to save thumbnails/presets and reapply them.
* Add a dark UI theme or visual thumbnails of presets.

---

## Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to your branch: `git push origin feat/my-feature`
5. Open a Pull Request

Please keep changes small and focused. Add clear commit messages and update this README when adding major features.

---

## Troubleshooting

* If Streamlit doesn't start, check you are using a supported Python version (3.8+ recommended).
* If colors or controls don't show, try refreshing the page or clearing the browser cache.
* If copying to clipboard fails, some browsers require a secure context (https) or user interaction. Use the download button as a fallback.

---

## License

This project is released under the **MIT License**. See `LICENSE` for details.

---

## Credits

* Created and designed by **Amna**
* Built with [Streamlit](https://streamlit.io) for quick UI prototyping
