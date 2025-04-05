import asyncio
import random
import string
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI()


class FlightData(BaseModel):
    fr24_id: str
    hex: Optional[str]
    callsign: Optional[str]
    lat: float
    lon: float
    track: int
    alt: int
    gspeed: int
    vspeed: int
    squawk: str
    timestamp: str
    source: str


def generate_random_hex() -> str:
    return ''.join(random.choices('0123456789ABCDEF', k=6))


def generate_random_callsign() -> str:
    airline = random.choice(['THY', 'KLM', 'BAW', 'SAS', 'RYR', 'AAR', 'MEA', 'SEH', 'HYS', 'FDB'])
    numbers = ''.join(random.choices('0123456789', k=random.randint(2, 3)))
    letters = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 3)))
    return f"{airline}{numbers}{letters}"


def generate_random_flight_data() -> Dict[str, Any]:
    now = datetime.utcnow()
    has_hex = random.random() > 0.1  # 90% chance to have hex
    has_callsign = random.random() > 0.1  # 90% chance to have callsign

    lat = random.uniform(45.0, 50.0)
    lon = random.uniform(14.0, 22.0)

    flight = {
        "fr24_id": ''.join(random.choices('0123456789abcdef', k=8)),
        "hex": generate_random_hex() if has_hex else None,
        "callsign": generate_random_callsign() if has_callsign else None,
        "lat": round(lat, 5),
        "lon": round(lon, 5),
        "track": random.randint(0, 359),
        "alt": random.choice([38000, 39000, 40000, 41000]),
        "gspeed": random.randint(260, 500),
        "vspeed": random.choice([-64, -32, 0, 32, 64]),
        "squawk": ''.join(random.choices('01234567', k=4)),
        "timestamp": (now - timedelta(seconds=random.randint(0, 60))).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": random.choice(["ADSB", "MLAT"])
    }

    return flight


async def flight_data_generator():
    while True:
        flight_data = generate_random_flight_data()
        yield f"data: {flight_data}\n\n"
        await asyncio.sleep(0.01)  # Wait 1 second before sending the next data


@app.get("/flights/stream")
async def stream_flights():
    return StreamingResponse(flight_data_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
