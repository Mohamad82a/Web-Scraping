import mysql.connector
import csv

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root', password='mmd123456',
            database='webscraping',
            port=8080,
            charset='utf8mb4'
            )
        self.cursor = self.connection.cursor()
        self.cursor.execute("SET NAMES 'utf8mb4'")
        
    def insert_post(self, title, description, image_url):
        query = '''INSERT INTO rajanews_posts (title, description, image_url) VALUES (%s,%s,%s)'''
        self.cursor.execute(query, (title, description, image_url))
        self.connection.commit()


    def fetch_posts(self):
        query = '''SELECT title, description, image_url FROM rajanews_posts'''
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    
    def close(self):
        self.cursor.close()
        self.connection.close()
            
            
    
if __name__ == '__main__':
    db = Database()
    


    # if db.connection.is_connected():
    #     cursor = db.connection.cursor()
    #     db.connection.commit()
        
