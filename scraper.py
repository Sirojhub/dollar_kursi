import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
import config

logger = logging.getLogger(__name__)

async def fetch_cbu_rates():
    """Fetches official rates from CBU API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(config.CBU_API_URL) as response:
                if response.status == 200:
                    data = await response.json()
                    for item in data:
                        if item['Ccy'] == 'USD':
                            return float(item['Rate'])
    except Exception as e:
        logger.error(f"Error fetching CBU rates: {e}")
    return None

async def fetch_agrobank_rates():
    """Attempts to fetch from Agrobank (Placeholder for future implementation)."""
    # In this environment, we know this will likely fail or return static HTML without data.
    # Implementation kept for structure.
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(config.AGROBANK_URL) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    # Placeholder: Logic to parse if they switch to SSR or we use a browser
                    return None
    except Exception as e:
        logger.error(f"Error fetching Agrobank rates: {e}")
    return None

async def get_current_rates():
    """
    Orchestrates fetching rates.
    Returns a dict: {'buy': float, 'sell': float, 'cb': float, 'source': str}
    """
    # Try Agrobank first (Best Effort)
    agro_rate = await fetch_agrobank_rates()
    
    # Always fetch CBU for comparison/fallback
    cbu_rate = await fetch_cbu_rates()

    if agro_rate:
        return {
            'buy': agro_rate['buy'],
            'sell': agro_rate['sell'],
            'cb': cbu_rate if cbu_rate else 0,
            'source': 'Agrobank'
        }
    elif cbu_rate:
        return {
            'buy': cbu_rate - 20, 
            'sell': cbu_rate + 20, 
            'cb': cbu_rate,
            'source': 'CBU (Fallback)'
        }
    else:
        # Final Fallback: Mock Data for Testing/Demo
        # Since government APIs are blocking requests in this environment
        logger.warning("All APIs failed. Using MOCK data.")
        return {
            'buy': 12800.0,
            'sell': 12900.0,
            'cb': 12850.0,
            'source': 'Mock Data (Test Mode)'
        }
