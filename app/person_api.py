from flask import Blueprint, jsonify, request
from database_manager import DatabaseManager
from person_service import PersonService
from random_user_api import RandomUserApi
from pony.orm import *

person_api_blueprint = Blueprint('person_api', __name__)
db = DatabaseManager().initialize_database()
person_service = PersonService(db)

@person_api_blueprint.route('/api/persons', methods=['POST'])
def add_new_person():
    json = request.get_json()
    new_person = person_service.add_person(dict(first_name=json['first_name'], last_name=json['last_name']))
    response = jsonify(new_person.to_dict())
    response.status_code = 201
    return response

@person_api_blueprint.route('/api/persons/<int:person_id>', methods=['DELETE'])
def remove_person(person_id):
    try:
        person_service.remove_person(person_id)
        return ('', 204)
    except ObjectNotFound:
        return ('', 404)

@person_api_blueprint.route('/api/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = person_service.get_person_by_id(person_id)
    if person:
        response = jsonify(person.to_dict())
        response.status_code = 200
        return response
    else:
        return ('', 404)

@person_api_blueprint.route('/api/persons/list', methods=['GET'])
def list_all_persons():
    all_persons = person_service.list_all_persons()
    all_persons = map(lambda x:x.to_dict(), all_persons)
    response = jsonify(all_persons)
    response.status_code = 200
    return response

@person_api_blueprint.route('/api/persons/import/random', methods=['POST'])
def import_random_person():
    random_person = RandomUserApi().get_random_person()
    new_person = person_service.add_person(random_person)
    response = jsonify(new_person.to_dict())
    response.status_code = 201
    return response
