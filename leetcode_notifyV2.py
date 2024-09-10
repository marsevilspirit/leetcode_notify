import subprocess
import requests
import json

# 常量定义
USERNAME = "username"
NOTIFY_HEAD = "example"
NOTIFY_TITLE = "LeetCode刷题提醒"
NOTIFY_ICON = "/home/mars/utils/leetcode_logo.png"
NOTIFY_TIMEOUT = 8000
GRAPHQL_URL = "https://leetcode.cn/graphql/"
HEADERS = {'Content-Type': 'application/json'}

# GraphQL 查询和变量
QUERY = """
query userProfileUserQuestionProgressV2($userSlug: String!) { 
    userProfileUserQuestionProgressV2(userSlug: $userSlug) { 
        numAcceptedQuestions { 
            count  
            difficulty 
        } 
    } 
}
"""
VARIABLES = {"userSlug": USERNAME}

# 生成消息内容
def generate_message(number):
    return f"你现在刷了{number}道题，继续保持。"

# 发送通知
def send_notification(title, message, icon=None, timeout=None, head=None):
    command = ['notify-send']
    if icon:
        command.extend(['-i', icon])
    if timeout:
        command.extend(['-t', str(timeout)])
    if head:
        command.extend(['-a', str(head)])
    command.extend([title, message])
    subprocess.run(command)

# 获取leetcode的题目数量
def get_leetcode_number():
    payload = {
        "query": QUERY,
        "variables": VARIABLES,
        "operationName": "userProfileUserQuestionProgressV2"
    }
    
    try:
        response = requests.post(GRAPHQL_URL, headers=HEADERS, data=json.dumps(payload))
        response.raise_for_status()  # 检查响应状态
        data = response.json()
        
        # 提取题目数量
        questions = data["data"]["userProfileUserQuestionProgressV2"]["numAcceptedQuestions"]
        total_count = sum(question['count'] for question in questions)
        return total_count
    
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
        return None

if __name__ == "__main__":
    number = get_leetcode_number()
    
    if number is not None:
        # 生成通知消息
        notify_message = generate_message(number)
        send_notification(NOTIFY_TITLE, notify_message, NOTIFY_ICON, NOTIFY_TIMEOUT, NOTIFY_HEAD)
    else:
        # 网络错误通知
        send_notification("网络有问题", "网络有问题, 请检查网络连接", NOTIFY_ICON, NOTIFY_TIMEOUT, NOTIFY_HEAD)
