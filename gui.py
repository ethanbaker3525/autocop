from tkinter      import *
from tkinter      import messagebox
from os           import system
from json         import loads
from json.decoder import JSONDecodeError
from time         import sleep
from pickle       import loads
import datetime

import supreme_driver

WAIT_FOR_CHANGE = True

class row:

    def __init__(self, root, driver):

        self.item_type_value = StringVar(root)
        self.item_type_value.set("Item Type")
        self.item_type = OptionMenu(root, self.item_type_value, *driver.catagories)

        self.keywords = Entry(root, textvariable=StringVar(root, value='Item Name'))
        self.size = Entry(root, textvariable=StringVar(root, value='Size'))
        self.color = Entry(root, textvariable=StringVar(root, value='Item Color'))

    def place(self, y):

        self.y = y

        self.item_type.place(x=2, y=y)
        self.keywords.place(x=127, y=y, width=150)
        self.size.place(x=279, y=y, width=70)
        self.color.place(x=352, y=y, width=90)

    def remove(self):

        self.item_type.destroy()
        self.keywords.destroy()
        self.size.destroy()
        self.color.destroy()


class bottom_widgets:

    def __init__(self, root):

        # Item selection
        self.add_item = Button(text='Add Item', command=root.dynamic_add_row)
        self.remove_item = Button(text='Remove Item', command=root.dynamic_sub_row)

        # Hidding
        self.proxy_ip = Entry(root, textvariable=StringVar(root, value='Proxy Ip'))
        self.proxy_port = Entry(root, textvariable=StringVar(root, value='Proxy Port'))
        self.checkout_delay = Entry(root, textvariable=StringVar(root, value='Checkout Delay'))

        # Passwords
        self.password1 = Entry(root, validate='focusin', textvariable=StringVar(root, value='Password'))
        self.password1.config(validatecommand=lambda: self.password1.config(show='*'))
        self.password2 = Entry(root, validate='focusin', textvariable=StringVar(root, value='Confirm Password'))
        self.password2.config(validatecommand=lambda: self.password2.config(show='*'))

        # Run
        self.run = Button(root, text='Run Bot', command=root.run_program)

    def place(self, y):

        self.add_item.place(y=y, x=6, width=218)
        self.remove_item.place(y=y, x=224, width=218)

        self.proxy_ip.place(y=y+31, x=6, width=145)
        self.proxy_port.place(y=y+31, x=152, width=145)
        self.checkout_delay.place(y=y+31, x=298, width=145)

        self.password1.place(y=y+61, x=6, width=218)
        self.password2.place(y=y+61, x=224, width= 218)
        self.run.place(y=y+91, x=6, width=437)



class app(Tk, supreme_driver.Supreme_Driver_Chrome):

    def __init__(self):

        Tk.__init__(self)
        supreme_driver.Supreme_Driver_Chrome.__init__(self, load_images=True)

        # Set basic settings
        self.geometry('449x154')
        self.resizable(False, False)
        self.title('Auto-Cop')
        ### CHANGE ICON

        # Item selection
        self.rows = []
        self.rows.append(row(self, self))
        self.rows[0].place(3)

        # Bottom widget
        self.bw = bottom_widgets(self)
        self.bw.place(len(self.rows)*30+2)
        try:
            self.get_encrypted_creds()

        except FileNotFoundError:
            messagebox.showwarning('Warning', 'You Have Not Setup Your Credit Card Information, Please Set It Up Now')
            self.update()
            system('python3.5 generate_creds.py')
            self.update()

    def dynamic_add_row(self):

        # Dynamically moves all items and creates a new row objetc
        self.geometry('449x'+str(self.get_h()+30))
        self.add_row()
        self.bw.place(len(self.rows)*30+2)

    def dynamic_sub_row(self):

        # Dynamically moves all items and removes one row object
        if len(self.rows) > 1:
            self.geometry('449x'+str(self.get_h()-30))
            self.rows.pop().remove()
            self.bw.place(len(self.rows)*30+2)

    def get_h(self):

        # Returns the hight of the app
        return int(self.geometry().split('+')[0].split('x')[1])

    def add_row(self):

        # Adds one row to the app
        self.rows.append(row(self, self))
        self.rows[-1].place(self.rows[-2].y + 30)

    def run_program(self):

        # Code that exectues when the run button is clicked
        # Check to see if the passwords are the same
        if self.bw.password1.get() != self.bw.password2.get():
            messagebox.showwarning('Error', 'Your Passwords Do Not Match')
        try:
            self.unencrypt_creds(self.bw.password1.get().encode('utf-8'))
        except Exception as e:
            print(e)
            messagebox.showwarning('Error', 'Your Password Is Incorrect')
            return
        try:
            delay = float(self.bw.checkout_delay.get())
        except Exception as e:
            print(e)
            if self.bw.checkout_delay.get() != 'Checkout Delay':
                messagebox.showwarning('Error', 'Your Checkout Delay is Incorrect')
                return
            else:
                delay=3


        # If everything is good

        # Setup proxy
        if self.bw.proxy_ip.get() != 'Proxy Ip' and self.bw.proxy_port.get() != 'Proxy Port':
            self.setup_proxy(self.bw.proxy_ip.get(), self.bw.proxy_port.get())

        # Get and sort items
        sorted_items = {'jackets':[], 'shirts':[], 'tops_sweaters':[], 'sweatshirts':[], 'pants':[], 'shorts':[], 'hats':[], 'bags':[], 'accessories':[], 'skate':[]}
        item_links = []
        for i in self.rows:
            sorted_items[i.item_type_value.get()].append(i)

        # Run the browser
        self.run()

        while WAIT_FOR_CHANGE:
            page = self.page_source
            self.refresh()
            if self.page_source != page:
                break

        # Goes through all the item types
        self.add_billing_cookie()
        self.add_items_to_cart(sorted_items)
        self.checkout(self.credit['card_number'], self.credit['exp_date'].split('/')[0], self.credit['exp_date'].split('/')[1], self.credit['cvv'], delay)

        self.bw.run.config(text='Exit')
