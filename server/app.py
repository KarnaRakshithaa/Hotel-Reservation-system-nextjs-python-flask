
from flask import Flask, render_template, request, jsonify, url_for  # Add this import statement
import mysql.connector
from queries import delete_old_bookings, delete_staff_details, display_customer, display_reservations, display_rooms, display_staff_details, insert_customer_details, insert_rooms, insert_staff_details, rooms_available, select_rooms
from flask_cors import CORS



import os
import google.generativeai as genai

genai.configure(api_key ='AIzaSyBfzHhBvP6ZLmSIiW8Gb91uuLEJF2RfKpo')
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()
app = Flask(__name__)



# @app.route('/')
# def enter_dates():
#     return render_template('enter_dates.html')




# @app.route('/manager_login')
# def manager_login():
#     return render_template('manager_login.html')








CORS(app, resources={r"/api/*": {"origins": "*"}})

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="60756075",
    database="LOL",
  
)

mycursor=db.cursor()




def send_to_chatbot():
    query='SELECT * FROM Room'
    mycursor.execute(query)
    result=mycursor.fetchall()
    room_message = "\n".join([f"Room Number: {room[0]}, Cost: {room[1]}, Room-Type: {room[2]}, Bed-Size: {room[3]}, Hotel Id: {room[4]}" for room in result])
    chat.send_message(room_message)
    query='SELECT * FROM Customer'
    mycursor.execute(query)
    result=mycursor.fetchall()
    cust_message = "\n".join([f"Customer id: {customer[0]}, Name: {customer[1]}, Phone: {customer[2]}, Address: {customer[3]} " for customer in result])
    chat.send_message(cust_message)
    query='SELECT * FROM Reservation'
    mycursor.execute(query)
    result=mycursor.fetchall()
    res_message = "\n".join([f"Reservation id: {reservation[0]}, Start Date: {reservation[1]}, End Date: {reservation[2]}, Customer ID: {reservation[3]}, Room Number: {reservation[4]} " for reservation in result])
    chat.send_message(res_message)
    query='SELECT * FROM Hotel'
    mycursor.execute(query)
    result=mycursor.fetchall()
    hotel_message = "\n".join([f"Hotel id: {hotel[0]}, Name: {hotel[1]}, Location: {hotel[2]}, Manager_ID: {hotel[3]}" for hotel in result])
    chat.send_message(hotel_message)
    query='SELECT * FROM Hotel_Staff'
    mycursor.execute(query)
    result=mycursor.fetchall()
    staff_message = "\n".join([f"Staff id: {staff[0]}, Name: {staff[1]}, Address: {staff[2]}, Salary: {staff[3]}, Gender: {staff[4]}, Hotel ID: {staff[5]}, DOB: {staff[6]}" for staff in result])
    chat.send_message(staff_message)
    print('message sent to chatbot')



# @app.route('/')
# def enter_dates():
#     return render_template('enter_dates.html')


@app.route("/chatbot")
def chatbotpage():
    send_to_chatbot()
    return render_template("chatbot.html")

@app.route("/getchatbotresponse", methods=['POST'])
def getchatbotresponse():
    message = request.json["message"]
    response = generate_content(message)
    return jsonify({"response": response})

def generate_content(message):
    global chat
    return chat.send_message(message).candidates[0].content.parts[0].text

@app.route('/api/addCustomer', methods=['POST'])
def addCustomer():
    try:
        # Extracting data from JSON body of the request
        data = request.json
        name = data['name']
        phone = data['phone']
    
        address = data['address']


        
        # Correctly calling the function with all required parameters
        insert_customer_details(mycursor, name, phone, address)
        db.commit()

        return jsonify({'success': True, 'message': 'New staff member added successfully'}), 201
    except Exception as e:
        print(f"Error inserting new staff member: {e}")
        db.rollback()
        return jsonify({'success': False, 'message': 'Failed to add customer member'}), 500
    


@app.route('/api/addStaff', methods=['POST'])
def addStaff():
    try:
        # Extracting data from JSON body of the request
        data = request.json
        name = data['name']
        address = data['address']
        salary = data['salary']
        gender = data['gender']
        hotel_id = data['hotel_id']
        dob = data['dob']
        
        # Correctly calling the function with all required parameters
        insert_staff_details(mycursor, name, address, salary, gender, hotel_id, dob)
        db.commit()

        return jsonify({'success': True, 'message': 'New staff member added successfully'}), 201
    except Exception as e:
        print(f"Error inserting new staff member: {e}")
        db.rollback()
        return jsonify({'success': False, 'message': 'Failed to add staff member'}), 500



@app.route('/api/viewReservations', methods=['GET'])
def viewReservations():
    reservations_data = display_reservations(mycursor)
    return jsonify(reservations_data)

@app.route('/api/cancel_booking', methods=['DELETE'])
def cancel_booking():
    data = request.json
    print(data)
    reservation_id = data['reservation_id']

    try:
        query = "DELETE FROM reservation WHERE id = %s"
        mycursor.execute(query, (reservation_id,))
        db.commit()
        return jsonify({'success': True, 'message': f"Reservation {reservation_id} cancelled successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500





# @app.route('/api/delete_old_reservations', methods=['DELETE'])
# def delete_old_reservations_api():
#     try:
#         delete_old_bookings(mycursor)  # No need to pass the cursor if it's globally available
#         db.commit()  # Make sure to commit the transaction to apply changes
#         return jsonify({'success': True, 'message': 'Old reservations deleted successfully'}), 200
#     except Exception as e:
#         db.rollback()  # Rollback in case of any exception
#         print(e)  # For debugging
#         return jsonify({'success': False, 'message': str(e)}), 500
 


@app.route('/api/addRoom', methods=['POST'])
def add_room():
    try:
        data = request.json
        cost = data['cost']
        room_type = data['roomType']
        bed_size = data['bedSize']
        hotel_id = data['hotelId']

        query = "INSERT INTO Room (cost, room_type, bed_size, hotel_id) VALUES (%s, %s, %s, %s)"
        mycursor.execute(query, (cost, room_type, bed_size, hotel_id))
        db.commit()

        return jsonify({'success': True, 'message': 'Room added successfully'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': 'Failed to add room', 'error': str(e)}), 500




@app.route('/api/viewRooms', methods=['GET'])
def viewRooms():
    available_rooms_data = display_rooms(mycursor)
    # Convert the tuple data into a list of dictionaries to jsonify it properly

    return jsonify(available_rooms_data)

@app.route('/api/available_rooms', methods=['GET'])
def available_rooms():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    available_rooms_data = rooms_available(mycursor, start_date, end_date)
    # Convert your data to a JSON-serializable format if necessary
    return jsonify(available_rooms_data) 

@app.route('/api/book_room', methods=['POST'])
def book_room():
    data = request.json
    start_date = data['start_date']
    end_date = data['end_date']
    room_no = data['room_no']
    Cid = data['Cid']

    try:
        query = """INSERT INTO Reservation (start_date, end_date, Cid, room_no) 
                   VALUES (%s, %s, %s, %s)"""
        mycursor.execute(query, (start_date, end_date, Cid, room_no))
        db.commit()
        reservation_id = mycursor.lastrowid
        return jsonify({'success': True, 'reservation_id': reservation_id}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
  
@app.route('/api/customers', methods=['GET'])
def viewCustomers():
    customer_data = display_customer(mycursor)
    return jsonify(customer_data)

@app.route('/api/viewStaff', methods=['GET'])
def viewStaff():
    staff_data = display_staff_details(mycursor)
    return jsonify(staff_data)  

# Ensure staff_data is in a JSON-serializable format, such as a list of dictionaries






@app.route('/api/deleteStaff/<int:staffID>', methods=['DELETE'])
def staffDeleted(staffID):
    try:
        query = "DELETE FROM Hotel_Staff WHERE id = %s"  # Adjusted to correct column name
        mycursor.execute(query, (staffID,))
        db.commit()
        
        if mycursor.rowcount > 0:
            return jsonify({'success': True, 'message': 'Staff member deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Staff member not found'}), 404
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


# @app.route("/api/home", methods=["GET"])
# def return_home():
#     return jsonify({
#         'message': "Hello World"
#     })

if __name__ == '__main__':
    app.run(debug=True,port=5000)