import datetime
from urllib.parse import quote

def build_travel_links(destination, checkin, checkout, min_price=None, max_price=None, adults=2, rooms=1):
    if type(checkin) == datetime.datetime:
        checkin = checkin.strftime("%Y-%m-%d")
    if type(checkout) == datetime.datetime:
        checkout = checkout.strftime("%Y-%m-%d")
    encoded_destination = quote(destination)


    price_filter = f"{min_price}-{max_price}" if min_price and max_price else ""
    
    booking_url = (
        f"https://www.booking.com/searchresults.html"
        f"?ss={destination}"
        f"&checkin_year={checkin[:4]}&checkin_month={int(checkin[5:7])}&checkin_monthday={int(checkin[8:])}"
        f"&checkout_year={checkout[:4]}&checkout_month={int(checkout[5:7])}&checkout_monthday={int(checkout[8:])}"
        f"&nflt=price%3D{price_filter}"
        f"&group_adults={adults}&no_rooms={rooms}"
    )


    google_flight_url = (
        f"https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{checkin}%20to%20{checkout}"
    )

    return {
        "booking": booking_url,
        "google_flights": google_flight_url
    }



# links = build_travel_links(
#     destination="Thailand",
#     checkin="2025-06-05",
#     checkout="2025-06-09",
#     min_price=1000,
#     max_price=5000,
#     adults=2,
#     rooms=2
# )
#
# for name, url in links.items():
#     print(f"{name}: {url}")
