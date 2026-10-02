from flask import Flask, request, jsonify
from .core import merge_pdfs

app = Flask(__name__)

@app.get('/')
def index():
    return '<h1>PDF Split and Merge</h1><p>Use the CLI for full functionality.</p>'

@app.post('/merge')
def merge():
    data = request.get_json(force=True)
    result = merge_pdfs(data['inputs'], data['output'])
    return jsonify({'output_files': result.output_files, 'warnings': result.warnings})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
