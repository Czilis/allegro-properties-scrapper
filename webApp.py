from flask import (
    Flask,
    render_template,
    request)

from Formatter import format_table_for_shop
from Parser import Parser

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    __formattedHtml = ""
    if request.method == 'POST':
        link = request.form['link']
        parser = Parser()
        __parsedParameters = parser.parse_product_parameter(link)
        __formattedHtml = format_table_for_shop(__parsedParameters)

    return render_template('page.html', generatedTable=__formattedHtml)
