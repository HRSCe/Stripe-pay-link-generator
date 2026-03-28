import threading
import customtkinter as ctk
import stripe
import pyperclip
import keyring

# --- SETTINGS ---
SERVICE_NAME = "StripeLinkGenerator"
USERNAME = "AdminUser"
REDIRECT_KEY = "redirect_url"
PRODUCT_NAME_KEY = "product_name"
CURRENCY_KEY = "currency" # Új kulcs a pénznemnek

def get_api_key():
    return keyring.get_password(SERVICE_NAME, USERNAME) or ""

def set_api_key(api_key):
    keyring.set_password(SERVICE_NAME, USERNAME, api_key)

def get_redirect_url():
    return keyring.get_password(SERVICE_NAME, REDIRECT_KEY) or ""

def set_redirect_url(url):
    if not url: 
        try: 
            keyring.delete_password(SERVICE_NAME, REDIRECT_KEY)
        except Exception: 
            pass
    else:
        keyring.set_password(SERVICE_NAME, REDIRECT_KEY, url)

def get_product_name():
    return keyring.get_password(SERVICE_NAME, PRODUCT_NAME_KEY) or ""

def set_product_name(name):
    if not name:
        try: 
            keyring.delete_password(SERVICE_NAME, PRODUCT_NAME_KEY)
        except Exception: 
            pass
    else:
        keyring.set_password(SERVICE_NAME, PRODUCT_NAME_KEY, name)

# Új funkciók a pénznem mentéséhez/betöltéséhez
def get_currency():
    return keyring.get_password(SERVICE_NAME, CURRENCY_KEY) or "huf"

def set_currency(currency):
    if not currency:
        try:
            keyring.delete_password(SERVICE_NAME, CURRENCY_KEY)
        except Exception:
            pass
    else:
        keyring.set_password(SERVICE_NAME, CURRENCY_KEY, currency.lower())

# --- MAIN APPLICATION ---
class StripeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Stripe Pro Link Generator")
        self.geometry("500x700") # Kicsit megnöveltem a magasságot, hogy minden elférjen
        self.resizable(False, False)
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.tabview = ctk.CTkTabview(self, width=460, height=650)
        self.tabview.pack(padx=20, pady=20)

        self.tab_main = self.tabview.add("Generate")
        self.tab_settings = self.tabview.add("Settings")

        # --- GENERATE TAB ---
        # Frissítve: kivettem a (HUF) fix szöveget
        self.label_info = ctk.CTkLabel(self.tab_main, text="Amount - One-time payment!", font=("Roboto", 14, "bold"))
        self.label_info.pack(pady=(15, 5))

        self.entry_amount = ctk.CTkEntry(self.tab_main, placeholder_text="e.g. 17000", width=200, height=40, font=("Roboto", 18))
        self.entry_amount.pack(pady=5)

        # --- OPTIONS (CHECKBOXES) ---
        self.options_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        self.options_frame.pack(pady=15)

        self.check_billing = ctk.CTkCheckBox(self.options_frame, text="Require Billing Address (Name + Address)", font=("Roboto", 12))
        self.check_billing.pack(anchor="w", pady=5)
        self.check_billing.select() 

        self.check_tax = ctk.CTkCheckBox(self.options_frame, text="Require Tax ID (For Companies)", font=("Roboto", 12))
        self.check_tax.pack(anchor="w", pady=5)

        self.check_phone = ctk.CTkCheckBox(self.options_frame, text="Require Phone Number", font=("Roboto", 12))
        self.check_phone.pack(anchor="w", pady=5)

        # BUTTON
        self.btn_generate = ctk.CTkButton(self.tab_main, text="GENERATE LINK", command=self.start_generation_thread, width=250, height=50, font=("Roboto", 14, "bold"), fg_color="#D94538", hover_color="#B5362B")
        self.btn_generate.pack(pady=10)

        # RESULT
        self.result_frame = ctk.CTkFrame(self.tab_main, fg_color="transparent")
        self.result_frame.pack(pady=10)

        self.entry_result = ctk.CTkEntry(self.result_frame, placeholder_text="Link will appear here...", width=300, height=35)
        self.entry_result.pack(side="left", padx=(0, 10))

        self.btn_copy = ctk.CTkButton(self.result_frame, text="📋", width=40, height=35, command=self.copy_to_clipboard, font=("Arial", 20))
        self.btn_copy.pack(side="left")

        self.label_status = ctk.CTkLabel(self.tab_main, text="", text_color="gray")
        self.label_status.pack(pady=10)

        # --- SETTINGS TAB ---
        self.label_api = ctk.CTkLabel(self.tab_settings, text="Stripe Secret Key:", font=("Roboto", 14))
        self.label_api.pack(pady=(10, 5))
        self.entry_api = ctk.CTkEntry(self.tab_settings, width=350, placeholder_text="sk_live_...", show="*")
        self.entry_api.pack(pady=5)
        
        self.label_prod = ctk.CTkLabel(self.tab_settings, text="Product Name on Invoice:", font=("Roboto", 14))
        self.label_prod.pack(pady=(15, 5))
        self.entry_prod = ctk.CTkEntry(self.tab_settings, width=350, placeholder_text="e.g. Accommodation fee")
        self.entry_prod.pack(pady=5)

        # ÚJ: Pénznem választó
        self.label_currency = ctk.CTkLabel(self.tab_settings, text="Currency:", font=("Roboto", 14))
        self.label_currency.pack(pady=(15, 5))
        self.combo_currency = ctk.CTkComboBox(self.tab_settings, values=["huf", "eur", "usd", "gbp"], width=350)
        self.combo_currency.pack(pady=5)

        self.label_redirect = ctk.CTkLabel(self.tab_settings, text="Redirect URL after payment (Optional):", font=("Roboto", 14))
        self.label_redirect.pack(pady=(15, 5))
        self.entry_redirect = ctk.CTkEntry(self.tab_settings, width=350)
        self.entry_redirect.pack(pady=5)

        # Load saved data
        if get_api_key(): self.entry_api.insert(0, get_api_key())
        if get_product_name(): self.entry_prod.insert(0, get_product_name())
        if get_redirect_url(): self.entry_redirect.insert(0, get_redirect_url())
        self.combo_currency.set(get_currency().lower()) # Betölti a mentett pénznemet

        self.btn_save = ctk.CTkButton(self.tab_settings, text="SAVE", command=self.save_settings, fg_color="green", hover_color="darkgreen")
        self.btn_save.pack(pady=20)
        
        self.label_settings_status = ctk.CTkLabel(self.tab_settings, text="", text_color="gray")
        self.label_settings_status.pack(pady=5)

    def save_settings(self):
        set_api_key(self.entry_api.get().strip())
        set_product_name(self.entry_prod.get().strip())
        set_redirect_url(self.entry_redirect.get().strip())
        set_currency(self.combo_currency.get().strip()) # Pénznem mentése
        self.label_settings_status.configure(text="Settings saved!", text_color="green")

    def copy_to_clipboard(self):
        link = self.entry_result.get()
        if link:
            pyperclip.copy(link)
            original = self.btn_copy.cget("fg_color")
            self.btn_copy.configure(fg_color="#2CC985") 
            self.after(1000, lambda: self.btn_copy.configure(fg_color=original))

    def start_generation_thread(self):
        threading.Thread(target=self.generate_link, daemon=True).start()

    def generate_link(self):
        api_key = get_api_key()
        redirect_url = get_redirect_url()
        product_name = get_product_name() or "Service Fee"
        currency = get_currency() # Pénznem lekérése

        if not api_key:
            self.label_status.configure(text="ERROR: No API key!", text_color="red")
            return

        amount_str = self.entry_amount.get().strip()
        if not amount_str.isdigit():
            self.label_status.configure(text="ERROR: Enter a valid number!", text_color="red")
            return

        req_billing = self.check_billing.get()
        req_tax = self.check_tax.get()
        req_phone = self.check_phone.get()

        self.btn_generate.configure(state="disabled", text="Working...")
        self.label_status.configure(text="Generating...", text_color="yellow")

        try:
            stripe.api_key = api_key
            price = stripe.Price.create(
                currency=currency, # Dinamikusan beállított pénznem
                unit_amount=int(amount_str) * 100,
                product_data={"name": product_name},
            )

            params = {
                "line_items": [{"price": price.id, "quantity": 1}],
                "restrictions": {"completed_sessions": {"limit": 1}},
                "invoice_creation": {"enabled": True} 
            }
            
            if req_billing:
                params["billing_address_collection"] = "required"
            else:
                params["billing_address_collection"] = "auto"

            if req_tax:
                params["tax_id_collection"] = {"enabled": True}
            
            if req_phone:
                params["phone_number_collection"] = {"enabled": True}

            if redirect_url and redirect_url.startswith("http"):
                params["after_completion"] = {"type": "redirect", "redirect": {"url": redirect_url}}
            
            payment_link = stripe.PaymentLink.create(**params)
            
            final_url = payment_link.url
            self.entry_result.delete(0, "end")
            self.entry_result.insert(0, final_url)
            pyperclip.copy(final_url)
            self.label_status.configure(text=f"DONE! ({product_name})", text_color="#2CC985")

        except Exception as e:
            self.label_status.configure(text="An error occurred!", text_color="red")
            print(e)
        finally:
            self.btn_generate.configure(state="normal", text="GENERATE LINK")

if __name__ == "__main__":
    app = StripeApp()
    app.mainloop()