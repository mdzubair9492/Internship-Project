import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="zubair123" 
)

cursor = conn.cursor()

try:
    cursor.execute("DROP USER IF EXISTS 'django_user'@'localhost'")
    cursor.execute("CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'django_password123'")
    cursor.execute("GRANT ALL PRIVILEGES ON hr_office_db.* TO 'django_user'@'localhost'")
    cursor.execute("FLUSH PRIVILEGES")
    
    print("✓ Django user created successfully!")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")

cursor.close()
conn.close()