from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = int(timeout)
        self.wait = WebDriverWait(driver, timeout)
        self.page_url = ''

    def find_element(self, by: By or int, value: str) -> WebElement:
        return self.wait.until(expected_conditions.visibility_of_element_located((by, value)),
                               message=f'Элемент {by, value} не найден')

    def find_elements(self, by: By or int, value: str) -> [WebElement]:
        return self.wait.until(expected_conditions.visibility_of_all_elements_located((by, value)),
                               message=f'Элементы {by, value} не найдены')

    def assert_that_present(self, by: By or int, value: str) -> bool:
        return type(self.find_element(by, value)) == WebElement

    def get_current_url(self) -> str:
        return self.driver.current_url


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.login = (By.ID, 'user-name')           #Локатор по ID для элемента строки ввода login
        self.password = (By.ID, 'password')         #Локатор по ID для элемента строки ввода password
        self.login_btn = (By.NAME, 'login-button')  #Локатор по Name для элемента кнопка Login

    def input_login(self, login: str) -> None:
        self.find_element(*self.login).send_keys(login)

    def input_password(self, password: str) -> None:
        self.find_element(*self.password).send_keys(password)

    def login_button_click(self) -> None:
        self.find_element(*self.login_btn).click()

    def auth(self, login: str, password: str) -> None:
        self.input_login(login)
        self.input_password(password)
        self.login_button_click()


class InventoryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/inventory.html'
        self.backpack_add_to_cart_button = (By.ID, 'add-to-cart-sauce-labs-backpack')
        self.backpack_price = (By.XPATH, '*//button[@id="add-to-cart-sauce-labs-backpack"]/preceding-sibling::div')
        self.cart = (By.ID, 'shopping_cart_container')
        self.cart_counter = (By.CSS_SELECTOR, '.shopping_cart_badge')


    def check_inventory_page_open(self) -> bool:
        return self.get_current_url() == self.page_url

    def backpack_add_to_cart_button_click(self) -> None:
        self.find_element(*self.backpack_add_to_cart_button).click()

    def get_backpack_price(self) -> float:
        return float(self.find_element(*self.backpack_price).text[1:])

    def get_cart_counter(self) -> int:
        return int(self.find_element(*self.cart_counter).text)

    def cart_button_click(self) -> None:
        self.find_element(*self.cart).click()


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/cart.html'
        self.cart_item = (By.CSS_SELECTOR, '.cart_item')
        self.item_quantity = (By.CSS_SELECTOR, '.cart_item > .cart_quantity')
        self.item_price = (By.XPATH, '*//div[@class="cart_item"]//div[@class="inventory_item_price"]')
        self.item_name = (By.XPATH, '*//div[@class="cart_item"]//div[@class="inventory_item_name"]')
        self.checkout_button = (By.ID, 'checkout')

    def get_items_number(self) -> int:
        return len(self.find_elements(*self.cart_item))

    def get_item_quantity(self) -> int:
        return int(self.find_element(*self.item_quantity).text)

    def get_item_price(self) -> float:
        return float(self.find_element(*self.item_price).text[1:])

    def get_item_name(self) -> str:
        return self.find_element(*self.item_name).text

    def checkout_button_click(self) -> None:
        self.find_element(*self.checkout_button).click()


class YouInformationPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/checkout-step-one.html'
        self.first_name = (By.ID, 'first-name')
        self.last_name = (By.ID, 'last-name')
        self.postal_code = (By.ID, 'postal-code')
        self.continue_button = (By.ID, 'continue')

    def input_first_name(self, first_name: str) -> None:
        self.find_element(*self.first_name).send_keys(first_name)

    def input_last_name(self, last_name: str) -> None:
        self.find_element(*self.last_name).send_keys(last_name)

    def input_postal_code(self, postal_code: str) -> None:
        self.find_element(*self.postal_code).send_keys(postal_code)

    def continue_button_click(self) -> None:
        self.find_element(*self.continue_button).click()


class OverviewPage(CartPage):
    def __init__(self, driver):
        super().__init__(driver)

        self.page_url = 'https://www.saucedemo.com/checkout-step-two.html'
        self.payment_info_label = (By.CSS_SELECTOR, '[data-test="payment-info-label"]')
        self.payment_info_value = (By.CSS_SELECTOR, '[data-test="payment-info-value"]')
        self.shipping_info_label = (By.CSS_SELECTOR, '[data-test="shipping-info-label"]')
        self.shipping_info_value = (By.CSS_SELECTOR, '[data-test="shipping-info-value"]')
        self.total_info_label = (By.CSS_SELECTOR, '[data-test="total-info-label"]')
        self.subtotal_label = (By.CSS_SELECTOR, '[data-test="subtotal-label"]')
        self.tax_label = (By.CSS_SELECTOR, '[data-test="tax-label"]')
        self.total_label = (By.CSS_SELECTOR, '[data-test="total-label"]')
        self.finish_button = (By.ID, 'finish')

    def get_payment_info_label(self) -> str:
        return self.find_element(*self.payment_info_label).text

    def get_payment_info_value(self) -> str:
        return self.find_element(*self.payment_info_value).text

    def get_shipping_info_label(self) -> str:
        return self.find_element(*self.shipping_info_label).text

    def get_shipping_info_value(self) -> str:
        return self.find_element(*self.shipping_info_value).text

    def get_total_info_label(self) -> str:
        return self.find_element(*self.total_info_label).text

    def get_subtotal_label(self) -> str:
        return self.find_element(*self.subtotal_label).text[:11]

    def get_subtotal_value(self) -> float:
        return float(self.find_element(*self.subtotal_label).text[13:])

    def get_tax_label(self) -> str:
        return self.find_element(*self.tax_label).text[:4]

    def get_tax_value(self) -> float:
        return float(self.find_element(*self.tax_label).text[6:])

    def get_total_label(self) -> str:
        return self.find_element(*self.total_label).text[:6]

    def get_total_value(self) -> float:
        return float(self.find_element(*self.total_label).text[8:])

    def finish_button_click(self) -> None:
        self.find_element(*self.finish_button).click()

class CompletePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, timeout=60)

        self.page_url = 'https://www.saucedemo.com/checkout-complete.html'
        self.title = (By.CSS_SELECTOR, '.title')
        self.complete_header = (By.CSS_SELECTOR, '.complete-header')
        self.complete_text = (By.CSS_SELECTOR, '.complete-text')
        self.back_home_button = (By.ID, 'back-to-products')

    def get_title(self) -> str:
        return self.find_element(*self.title).text

    def get_complete_header(self) -> str:
        return self.find_element(*self.complete_header).text

    def get_complete_text(self) -> str:
        return self.find_element(*self.complete_text).text

    def back_home_button_present(self) -> bool:
        return self.assert_that_present(*self.back_home_button)
