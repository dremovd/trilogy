from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import unittest
import time

test_user_data = {
    'username': 'jcosten0@purevolume.com',
    'password': 'password',
}

LOAD_TIME = 3  # seconds

class TestConduitRoster(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:4200/')
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def login(self, email, password):
        self.driver.get('http://localhost:4200/login')

        email_field = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname=email]')
        email_field.send_keys(email)

        password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname=password]')
        password_field.send_keys(password)

        sign_in_button = self.driver.find_element(By.XPATH, '//button[text()="Sign in"]')
        sign_in_button.click()

        # Wait for login to complete
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="Settings"]'))
        )

    def get_author_articles_count(self, username):
        # Navigate to the Roster page
        self.driver.find_element(By.LINK_TEXT, 'Roster').click()

        # Wait for the Roster page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'page-title'))
        )

        # Find the row corresponding to the author
        author_row = self.driver.find_element(By.XPATH, f"//table/tbody/tr[td/a[text()='{username}']]")

        # Extract the total number of articles
        return int(author_row.find_element(By.XPATH, './/td[2]').text)

    def test_roster_page_not_logged_in(self):
        driver = self.driver

        # Navigate to the Roster page
        roster_link = driver.find_element(By.LINK_TEXT, 'Roster')
        roster_link.click()

        # Wait for the Roster page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'page-title'))
        )

        # Verify the "Conduit Roster" header
        header_text = driver.find_element(By.CLASS_NAME, 'page-title').text
        self.assertEqual(header_text, 'Conduit Roster')

        # Get the rows from the table
        rows = driver.find_elements(By.XPATH, '//table/tbody/tr')

        # Iterate through the rows and extract the likes
        likes = []
        for row in rows:
            likes.append(int(row.find_element(By.XPATH, './/td[3]').text))

        # Verify that the likes are sorted in descending order
        self.assertEqual(sorted(likes, reverse=True), likes)

    def test_roster_page_new_article(self):
        driver = self.driver

        # Log in with valid credentials
        self.login(test_user_data['username'], test_user_data['password'])

        # Navigate to the new article page
        driver.find_element(By.LINK_TEXT, 'New Article').click()

        # Fill in the article form
        driver.find_element(By.NAME, 'title').send_keys('Test Article')
        driver.find_element(By.NAME, 'description').send_keys('Test Description')
        driver.find_element(By.NAME, 'body').send_keys('Test Body')
        tag_field = driver.find_element(By.NAME, 'tagList')
        tag_field.send_keys('test', Keys.RETURN)

        # Publish the article
        driver.find_element(By.XPATH, '//button[text()="Publish Article"]').click()

        # Verify that the article was published
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-page'))
        )

        # Get the current number of articles for the author
        current_articles_count = self.get_author_articles_count('valid_user')

        # Verify that the total number of articles has been incremented by 1
        self.assertEqual(current_articles_count, self.initial_articles_count + 1)

    def get_author_likes_count(self, username):
        # Navigate to the Roster page
        self.driver.find_element(By.LINK_TEXT, 'Roster').click()

        # Wait for the Roster page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'page-title'))
        )

        # Find the row corresponding to the author
        author_row = self.driver.find_element(By.XPATH, f"//table/tbody/tr[td/a[text()='{username}']]")

        # Extract the total number of likes
        return int(author_row.find_element(By.XPATH, './/td[3]').text)

    def test_roster_page_like_article(self):
        driver = self.driver

        # Log in with valid credentials
        self.login('valid_user@email.com', 'valid_password')

        # Navigate to an article page (replace with the URL of an article that the user can like)
        driver.get('http://localhost:4200/article/test-article-slug')

        # Wait for the article page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-page'))
        )

        # Click on the like button
        driver.find_element(By.XPATH, '//button[contains(@class, "btn-outline-primary")]').click()

        # Wait for the like action to complete
        time.sleep(2)  # You may replace this with a more specific wait condition

        # Get the author's username from the article page
        author_username = driver.find_element(By.XPATH, '//a[contains(@class, "author")]').text

        # Get the current number of likes for the author
        current_likes_count = self.get_author_likes_count(author_username)

        # Verify that the total number of likes has been incremented by 1
        self.assertEqual(current_likes_count, self.initial_likes_count + 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
