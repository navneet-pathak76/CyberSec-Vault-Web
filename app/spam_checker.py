import re

def is_spam_message(message):
    spam_keywords = [
        'win', 'free', 'prize', 'lottery', 'urgent', 'congratulations', 'act now',
        'limited time', 'guaranteed', 'click here', 'exclusive deal', 'money back',
        'urgent reply', 'cheap', 'get rich', 'make money fast', 'work from home',
        'credit card', 'instant loan', 'zero interest', 'risk-free', 'claim', '100% free', 'winner'
    ]

    message_lower = message.lower()

    score = sum(keyword in message_lower for keyword in spam_keywords)

    if score >= 5:
        return "High Spam 🔴"
    elif score >= 3:
        return "Medium Spam 🟠"
    elif score >= 1:
        return "Low Spam 🟡"
    else:
        return "Message Seems Legit 🟢"
