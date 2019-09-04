from search_for_result.bandsintown_ask import ask_for_events
from search_for_result.kiwi_ask import ask_for_flights
from search_for_result.stay22_ask import ask_for_place
import calendar, datetime


def find_best_results(information):
    error = False
    upcoming = ask_for_events(information["artist"], "upcoming")
    suitable_upcoming = []
    wrong_date_same_country_upcoming = []
    ok_date_same_country_upcoming = []

    def search_nearest_free_dates(date):
        full_trip = [date]

        def next_day(date2):
            date2 = date2.split("/")
            day = date2[0]
            if day[0] == "0":
                day = int(day[1])
            else:
                day = int(day)
            month = date2[1]
            if month[0] == "0":
                month = int(month[1])
            else:
                month = int(month)
            year = int(date2[2])
            if day < calendar.monthrange(year, month)[1]:
                next_day, next_month, next_year = str(day + 1), str(
                    month), str(year)
            elif month == 12:
                next_day, next_month, next_year = str(1), str(1), str(year + 1)
            else:
                next_day, next_month, next_year = str(1), str(month + 1), str(
                    year)
            if len(next_day) == 1:
                next_day = "0" + next_day
            if len(next_month) == 1:
                next_month = "0" + next_month
            return "/".join([next_day, next_month, next_year])

        if next_day(date) not in information["free_dates"]:
            return False

        def previous_day(date2):
            date2 = date2.split("/")
            day = date2[0]
            if day[0] == "0":
                day = int(day[1])
            else:
                day = int(day)
            month = date2[1]
            if month[0] == "0":
                month = int(month[1])
            else:
                month = int(month)
            year = int(date2[2])
            if day == 1 and month == 1:
                previous_day, previous_month, previous_year = str(
                    calendar.monthrange(year - 1, 12)), str(12), str(year - 1)
            elif day == 1:
                previous_day, previous_month, previous_year = str(
                    calendar.monthrange(year, month - 1)), str(month - 1), str(
                    year)
            else:
                previous_day, previous_month, previous_year = str(
                    day - 1), str(month), str(year)
            if len(previous_day) == 1:
                previous_day = "0" + previous_day
            if len(previous_month) == 1:
                previous_month = "0" + previous_month
            return "/".join([previous_day, previous_month, previous_year])

        date2 = date
        while previous_day(date2) in information["free_dates"]:
            full_trip.append(previous_day(date2))
            date2 = previous_day(date2)
        full_trip.reverse()
        date2 = date
        while next_day(date2) in information["free_dates"]:
            full_trip.append(next_day(date2))
            date2 = next_day(date2)
        return full_trip

    if upcoming is None:
        error = True
        msg = "Bandsintown don't have information about this artist"
    elif len(upcoming) == 0:
        error = True
        msg = "This artist don't have future events on Bandsintown"
    else:
        for event in upcoming:
            date = "/".join(event["datetime"].split("T")[0].split("-")[::-1])
            time = event["datetime"].split("T")[1][0:4]
            event["datetime"] = (date, time)
            if date in information["free_dates"]:
                if event["venue"]["country"] == information["country"]:
                    ok_date_same_country_upcoming.append(event)
                else:
                    event["full_trip"] = search_nearest_free_dates(date)
                    if event["full_trip"] is False:
                        continue
                    suitable_upcoming.append(event)
            elif event["venue"]["country"] == information["country"]:
                wrong_date_same_country_upcoming.append(event)

    def search_total_price(dates, main_date, location):
        flight = ask_for_flights(
            (information["city"], information["country"]),
            (location[0], location[1]), dates[0], main_date[0],
            dates[dates.index(main_date[0]) + 1], dates[-1], 3,
            information["adults"], str(int(main_date[1][0:2]) - 2) + ":00",
            "price")
        try:
            flight = flight["data"][0]
        except:
            return 100000
        price_of_flight = flight["price"]
        route = flight["route"]
        dTime = flight["dTime"]
        aTime = flight["aTime"]
        for path in route:
            if path["flyTo"] == flight["flyTo"]:
                aTime = path["aTime"]
            if path["flyFrom"] == flight["flyFrom"]:
                dTime = path["dTime"]
        dTime = datetime.datetime.utcfromtimestamp(int(dTime))
        aTime = datetime.datetime.utcfromtimestamp(int(aTime))
        dyear = str(dTime.year)
        dmonth = str(dTime.month)
        if len(dmonth) == 1:
            dmonth = "0" + dmonth
        dday = str(dTime.day)
        if len(dday) == 1:
            dday = "0" + dday
        detime = str(dTime.time().hour) + "00"
        dTime = "{}/{}/{}".format(dday, dmonth, dyear)
        ayear = str(aTime.year)
        amonth = str(aTime.month)
        if len(amonth) == 1:
            amonth = "0" + amonth
        aday = str(aTime.day)
        if len(aday) == 1:
            aday = "0" + aday
        aetime = str(aTime.time().hour) + "00"
        aTime = "{}/{}/{}".format(aday, amonth, ayear)
        price_of_accomodation = ask_for_place(location[2], location[3], aTime,
                                              dTime, "1")
        total_price = price_of_flight + price_of_accomodation
        return total_price

    min_price = 10000000
    best_event = suitable_upcoming[0]
    for event in suitable_upcoming:
        event["total_price"] = search_total_price(event["full_trip"],
                                                  event["datetime"], (
                                                      event["venue"]["city"],
                                                      event["venue"][
                                                          "country"],
                                                      event["venue"][
                                                          "latitude"],
                                                      event["venue"][
                                                          "longitude"]))
        if event["total_price"] < min_price:
            min_price = event["total_price"]
            best_event = event
    return best_event
