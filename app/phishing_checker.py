import re

def is_phishing_url(url):
    url = url.lower()
    phishing_keywords = [
        'login', 'verify', 'update', 'secure', 'free', 
        'bank', 'account', 'paypal', 'confirm', 'password'
    ]

    if '@' in url:
        return "Dangerous 🔴 (Contains '@' symbol)"

    if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
        return "Dangerous 🔴 (Uses IP address)"

    if len(url) > 75:
        return "Suspicious 🟠 (Unusually long URL)"

    if any(keyword in url for keyword in phishing_keywords):
        return "Suspicious 🟠 (Contains suspicious keywords)"

    return "Safe 🟢"
