from db_connection import DBConnection
from bs4 import BeautifulSoup
from pymongo.errors import PyMongoError  # MongoDB error handling
import re

# Instantiate DBConnection to connect to MongoDB
db_connection = DBConnection()
pages_collection = db_connection.db["pages"]
professors_collection = db_connection.db["professors"]

# Retrieve the HTML content from MongoDB using the specified URL
faculty_page = pages_collection.find_one(
    {"url": "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml#main"}
)

# Check if the faculty page is found and contains HTML content
if not faculty_page:
    print("Faculty page not found.")
elif "html" not in faculty_page:
    print("No HTML content found in the faculty page.")
else:
    ''' html = <strong>Title:</strong> Professor </strong> <br> <strong>Phone</strong> 909 -991-3527 <strong>Email</strong> '''
    html_content = faculty_page["html"]
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract professor information from the HTML content
    professor_cards = soup.find_all("div", class_="clearfix")

    if not professor_cards:
        print("No professor information found.")
    else:

        professor_data = {}
        for card in professor_cards:
        
            # Extracting professor details from the HTML structure
            name_tag = card.find("h2")
            professor_data["Name"] = name_tag.get_text(strip=True) if name_tag else "Unknown"

            tags = card.find_all("strong")
            for t in tags:
                key = t.get_text().rstrip(":")  # Remove ":" from the end of the key
                value = t.find_next_sibling() 
                if value:
                    value_text = value.get_text(strip=True)
                    professor_data[key] = value_text

        print(professor_data)

        # Insert the professor data into the MongoDB collection
        try:
            professors_collection.insert_one(professor_data)
        except PyMongoError as e:
            print(f"Failed to insert professor data: {e}")

    print("Professor information successfully stored in MongoDB.")
