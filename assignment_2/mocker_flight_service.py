import asyncio
import json
import random
from datetime import datetime
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import StreamingResponse

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
    airline = random.choice(
        ['THY100', 'KLM100', 'BAW100', 'SAS100', 'RYR100', 'AAR100', 'MEA100', 'SEH100', 'HYS100', 'FDB100'])
    return f"{airline}"


flight_positions = {}


def generate_random_flight_data() -> Dict[str, Any]:
    now = datetime.utcnow()
    has_hex = random.random() > 0.1
    has_callsign = random.random() > 0.1

    fr24_id = ''.join(random.choices('0123456789abcdef', k=8))
    if fr24_id not in flight_positions:
        lat = random.uniform(45.0, 50.0)
        lon = random.uniform(14.0, 22.0)
        flight_positions[fr24_id] = (lat, lon)
    else:
        lat, lon = flight_positions[fr24_id]
        lat += random.uniform(0.001, 0.01)
        lon += random.uniform(0.001, 0.01)
        flight_positions[fr24_id] = (lat, lon)

    flight = {
        "fr24_id": fr24_id,
        "hex": generate_random_hex() if has_hex else None,
        "callsign": generate_random_callsign() if has_callsign else None,
        "lat": round(lat, 5),
        "lon": round(lon, 5),
        "track": random.randint(0, 359),
        "alt": random.choice([38000, 39000, 40000, 41000]),
        "gspeed": random.randint(260, 500),
        "vspeed": random.choice([-64, -32, 0, 32, 64]),
        "squawk": ''.join(random.choices('01234567', k=4)),
        "timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": random.choice(["ADSB", "MLAT"])
    }

    return flight


async def flight_data_generator():
    while True:
        flights = [generate_random_flight_data() for _ in range(5)]
        yield f"data: {json.dumps(flights)}\n\n"
        await asyncio.sleep(1)


@app.get("/stream")
async def stream_flights():
    return StreamingResponse(flight_data_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
