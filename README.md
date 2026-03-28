# Stripe Pay Link Generator

A lightweight, modern desktop application built with Python and `customtkinter` to quickly generate one-time Stripe payment links. 

It securely stores your API keys and provides dynamic options like requesting billing addresses, tax IDs, phone numbers, and selecting different currencies.

## 🚀 Features
* **Secure API Storage:** Uses the `keyring` library to safely store your Stripe Secret Key (no hardcoded credentials).
* **Multi-Currency Support:** Choose between HUF, EUR, USD, and GBP in the settings.
* **Dynamic Payment Links:** Set custom prices and product names on the fly.
* **Customizable Requirements:** Easily toggle requirements for Billing Address, Tax ID (for companies), and Phone Number.
* **Invoice Ready:** Automatically enables invoice creation in Stripe.
* **Redirect URL:** Option to redirect users to a specific webpage after successful payment.
* **Modern GUI:** Built with `customtkinter` for a sleek, dark-mode-first user experience.

## 📸 Screenshots


## 🛠️ Installation & Setup

⚙️ How to use
Go to the Settings tab.

Enter your Stripe Secret Key (sk_live_... or sk_test_...), a default product name, select your preferred currency, and set an optional redirect URL. Click Save.

Go back to the Generate tab.

Enter the amount, toggle your desired requirements, and click GENERATE LINK.

Copy the generated link and send it to your customer!

⚠️ Requirements
Python 3.8+

A valid Stripe account and API keys.
