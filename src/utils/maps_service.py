import requests
import math
from typing import Dict, Tuple, Optional


class MapsService:

    # API Endpoints
    NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org"

    HEADERS = {"User-Agent": "DonationApp/1.0 (Flet Python App)"}

    # config: shipping cost
    BASE_SHIPPING_COST = 10000
    COST_PER_KM = 2000
    MAX_DISTANCE_KM = 100

    # convert: address string ke coordinates
    @staticmethod
    def geocode_address(address: str) -> Optional[Dict]:
        try:
            params = {"q": address, "format": "json", "limit": 1, "addressdetails": 1}

            response = requests.get(
                f"{MapsService.NOMINATIM_BASE_URL}/search",
                params=params,
                headers=MapsService.HEADERS,
                timeout=10,
            )
            response.raise_for_status()

            results = response.json()
            if results and len(results) > 0:
                result = results[0]
                return {
                    "lat": float(result["lat"]),
                    "lon": float(result["lon"]),
                    "display_name": result.get("display_name", ""),
                    "city": result.get("address", {}).get("city", ""),
                    "country": result.get("address", {}).get("country", ""),
                }
            return None

        except Exception as e:
            print(f"Geocoding error: {e}")
            return None

    # convert: coordinates ke address string
    @staticmethod
    def reverse_geocode(lat: float, lon: float) -> Optional[str]:
        try:
            params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1}

            response = requests.get(
                f"{MapsService.NOMINATIM_BASE_URL}/reverse",
                params=params,
                headers=MapsService.HEADERS,
                timeout=10,
            )
            response.raise_for_status()

            result = response.json()
            return result.get("display_name", None)

        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return None

    @staticmethod
    def calculate_distance(
        origin: Tuple[float, float], destination: Tuple[float, float]
    ) -> float:
        lat1, lon1 = origin
        lat2, lon2 = destination

        R = 6371.0

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return round(distance, 2)

    @staticmethod
    def calculate_shipping_cost(distance_km: float) -> Dict:
        if distance_km > MapsService.MAX_DISTANCE_KM:
            return {
                "cost": None,
                "distance": distance_km,
                "message": f"Shipping not available for distances over {MapsService.MAX_DISTANCE_KM} km",
            }

        cost = MapsService.BASE_SHIPPING_COST + (distance_km * MapsService.COST_PER_KM)
        cost = round(cost, -3)

        return {
            "cost": int(cost),
            "distance": distance_km,
            "message": f"Shipping cost for {distance_km} km",
        }

    @staticmethod
    def lat_lon_to_tile(lat: float, lon: float, zoom: int) -> Tuple[int, int]:
        n = 2.0**zoom
        x_tile = int((lon + 180.0) / 360.0 * n)
        y_tile = int(
            (
                1.0
                - math.log(
                    math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))
                )
                / math.pi
            )
            / 2.0
            * n
        )
        return x_tile, y_tile

    @staticmethod
    def get_static_map_url(
        lat: float, lon: float, zoom: int = 15, width: int = 500, height: int = 250
    ) -> str:
        services = [
            # 1: Google-like static maps
            f"https://maps.geoapify.com/v1/staticmap?style=osm-bright&width={width}&height={height}&center=lonlat:{lon},{lat}&zoom={zoom}&marker=lonlat:{lon},{lat};color:%23ff0000;size:medium&apiKey=",
            # 2: MapBox-style
            f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-s+ff0000({lon},{lat})/{lon},{lat},{zoom}/{width}x{height}?access_token=pk.test",
            # 3: Direct OSM tile
            MapsService._get_osm_tile_url(lat, lon, zoom, width, height),
        ]

        url = services[2]
        print(f"[DEBUG] Generated map URL: {url}")
        return url

    @staticmethod
    def _get_osm_tile_url(
        lat: float, lon: float, zoom: int, width: int, height: int
    ) -> str:
        x_tile, y_tile = MapsService.lat_lon_to_tile(lat, lon, zoom)

        # OpenStreetMap tile serve
        # alternative servers lain: a.tile.openstreetmap.org, b.tile.openstreetmap.org, c.tile.openstreetmap.org
        url = f"https://tile.openstreetmap.org/{zoom}/{x_tile}/{y_tile}.png"

        print(f"[DEBUG] OSM Tile URL: {url}")
        print(f"[DEBUG] Tile coordinates: x={x_tile}, y={y_tile}, zoom={zoom}")

        return url

    @staticmethod
    def get_static_map_url_alternative(
        lat: float, lon: float, zoom: int = 15, width: int = 500, height: int = 250
    ) -> str:
        # location IQ (OpenStreetMap-based)
        url = f"https://maps.locationiq.com/v3/staticmap?key=pk.0f147952a41c555a5b70614039fd148b&center={lat},{lon}&zoom={zoom}&size={width}x{height}&format=png&markers=icon:small-red-cutout|{lat},{lon}"

        print(f"[DEBUG] LocationIQ URL: {url}")
        return url

    @staticmethod
    def parse_seller_address(seller_address: str) -> Optional[Tuple[float, float]]:
        result = MapsService.geocode_address(seller_address)
        if result:
            return (result["lat"], result["lon"])
        return None
