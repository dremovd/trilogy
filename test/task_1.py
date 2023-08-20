from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import unittest
import time

LOAD_TIME = 3 # seconds

test_user_data = {
    'username': 'jcosten0@purevolume.com',
    'password': 'password',
}

class TestCreateArticleWithTags(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:4200/')
        time.sleep(LOAD_TIME)  # Allow the page to load

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
        time.sleep(2)  # Allow login to complete

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

    def test_create_article_with_tags(self):
        # Login
        self.login(test_user_data['username'], test_user_data['password'])

        # Navigate to the page to create a new article
        self.create_post()

        self.browser.get('http://localhost:4200/')
        time.sleep(LOAD_TIME)
        
        # Navigate to the "Global Feed" tab
        global_feed_tab = self.browser.find_element(By.XPATH, '//a[@data-e2e-id="global-feed"]')
        global_feed_tab.click()
        time.sleep(LOAD_TIME)  # Allow navigation to global feed page

        # Locate the container for the first article in the global feed
        first_article_container = self.browser.find_element(By.XPATH, '//div[contains(@class,"article-preview")][1]')

        # Find the tags within that container
        post_tags = first_article_container.find_elements(By.XPATH, './/li[contains(@class,"tag-default tag-pill tag-outline")]')

        # Verify the tags
        self.assertEqual(len(post_tags), 2, 'Expected 2 tags, found {}'.format(len(post_tags)))
        self.assertEqual(post_tags[0].text, 'coding')
        self.assertEqual(post_tags[1].text, 'testing')

        # Verify the new "testing" tag is visible in the "Popular Tags" section
        popular_tag_elements = self.browser.find_elements(By.XPATH, '//div[@class="tag-list"]/a')
        self.assertIn('testing', [tag.text for tag in popular_tag_elements])

        # Click the "testing" tag and verify the new post is visible
        for tag in popular_tag_elements:
            if tag.text == 'testing':
                tag.click()
                break
        time.sleep(LOAD_TIME)  # Allow navigation to tag page
        post_elements = self.browser.find_elements(By.XPATH, '//div[contains(@class,"article-preview")]')
        self.assertGreaterEqual(len(post_elements), 1, 'No posts found for the "testing" tag')

    def tearDown(self):
        self.browser.quit()


if __name__ == "__main__":
    unittest.main()

