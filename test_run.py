from pages import LoginPage, InventoryPage, CartPage, YouInformationPage, OverviewPage, CompletePage


def test_auth(driver):
    auth_page = LoginPage(driver)
    auth_page.input_login('standard_user')
    auth_page.input_password('secret_sauce')
    auth_page.login_button_click()

    assert InventoryPage(driver).check_inventory_page_open()

def test_item_buy(driver):
    LoginPage(driver).auth(login='standard_user', password='secret_sauce')
    inventory_page = InventoryPage(driver)
    backpack_price = inventory_page.get_backpack_price()
    inventory_page.backpack_add_to_cart_button_click()

    assert inventory_page.get_cart_counter() == 1

    inventory_page.cart_button_click()
    cart_page = CartPage(driver)

    assert cart_page.get_items_number() == 1
    assert cart_page.get_item_quantity() == 1
    assert cart_page.get_item_name() == 'Sauce Labs Backpack'
    assert cart_page.get_item_price() == backpack_price

    cart_page.checkout_button_click()

    you_information_page = YouInformationPage(driver)
    you_information_page.input_first_name('Joe')
    you_information_page.input_last_name('Lowson')
    you_information_page.input_postal_code('1234')
    you_information_page.continue_button_click()

    overview_page = OverviewPage(driver)
    assert overview_page.get_items_number() == 1
    assert overview_page.get_item_quantity() == 1
    assert overview_page.get_item_name() == 'Sauce Labs Backpack'
    assert overview_page.get_item_price() == backpack_price
    assert overview_page.get_payment_info_label() == 'Payment Information:'
    assert overview_page.get_payment_info_value() == 'SauceCard #31337'
    assert overview_page.get_shipping_info_label() == 'Shipping Information:'
    assert overview_page.get_shipping_info_value() =='Free Pony Express Delivery!'
    assert overview_page.get_total_info_label() == 'Price Total'
    assert overview_page.get_subtotal_label() == 'Item total:'
    assert overview_page.get_subtotal_value() == backpack_price
    assert overview_page.get_tax_label() == 'Tax:'
    tax = 2.40
    assert overview_page.get_tax_value() == tax
    assert overview_page.get_total_label() == 'Total:'
    assert overview_page.get_total_value() == backpack_price + tax

    overview_page.finish_button_click()

    complete_page = CompletePage(driver)
    assert complete_page.get_title() == 'Checkout: Complete!'
    assert complete_page.get_complete_header() == 'Thank you for your order!'
    assert complete_page.get_complete_text() == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
    assert complete_page.back_home_button_present()