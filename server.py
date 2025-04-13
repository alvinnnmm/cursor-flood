from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flood_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Should use a secure key in production

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class FloodRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.JSON, nullable=False)
    date = db.Column(db.Date, nullable=False)
    river_level = db.Column(db.Float)
    flood_occurred = db.Column(db.Boolean, nullable=False)
    weather_conditions = db.Column(db.JSON)
    affected_areas = db.Column(db.String(200))
    comments = db.Column(db.String(500))

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.password == data['password']:  # Note: Should use password hashing in production
        access_token = create_access_token(identity=user.username)
        return jsonify({
            'access_token': access_token,
            'user': {'id': user.id, 'username': user.username}
        }), 200
        
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/history/add', methods=['POST'])
@jwt_required()
def add_flood_record():
    """Add a new flood record"""
    data = request.get_json()
    
    try:
        record = FloodRecord(
            location=data['location'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            river_level=data.get('river_level'),
            flood_occurred=data['flood_occurred'],
            weather_conditions=data.get('weather_conditions', {}),
            affected_areas=data.get('affected_areas', ''),
            comments=data.get('comments', '')
        )
        
        db.session.add(record)
        db.session.commit()
        
        return jsonify({'message': 'Flood record added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/history/all', methods=['GET'])
@jwt_required()
def get_all_flood_records():
    """Get all flood records"""
    try:
        records = FloodRecord.query.order_by(FloodRecord.date).all()
        return jsonify([{
            'id': record.id,
            'location': record.location,
            'date': record.date.strftime('%Y-%m-%d'),
            'river_level': record.river_level,
            'flood_occurred': record.flood_occurred,
            'weather_conditions': record.weather_conditions,
            'affected_areas': record.affected_areas,
            'comments': record.comments
        } for record in records]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create test user if not exists
        if not User.query.filter_by(username='yapa920@gmail.com').first():
            user = User(username='yapa920@gmail.com', password='Alvin1234567')
            db.session.add(user)
            db.session.commit()
    
    app.run(host='127.0.0.1', port=5000, debug=True) 