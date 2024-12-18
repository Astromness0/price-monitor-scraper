# 🛒 E-commerce Price Monitor

A Python-based web scraper that monitors product prices across multiple online stores and sends alerts when prices drop below a specified threshold.

## Features

- ✅ Monitor multiple products simultaneously
- ✅ Configurable price drop threshold
- ✅ Email notifications for price drops
- ✅ Price history tracking
- ✅ Customizable check intervals
- ✅ Support for any website with CSS selectors

## Requirements

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.json` to add your products and email settings:

```json
{
  "price_drop_threshold": 10,
  "products": [
    {
      "name": "Gaming Laptop",
      "url": "https://store.com/laptop",
      "price_selector": ".product-price"
    }
  ],
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "from": "your-email@gmail.com",
    "to": "alerts@gmail.com",
    "username": "your-email@gmail.com",
    "password": "your-app-password"
  }
}
```

## Usage

### Basic monitoring (checks every hour):
```bash
python scraper.py
```

### Custom interval (checks every 30 minutes):
```python
monitor = PriceMonitor()
monitor.monitor(interval=1800)  # 30 minutes in seconds
```

## How It Works

1. **Web Scraping**: Uses BeautifulSoup to extract prices from product pages
2. **Price Tracking**: Compares current price with previous price
3. **Alert System**: Sends email when price drops by threshold percentage
4. **Data Persistence**: Saves price history to JSON file

## Finding CSS Selectors

1. Open product page in browser
2. Right-click on price element → Inspect
3. Copy CSS selector from browser DevTools
4. Add to config.json

## Example Output

```
Starting price monitor for 3 products...
Gaming Laptop: $899.99
Wireless Headphones: $79.99
Price drop alert: Gaming Laptop - $849.99 (5.6% off)
Alert sent for Gaming Laptop
Waiting 3600 seconds before next check...
```

## Use Cases

- 🎮 Track gaming console/GPU prices
- 📱 Monitor smartphone deals
- 👟 Watch for sneaker drops
- 🏠 Home appliances price tracking
- 📚 Textbook price monitoring

## Notes

- Respect website robots.txt and terms of service
- Add delays between requests to avoid rate limiting
- Some sites may require additional anti-bot bypass techniques

## License

MIT License - Feel free to use and modify

## Troubleshooting

**Issue: SSL Certificate errors**
- Solution: Add `verify=False` to requests (not recommended for production)

**Issue: Rate limiting**
- Solution: Increase interval between checks
