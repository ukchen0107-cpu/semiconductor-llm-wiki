# 半導體製程 LLM Wiki｜從一片矽晶圓到一顆晶片

一套可持續累積的繁體中文半導體製程知識庫與互動教學 HTML 簡報。包含 **8 份已整理的官方技術／教學來源摘要**、可追溯的 Wiki 條目、互動簡報、GitHub Actions 自動建置、單元測試與 Graph / Loop 說明。

## 本機操作
```bash
python scripts/build.py
python -m unittest discover -s tests -v
python -m http.server 8000
```
開啟 `http://localhost:8000/` 看 Wiki，或 `http://localhost:8000/slides/` 看簡報。`localhost` **只能用於測試，不能當繳交網址**。

## 新增來源
1. 依 `AGENTS.md` 的「先討論、後生成」決定問題與來源。
2. 複製 `data/sources/S08.json` 作為範例，新增 `S09.json`，更換 ID、資料與來源（不能覆蓋原資料）。
3. 執行 build + tests，檢查新增條目的 Wiki 首頁及簡報來源區。
4. push 至 GitHub 後，GitHub Actions 會自動重建並部署 GitHub Pages（需在 Settings → Pages 啟用 GitHub Actions）。

## 部署
建立 **Public** GitHub Repo，把整個資料夾的內容 push 到 `main`；在 **Settings → Pages → Build and deployment → Source → GitHub Actions** 啟用。Actions 會自動生成 Wiki/簡報並發布。繳交時交 `https://github.com/帳號/repo` 與 `https://帳號.github.io/repo/`，另提供簡報 `https://帳號.github.io/repo/slides/`。

詳細流程、實作檢查與反思請見 [`docs/workflow.md`](docs/workflow.md)。