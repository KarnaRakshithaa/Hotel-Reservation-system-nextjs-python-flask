import mysql.connector
from datetime import datetime, timedelta



# mycursor.execute("""SELECT Hotel.name AS hotel_name
# FROM Room
# JOIN Hotel ON Room.hotel_id = Hotel.id
# WHERE Room.number = 1;
# """)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="60756075",
    database="LOL"
)
mycursor=db.cursor()

def insert_customer_details(mycursor, name, phone, address):
    query = "INSERT INTO customer (name, phone, address) VALUES (%s, %s, %s)"
    values = (name, phone, address)
    mycursor.execute(query, values)


def delete_staff_details(id):
    query = """
            DELETE FROM Customer WHERE id = %s
            """
    values = (id,)
    mycursor.execute(query, values)
    return mycursor.fetchall()
    

def insert_rooms(cost, room_type, bed_size, hotel_id):
    query = """INSERT INTO Room (cost, room_type, bed_size, hotel_id) VALUES (%s, %s, %s, %s)"""
    values = (cost, room_type, bed_size, hotel_id)
    mycursor.execute(query, values)
    db.commit()
    return mycursor.lastrowid





def display_rooms(mycursor):
    query = "SELECT number, cost, room_type, bed_size, hotel_id FROM Room"
    mycursor.execute(query)
    result = mycursor.fetchall()
    rooms_list = [
        {"roomId": number, "cost": cost, "roomType": room_type, "bedSize": bed_size, "hotelId": hotel_id}
        for number, cost, room_type, bed_size, hotel_id in result
    ]
    return rooms_list

def rooms_available(mycursor,start_date, end_date):
    query = """
        SELECT *
        FROM Room
        WHERE Room.number NOT IN (
            SELECT room_no
            FROM Reservation 
            WHERE Reservation.start_date <= %s AND Reservation.end_date >= %s
        )
    """
    mycursor.execute(query, (end_date, start_date))
    return mycursor.fetchall()

def select_rooms(start_date, end_date, Cid, room_no):
    try:
        query = "INSERT INTO Reservation (start_date, end_date, Cid, room_no) VALUES (%s, %s, %s, %s)"
        mycursor.execute(query, (start_date, end_date, Cid, room_no))
        db.commit()
        return mycursor.lastrowid
    except Exception as e:
        db.rollback()
        return None
    
def delete_old_bookings(cursor):
    query = """DELETE FROM Reservation WHERE end_date < NOW()"""
    cursor.execute(query)
    return mycursor.fetchall()

# def select_customers_one_month_ago(mycursor):
#     try:
#         # Calculate the date one month ago
#         one_month_ago = datetime.now() - timedelta(days=30)
        
#         # SQL query to select customers who made reservations one month ago
#         query = """
#             SELECT c.name, c.phone, c.address
#             FROM Customer c
#             JOIN Reservation r ON c.id = r.Cid
#             WHERE r.start_date >= %s
#         """
        
#         # Execute the query with the one month ago date as parameter
#         mycursor.execute(query, (one_month_ago,))
        
#         # Fetch all the selected customers
#         customers = mycursor.fetchall()
#         print(customers)
        
#         return customers
    
#     except mysql.connector.Error as err:
#         print("Error:", err)

def delete_staff_details(id):
    query = """
            DELETE FROM Hotel_Staff WHERE id = %s
            """
    values = (id,)
    mycursor.execute(query, values)
    return mycursor.fetchall()


def display_reservations():
    query="SELECT * FROM Reservation"
    mycursor.execute(query)
    return mycursor.fetchall()

def display_hotel_details():
    query="SELECT * FROM Hotel"
    mycursor.execute(query)

start_date = "2024-02-05"
end_date = "2024-02-08"



    
def insert_staff_details(mycursor,name, address, salary,gender,hotel_id,dob):
    query = """
            INSERT INTO Hotel_Staff(name, address, salary,gender,hotel_id,dob) VALUES (%s,%s,%s,%s,%s,%s)
            """
    values = (name, address, salary,gender,hotel_id,dob)
    mycursor.execute(query, values)

# mycursor.execute("SELECT * FROM Reservation")
def display_reservations(mycursor):
    query="SELECT * FROM Reservation"
    mycursor.execute(query)
    return mycursor.fetchall()

def insert_rooms(mycursor,cost,room_type,bed_size,hotel_id):
    query = """
            INSERT INTO Room(cost,room_type,bed_size,hotel_id) VALUES (%s, %s, %s , %s)
            """
    values = (cost,room_type,bed_size,hotel_id)
    mycursor.execute(query, values)



def select_rooms(mycursor,start_date,end_date,Cid,room_no):
    query="""INSERT INTO Reservation(start_date,end_date,Cid,room_no) VALUES(%s,%s,%s,%s)"""
    values = (start_date,end_date,Cid,room_no)
    mycursor.execute(query, values)

def cancel_room(mycursor,reservation_id):
    query="DELETE FROM Reservation WHERE id = %s"
    values=(reservation_id,)
    mycursor.execute(query,values)


def display_customer(mycursor):
    query = "SELECT name, phone, address, id FROM Customer"
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result

def display_staff_details(mycursor):
    query="SELECT * FROM Hotel_Staff"
    mycursor.execute(query)
    result = mycursor.fetchall()
    staff_list = []
    for row in result:
        staff_list.append({
            'staff_id': row[0],
            'name': row[1],
            'address': row[2],
            'salary':row[3],
            'gender':row[4],
            'hotel_id':row[5],
            'dob':row[6]
            # Add more fields as per your database schema
        })
    return staff_list

# def delete_customer_details(mycursor, id):
#     # First, delete related reservations
#     query_delete_reservations = "DELETE FROM Reservation WHERE Cid = %s"
#     mycursor.execute(query_delete_reservations, (id,))
    
#     # Then, delete the customer
#     query_delete_customer = "DELETE FROM Customer WHERE id = %s"
#     mycursor.execute(query_delete_customer, (id,))
    
#     db.commit()


# display_staff_details()
# def insert_staff_details(name, address, salary,gender,hotel_id,dob):
#     query = """
#             INSERT INTO Hotel_Staff(name, address, salary,gender,hotel_id,dob) VALUES (%s,%s,%s,%s,%s,%s)
#             """
#     values = (name, address, salary,gender,hotel_id,dob)
#     mycursor.execute(query, values)
#     db.commit()
start_date = "2024-02-09"
end_date = "2024-02-12"
# availablerooms =rooms_available(mycursor,start_date,end_date)


# select_rooms(start_date,end_date,2,9) 
# display_rooms()
# # rooms_available(mycursor,start_date,end_date)
# insert_rooms(12000,'AC','Double',2)
# insert_customer_details("Rakshita",1234567890,"Bangalore")
# select_rooms(start_date,end_date,5,1) 
# insert_staff_details("Tina","India",25000,"Female",2,'1995-1-1')
# insert_rooms(20000,'Non-AC','Double',2)
# select_customers_one_month_ago(mycursor)

# delete_customer_details(mycursor, 8)



db.commit()

mycursor.close()
db.close()