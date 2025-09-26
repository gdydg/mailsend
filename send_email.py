# 文件路径: send_email.py
# 描述: 这是一个使用 Python 发送邮件的脚本，现已升级以支持多个附件。

import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def attach_file(msg, attachment_path):
    """一个辅助函数，用于将单个文件附加到邮件中"""
    try:
        with open(attachment_path, 'rb') as attachment:
            filename = os.path.basename(attachment_path)
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            
            # 为内嵌图片添加 Content-ID (cid)
            # 只有当文件名是 screenshot.png 时，我们才假定它是要内嵌的图片
            if filename == "screenshot.png":
                part.add_header('Content-ID', f'<{filename}>')
            
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            msg.attach(part)
            print(f"附件 '{filename}' 已成功附加。")
    except FileNotFoundError:
        print(f"警告：附件文件未找到于路径 '{attachment_path}'，已跳过。")
    except Exception as e:
        print(f"附加文件 '{attachment_path}' 时出错: {e}")

def send_email():
    # --- 邮件配置 ---
    username = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    server_address = "mail12.serv00.com"
    server_port = 587
    from_name = "FBI"
    from_addr = username
    subject = "【多附件更新】来自 FBI"

    # --- 从命令行参数获取信息 ---
    if len(sys.argv) < 3:
        print("错误：需要提供收件人邮箱和姓名作为参数。")
        sys.exit(1)

    to_addr = sys.argv[1]
    to_name = sys.argv[2]
    
    # 第四个参数现在是逗号分隔的附件列表字符串
    attachment_paths_str = sys.argv[3] if len(sys.argv) > 3 else ""

    # --- 构造邮件正文 (HTML) ---
    html_body = f"""
    <h3>紧急调查通知</h3>
    <hr>
    <p>你好, <strong>{to_name}</strong> 先生,</p>
    <p>我们注意到一些需要您配合调查的情况。您可能涉嫌违反了佛罗里达州的相关法律。</p>
    <p><strong>具体事项如下:</strong></p>
    <ul>
      <li>涉嫌浏览并传播限制内容。</li>
      <li>需要您前来警局进行情况说明。</li>
    </ul>
    <p>相关证据材料（内嵌图片和附件）如下：</p>
    <p><img src="cid:screenshot.png" alt="证据截图" style="width: 400px; height: auto;"></p>
    <p>更多详情请<a href="https://www.fbi.gov">点击此处访问官网</a>。</p>
    <p>请尽快与我们联系。</p>
    <p><em>此致,</em><br><em>FBI</em></p>
    """

    # --- 创建邮件对象 ---
    msg = MIMEMultipart()
    msg['From'] = f"{from_name} <{from_addr}>"
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    # --- 附加所有文件 ---
    if attachment_paths_str:
        # 按逗号分割字符串，得到一个附件路径列表
        attachment_list = [path.strip() for path in attachment_paths_str.split(',')]
        for path in attachment_list:
            if path: # 确保路径不为空
                attach_file(msg, path)

    # --- 发送邮件 ---
    try:
        server = smtplib.SMTP(server_address, server_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        print(f"邮件已成功发送至 {to_addr}")
    except Exception as e:
        print(f"邮件发送失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    send_email()
