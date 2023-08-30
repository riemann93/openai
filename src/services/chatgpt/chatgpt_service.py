import time
import configparser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class OpenAIChatbot:

    def __init__(self, config_file='config.ini', selectors_file='selectors.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

        self.selectors = configparser.ConfigParser()
        self.selectors.read(selectors_file)

        self.browser = webdriver.Chrome()

    def _load_decomposer_prompt(self, main_task):
        """Load the decomposer prompt from the file and insert the main task."""

        # Determine which prompt to use next
        try:
            with open('../../Prompts/last_used.txt', 'r') as f:
                last_used = f.read().strip()
                if last_used == 'decomposer.txt':
                    prompt_file = '_decomposer.txt'
                else:
                    prompt_file = 'decomposer.txt'
        except FileNotFoundError:
            # If the file doesn't exist yet, use the default decomposer.txt and create the file
            prompt_file = 'decomposer.txt'

        # Load the chosen prompt
        try:
            with open(f'prompts/{prompt_file}', 'r') as file:
                prompt = file.read().strip()
                # Replace the placeholder with the main task
                formatted_prompt = prompt.replace("[Input main task here]", main_task)

                # Save the used prompt to the last_used.txt file
                with open('../../Prompts/last_used.txt', 'w') as f:
                    f.write(prompt_file)

                return formatted_prompt
        except FileNotFoundError:
            print(f"Warning: '{prompt_file}' not found. Using default prompt.")
            return main_task

    def _click_element(self, identifier, by_text=False, timeout=10):
        """
        Clicks on an element given its identifier.

        Parameters:
            - identifier (str): the CSS selector or the button text, based on by_text value.
            - timeout (int): maximum seconds to wait for the element to become clickable.
            - by_text (bool): if True, it will use XPath to locate button by its text.
                              Otherwise, it will use CSS selector.

        Returns:
            None
        """
        try:
            if by_text:
                # If you're searching by text, use XPath with text() method.
                elements = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_all_elements_located((By.XPATH, f"//button[contains(., '{identifier}')]"))
                )
            else:
                # Otherwise, assume the identifier is a CSS selector.
                elements = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, identifier))
                )

            # Filter out invisible elements and click the first visible one.
            for element in elements:
                if element.is_displayed():
                    element.click()
                    return

            # If none of the elements are visible/clickable, raise an exception.
            raise Exception(f"No clickable element found for identifier: {identifier}")

        except Exception as e:
            print(f"Error while trying to click the element: {e}")

    # def _click_element(self, identifier, timeout=10, by_text=False):
    #
    #     if by_text:
    #         xpath = f"//button[contains(., '{identifier}')]"
    #         element = WebDriverWait(self.browser, timeout).until(
    #             EC.element_to_be_clickable((By.XPATH, xpath))
    #         )
    #     else:
    #         element = WebDriverWait(self.browser, timeout).until(
    #             EC.element_to_be_clickable((By.CSS_SELECTOR, identifier))
    #         )
    #
    #     element.click()

    def _click_element_by_xpath(self, xpath, timeout=10):
        element = WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()

    def _input_text(self, css_selector, text, timeout=10):
        element = WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.send_keys(text)

    def _input_text_line_by_line(self, css_selector, text):
        input_element = self.browser.find_element(By.CSS_SELECTOR, css_selector)
        lines = text.split('\n')

        for i, line in enumerate(lines):
            input_element.send_keys(line)

            # If it's not the last line, insert a newline using Shift+Enter
            if i != len(lines) - 1:
                input_element.send_keys(Keys.SHIFT, Keys.RETURN)

            # Using a fixed sleep instead of waiting for the input to update
            time.sleep(0.5)  # adjust this value based on observed behavior

    def _login_to_openai(self):
        self.browser.get('https://chat.openai.com')
        time.sleep(3)

        self._click_element('Log in', by_text=True)
        self._input_text(self.selectors['EMAIL']['input'], self.config['LOGIN']['email'])
        self._click_element('Continue', by_text=True)

        self._input_text(self.selectors['PASSWORD']['input'], self.config['LOGIN']['password'])
        time.sleep(1)
        self._click_element('Continue', by_text=True)

        self._click_element('Okay, let’s go', by_text=True)

    def get_response_from_chatbot(self, text_prompt):
        # Ensure text_prompt is always provided
        assert text_prompt is not None, "A text_prompt is required"

        full_prompt = self._load_decomposer_prompt(text_prompt)

        self._login_to_openai()

        self._input_text_line_by_line(self.selectors['CHAT']['input'], full_prompt)
        self.browser.find_element(By.CSS_SELECTOR, self.selectors['CHAT']['input']).send_keys(Keys.RETURN)

        # Wait for the "Regenerate" button to appear
        regenerate_xpath = "//button[contains(., 'Regenerate')]"
        WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.XPATH, regenerate_xpath)))

        try:
            response_element = self.browser.find_element(By.CSS_SELECTOR, self.selectors['CHAT']['response'])
            response_text = response_element.text
            return response_text
        except Exception as e:
            print(f"Error while fetching response: {e}")
            return None


if __name__ == "__main__":
    bot = OpenAIChatbot()
    response = bot.get_response_from_chatbot("Hello, how are you?")
    print(f"OpenAI's Response: {response}")