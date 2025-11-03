import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from inventory import Inventory
from order import Order
from report import SalesReport
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HamiMiniMarket — Inventory & Orders')
        self.geometry('800x520')

        self.inventory = Inventory()
        self.report = SalesReport()

        self.order = Order(self.inventory)

        self.create_widgets()
        self.refresh_products()

    def create_widgets(self):
        left = ttk.Frame(self)
        left.pack(side='left', fill='y', padx=8, pady=8)
        ttk.Label(left, text='Products').pack(anchor='w')

# add ID, Name, Price, and Stock columns
        self.products_tree = ttk.Treeview(
            left,
            columns=('id', 'name', 'price', 'stock'),
            show='headings',
            height=18
        )

        self.products_tree.heading('id', text='ID')
        self.products_tree.heading('name', text='Name')
        self.products_tree.heading('price', text='Price')
        self.products_tree.heading('stock', text='Stock')

        # optionally set column widths for a better layout
        self.products_tree.column('id', width=60, anchor='center')
        self.products_tree.column('name', width=160)
        self.products_tree.column('price', width=80, anchor='e')
        self.products_tree.column('stock', width=80, anchor='center')

        self.products_tree.pack(fill='y')
        self.products_tree.heading('price', text='Price')
        self.products_tree.heading('stock', text='Stock')
        self.products_tree.pack()
        search_frame = ttk.Frame(left)
        search_frame.pack(fill='x', pady=4)
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side='left', fill='x', expand=True)
        ttk.Button(search_frame, text='Search', command=self.search_products).pack(side='left')
        ttk.Button(search_frame, text='Restock (CSV)', command=self.restock).pack(side='left')

        mid = ttk.Frame(self)
        mid.pack(side='left', fill='both', expand=True, padx=8, pady=8)

        qty_frame = ttk.Frame(mid)
        qty_frame.pack(anchor='n', pady=6)
        ttk.Label(qty_frame, text='Qty:').pack(side='left')
        self.qty_var = tk.IntVar(value=1)
        ttk.Entry(qty_frame, textvariable=self.qty_var, width=6).pack(side='left')
        ttk.Button(qty_frame, text='Add to Cart', command=self.add_to_cart).pack(side='left', padx=6)

        ttk.Label(mid, text='Cart').pack(anchor='w')
        self.cart_tree = ttk.Treeview(mid, columns=('price','qty','total'), show='headings', height=10)
        for c,h in [('price','Price'),('qty','Qty'),('total','Line total')]:
            self.cart_tree.heading(c, text=h)
        self.cart_tree.pack(fill='both', expand=True)

        btn_frame = ttk.Frame(mid)
        btn_frame.pack(fill='x', pady=6)
        ttk.Button(btn_frame, text='Remove Selected', command=self.remove_selected).pack(side='left')
        ttk.Button(btn_frame, text='Confirm Order', command=self.confirm_order).pack(side='right')

        right = ttk.Frame(self)
        right.pack(side='right', fill='y', padx=8, pady=8)
        ttk.Label(right, text='Summary').pack(anchor='w')
        self.summary_lbl = ttk.Label(right, text='Total: 0.00')
        self.summary_lbl.pack(anchor='w', pady=4)

        self.low_stock_box = tk.Text(right, width=28, height=12, state='disabled')
        self.low_stock_box.pack()

    def refresh_products(self, products=None):
        for r in self.products_tree.get_children():
            self.products_tree.delete(r)
        products = products if products is not None else self.inventory.list_products()
        for p in products:
            self.products_tree.insert(
                '',
                'end',
                iid=p.product_id,
                values=(p.product_id, p.name, f'{p.price:.2f}', p.stock)
            )
        self.refresh_low_stock()
        
        

    def refresh_low_stock(self):
        lows = self.inventory.low_stock()
        self.low_stock_box.config(state='normal')
        self.low_stock_box.delete('1.0', 'end')
        if lows:
            self.low_stock_box.insert('end', 'Low stock items:\n')
            for p in lows:
                self.low_stock_box.insert('end', f'{p.name} (id:{p.product_id}) — {p.stock}\n')
        else:
            self.low_stock_box.insert('end', 'No low stock items')
        self.low_stock_box.config(state='disabled')


    def search_products(self):
        term = self.search_var.get().strip().lower()
        if not term:
            self.refresh_products()
            return
        filtered = [p for p in self.inventory.list_products() if term in p.name.lower()]
        self.refresh_products(filtered)

    def add_to_cart(self):
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning('No selection','Select a product first')
            return
        pid = selected[0]
        qty = self.qty_var.get()
        ok,msg = self.order.add_item(pid, qty)
        if not ok:
            messagebox.showerror('Error', msg)
            return
        self.refresh_cart()

    def refresh_cart(self):
        for r in self.cart_tree.get_children():
            self.cart_tree.delete(r)
        for it in self.order.items:
            self.cart_tree.insert('', 'end', iid=it.product_id, values=(f'{it.price:.2f}', it.qty, f'{it.price*it.qty:.2f}'))
        self.summary_lbl.config(text=f'Total: {self.order.total():.2f}')

    def remove_selected(self):
        sel = self.cart_tree.selection()
        if not sel:
            return
        pid = sel[0]
        self.order.remove_item(pid)
        self.refresh_cart()

    def confirm_order(self):
        if not self.order.items:
            messagebox.showwarning('Empty cart','Add items before confirming')
            return
        customer = simpledialog.askstring('Customer name','Enter customer name (optional):') or ''
        while not customer.isalpha():  # only letters
            customer = simpledialog.askstring('Customer name','Enter customer name (letters only):') or ''

        order_data = self.order.confirm(customer)
        # save to sales
        self.report.save_order(order_data)
        messagebox.showinfo('Order confirmed', f'Order saved. Total: {order_data["total"]:.2f}')
        self.inventory.load()
        self.refresh_products()
        self.refresh_cart()

    def restock(self):
        self.inventory.restock_from_csv()
        self.inventory.load()
        self.refresh_products()
        messagebox.showinfo('Restock','Restock applied from restock.csv (if exists)')

if __name__ == '__main__':
    app = App()
    app.mainloop()
    
    






