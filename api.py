from typing import Optional
from flask import Flask
from flask_restful import Resource, Api
import db
from loguru import logger
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

class Documents(Resource):
    def get(self, document_id: Optional[int] = None ):
        try:
            if document_id is None:
                logger.debug("call /documents ")
                documents = db.get_documents()
                return {'status': 200, 'data': documents}, 200
            else:
                logger.debug(f"call /documents with params  {document_id}")
                document = db.get_documents(document_id)
                if len(document)  == 0:
                    return {'status': 404, 'errors': 'Document not found'}, 404
                return {'status': 200, 'data': document}, 200
        except db.DatabaseError as e:
            return {'status': 500, 'errors': str(e)}, 500

class DocumentsByTag(Resource):
    def get(self, tag_id):
        try:
            logger.debug(f"call /tags/{tag_id}/documents")
            documents = db.get_tag_by_document_id(tag_id)
            if not documents:
                return {'status': 404, 'errors': 'No documents found for the given tag'}, 404
            return {'status': 200, 'data': documents}, 200
        except db.DatabaseError as e:
            return {'status': 500, 'errors': str(e)}, 500


class AllDocument(Resource):
    def get(self, document_id: Optional[int] = None ):
        try:
            if document_id is None:
                logger.debug("call /all ")
                documents = db.get_all_documents()
            else:
                logger.debug(f"call /all with params  {document_id}")
                documents = db.get_all_documents(document_id)
            if not documents:
                return {'status': 404, 'errors': 'No documents found for the given tag'}, 404
            return {'status': 200, 'data': documents}, 200
        except db.DatabaseError as e:
            return {'status': 500, 'errors': str(e)}, 500



# Ajouter une route pour récupérer les documents par tag
api.add_resource(DocumentsByTag, '/tags/<int:tag_id>/documents')
api.add_resource(Documents,'/documents' ,  '/documents/<int:document_id>')
api.add_resource(AllDocument, '/all','/all/<int:document_id>')



if __name__ == '__main__':
    app.run(debug=True, port=7003)