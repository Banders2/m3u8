from flask import Flask, request
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import m3u8

app = Flask(__name__)

def getM3u8Links(network_requests):
    m3u8Links = {}
    for n in network_requests:
        if ".m3u8" in n["name"]:
            m3u8Links[n["name"]] = n["name"]
    return m3u8Links

@app.route('/', methods=['GET'])
def getPlayitasPrices():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    args = request.args
    target = args.get("target", default="", type=str)
    m3u8Html = ""
    if(target):
        driver.get(target)
        time.sleep(5)
        JS_get_network_requests = "var performance = window.performance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
        network_requests = driver.execute_script(JS_get_network_requests)
        m3u8Links = getM3u8Links(network_requests)
        for m3u8Link in m3u8Links:
            m3u8Html += f'<a href="{m3u8Link}">{m3u8Link}</a><br><br>'
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