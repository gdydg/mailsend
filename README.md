# GitHub Action 批量发送邮件

最近看到serv00的webmail邮箱（理论上其他webmail也行，比如站内的，至于serv00邮箱怎么创建可以站内搜搜），想着可不可以利用他批量轰......哦，批量发件给客户，于是创建了这个项目，项目利用 GitHub Actions 实现自动化批量发送邮件。你只需要维护一个收件人列表，修改邮件内容，然后手动触发，即可轻松完成邮件的批量发送。

[项目地址](https://github.com/gdydg/mailsend)

## ✨ 主要功能
- 批量发送: 从 recipients.csv 文件中读取收件人列表，为每个人发送一封独立的邮件。

- 个性化内容: 支持在邮件主题和正文中插入变量（如收件人姓名）。

- 富文本格式: 支持直接使用 HTML 编写邮件正文，实现复杂的格式、链接和颜色。

- 安全可靠: 邮箱密码等敏感信息通过 GitHub Secrets 加密存储，不会暴露在代码中。

# 🚀 设置指南

请按照以下步骤完成配置，整个过程大约需要 5-10 分钟。

## 步骤 1: 准备文件结构

确保你的仓库中包含以下文件：

```
├── .github/

│   └── workflows/

│       └── send-emails.yml

├── recipients.csv   
    
```

send-emails.yml: 这是工作流程的配置文件，定义了所有自动化操作。

recipients.csv: 一个 CSV 文件，用于存放收件人的邮箱和姓名。


## 步骤 2: 编辑收件人列表 (recipients.csv)

打开 recipients.csv 文件，按照以下格式添加收件人信息，第一行是表头，必须保留（多个相同的地址就是发多遍邮件给一个人）。
```
email,name
user1@example.com,张三
user2@example.com,李四
another-user@example.com,王五
```

## 步骤 3: 配置邮箱凭证 (GitHub Secrets)

这是最重要的一步，我们需要安全地存储你的邮箱密码。

在你的 GitHub 仓库页面，点击 `Settings` (设置)。

在左侧菜单中，找到 `Secrets and variables`，然后点击 Actions。

点击 `New repository secret` (新建仓库机密) 按钮。

- 创建第一个机密：

Name: `MAIL_USERNAME`

Secret: 你的邮箱地址 (例如: your-email@domain.com)

- 再次点击 New repository secret，创建第二个机密：

Name: `MAIL_PASSWORD`

Secret: 你的邮箱密码或应用专用密码

重要提示: 如果你的邮箱开启了二次验证 (2FA)，你通常需要在这里填写 应用专用密码 (App-specific Password) 而不是你的登录密码。请查阅你邮箱服务商的文档了解如何生成它。

## 步骤 4: 自定义邮件内容 (send-emails.yml)

打开 `.github/workflows/send-emails.yml` 文件，你可以根据需求修改以下几个部分：

SMTP 服务器配置:

### SMTP服务器配置(重要)

- server_address: mail12.serv00.com # 修改为你的邮箱SMTP服务器地址

- server_port: 587                # 修改为你的服务器端口

发件人、主题和正文:

### 邮件内容

subject: "FBI" # <-- 修改邮件主题

### 收件人和发件人
to: ${{ matrix.recipient.email }}    #csv文件修改收件人地址

from: FBI <${{ secrets.MAIL_USERNAME }}> # <-- 修改发件人名称

### 使用 html_body 直接发送 HTML 格式的邮件

html_body: |
  <h3>紧急调查通知</h3>
  <hr>
  <p>你好, <strong>${{ matrix.recipient.name }}</strong> 先生,</p>
  <!-- 在这里修改你的邮件正文 -->
  <p><img src="https://imge.ssss.bio/file/1758472981046_屏幕截图_2025-09-14_223546.png" alt="屏幕截图 2025-09-14 223546.png" width=100%></p>
  <p>更多详情请<a href="https://www.fbi.gov">点击此处访问官网</a>。</p>
  <p>请尽快与我们联系。</p>
  <p><em>此致,</em><br><em>FBI</em></p>

# ▶️ 如何发送邮件
所有配置完成后，发送邮件的步骤非常简单：

进入你的 GitHub 仓库页面，点击顶部的 Actions 标签。

在左侧的工作流列表中，点击 Send Bulk Emails Workflow。

你会看到一个 "This workflow has a workflow_dispatch event" 的提示。点击右侧的 Run workflow (运行工作流) 按钮。

会弹出一个小窗口，直接点击绿色的 Run workflow 按钮即可。
