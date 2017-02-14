import os
import os.path
import json
from flask import Flask, request, redirect, jsonify

app = Flask(__name__, static_folder='static')

image_folder = 'uncropped'

lion_faces = [
    image_folder + '/' + x
    for x in os.listdir('static/' + image_folder)
    if x.lower().endswith('.jpg')]


@app.route('/')
def hello():
    return redirect("/static/train.html", code=302)


@app.route('/next', methods=['POST'])
def next_annotation():
    global lion_faces
    annotation_idx = request.get_json().get('annotation_idx')
    path = 'static/' + lion_faces[annotation_idx] + '.json'
    annotation_exists = False
    try:
        with open(path) as f:
            roi = json.load(f)['roi']
            if len(roi) > 0:
                annotation_exists = True
    except:
        pass
    if annotation_idx < len(lion_faces):
        return jsonify({
            'img_url': lion_faces[annotation_idx],
            'annotation_exists': annotation_exists
        }), 200
    else:
        return jsonify({'status': 'error', 'info': 'exceeded max idx'}), 400


@app.route('/annotation', methods=['POST'])
def annotation_post():
    j = request.get_json()
    roi = j.get('roi')
    if isinstance(roi, list) and len(roi) > 0:  # only save a json if 1+ annotations were created 
        fname = 'static/' + lion_faces[j['annotation_idx']] + '.json'
        with open(fname, 'w') as f:
            json.dump(j, f)
    return jsonify(ok=True), 200


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
