# AI Maze Game — VS Code + Unsloth/Laya

A small browser maze game. Move with arrow keys/WASD, or ask the local Laya model to suggest a move. The browser talks to a tiny Python/Flask backend, which calls Unsloth's local Decision API. This backend also avoids browser CORS issues and keeps the API token out of browser JavaScript.

> This is an implementation of the earlier “AI Maze Game” idea, not a verified copy of any external challenge spec. It uses a sample maze and Laya choice decisions; adapt rules if your assignment says otherwise.

## 1) Install Python (Windows)

Download Python from the official page: https://www.python.org/downloads/windows/

Recommended: Python 3.13.x (64-bit). In the installer, tick **Add python.exe to PATH**, then click **Install Now**. Open a new VS Code terminal and verify:

```powershell
py --version
```

If `py` is not recognized, try `python --version`. Restart VS Code after installation.

## 2) Download and install Unsloth Desktop

Official download: https://unsloth.ai/download

Install and open Unsloth Desktop. You do not need to `pip install unsloth` for this desktop-app route.

## 3) Download Laya model

In Unsloth Desktop, open **Settings → API → Decision API**. Turn on **Serve requests** and allow it to download the default multilingual Laya model when prompted. The documented default is about 678 MB and needs around 4 GB RAM. CPU works; GPU is optional.

On the same settings page, copy an **Access token**. Alternatively, enable **Keyless API access → Chat and inference** for localhost if your version offers it. Keep the token private.

Expected local API URL: `http://localhost:8888/v1/systemone`. Use the URL shown by your app if different.

## 4) Open project in VS Code

1. Extract `AI-Maze-Game.zip` to a normal folder, e.g. Desktop.
2. In VS Code, choose **File → Open Folder…** and select `ai-maze-game`.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment and install packages:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt terminal and run:

```bat
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py -3.13` is unavailable, use `py -m venv .venv` instead.

5. Copy `.env.example` to `.env`. On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

6. Open `.env` and paste your local token after `UNSLOTH_API_KEY=`. If keyless access is enabled, leave it blank. Do not share or upload `.env`.

## 5) Test Laya in Unsloth UI

First confirm Unsloth is running, **Serve requests** is enabled, and Laya has finished downloading. The first model request can take 10–20 seconds. You can test the API from the project page with **Ask Laya** after starting Flask below.

## 6) Try curl (Windows)

Open a second VS Code terminal while Unsloth is running. Replace `YOUR_LOCAL_TOKEN` with your token. If keyless access is enabled, remove the Authorization line.

```powershell
curl.exe http://localhost:8888/v1/systemone -H "Authorization: Bearer YOUR_LOCAL_TOKEN" -H "Content-Type: application/json" -d '{"model":"laya","state":"A player is in a maze. The north path is blocked by a wall. East is open and leads closer to the goal. South is open but leads away from the goal. West is blocked.","questions":{"move":{"type":"choice","instructions":"Choose the safest useful next move toward the maze exit. Consider walls and progress.","criteria":{"up":"north path is open and useful","right":"east path is open and useful","down":"south path is open and useful","left":"west path is open and useful"}}}}'
```

Success should return JSON containing an `answers` object and `answers.move.choice` (usually one of `up`, `right`, `down`, `left`). Exact probabilities vary.

## 7) Run the game

In VS Code terminal, with `.venv` active:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser. Keep Unsloth open in the background. Use arrow keys/WASD for manual movement; click **Ask Laya** to get a suggestion; click **Let Laya play** to let it take multiple steps. Use **Reset maze** to restart.

## Troubleshooting

- **Connection refused / 502:** Open Unsloth and enable Settings → API → Decision API → Serve requests; verify its URL/port.
- **401/403:** token incorrect, or enable keyless access for localhost and leave token blank.
- **404:** check the exact endpoint shown by Unsloth; expected path is `/v1/systemone`.
- **No Python / py not recognized:** install Python from the official link, tick Add to PATH, then restart VS Code.
- **PowerShell activation blocked:** use the Command Prompt activation command above.
- **Laya chooses a wall:** model suggestions are probabilistic. The game prevents wall moves and reports that the suggested direction is blocked; manual movement remains available.

## Security

The `.env` file contains your local token. Never commit it to GitHub or share it. The backend only forwards requests to the local Unsloth API.
