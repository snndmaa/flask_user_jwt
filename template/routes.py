from app import app
from template.models import Template
from token_required import token_required

@app.route('/template/', methods=['POST'])
@token_required
def create_template():
    return Template().create()

@app.route('/template/', methods=['GET'])
@token_required
def get_templates(current_user):
    return Template().get_all()

@app.route('/template/<template_id>', methods=['GET'])
@token_required
def get_template(current_user, template_id):
    return Template().get_one(template_id)

@app.route('/template/<template_id>', methods=['PUT'])
@token_required
def update_template(current_user, template_id):
    return Template().update_one(template_id)

@app.route('/template/<template_id>', methods=['DELETE'])
@token_required
def delete_template(current_user, template_id):
    return Template().delete_one(template_id)