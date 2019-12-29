#v.20191230.0
# -*- coding: utf-8 -*-

from flask import Flask, request, Markup

app = Flask(__name__)

@app.route('/')
def index():
	html = '''
	<form action="/test">
		<p><label>test: </label>
		<input type="text" name="url" value="url" size="30">
		<input type="text" name="path" value="path" size="30">
		<button type="submit" formmethod="get">GET</button>
		<button type="submit" formmethod="post">POST</button></p>
	</form>
	'''
	return Markup(html)


@app.route('/test', methods=['GET', 'POST'])
def test():
	try:
		if request.method == 'POST':
			import urlutil
			obj = urlutil.Urlutil()
			getImgs(request.form['url'], request.form['path'])
			return request.form['url']
		else:
			print(request.headers)
			print(request.get_data())
			return request.args.get('url', '')
	except Exception as e:
		return str(e)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
