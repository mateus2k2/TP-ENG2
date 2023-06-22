from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended import current_user
from app.models.user import UserModel
from app.config.db import db


class UserLogin(Resource):
    def __init__(self):
        pass

    parser = reqparse.RequestParser() 
    parser.add_argument('email', type=str, required=True, help='Not Blank')
    parser.add_argument('password', type=str, required=True, help='Not Blank')

    def post(self):
        data = UserLogin.parser.parse_args()
        email = data['email']
        password = data['password']

        user = db.session.query(UserModel).filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return {'status': 'Login failed.'}, 401
        
        access_token = create_access_token(identity={"user": user.email})
        # access_token = create_access_token(identity=json.dumps(user, cls=AlchemyEncoder))
        return jsonify(
            token=access_token,
            status="APPROVED"
        )


class UserRegister(Resource):
    def __init__(self):
        # self.logger = create_logger()
        pass

    parser = reqparse.RequestParser()  
    parser.add_argument('email', type=str, required=True, help='Not Blank')
    parser.add_argument('password', type=str, required=True, help='Not Blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {'message': 'user has already been created.'}, 400

        user = UserModel(**data)
        user.set_password(data['password'])  
        user.save_to_db()

        return {'message': 'user has been created successfully.'}, 201
