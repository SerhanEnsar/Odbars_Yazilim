# 🛩️ ODBARS — TEKNOFEST 2026 AI in Aviation Ground Control Station

ODBARS (Otonom Düşman Bulma ve Analiz Robotik Sistemi) is the software suite developed for the TEKNOFEST 2026 "Artificial Intelligence in Aviation" competition. It consists of a React/Electron-based Ground Control Station (GCS) panel and a Python-based autonomous agent.

## 🏆 Competition

- **Event:** TEKNOFEST 2026 — Yapay Zeka İnsansız Hava Araçları Yarışması (AI in Aviation)
- **Category:** Autonomous target detection and analysis
- **Language:** Turkish (Türkçe)

## 🧩 Project Structure

```
Odbars_Yazilim/
├── panel/          ← React + Vite + Electron GCS interface
├── agent/          ← Python autonomous decision agent
└── docs/           ← Architecture plans and system documentation
```

## ✨ Features

### GCS Panel (`panel/`)
- **Real-time telemetry display** — Battery, activity, signal status
- **Camera feed integration** — Live video from UAV
- **Mission control UI** — Built with React + Lucide icons
- **Desktop app** — Packaged with Electron for offline field use

### Autonomous Agent (`agent/`)
- Target detection and classification logic
- Mission state machine

## 🛠 Tech Stack

| Component | Technology |
|---|---|
| GCS UI | React 18 · Vite · Lucide Icons |
| Desktop | Electron |
| Agent | Python 3 |
| Styling | CSS (custom) |

## 🚀 Getting Started

### GCS Panel

```bash
cd panel
npm install
npm run dev        # Development server
npm run electron   # Launch as desktop app
```

### Agent

```bash
cd agent
# See INSTRUCTIONS.md for environment setup and run commands
```

## 📐 Architecture

See [`docs/system/architecture.md`](docs/system/architecture.md) for full system design.

## 📄 License

MIT
