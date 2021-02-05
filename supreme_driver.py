# imporing everything
from time                            import sleep
from pickle                          import load, loads

from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium                        import webdriver
from pynput.keyboard                 import Key, Controller



class Supreme_Driver_Chrome(webdriver.Chrome):

    def __init__(self, creds_dir='encrypted_credentials.json', load_images=False):

        self.catagories = ['jackets', 'shirts', 'tops_sweaters', 'sweatshirts', 'pants', 'shorts', 'hats', 'bags', 'accessories', 'skate']
        self.creds_dir = creds_dir
        self.encrypted_creds = None
        self.capabilities = None
        self.chrome_options=None

        if not load_images:
            self.chrome_options = webdriver.ChromeOptions()
            self.chrome_options.add_experimental_option("prefs",{"profile.managed_default_content_settings.images":2})

        self.keyboard = Controller()

    def setup_proxy(self, ip, port):

        # setting up proxy
        self.prox = Proxy()
        self.prox.proxy_type = ProxyType.MANUAL
        self.prox.http_proxy = ip+':'+port
        self.capabilities = webdriver.DesiredCapabilities.CHROME
        self.prox.add_to_capabilities(self.capabilities)

    def run(self):

        ### GET PASSWORD
        super(Supreme_Driver_Chrome, self).__init__(desired_capabilities=self.capabilities, chrome_options=self.chrome_options)
        self.get('http://www.supremenewyork.com')

    def get_encrypted_creds(self, credit_card='encrypted_credit_card_info.pkl', cookie='encrypted_billing_cookie.pkl'):
        self.crypt_cookie = load(open(cookie, 'rb'))
        self.crypt_credit = load(open(credit_card, 'rb'))

    def unencrypt_creds(self, password):
        try:
            self.cookie = loads(self.crypt_cookie.decrypt(password))
            self.credit = loads(self.crypt_credit.decrypt(password))
        except:
            self.get_encrypted_creds()
            self.cookie = loads(self.crypt_cookie.decrypt(password))
            self.credit = loads(self.crypt_credit.decrypt(password))

    def add_billing_cookie(self):
        print(self.cookie)
        self.add_cookie(self.cookie)

    def add_items_to_cart(self, sorted_items):
        item_links = []
        for type, items in sorted_items.items():
            if items != []:
                self.get('http://www.supremenewyork.com/shop/all/'+type)

                # Gets all color and item name of all items in that catagory
                elms = self.find_elements_by_class_name("name-link")
                for i in range(int(len(elms)/2)):
                    break_var = False
                    for item in items:

                        # If the item matches it adds it to the list of links
                        if item.color.get() in elms[i*2+1].text.lower() and item.keywords.get() in elms[i*2].text.lower():
                            item_links.append({'link':elms[i*2].get_attribute("href"), 'item':item})

                            # When the items are added to the list the loop stops
                            break_var = True
                            break
                    if break_var:
                        break

        # Goes through all the links and adds the item to the cart
        for link in item_links:
            self.get(link['link'])
            options = self.find_elements_by_tag_name('option')
            for op in options:
                if link['item'].size.get() in op.text:
                    op.click()

            # If it's out of stock it will pass
            try:
                self.find_element_by_name('commit').click()
            except:
                pass

    def checkout(self, card_number, exp_m, exp_y, cvv, delay):
        sleeper = 0.25
        while 1:
            try:
                self.find_element_by_css_selector('.button.checkout').click()
                break
            except:
                sleeper += 0.25
                sleep(sleeper)

        for op in self.find_element_by_id('credit_card_month').find_elements_by_tag_name('option'):
            if op.text == exp_m:
                op.click()
                break
        for op in self.find_element_by_id('credit_card_year').find_elements_by_tag_name('option'):
            if op.text == exp_y:
                op.click()
                break
        self.find_elements_by_class_name('icheckbox_minimal')[1].click()
        self.find_element_by_id('nnaerb').click()
        self.keyboard.type(card_number)
        for _ in range(3):
            self.keyboard.press(Key.tab)
        self.keyboard.type(cvv)
        self.keyboard.press(Key.tab)
        sleep(delay)
        self.keyboard.press(Key.enter)



if __name__ == '__main__':
    item = 'Plaid Knit Polo'
    driver = Supreme_Driver_Chrome()
    #driver.setup_proxy('104.254.244.54', '80')
    driver.run()
    driver.get('http://www.speedtest.net/')
    sleep(5)
    driver.close()
