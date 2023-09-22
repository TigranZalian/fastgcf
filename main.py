# Import necessary modules
import asyncio
from datetime import date
from fastgcf import router

# Simply use a decorator
@router.get()
async def main(start_date: date, end_date: date):
    await asyncio.sleep(1)  # Simulate async processing
    return {"start_date": start_date, "end_date": end_date}

# That's it! Your Google Cloud Function is ready to handle and validate async GET requests seamlessly.