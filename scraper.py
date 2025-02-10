#!/usr/bin/env python3
"""
E-commerce Price Monitor
Monitors product prices across multiple online stores and sends alerts
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class PriceMonitor:
    def __init__(self, config_file='config.json'):
        """Initialize the price monitor with configuration"""
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        self.products = self.config.get('products', [])
        self.threshold = self.config.get('price_drop_threshold', 10)
        
    def get_headers(self):
        """Return headers to mimic a real browser"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def extract_price(self, html, selector):
        """Extract price from HTML using CSS selector"""
        soup = BeautifulSoup(html, 'html.parser')
        price_element = soup.select_one(selector)
        
        if price_element:
            price_text = price_element.text.strip()
            # Remove currency symbols and convert to float
            price = float(''.join(filter(str.isdigit or str.isdecimal, price_text.replace(',', '.'))))
            return price
        return None
    
    def check_price(self, product):
        """Check current price for a product"""
        try:
            response = requests.get(product['url'], headers=self.get_headers(), timeout=15)
            response.raise_for_status()
            
            current_price = self.extract_price(response.text, product['price_selector'])
            
            if current_price:
                product['last_checked'] = datetime.now().isoformat()
                
                if 'last_price' in product:
                    price_diff = product['last_price'] - current_price
                    price_drop_percent = (price_diff / product['last_price']) * 100
                    
                    if price_drop_percent >= self.threshold:
                        self.send_alert(product, current_price, price_drop_percent)
                
                product['last_price'] = current_price
                return current_price
            
        except Exception as e:
            print(f"Error checking {product['name']}: {str(e)}")
            return None
    
    def send_alert(self, product, new_price, drop_percent):
        """Send email alert for price drop"""
        email_config = self.config.get('email', {})
        
        if not email_config.get('enabled', False):
            print(f"Price drop alert: {product['name']} - ${new_price} ({drop_percent:.1f}% off)")
            return
        
        msg = MIMEMultipart()
        msg['From'] = email_config['from']
        msg['To'] = email_config['to']
        msg['Subject'] = f"Price Drop Alert: {product['name']}"
        
        body = f"""
        Price Drop Detected!
        
        Product: {product['name']}
        New Price: ${new_price}
        Previous Price: ${product['last_price']}
        Discount: {drop_percent:.1f}%
        
        Link: {product['url']}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            server.send_message(msg)
            server.quit()
            print(f"Alert sent for {product['name']}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
    
    def monitor(self, interval=1800):
        """Monitor prices at specified interval (in seconds)"""
        print(f"Starting price monitor for {len(self.products)} products...")
        
        while True:
            for product in self.products:
                price = self.check_price(product)
                if price:
                    print(f"{product['name']}: ${price}")
            
            # Save updated prices
            self.save_data()
            
            print(f"Waiting {interval} seconds before next check...")
            time.sleep(interval)
    
    def save_data(self):
        """Save current state to file"""
        with open('price_history.json', 'w') as f:
            json.dump(self.products, f, indent=2)

if __name__ == '__main__':
    monitor = PriceMonitor()
    monitor.monitor(interval=1800)  # Check every hour

# Additional utility functions can be added here
