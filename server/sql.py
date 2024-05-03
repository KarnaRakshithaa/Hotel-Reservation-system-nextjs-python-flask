import mysql.connector


# mycursor.execute("CREATE DATABASE LOL")
# mycursor.execute("""
#         CREATE TABLE Customer(
#             name VARCHAR(25), 
#             phone VARCHAR(10), 
#             address VARCHAR(50), 
#             id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
#         )
# """)


# mycursor.execute("""
#             CREATE TABLE Hotel (
#                 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                 name VARCHAR(25),
#                 location VARCHAR(50),
#                 INDEX idx_location (location),
#                 manager_id INT 
#                 FOREIGN KEY (manager_id) REFERENCES Hotel_Staff(id)  
#     )
                 
#     """)
# mycursor=db.cursor()
# mycursor.execute("""
#             INSERT INTO Hotel(name,location) VALUES (%s,%s)""",
#             ("FourSeasons","bangalore"))
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="60756075",
    database="LOL"
)


mycursor=db.cursor()
# mycursor.execute("""
#         CREATE TABLE Room(
#                  number INT AUTO_INCREMENT PRIMARY KEY,
#                  cost INT,
#                  room_type VARCHAR(10),,
#                  bed_size VARCHAR(10),
#                  hotel_id INT,
#                  FOREIGN KEY(hotel_id) REFERENCES Hotel(id)
#         )
#                  """)
for x in mycursor:
    print(x)

mycursor.close()
db.close()
# mycursor.execute("""
#      CREATE TABLE Reservation(
#                 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                 start_date DATE,
#                 end_date DATE,
#                 Cid INT,
#                 FOREIGN KEY(Cid) REFERENCES Customer(id),
#                 room_no INT,
#                 FOREIGN KEY(room_no) REFERENCES Room(number)
#                  )
#                   """)

# db=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="60756075",
#     database="DBMSEL"
# )





# mycursor.execute("""
#         CREATE TABLE Hotel_Staff(
#                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#                  name VARCHAR(25),
#                  address VARCHAR(50), 
#                  salary INT,
#                  gender VARCHAR(10),
#                  hotel_id INT,
#                  dob DATE,
#                  FOREIGN KEY(hotel_id) REFERENCES Hotel(id)
#         )
#                  """)

# mycursor.execute("""
#             CREATE TABLE Location(
#                  hotel_id INT,
#                  FOREIGN KEY(hotel_id) REFERENCES Hotel(id),
#                  hotel_loc VARCHAR(50),
#                  FOREIGN KEY(hotel_loc) REFERENCES Hotel(location)
#             )
#                  """)
# mycursor.execute("""
#     ALTER TABLE Customer
#     ADD COLUMN email VARCHAR(50)
# """)


db.commit()

# mycursor.execute("DESCRIBE Hotel")

