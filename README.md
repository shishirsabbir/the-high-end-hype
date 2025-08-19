# The High-End Hype

The High-End Hype is a comprehensive Shopify project focused on aggregating and showcasing the latest products from the world's top shoe brands. This project automates the process of scraping product data from leading footwear websites, storing the information in a robust FastAPI + SQLAlchemy backend, and seamlessly uploading curated collections to a customized Shopify store.

## Features

- **Web Scraping:** Automatically extracts product details from 10 leading shoe brands, including Nike, Adidas, Puma, and more.
- **Backend API:** Utilizes FastAPI and SQLAlchemy for efficient data storage, management, and retrieval.
- **Shopify Integration:** Uploads product data directly to a Shopify store, streamlining inventory management.
- **Store Customization:** Provides tailored Shopify customizations to enhance user experience and brand identity.

## Tech Stack

- **Python** (Scraping, API, Database)
- **FastAPI** (RESTful API)
- **SQLAlchemy** (ORM for database operations)
- **Shopify API** (Store integration and customization)

## Getting Started

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/the-high-end-hype.git
   cd the-high-end-hype
2. **Install Dependencies**
```bash
pip install -r requirements.txt
```
3. **Configure Environment**
- Set up your database connection in .env
- Add Shopify API credentials
4. **Run the Scraper**
```python
python crawler/main.py
```
5. **Start FastAPI server**
```bash
fastapi dev
```
6. **Upload Products to Shopify**
- Use provided scripts or API endpoints to sync data.
Customization
- Modify Shopify themes and settings as needed in the ```shopify/``` directory.
- Refer to the documentation for advanced customization options.

## Developers
1. Shishir Sabbir
2. Elias Ahmed
