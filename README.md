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

<img width="491" height="719" alt="stripe1" src="https://github.com/user-attachments/assets/1de5ce15-ad13-49b5-8d11-5f259ee16f2c" />
<img width="488" height="713" alt="stripe2" src="https://github.com/user-attachments/assets/7ed60c55-cba6-490e-9a27-1f2d5e66fc1c" />


## 🛠️ Installation & Setup

You can run this application in two ways: by downloading the ready-to-use executable or by running the Python source code.

### Option 1

1. Go to the Releases page on the right side of this repository.
2. Download the latest .exe file.
3. Double-click the downloaded file to run it. 
(Note: Windows Defender might show a warning. Click 'More info' -> 'Run anyway').

### Option 2

Prerequisites: You need to have Python 3.8+ installed on your computer.

1. Clone the repository:
git clone https://github.com/HRSCe/Stripe-pay-link-generator.git

2. Enter the directory:
cd StripeLinkGenerator

3. Create a virtual environment:
python -m venv .venv

4. Activate the virtual environment:
- On Windows: .venv\Scripts\activate
- On macOS/Linux: source .venv/bin/activate

5. Install the required dependencies:
pip install -r requirements.txt

6. Run the application:
python main.py

---

## Initial Setup (How to get your Stripe Key)

1. Log in to your Stripe Dashboard.
2. Turn on 'Test mode' if you just want to test it.
3. Go to Developers -> API keys.
4. Copy your Secret key (sk_test_... or sk_live_...).
5. Open the app, go to Settings, paste the key, and set your currency.
6. Click SAVE.

⚠️ Requirements
Python 3.8+
A valid Stripe account and API keys.
