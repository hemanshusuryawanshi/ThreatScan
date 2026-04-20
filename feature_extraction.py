import urllib.parse
import re

def extract_features(url):
    """
    Extracts lexical features from a URL string to be used for ML classification.
    """
    features = {}
    
    # Basic URL length features
    features['url_length'] = len(url)
    
    # Parse URL 
    try:
        parsed_url = urllib.parse.urlparse(url)
        hostname = str(parsed_url.hostname)
        path = str(parsed_url.path)
    except:
        hostname = ""
        path = ""
        
    features['hostname_length'] = len(hostname)
    features['path_length'] = len(path)
    
    # Character counts in the URL
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_at'] = url.count('@')
    features['num_question_marks'] = url.count('?')
    features['num_ampersands'] = url.count('&')
    features['num_equals'] = url.count('=')
    features['num_slashes'] = url.count('/')
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_parameters'] = url.count('&') + (1 if url.count('?') > 0 else 0)
    
    # Suspicious words often found in phishing or malicious URLs
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'banking', 
                        'confirm', 'free', 'bonus', 'admin', 'client', 'paypal', 'support']
    
    for word in suspicious_words:
        features[f'has_word_{word}'] = 1 if word in url.lower() else 0
        
    # Check if the hostname is an IP Address (common in malware/phishing)
    # A simple regex for IPv4
    ip_pattern = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    features['is_ip_address'] = 1 if ip_pattern.match(hostname) else 0
    
    # Check for HTTP (not HTTPS)
    features['is_http'] = 1 if url.startswith('http://') else 0
    features['is_https'] = 1 if url.startswith('https://') else 0
    
    # Check for shorteners (e.g., bit.ly, t.co)
    shorteners = ['bit.ly', 'goo.gl', 't.co', 'tinyurl.com', 'ow.ly', 'is.gd', 'buff.ly', 'adf.ly', 'bit.do']
    features['uses_shortener'] = 1 if any(short in hostname for short in shorteners) else 0
    
    return features
