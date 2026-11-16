# tools/test_server.py
import urllib.request

url = 'http://127.0.0.1:8000/app/index.html'
try:
    with urllib.request.urlopen(url) as resp:
        print('HTTP Status:', resp.status)
        content = resp.read().decode('utf-8')
        print('Content length:', len(content))
        for token in ['id="view-home"', 'id="view-chat"', 'id="view-phone"', 'id="view-docs"', 'id="view-whiteboards"', 'id="view-clips"', 'id="wpMoreAppsPopover"', 'id="wpAppSuiteModalDialog"']:
            print(f'  {token}: {token in content}')
except Exception as e:
    print('Request error:', e)
