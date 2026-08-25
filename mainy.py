import requests

url =  "https://www.aicpb.com/en/ai-rankings/products/ai-chatbot-rankings/websites"

response = requests.get(url, timeout=30)

print("Status:", response.status_code)
print("URL:", response.url)
print("Length:", len(response.text))
print("Error:", response.text[:500])