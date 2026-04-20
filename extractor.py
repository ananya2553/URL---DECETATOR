import re
from tldextract import extract

def get_url_features(url):
    features = {}
    url = str(url)
    
    # URL parsing using tldextract
    ext = extract(url)
    # Domain aur Subdomain ki length alag se check karna zaruri hai
    features['subdomain_len'] = len(ext.subdomain)
    features['domain_len'] = len(ext.domain)
    
    # 1. Length features
    features['url_length'] = len(url)
    
    # 2. Character counts (Revised list)
    features['dot_count'] = url.count('.')
    features['hyphen_count'] = url.count('-')
    features['at_count'] = url.count('@')
    features['slash_count'] = url.count('/')
    
    # 3. Security & IP Check
    features['is_https'] = 1 if url.startswith('https') else 0
    ip_pattern = r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    features['is_ip'] = 1 if re.search(ip_pattern, url) else 0
    
    # 4. Digit features
    digits = sum(c.isdigit() for c in url)
    features['digit_ratio'] = digits / len(url) if len(url) > 0 else 0
    
    # 5. Suspicious Words
    suspicious_words = ['login', 'verify', 'update', 'bank', 'free', 'win']
    features['suspicious_words_count'] = sum(1 for word in suspicious_words if word in url.lower())

    return features
