import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

def scrape_website(url):
    result = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract relevant information from the web page
    # Modify this code to suit your scraping needs
    # Here, we are extracting all the text within <p> tags
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        result.append(p.get_text())

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website_url = request.form['website_url']
        scraped_data = scrape_website(website_url)
        return render_template('index.html', data=scraped_data)

    return render_template('form.html')

@app.route('/download', methods=['POST'])
def download():
    scraped_text = request.form['scraped_text']
    
    # Save the scraped text to a temporary file
    with open('scraped_data.txt', 'w') as file:
        file.write(scraped_text)
    
    # Send the file for download
    return send_file('scraped_data.txt', as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)