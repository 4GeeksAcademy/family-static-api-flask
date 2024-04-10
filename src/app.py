import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/member', methods=['POST'])
def add_a_member():
    try:
        request_body = request.json
        member = jackson_family.add_member(request_body)
        if member is None:
            return jsonify({'msg': 'Member not found'}), 404
        return jsonify(member), 200
    except:
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_a_member(id):
    try:
        members = jackson_family.delete_member(id)
        if members is None:
            return jsonify({'msg': 'Member not found'}), 404
        return jsonify(members), 200 
    except:
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/member/<int:id>', methods=['GET'])
def get_member_info(id):
    try:
        member = jackson_family.get_member(id)
        if member is None:
            return jsonify({'msg': 'Member not found'}), 404
        return jsonify(member), 200
    except:
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/members', methods=['GET'])
def get_members_info():
    try:
        members = jackson_family.get_all_members()
        if members == []:
            return jsonify({'msg': 'Members not found'}), 404
        return jsonify(members), 200
    except:
        return jsonify({'error': 'Internal Server Error'}), 500
    
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
