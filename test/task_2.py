from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

import unittest
import time

test_user_data = {
    'username': 'jcosten0@purevolume.com',
    'password': 'password',
    'name': 'John Costen',
}

LOAD_TIME = 3  # seconds

class TestConduitRoster(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:4200/')
        time.sleep(LOAD_TIME)  # Allow the page to load

    def tearDown(self):
        self.browser.quit()

    def login(self, username, password):
        # Navigate to the login page
        login_link = self.browser.find_element(By.LINK_TEXT, 'Sign in')
        login_link.click()
        time.sleep(LOAD_TIME)  # Allow navigation to login page

        # Click and type username
        username_field = self.browser.find_element(By.XPATH, '//input[@placeholder="Username"]')
        ActionChains(self.browser).click(username_field).pause(2).send_keys(username).perform()

        # Click and type password
        password_field = self.browser.find_element(By.XPATH, '//input[@placeholder="Password"]')
        ActionChains(self.browser).click(password_field).pause(2).send_keys(password).perform()
        time.sleep(LOAD_TIME)  # Allow login to complete

        # Click login button
        login_button = self.browser.find_element(By.XPATH, '//button[@data-e2e-id="sign-in"]')
        login_button.click()
        time.sleep(LOAD_TIME)  # Allow login to complete

    def create_post(self, title='Sample Article', description='This is a sample article.', body='The body of the sample article.', tags='coding, testing'):
        new_post_button = self.browser.find_element(By.XPATH, '//a[@href="/editor"]')
        new_post_button.click()
        time.sleep(LOAD_TIME)  # Allow navigation to new article page

        # Fill in the article details
        title_field = self.browser.find_element(By.XPATH, '//input[@placeholder="Article Title"]')
        title_field.send_keys(title)
        description_field = self.browser.find_element(By.XPATH, '//input[@placeholder="What\'s this article about?"]')
        description_field.send_keys(description)
        body_field = self.browser.find_element(By.XPATH, '//textarea[@placeholder="Write your article (in markdown)"]')
        body_field.send_keys(body)
        tags_field = self.browser.find_element(By.XPATH, '//input[@placeholder="Enter Tags"]')
        tags_field.send_keys(tags)
        time.sleep(LOAD_TIME)  # Allow article submission to complete

        # Submit the article
        submit_button = self.browser.find_element(By.XPATH, '//button[contains(text(),"Publish Article")]')
        submit_button.click()
        time.sleep(LOAD_TIME)  # Allow article submission to complete


    def get_author_articles_count(self, name):
        # Navigate to the Roster page
        self.browser.find_element(By.LINK_TEXT, 'Roster').click()

        # Wait for the Roster page to load
        WebDriverWait(self.browser, LOAD_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'page-title'))
        )

        # Find the row corresponding to the author
        author_row = self.browser.find_element(By.XPATH, f"//table/tbody/tr[td/a[text()='{name}']]")

        # Extract the total number of articles
        return int(author_row.find_element(By.XPATH, './/td[2]').text)

    def test_roster_page_not_logged_in(self):
        driver = self.browser

        # Navigate to the Roster page
        roster_link = driver.find_element(By.LINK_TEXT, 'Roster')
        roster_link.click()

        # Wait for the Roster page to load
        WebDriverWait(driver, LOAD_TIME).until(
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
        driver = self.browser

        # Log in with valid credentials
        self.login(test_user_data['username'], test_user_data['password'])

        initial_articles_count = self.get_author_articles_count(test_user_data['name'])
        self.create_post()

        # Verify that the article was published
        WebDriverWait(driver, LOAD_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-page'))
        )

        # Get the current number of articles for the author
        current_articles_count = self.get_author_articles_count(test_user_data['name'])

        # Verify that the total number of articles has been incremented by 1
        self.assertEqual(current_articles_count, initial_articles_count + 1)

    def get_author_likes_count(self, name):
        # Navigate to the Roster page
        self.browser.find_element(By.LINK_TEXT, 'Roster').click()

        # Wait for the Roster page to load
        WebDriverWait(self.browser, LOAD_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'page-title'))
        )

        # Find the row corresponding to the author
        author_row = self.browser.find_element(By.XPATH, f"//table/tbody/tr[td/a[text()='{name}']]")

        # Extract the total number of likes
        return int(author_row.find_element(By.XPATH, './/td[3]').text)

    def test_roster_page_like_article(self):
        driver = self.browser

        # Log in with valid credentials
        self.login(test_user_data['username'], test_user_data['password'])

        # Navigate to an article page (replace with the URL of an article that the user can like)
        driver.get('http://localhost:4200/article/how-to-do-something')

        # Wait for the article page to load
        WebDriverWait(driver, LOAD_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-page'))
        )

        # Get the author's username from the article page
        author_username = driver.find_element(By.XPATH, '//a[contains(@class, "author")]').text

        # Get the current number of likes for the author
        initial_likes_count = self.get_author_likes_count(author_username)

        # Navigate to an article page (replace with the URL of an article that the user can like)
        driver.get('http://localhost:4200/article/how-to-do-something')

        # Wait for the article page to load
        WebDriverWait(driver, LOAD_TIME).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'article-page'))
        )

        # Full XPath of the like button
        like_button_xpath = '/html/body/cdt-root/cdt-article/div/div[1]/div/cdt-article-meta/div/span[2]/button[2]'

        # Wait for the like button to be clickable
        like_button = WebDriverWait(driver, LOAD_TIME).until(
            EC.element_to_be_clickable((By.XPATH, like_button_xpath))
        )

        # Click on the like button
        like_button.click()

        # Wait for the like action to complete
        time.sleep(LOAD_TIME)

        # Get the current number of likes for the author
        current_likes_count = self.get_author_likes_count(author_username)

        # Verify that the total number of likes has been incremented by 1
        self.assertEqual(abs(current_likes_count - initial_likes_count), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
