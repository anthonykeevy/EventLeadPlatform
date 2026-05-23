# Understand-Anything — EventLeadPlatform

Quick reference for installing, scanning, and running the interactive codebase dashboard on this repo. All generated artifacts stay **local** under `.understand-anything/` (gitignored).

For starting the EventLead app itself (backend, frontend, MailHog), see [SERVICE-MANAGEMENT-GUIDE.md](SERVICE-MANAGEMENT-GUIDE.md).

---

## Prerequisites

| Tool | Version | Notes |
|------|---------|--------|
| Node.js | ≥ 22 | `node --version` |
| pnpm | ≥ 10 | `npm install -g pnpm` if missing |
| Python | 3.x | Used by `merge-batch-graphs.py` during scan |
| Git | any | Repo must be a git checkout |

---

## One-time install (this machine)

Understand-Anything is installed under the user profile, not inside this repo:

| Path | Purpose |
|------|---------|
| `%USERPROFILE%\.understand-anything\repo` | Plugin source (cloned from GitHub) |
| `%USERPROFILE%\.understand-anything-plugin` | Junction → plugin package |
| `%USERPROFILE%\.cursor\skills-cursor\understand*` | Cursor agent skills (`/understand`, etc.) |

**Fresh install (Windows):** if the installer script fails on encoding, clone and link manually:

```powershell
git clone https://github.com/Lum1104/Understand-Anything.git "$env:USERPROFILE\.understand-anything\repo"
cd "$env:USERPROFILE\.understand-anything\repo"
pnpm install
pnpm --filter @understand-anything/core build
pnpm --filter @understand-anything/dashboard build
```

Then junction skills from `understand-anything-plugin\skills\` into `%USERPROFILE%\.cursor\skills-cursor\` (one junction per skill folder). Restart Cursor after linking.

**Update plugin:**

```powershell
git -C "$env:USERPROFILE\.understand-anything\repo" pull --ff-only
cd "$env:USERPROFILE\.understand-anything\repo"
pnpm install
pnpm --filter @understand-anything/core build
```

---

## Run a codebase scan

From the **repo root** in Cursor, invoke the agent skill:

| Command | What it does |
|---------|----------------|
| `/understand` | Full scan if no graph exists; incremental if commit changed |
| `/understand --full` | Force full rebuild (ignore existing graph) |
| `/understand-domain` | Business domain flow graph (uses existing graph if present) |

**Outputs** (all under `.understand-anything/`):

| File | Description |
|------|-------------|
| `knowledge-graph.json` | Structural graph (files, functions, layers, tour) |
| `domain-graph.json` | Business domains / flows (after `/understand-domain`) |
| `meta.json` | Last commit hash, node/edge counts |
| `intermediate/` | Batch files and merge scratch (local only) |
| `tmp/` | Scan scripts and temp inputs |
| `.understandignore` | Optional exclude patterns (same syntax as `.gitignore`) |

**Do not commit** anything under `.understand-anything/` — `.gitignore` excludes the whole directory.

---

## Start the dashboard service

The dashboard is a Vite dev server served from the plugin install, pointed at this repo via `GRAPH_DIR`.

```powershell
# From repo root
$env:GRAPH_DIR = (Get-Location).Path
cd "$env:USERPROFILE\.understand-anything\repo\understand-anything-plugin\packages\dashboard"
npx vite --host 127.0.0.1
```

On startup the terminal prints a **tokenized URL** — you must use it (token is required):

```
🔑  Dashboard URL: http://127.0.0.1:5173/?token=<TOKEN>
```

Open that full URL in a browser. The token is stored in `sessionStorage` after first load.

| View | How |
|------|-----|
| Structural graph | Default view after load |
| Domain flows | Click **Domain** in the toolbar |
| Guided tour | **Learn** → **Start Tour** |
| Search | Fuzzy or Semantic in the search bar |

**Stop:** Ctrl+C in the dashboard terminal.

**Troubleshooting**

- **“No knowledge graph loaded”** — run `/understand` first; confirm `.understand-anything/knowledge-graph.json` exists.
- **Token gate** — use the URL with `?token=...` from the terminal output.
- **Wrong project** — ensure `GRAPH_DIR` is set to this repo root before starting Vite.
- **Port in use** — Vite picks the next free port; read the terminal for the actual URL.

---

## Typical workflow

1. Pull latest code on your branch.
2. In Cursor: `/understand --full` (or `/understand` for incremental after small changes).
3. Optional: `/understand-domain` for business-flow view.
4. Start dashboard (commands above) and explore at the tokenized URL.
5. Use `/understand-diff` before large commits to see ripple impact (requires graph + git diff).

---

## Related docs

- [SERVICE-MANAGEMENT-GUIDE.md](SERVICE-MANAGEMENT-GUIDE.md) — backend, frontend, MailHog
- [customer-discovery/](customer-discovery/) — scorecard and MVP gap docs (cross-check domain view against these)
- Upstream: [Understand-Anything on GitHub](https://github.com/Lum1104/Understand-Anything)
