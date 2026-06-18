# GovClaw-taipei-daily-news (臺北市政府每日新聞摘要自動化生產線)

本專案提供台北市政府每日新聞摘要的自動化處理流程，包含「抓取開放資料 → LLM 選文與撰寫播報稿 → 語音合成 (TTS) 與 AI 配圖 → 自動生成新聞影片 → 自動發布至 YouTube、Podcast 平台、網站與 LINE 官方帳號」。

## 系統架構

1. **資料抓取 (Fetch)**：定期抓取臺北市政府新聞稿開放資料。
2. **選文與生成 (LLM)**：利用 Gemini 模型篩選當日五大重點新聞，並撰寫適合語音播報的 Traditional Chinese (zh-TW) 腳本。
3. **影音合成 (TTS & Video)**：
   - 透過 Gemini 3.1 Flash TTS (Vertex AI) 進行播報配音。
   - 使用 Playwright 渲染精美的 Neobrutalism 風格簡報網頁並自動截圖。
   - 透過 FFmpeg 合成語音與截圖，產出新聞影片。
4. **多管道部署 (Deploy)**：
   - **LINE**：主動廣播圖文摘要（Flex Message）至訂閱用戶。
   - **YouTube**：上傳生成的每日市政摘要影片。
   - **Podcast**：自動產生 Spotify/Apple Podcast 相容的 RSS Feed 並同步音檔。
   - **Web**：靜態網頁（GitHub Pages）每日更新，方便市民點閱。

---

## 環境設定與安裝

### 1. 安裝相依套件

請確保您的系統已安裝 Python 3.10+，並安裝以下套件：

```bash
pip install -r requirements.txt
# 或手動安裝主要相依套件：
pip install playwright python-dotenv google-auth google-auth-oauthlib google-api-python-client
playwright install chromium
```

### 2. 環境變數設定

複製專案根目錄下的 `.env.example` 並重新命名為 `.env`：

```bash
cp .env.example .env
```

請編輯 `.env` 並填入您的 API 金鑰（**注意：切勿將包含金鑰的 `.env` 檔案提交至 Git**）：

```ini
# LINE 官方帳號設定
LINE_CHANNEL_ACCESS_TOKEN=您的_LINE_Channel_Access_Token

# GCP 憑證與專案設定 (主要生產線 TTS 使用)
# 系統會讀取 Google Application Default Credentials，需在環境中完成 gcloud auth application-default login

# 雅婷 TTS (實驗性/歷史測試腳本使用，選用)
YATING_TTS_API_KEY=您的_雅婷_TTS_API_Key

# ElevenLabs (日文/英文配音，選用)
ELEVENLABS_API_KEY=您的_ElevenLabs_API_Key

# 專案工作資料夾（若不設定，預設為本專案的根目錄）
TW_GOV_VIDEO_BASE=C:\Users\username\專案路徑
```

---

## 資料夾結構

```text
├── .env.example         # 環境變數範本
├── .gitignore           # 排除環境變數與本機生成產物
├── README.md            # 本文件
├── requirements.txt     # Python 相依套件清單
├── HEARTBEAT_PROMPT.md  # Pipeline 自動排程與 LLM 運作提示詞
├── scripts/             # 生產線核心程式碼
│   ├── config.py        # 統一路徑與設定管理
│   ├── process_news.py  # 新聞篩選與 JSON 契約生成
│   ├── deploy_web.py    # 靜態網頁生成與 HTML 轉義
│   ├── deploy_podcast.py# Podcast RSS 生成與同步
│   ├── send_line.py     # LINE 官方帳號廣播
│   └── ...
├── docs/                # GitHub Pages 靜態網站輸出 (index.html、podcast.xml、podcasts/ 音檔等)
└── experiments/         # 實驗與測試腳本 (已從版控中排除)
```

## 自動化排程執行 (Heartbeat)

系統運行狀態會儲存在 `memory/heartbeat-state.json` 中：
- `12pm_fetch_date`：標記今日 12:00 PM 的抓取是否已完成。
- `5pm_pipeline_date`：標記今日 5:00 PM 的影片生成與發布流程是否已完成或正在執行 (`running`)。

若執行途中因意外中斷鎖定在 `running`，系統會自動在逾時（超過 4 小時）後重置狀態，確保隔日排程能正常繼續執行。
