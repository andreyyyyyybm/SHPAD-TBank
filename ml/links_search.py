import datetime
from urllib.parse import quote

def build_travel_links(destination, checkin, checkout, min_price=None, max_price=None, adults=1, rooms=1):
    print(type(checkin))
    if type(checkin) == datetime.datetime:
        checkin = checkin.strftime("%Y-%m-%d")
    if type(checkout) == datetime.datetime:
        checkout = checkout.strftime("%Y-%m-%d")

    encoded_destination = quote(destination)


    price_filter = f"{min_price}-{max_price}" if min_price and max_price else ""


    booking_url = (
        f"https://www.booking.com/searchresults.html"
        f"?ss={encoded_destination}"
        f"&checkin_year={checkin[:4]}&checkin_month={int(checkin[5:7])}&checkin_monthday={int(checkin[8:])}"
        f"&checkout_year={checkout[:4]}&checkout_month={int(checkout[5:7])}&checkout_monthday={int(checkout[8:])}"
        f"&nflt=price%3D{price_filter}"
        f"&group_adults={adults}&no_rooms={rooms}"
    )


    ostrovok_url = (
        f"https://ostrovok.ru/hotel/russia/{encoded_destination.lower()}/?"
        f"checkIn={checkin}&checkOut={checkout}"
        f"&adults={adults}&rooms={rooms}"
    )

    aviasales_url = (
        f"https://www.aviasales.ru/search?origin=LED&destination={encoded_destination}"
        f"&depart_date={checkin}&return_date={checkout}&adults={adults}"
    )

    return {
        "booking": booking_url,
        "ostrovok": ostrovok_url,
        "aviasales": aviasales_url
    }

if __name__ == "__main__":
    destination = "Thailand"
    checkin = "2025-06-05"
    checkout = "2025-06-09"
    min_price = 1000
    max_price = 5000 
    guests_num = 1
    rooms = 1

    links = build_travel_links(destination, checkin, checkout, min_price, max_price, guests_num, rooms)

    for name, url in links.items():
        print(f"{name}: {url}")
