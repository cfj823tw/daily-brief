# Daily Brief 設置指南 🚀

本指南將幫助你快速設置每日新聞自動發送系統。

## 📋 前置需求

- GitHub 帳戶
- 電子郵箱（Gmail、Outlook、QQ、163 等）
- NewsAPI.org 免費 API 密鑰

## 🔑 第一步：獲取 NewsAPI 密鑰

1. 訪問 [newsapi.org](https://newsapi.org/)
2. 點擊 "Register" 註冊帳戶
3. 註冊後登錄，進入 Dashboard
4. 複製你的 **API Key**（在 Dashboard 頁面顯示）
   - 免費版本每天 100 個請求，足夠日常使用
   - 包含全球 50,000+ 媒體來源

## 🔐 第二步：配置 GitHub Secrets

### 獲取郵箱應用密碼

#### 📧 Gmail 用戶
1. 訪問 [myaccount.google.com](https://myaccount.google.com)
2. 進入 "Security"（左側導航）
3. 啟用 "2-Step Verification"（如未啟用）
4. 在 "App passwords" 中選擇 Mail 和 Windows Computer
5. 複製生成的 16 位密碼

#### 🔵 Outlook / Hotmail 用戶
1. 訪問 [account.microsoft.com](https://account.microsoft.com)
2. 進入 "Security" 
3. 設置應用密碼或使用普通密碼

#### 🏠 QQ 郵箱用戶
1. 訪問 [mail.qq.com](https://mail.qq.com)
2. 進入 "設置" → "帳戶"
3. 在 "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服務" 中啟用
4. 設置授權碼（而非密碼）

#### 🏠 163 郵箱用戶
1. 訪問 [mail.163.com](https://mail.163.com)
2. 進入 "設置" → "POP3/SMTP/IMAP"
3. 啟用服務並設置授權碼

### 添加 Secrets 到 GitHub

1. 進入倉庫頁面：https://github.com/cfj823tw/daily-brief
2. 點擊 "Settings"（右上角）
3. 左側導航點擊 "Secrets and variables" → "Actions"
4. 點擊 "New repository secret"
5. 添加以下 4 個 secrets：

| 名稱 | 值 | 說明 |
|------|-----|------|
| `NEWSAPI_KEY` | 你的 API Key | 從 newsapi.org 複製 |
| `EMAIL_USER` | 你的郵箱地址 | 例：your.email@gmail.com |
| `EMAIL_PASSWORD` | 應用專用密碼 | Gmail 需要應用密碼，非登錄密碼 |
| `RECIPIENT_EMAIL` | 接收郵箱地址 | 通常與 EMAIL_USER 相同 |

## ✅ 第三步：測試工作流

1. 進入倉庫的 "Actions" 選項卡
2. 左側選擇 "Daily News Brief" 工作流
3. 點擊 "Run workflow" → "Run workflow"
4. 等待 1-2 分鐘
5. 檢查郵箱是否收到郵件

### 常見問題

**❌ 郵件未收到？**
- 檢查垃圾郵件/廣告郵件文件夾
- 確認 Secrets 配置正確（無多餘空格）
- 檢查郵箱是否需要允許 "不安全應用" 訪問（Gmail）

**❌ 新聞為空？**
- 檢查 NEWSAPI_KEY 是否正確
- 確認 API 配額未用完（免費版 100/天）

**❌ 認證失敗？**
- 確保使用的是應用專用密碼，不是登錄密碼
- QQ 和 163 需要使用授權碼，不是密碼

## ⏰ 第四步：確認自動排程

工作流默認設置：
- **時間**：每天 01:00 UTC（台灣時間 09:00 AM）
- **頻率**：每天 1 次
- **條數**：20 條新聞

### 修改時間

如需修改運行時間：

1. 編輯 `.github/workflows/daily-news.yml`
2. 修改 `cron` 字段：

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # 現在：每天 01:00 UTC
    # - cron: '0 9 * * *'  # 改為：每天 09:00 UTC
```

**Cron 格式**：`分 小時 日 月 星期`

| 例子 | 含義 |
|------|------|
| `0 1 * * *` | 每天 01:00 UTC |
| `0 9 * * *` | 每天 09:00 UTC |
| `0 */6 * * *` | 每 6 小時 |
| `0 9 * * 1` | 每週一 09:00 UTC |

## 📊 監控運行狀態

進入 "Actions" 選項卡可以看到：
- ✅ 運行成功/失敗
- ⏱️ 運行時間
- 📝 詳細日誌
- 📁 生成的日誌文件

## 🔧 下一步

- 💡 自定義新聞關鍵詞（編輯 `scripts/fetch_and_send.py` 中的搜索條件）
- 🎨 修改郵件樣式（編輯 `scripts/fetch_and_send.py` 中的 HTML 部分）
- 📧 添加多個接收者
- 🔔 設置通知提醒

## 📞 需要幫助？

- 查看 GitHub Actions 日誌獲取詳細錯誤信息
- 檢查 Secrets 配置是否正確
- 確認郵箱提供商的安全設置允許自動化工具訪問

---

**享受每日自動科技新聞摘要！** 📰✨
