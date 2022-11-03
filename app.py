from flask import Flask, request
import time
# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import m3u8
from seleniumwire import webdriver
import json

app = Flask(__name__)

debug = False

def saveRequestsAsFile(requests):
  networklist = []
  for networkRequest in requests:
    network = {
          'url':networkRequest.url,
          'headers': headerValue(networkRequest.response.headers) ,
      }
    networklist.append(network)

  networkJson = json.dumps(networklist)
  f = open("network.json", "a")
  f.write(networkJson)
  f.close()

def getM3u8Links(network_requests):
  m3u8Links = {}
  for n in network_requests:
    if ".m3u8" in n["name"]:
      m3u8Links[n["name"]] = n["name"]
  return m3u8Links

def headerValue(headersInput):
  headers = []
  if (headersInput == None):
    return headers
  for header in headersInput.items():
    headers.append(f'{header[0]} : {header[1]}')
  return headers

@app.route('/', methods=['GET'])
def getPlayitasPrices():
  options = Options()
  # https://stackoverflow.com/questions/29916054/change-user-agent-for-selenium-web-driver
  # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
  options.headless = True
  driver = webdriver.Chrome(options=options)
  args = request.args
  target = args.get("target", default="", type=str)
  m3u8Html = ""
  if(target):
    driver.get(target)
    driver.save_screenshot("ss1.png")
    agent = driver.execute_script("return navigator.userAgent")
    print(agent)
    time.sleep(10)
    JS_get_network_requests = "var performance = window.performance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
    network_requests = driver.execute_script(JS_get_network_requests)
    driver.save_screenshot("ss2.png")
    print(network_requests)
    m3u8Links = getM3u8Links(network_requests)
    for m3u8Link in m3u8Links:
      m3u8Html += f'<a href="{m3u8Link}">{m3u8Link}</a><br><br>'

    if(debug):
      saveRequestsAsFile(driver.requests)

  driver.close()
  return f'''
  <html>
      <head>
      </head>
      <body>
          <form action="/">
              <input type="text" name="target" value="{target}" placeholder="target website"><br>
              <input type="submit" value="Submit">
          </form>
          {m3u8Html}
      </body>
  </html>
  '''

if __name__ == '__main__':
  app.run()