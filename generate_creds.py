import crypt
from getpass import getpass
from pickle import dump, dumps

def get_confirm(get_text, confirm_text, failure_text, get_meth=getpass, input_text='password: '):
    while 1:
        data = get_meth(get_text)
        if data == get_meth(confirm_text):
            return data
        else:
            print(failure_text)

print('Please enter your credit card information:')
card_number = input('Please enter your credit card number: ')
exp_date = input('Please enter your credit card experation date (month/year): ')
cvv = input('Please enter your cvv: ')

print('')

print('Please enter your billing/shipping information:')
name = input('Please enter your name (first and last): ')
email = input('Please enter your email: ')
tel = input('Please enter your telephone number: ')
addr = input('Please enter your address: ')
zip = input('Please enter your zip code: ')
city = input('Please enter your city name: ')
state = input('Please enter your two letter state abbreviation: ')

print('')

key = get_confirm('Please enter a password to encrypt your credentials: ','Please confirm your password: ','Sorry, your password did not match').encode('utf-8')

encrypted_credit_card_info = crypt.Encryption(dumps({'card_number':card_number, 'exp_date':exp_date, 'cvv':cvv}), key)
encrypted_billing_cookie = crypt.Encryption(dumps({'value': '{name}%7C{addr}%7C%7C{city}%7C{state_abv}%7C{zip}%7CUSA%7C{email}%7C{phone}'.format(name=name.replace(' ','+'), addr=addr.replace(' ','+'), city=city, state_abv=state.upper(), zip=zip, email=email, phone=tel), 'path': '/', 'domain': 'www.supremenewyork.com', 'secure': False, 'name': 'address', 'httpOnly': False}), key)
#, 'expiry': 1545755719.445382, 'path': '/', 'domain': 'www.supremenewyork.com', 'secure': False, 'name': 'address', 'httpOnly': False
# x = {'value': 'George+Gee%7C304+Greenwood+Road%7C%7CLouisville%7CKY%7C40203%7CUSA%7Cgeorge%40gmail.com%7C4032030342', 'expiry': 1545755719.445382, 'path': '/', 'domain': 'www.supremenewyork.com', 'secure': False, 'name': 'address', 'httpOnly': False}
dump(encrypted_credit_card_info, open('encrypted_credit_card_info.pkl', 'wb'))
dump(encrypted_billing_cookie, open('encrypted_billing_cookie.pkl', 'wb'))

input('Credentials sucsessfully encrypted and written! Press enter to exit')
