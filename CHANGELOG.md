# 本次修改與優化紀錄 (CHANGELOG)

本專案已完成以下優化與問題修正，可直接作為 Git Commit Message 或版本紀錄：

## 🛠️ 修改清單與變更說明

### 1. `deploy_web.py` — 修掉網頁生成崩潰 Bug
*   **問題**：原先的 `import html` 模組在 `main()` 函式中被同名的區域變數 `html = f"..."` 蓋掉（Shadowing），導致後續呼叫 `html.escape()` 時拋出 `AttributeError` 造成崩潰。
*   **修正**：將存放 HTML 字串的變數重新命名為 `page`，保留 `html` 模組的原始名稱；同時一併更新對齊分頁注入時的 `.replace()` 比對字串。

### 2. `HEARTBEAT_PROMPT.md` — 補上 Podcast 部署流程
*   **問題**：原先 Step 5 僅執行 `deploy_web.py` 便進行 `git commit`，導致 RSS/Podcast 資訊不會自動更新。
*   **修正**：在 `deploy_web.py` 後方加上 `deploy_podcast.py`（該腳本讀取的 `temp_audio.mp3` 會由前方的 `render_video.py` 產生，確保執行順序正確），並將 commit 訊息調整為 `"Auto-update website and podcast"`。

### 3. `requirements.txt` — 新增相依套件清單
*   **問題**：README 中指引使用者執行 `pip install -r requirements.txt`，但專案目錄下先前缺乏此檔案，導致指令執行失敗。
*   **修正**：新建 `requirements.txt` 檔案，內容包含專案所需套件：
    *   `playwright`
    *   `python-dotenv`
    *   `google-auth`
    *   `google-auth-oauthlib`
    *   `google-api-python-client`

### 4. 11 支腳本對接 `config.py` — 完善環境變數配置
*   **問題**：先前多個腳本仍各自寫死 `Path.home() / "tw-gov-video"`，未真正遵循 `TW_GOV_VIDEO_BASE` 環境變數。
*   **修正**：已將以下 11 支腳本全部改為自 `config` 模組導入路徑：
    *   `do_5pm.py`
    *   `do_fetch.py`
    *   `exp_tts.py`
    *   `extract_full_text.py`
    *   `fix_json.py`
    *   `generate_images.py`
    *   `inject_images.py`
    *   `pick_5.py`
    *   `render_video.py`
    *   `tts.py`
    *   `upload_youtube.py`
    *   現在整個專案的工作目錄已由 `config.py` 單一入口統一管理，只需設定 `TW_GOV_VIDEO_BASE` 即可一鍵切換所有路徑。

---

## 🔒 重要安全性提醒

*   **金鑰撤銷**：那三把金鑰（LINE Channel Access Token / 雅婷 TTS API key / ElevenLabs API key）因為曾經明碼存放在 Git 歷史紀錄與遠端 GitHub 上，**依然必須前往各自的後台進行撤銷並重新產生**。改為環境變數讀取只防堵了未來的外洩，歷史紀錄中已外洩的金鑰仍然有效（特別是 ElevenLabs 為按量計費，最需優先撤銷）。
