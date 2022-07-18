from flask import jsonify, request
from app import db
import uuid


class Template:

    def create(self):

        fields = request.json
        #Create template object
        template = {
            '_id': uuid.uuid4().hex,
            'template_name': fields['template_name'],
            'subject': fields['subject'],
            'body': fields['body']
        }
        filter = { 'template_name': fields['template_name'] }

        #Check for an existing template_name
        if db.templates.find_one(filter):
            return jsonify({ "error": "A template with this name already exists!" })

        #Non empty field validation
        if fields['template_name'] and fields['subject'] and fields['body']:
            db.templates.insert_one(template)
            return jsonify(template), 201
        else:
            return jsonify({ "error": "Missing Field(s)!" }), 400

    def get_all(self):

        container = []
        collection = db.templates
        documents = collection.find({})

        #Check if template exists
        if collection.count_documents({}) == 0:
            return jsonify({ "message": "There are no templates currently" }) 

        for doc in documents:
            container.append(doc)
        return jsonify( container )

    def get_one(self, template_id):

        filter = { "_id": template_id }
        template = db.templates.find_one(filter)
        
        if not template:
            return jsonify({ "error": "template does not exist!" })

        return jsonify( template )

    def update_one(self, template_id):

        try:
            fields = request.json
            filter = {'_id': template_id}
            new_values = {
                "$set": { 'template_name': fields['template_name'], 'subject': fields['subject'], 'body': fields['body'] },
            }
            template = db.templates.find_one({ "_id": template_id })

            #Check if templates exists
            if not template:
                return jsonify({ "error": "template does not exist!" })

            db.templates.update_many(filter, new_values)

            return jsonify(template)
        
        except KeyError:
            return jsonify({ "error": "Missing Fields!" })

        except:
            return jsonify({ "error": "Special Error" })

    def delete_one(self, template_id):

        filter = { '_id': template_id }

        #Check if template exists
        if not db.templates.find_one(filter):
            return jsonify({ "error": "template does not exist!" })

        db.templates.find_one_and_delete(filter, projection=None, sort=None)
        return jsonify({"message": "Successfully Deleted"})
