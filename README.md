# robo_ball

A website showcasing our ball juggling robot project.

## Local preview

Open `index.html` in a browser, or run a tiny local server so relative links work cleanly:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deploying to GitHub Pages

1. Push this repo to GitHub (already named `robo_ball`).
2. On GitHub, go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to `Deploy from a branch`.
4. Pick branch `main` and folder `/ (root)`. Save.
5. Wait ~30s, then visit `https://<your-username>.github.io/robo_ball/`.

## Structure

```
index.html          Homepage
goal.html           Project goal
design.html         Mechanical & electrical design
perception.html     Ball detection & tracking
planning.html       Trajectory planning & control
challenges.html     Hard problems we ran into
future.html         Future improvements
styles.css          Shared styling for all pages
```

## Adding images

Create an `images/` folder and reference files like:

```html
<figure>
  <img src="images/cad.png" alt="CAD render of the robot" />
  <figcaption>CAD render of the v2 frame.</figcaption>
</figure>
```
