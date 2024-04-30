from db_connection import DBConnection
from bs4 import BeautifulSoup
from pymongo.errors import PyMongoError  # MongoDB error handling

# Instantiate DBConnection to connect to MongoDB
db_connection = DBConnection()
pages_collection = db_connection.db["pages"]
professors_collection = db_connection.db["professors"]

# Retrieve the HTML content from MongoDB using the specified URL
faculty_page = pages_collection.find_one(
    {"url": "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"}
)

# Check if the faculty page is found and contains HTML content
if not faculty_page:
    print("Faculty page not found.")
elif "html" not in faculty_page:
    print("No HTML content found in the faculty page.")
else:
    html_content = faculty_page["html"]
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract professor information from the HTML content
    professor_cards = soup.find_all("div", class_="clearfix")

    if not professor_cards:
        print("No professor information found.")
    else:
        for card in professor_cards:
            professor_data = {}
            
            # Extracting professor details from the HTML structure
            name_tag = card.find("h2")
            professor_data["name"] = name_tag.text.strip() if name_tag else "Unknown"

            for i in range(4):
                if card.card.find("p").find("strong").get_text() == "Title:":
                    title_tag = card.find("p").find("strong").find_next_sibling().strip()
                    professor_data["title"] = title_tag.text.strip() if title_tag else "Unknown"

                if card.card.find("p").find("strong").get_text() == "Office:":
                    office_tag = card.find("p").find("strong").find_next_sibling().strip()
                    professor_data["office"] = office_tag.text.strip() if office_tag else "Unknown"

                if card.card.find("p").find("strong").get_text() == "Phone:":
                    phone_tag = card.find("p").find("strong").find_next_sibling().strip()
                    professor_data["phone"] = phone_tag.text.strip() if phone_tag else "Unknown"

                if card.card.find("p").find("strong").get_text() == "Email:":
                    email_tag = card.find("a", href=lambda x: x and "mailto:" in x)
                    professor_data["email"] = email_tag["href"].replace("mailto:", "") if email_tag else "Unknown"

                if card.card.find("p").find("strong").get_text() == "Web:":
                    website_tag = card.find("a", href=lambda x: x and "http" in x)
                    professor_data["website"] = website_tag["href"] if website_tag else "Unknown"

                # Insert the professor data into the MongoDB collection
                try:
                    professors_collection.insert_one(professor_data)
                except PyMongoError as e:
                    print(f"Failed to insert professor data: {e}")

        print("Professor information successfully stored in MongoDB.")