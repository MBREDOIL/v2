from http.server import BaseHTTPRequestHandler
from io import BytesIO
import json
import aiohttp
from bs4 import BeautifulSoup
import asyncio

class handler(BaseHTTPRequestHandler):
    async def fetch_results(self):
        try:
            url = "http://14.139.56.104"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    table = soup.find('table', {'id': 'ResultList'})
                    results = []
                    
                    for row in table.find_all('tr')[1:]:  # Skip header
                        cols = row.find_all('td')
                        if len(cols) >= 2:
                            link = cols[1].find('a')
                            if link:
                                results.append({
                                    'name': link.text.strip(),
                                    'url': link['href']
                                })
                    return results[:50]  # Limit to 50 results
        except Exception as e:
            print(f"Error fetching results: {str(e)}")
            return []

    def do_GET(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            results = loop.run_until_complete(self.fetch_results())
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'status': 'success',
                'results': results
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'error',
                'message': str(e)
            }
            self.wfile.write(json.dumps(response).encode())
        finally:
            loop.close()
