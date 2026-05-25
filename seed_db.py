import sys
import os
import logging

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, engine, Base
from backend.models import Country
from backend.scraper.scheduler import run_all_scrapers

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def reseed_database():
    logger.info("Starting database reseed (real scrapers only)...")
    
    logger.info("Dropping existing database tables...")
    Base.metadata.drop_all(bind=engine)
    
    logger.info("Creating fresh database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        logger.info("Seeding global country catalog...")
        countries_list = [
            {"name": "United States", "code": "US", "continent": "North America"},
            {"name": "Japan", "code": "JP", "continent": "Asia"},
            {"name": "Germany", "code": "DE", "continent": "Europe"},
            {"name": "United Kingdom", "code": "GB", "continent": "Europe"},
            {"name": "Canada", "code": "CA", "continent": "North America"},
            {"name": "Australia", "code": "AU", "continent": "Oceania"},
            {"name": "India", "code": "IN", "continent": "Asia"},
            {"name": "Nepal", "code": "NP", "continent": "Asia"},
            {"name": "France", "code": "FR", "continent": "Europe"},
            {"name": "Sweden", "code": "SE", "continent": "Europe"},
            {"name": "Singapore", "code": "SG", "continent": "Asia"},
            {"name": "South Korea", "code": "KR", "continent": "Asia"},
            {"name": "Brazil", "code": "BR", "continent": "South America"},
            {"name": "Netherlands", "code": "NL", "continent": "Europe"}
        ]
        
        for item in countries_list:
            c = Country(name=item["name"], code=item["code"], continent=item["continent"])
            db.add(c)
        db.commit()
        logger.info(f"Cataloged {len(countries_list)} countries.")
        
    except Exception as e:
        logger.error(f"Failed to seed database: {e}")
        db.rollback()
    finally:
        db.close()
    
    logger.info("Running real scrapers to populate jobs...")
    run_all_scrapers()
    logger.info("Database reseed complete.")

if __name__ == "__main__":
    reseed_database()
