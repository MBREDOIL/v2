from http.server import BaseHTTPRequestHandler
import json
import requests
from bs4 import BeautifulSoup

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Fetch results from university website
            response = requests.get("http://14.139.56.104", timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'id': 'ResultList'})
            results = []
            
            for row in table.find_all('tr')[1:5]:  # Only first 5 results for testing
                cols = row.find_all('td')
                if len(cols) >= 2:
                    link = cols[1].find('a')
                    if link:
                        results.append({
                            'name': link.text.strip(),
                            'url': link['href']
                        })

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'success',
                'results': results
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'error',
                'message': str(e)
            }).encode())
