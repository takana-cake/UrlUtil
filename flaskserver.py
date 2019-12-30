#v.20191230.1
# -*- coding: utf-8 -*-

from flask import Flask, request, Markup
import sys, os

app = Flask(__name__)

@app.route('/')
def index():
	html = '''
	<form action="/getimgs">
		<p><label>getImgs: </label>
		<input type="text" name="url" value="url" size="30" onclick="this.select(0,this.value.length)">
		<input type="text" name="path" value="Folder name" size="30" onclick="this.select(0,this.value.length)">
		<button type="submit" formmethod="post">POST</button></p>
	</form>
	'''
	return Markup(html)


@app.route('/getimgs', methods=['POST'])
def getimgs():
	try:
		if request.method == 'POST':
			path = request.form['path']
			if os.path.exists(path) is False:
				os.makedirs(path)
			sys.path.append(os.path.dirname(__file__) + "/app")
			import urlutil
			obj = urlutil.Urlutil()
			obj.getImgs(request.form['url'], path)
			return request.form['url'] + '</br><a href="#" onclick="history.back(); return false;">back</a>'
		else:
			return request.args.get('url', '') + '</br><a href="#" onclick="history.back(); return false;">back</a>'
	except Exception as e:
		return str(e) + '</br><a href="#" onclick="history.back(); return false;">back</a>'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
