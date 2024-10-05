import os
import requests
from flask import jsonify, Blueprint, render_template, request
from .parser import parse_schedule
import sqlite3

bp = Blueprint('routes', __name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'feedback.db')

# Landing Page Route
@bp.route('/')
def landing_page():
    return render_template('landing.html')

@bp.route('/api/schedule', methods=['GET'])
def get_schedule():
    class_name = request.args.get('class_name')
    print(f"Class Name Received: {class_name}")  # Debug log

    if class_name == "AI":
        filename = 'AI_routine.txt'
    elif class_name == "CST":
        filename = 'CST2_routine.txt'
    else:
        return jsonify({"error": "Class not found"}), 404

    schedule_data = parse_schedule(filename)
    return jsonify(schedule_data)

# AI Schedule Route
@bp.route('/schedule/AI', methods=['GET'])
def ai_schedule():
    # Load AI schedule data for the index template
    filename = 'AI_routine.txt'
    schedule_data = parse_schedule(filename)  # Fetch the schedule data
    return render_template('index.html', class_name="AI", schedule=schedule_data)

@bp.route('/schedule/CST', methods=['GET'])
def cst_schedule():
    # Load CST schedule data for the index template
    filename = 'CST2_routine.txt'
    schedule_data = parse_schedule(filename)  # Fetch the schedule data
    return render_template('index.html', class_name="CST Class 2", schedule=schedule_data)

# API route to fetch schedule data dynamically based on the class
@bp.route('/schedule/<class_name>', methods=['GET'])
def schedule(class_name):
    if class_name == "AI":
        filename = 'AI_routine.txt'
    elif class_name == "CST":
        filename = 'CST2_routine.txt'
    else:
        return jsonify({"error": "Class not found"}), 404

    schedule_data = parse_schedule(filename)
    return render_template('index.html', class_name=class_name, schedule=schedule_data)


# Class details page
@bp.route('/class_details', methods=['GET'])
def class_details():
    return render_template('class_details.html')

@bp.errorhandler(404)
def not_found(e):
    return "does not exists", 404

@bp.route('/api/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        category = data.get('category')

        if not name or not email or not message:
            return jsonify({"error": "Missing required fields"}), 400

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (name, email, message, category) VALUES (?, ?, ?, ?)",
            (name, email, message, category)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Feedback submitted successfully!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while submitting feedback."}), 500

@bp.route('/api/admin/feedback', methods=['GET'])
def get_feedback():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, message, category, resolved FROM feedback")
        feedback_items = cursor.fetchall()
        conn.close()

        feedback_list = [
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'message': row[3],
                'category': row[4],
                'resolved': bool(row[5])
            } for row in feedback_items
        ]

        return jsonify(feedback_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to retrieve feedback."}), 500

@bp.route('/api/admin/feedback/<int:feedback_id>/resolve', methods=['POST'])
def resolve_feedback(feedback_id):
    try:
        data = request.get_json()
        resolved = data.get('resolved', False)

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE feedback SET resolved = ? WHERE id = ?", (resolved, feedback_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Feedback updated successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to update feedback."}), 500