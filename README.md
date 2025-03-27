# Commit Message Generator

[English](README.en.md) | 繁體中文

這是一個使用 Google Gemini API 來生成 Git commit message 的工具。它提供了一個 REST API 介面，可以接收 git diff 並返回合適的 commit message 建議。

## 功能特點

- 使用 Google Gemini API 進行智能分析
- 提供 REST API 介面
- 支援 Docker 和 Docker Compose 部署
- 整合 Ngrok 提供臨時公開訪問
- 自動生成符合規範的 commit message (目前僅標題)

## 安裝

### 使用 Docker Compose（推薦）

1. 確保已安裝 Docker 和 Docker Compose
2. 複製環境變數範例檔案：
   ```bash
   cp .env.example .env
   ```
3. 複製配置檔案範例：
   ```bash
   cp example-config.json config.json
   ```
4. 編輯 `.env` 檔案，設定必要的環境變數：
   - `GEMINI_API_KEY`：你的 Google Gemini API 金鑰
   - `NGROK_AUTHTOKEN`：你的 Ngrok Authtoken（必要，用於公開訪問）
   - `NGROK_URL`：你的 Ngrok 網域（選擇性，用於固定網域）

5. 啟動服務：
   ```bash
   docker-compose up -d
   ```

### Local 安裝

1. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```
2. 複製環境變數範例檔案：
   ```bash
   cp .env.example .env
   ```
3. 複製配置檔案範例：
   ```bash
   cp example-config.json config.json
   ```
4. 編輯 `.env` 檔案，設定必要的環境變數：
   - `GEMINI_API_KEY`：你的 Google Gemini API 金鑰
   - `NGROK_AUTHTOKEN`：你的 Ngrok Authtoken（必要，用於公開訪問）
   - `NGROK_URL`：你的 Ngrok 網域（選擇性，用於固定網域）
5. 導出環境變數：
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   export NGROK_AUTHTOKEN="your-ngrok-authtoken-here"
   export NGROK_URL="your-ngrok-url-here"  # 選擇性
   ```
6. 啟動服務：
   ```bash
   uvicorn main:app --reload
   ```
   如果遇到 "Address already in use" 錯誤，可以使用其他端口：
   ```bash
   uvicorn main:app --reload --port 8080
   ```

## API 使用

### 生成 Commit 標題

```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"git_diff": "你的 git diff 內容"}'
```

### API 文件

訪問 http://localhost:8000/docs 查看完整的 API 文件。

## 配置

可以通過修改 `config.json` 檔案來自定義：

- 系統指令 (`system_instruction`)：定義 AI 模型的行為和提示內容
- 範例內容 (`example_contents`)：提供範例以幫助模型理解任務
- 生成參數 (`generate_content_config`)：控制 AI 生成的溫度等參數
- 回應格式 (`response_schema`)：定義 API 回應的結構

### config.json 參數說明

```json
{
  "system_instruction": "AI 系統指令，定義模型行為",
  "example_contents": [
    {
      "role": "user/model",  // 角色：使用者或模型
      "parts": [
        {
          "text": "問答範本"  // 用於少量樣本提示（Few-Shot)的問答範本
        }
      ]
    }
  ],
  "generate_content_config": {
    "temperature": 0.15,  // 控制創意程度，值越低越準確但多樣性較少
    "response_mime_type": "application/json",  // 回應格式
    "response_schema": {  // 回應結構定義
      "type": "OBJECT",
      "required": ["recommendation"],  // 必要欄位
      "properties": {
        "options": {  // 建議選項清單
          "type": "ARRAY",
          "items": {
            "type": "STRING"
          }
        },
        "recommendation": {  // 推薦選項
          "type": "STRING"
        },
        "explanation": {  // 解釋說明
          "type": "STRING"
        }
      }
    }
  }
}
```

首次使用，請複製 `example-config.json` 到 `config.json`，然後根據需要修改。

## 開發

專案結構：
```
.
├── main.py
├── core/
│   └── generator.py
├── config.json
├── example-config.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── ngrok.yml
├── README.md
├── restart.sh
└── rebuild.sh
```

## 安全注意事項

- **千萬不要** 將含有真實 API 金鑰的 `.env` 或 `config.json` 檔案提交到版本控制系統
- 部署前應該先設定好適當的環境變數
- 定期更換 API 金鑰以增強安全性

## 其他注意事項

- 使用 Docker Compose 部署時，服務會自動重啟（除非手動停止）
- Ngrok 服務提供臨時的公開訪問，適合開發和測試使用
- 所有敏感配置都應通過環境變數或 `.env` 檔案設定 

## 常見問題

### Missing key inputs argument! To use the Google AI API, provide (`api_key`) arguments.

如果你在使用服務時遇到此錯誤，表示系統無法讀取 Google Gemini API 金鑰。請檢查：

1. 確認已正確設定 `.env` 檔案中的 `GEMINI_API_KEY` 
2. 確認 API 金鑰格式正確且有效
3. 對於 Local 安裝版本，請確保已手動導出環境變數（見「Local 安裝」第 5 步）
4. 重新啟動服務，確保環境變數被正確載入

如果你使用的是 Local 安裝版本，也可以嘗試直接在環境中設定變數：
```bash
export GEMINI_API_KEY="your-api-key-here"
uvicorn main:app --reload
``` 