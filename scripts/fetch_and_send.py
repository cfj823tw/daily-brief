#!/usr/bin/env python3
"""
每日科技及科學新聞收集和郵件發送腳本
"""

import os
import json
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# 創建日誌目錄
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

def fetch_news(api_key, count=20):
    """
    從 NewsAPI 獲取科技和科學新聞
    """
    url = 'https://newsapi.org/v2/everything'
    
    # 搜索科技和科學新聞
    params = {
        'q': '(technology OR science OR AI OR innovation)',
        'sortBy': 'publishedAt',
        'language': 'en',
        'pageSize': count,
        'apiKey': api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = data.get('articles', [])
            print(f"✅ 成功獲取 {len(articles)} 條新聞")
            return articles
        else:
            error_msg = data.get('message', 'Unknown error')
            print(f"❌ API 錯誤: {error_msg}")
            return []
    except Exception as e:
        print(f"❌ 獲取新聞失敗: {str(e)}")
        return []

def create_email_content(articles):
    """
    創建 HTML 郵件內容
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #007bff;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                color: #007bff;
                margin: 0;
                font-size: 28px;
            }}
            .date {{
                color: #666;
                font-size: 14px;
                margin-top: 10px;
            }}
            .news-item {{
                border-left: 4px solid #007bff;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
                border-radius: 4px;
            }}
            .news-title {{
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin: 0 0 10px 0;
            }}
            .news-source {{
                color: #007bff;
                font-size: 12px;
                margin-bottom: 8px;
            }}
            .news-description {{
                color: #666;
                font-size: 14px;
                line-height: 1.6;
                margin: 10px 0;
            }}
            .news-link {{
                display: inline-block;
                color: #007bff;
                text-decoration: none;
                font-size: 13px;
                margin-top: 10px;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                border-top: 1px solid #ddd;
                padding-top: 20px;
                color: #999;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📰 Daily Brief - 科技日報</h1>
                <div class="date">每日精選 - {today}</div>
            </div>
    """
    
    for i, article in enumerate(articles, 1):
        title = article.get('title', 'No title')
        source = article.get('source', {}).get('name', 'Unknown')
        description = article.get('description', 'No description')
        url = article.get('url', '#')
        
        html += f"""
            <div class="news-item">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div class="news-title">{i}. {title}</div>
                        <div class="news-source">📋 {source}</div>
                        <div class="news-description">{description}</div>
                        <a href="{url}" class="news-link" target="_blank">🔗 閱讀全文 →</a>
                    </div>
                </div>
            </div>
        """
    
    html += f"""
            <div class="footer">
                <p>✉️ Daily Brief - 每日自動發送科技及科學新聞</p>
                <p>共 {len(articles)} 條新聞 | {today}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(subject, html_content, email_user, email_password, recipient_email):
    """
    發送郵件
    """
    try:
        # 確定 SMTP 伺服器
        if 'gmail' in email_user.lower():
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
        elif 'outlook' in email_user.lower() or 'hotmail' in email_user.lower():
            smtp_server = 'smtp-mail.outlook.com'
            smtp_port = 587
        elif 'qq' in email_user.lower():
            smtp_server = 'smtp.qq.com'
            smtp_port = 587
        elif '163' in email_user.lower():
            smtp_server = 'smtp.163.com'
            smtp_port = 587
        else:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
        
        # 創建郵件
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = email_user
        message['To'] = recipient_email
        
        # 添加 HTML 內容
        message.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 發送郵件
        print(f"📧 連接到 {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(message)
        
        print(f"✅ 郵件已成功發送給 {recipient_email}")
        return True
    except Exception as e:
        print(f"❌ 郵件發送失敗: {str(e)}")
        return False

def main():
    """
    主函數
    """
    # 獲取環境變數
    api_key = os.getenv('NEWSAPI_KEY')
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    
    # 驗證環境變數
    if not all([api_key, email_user, email_password, recipient_email]):
        print("❌ 缺少必要的環境變數")
        print(f"  NEWSAPI_KEY: {bool(api_key)}")
        print(f"  EMAIL_USER: {bool(email_user)}")
        print(f"  EMAIL_PASSWORD: {bool(email_password)}")
        print(f"  RECIPIENT_EMAIL: {bool(recipient_email)}")
        return
    
    print("🚀 開始每日新聞收集...")
    print(f"⏰ 時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 獲取新聞
    articles = fetch_news(api_key, count=20)
    
    if not articles:
        print("⚠️  未獲取到新聞")
        return
    
    # 創建郵件內容
    html_content = create_email_content(articles)
    
    # 發送郵件
    subject = f"📰 Daily Brief - {datetime.now().strftime('%Y-%m-%d')}"
    success = send_email(subject, html_content, email_user, email_password, recipient_email)
    
    # 保存日誌
    log_file = log_dir / f"daily-news-{datetime.now().strftime('%Y-%m-%d')}.log"
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"新聞數: {len(articles)}\n")
        f.write(f"發送狀態: {'成功' if success else '失敗'}\n")
        f.write(f"收件人: {recipient_email}\n\n")
        f.write("新聞列表:\n")
        for i, article in enumerate(articles, 1):
            f.write(f"{i}. {article.get('title')}\n")
            f.write(f"   來源: {article.get('source', {}).get('name')}\n")
            f.write(f"   URL: {article.get('url')}\n\n")
    
    print(f"\n✅ 運行完成！日誌已保存至: {log_file}")

if __name__ == '__main__':
    main()
