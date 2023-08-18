from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

LOAD_TIME = 3  # seconds

class TestConduitRoster(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:4200/')
        time.sleep(LOAD_TIME)  # Allow the page to load

    def test_roster_page_not_logged_in(self):
        # Navigate to the Roster page
        roster_link = self.browser.find_element(By.LINK_TEXT, 'Roster')
        roster_link.click()
        time.sleep(LOAD_TIME)  # Allow navigation to Roster page

        # Verify the presence of the "Conduit Roaster" header
        header = self.browser.find_element(By.XPATH, '//h1[text()="Conduit Roaster"]')
        self.assertIsNotNone(header)

        # Verify the table structure and contents
        table_rows = self.browser.find_elements(By.XPATH, '//table/tbody/tr')
        prev_likes = float('inf') # To check the sorting based on likes

        for row in table_rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            username = cells[0].find_element(By.TAG_NAME, 'a').text
            articles_authored = int(cells[1].text)
            likes = int(cells[2].text)
            first_article_date = cells[3].text

            # Validate data types and values as needed
            # ...

            # Check the sorting based on likes
            self.assertGreaterEqual(prev_likes, likes)
            prev_likes = likes

    def test_roster_page_new_article(self):
        # Log in and create a new article
        # (Assuming login and article creation logic is implemented)

        # Navigate to the Roster page
        roster_link = self.browser.find_element(By.LINK_TEXT, 'Roster')
        roster_link.click()
        time.sleep(LOAD_TIME)  # Allow navigation to Roster page

        # Find the row for the logged-in user
        user_row = self.browser.find_element(By.XPATH, f'//table/tbody/tr[td/a[text()="{test_user_data["username"]}"]]')
        articles_cell = user_row.find_element(By.XPATH, 'td[2]')

        # Verify the increment in the total number of articles for the logged-in user
        self.assertEqual(int(articles_cell.text), previous_articles_count + 1)  # previous_articles_count should be fetched before article creation

    def test_roster_page_like_article(self):
        # Log in and like an existing article
        # (Assuming login and like article logic is implemented)

        # Navigate to the Roster page
        roster_link = self.browser.find_element(By.LINK_TEXT, 'Roster')
        roster_link.click()
        time.sleep(LOAD_TIME)  # Allow navigation to Roster page

        # Find the row for the article's author
        author_row = self.browser.find_element(By.XPATH, f'//table/tbody/tr[td/a[text()="{author_username}"]]')
        likes_cell = author_row.find_element(By.XPATH, 'td[3]')

        # Verify the increment in the total number of likes for that article's author
        self.assertEqual(int(likes_cell.text), previous_likes_count + 1)  # previous_likes_count should be fetched before liking the article

    def tearDown(self):
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()
