import asyncio
from datetime import date
from fastgcf import router

# Simply use a decorator
@router.get()
async def main(start_date: date, end_date: date):
    return {"start_date": start_date, "end_date": end_date}
