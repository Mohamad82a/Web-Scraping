from bs4 import BeautifulSoup
import requests
import sys
import csv
sys.path.append(r"c:\Users\Asus\Desktop\Crawling Rajanews\storage")
from db import Database


website = requests.get('https://www.rajanews.com/')
website.encoding = 'utf-8'
soup = BeautifulSoup(website.content, 'lxml')

contextual_links = soup.find('div', class_='contextual-links-region')
region_content = contextual_links.find('div', class_='region-content')
homepage = contextual_links.find('div', class_='homepage')
posts = homepage.find_all('div', class_='item')


db = Database()

with open('post-details.txt', 'a', encoding='utf-8') as file_data:

    for counter, post in enumerate(posts[:10], start=1):
        blank = post.find('a', target='_blank')
        lead = post.find('div', class_='lead')
        
        description = lead.get_text(strip=True)
        
        image_link = post.find('a', class_='image-link')
        image = image_link.find('img').get('src')


        if blank:     
            title = blank.find('div', class_='title')
            if title:
                title_text = blank.get_text(strip=True)
                display_title = title_text

        if description:
            display_description = description 


            display_title = display_title.encode('utf-8').decode('utf-8')
            display_description = display_description.encode('utf-8').decode('utf-8')


        if image:
            file = requests.get(image).content
            with open(f'post-image{counter}.png', 'wb') as image_file:
                image_file.write(file)
        
        db.insert_post(display_title, display_description, image)
        
        file_data.write(f"Post {counter}: {display_title}\n")
        file_data.write(f"Description {counter}: {display_description}\n")
        file_data.write(f"Post Image URL: {image}\n")
        file_data.write("\n" + "-"*30 + "\n\n")

    posts_from_db = db.fetch_posts()

    with open('posts_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Description", "Image URL"])
        
        for post in posts_from_db:
            writer.writerow([f'Title: {post[0]}, Description: {post[1]}, Image URL: {post[2]}'])
            writer.writerow([])


    db.connection.commit()
db.connection.close()