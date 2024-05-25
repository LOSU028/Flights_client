#!/usr/bin/env python3
import argparse
import logging
import os
import requests
import json
import re


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('books.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL", "http://localhost:8000")

def print_flight(flight):
    for k in flight.keys():
        print(f"{k}: {flight[k]}")
    print("="*50)

def list_flights(age,limit=10):
    suffix = "/flight"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "age": age,
        "limit":limit
    }

    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for flight in json_resp:
            print_flight(flight)
    else:
        print(f"Error: {response}")

def list_busiest_airports(num_airports):
    endpoint = FLIGHTS_API_URL + "/flight/busiest_airports"
    params = {
        "num_airports": num_airports
    }

    response = requests.get(endpoint, params=params)
    if response.ok:
        busiest_airports = response.json()
        for airport in busiest_airports:
            print(f"{airport['_id']} - {airport['total_passengers']} passengers")
    else:
        print(f"Error: {response}")

def list_busiest_airport_months(airport_code, num_months):
    endpoint = FLIGHTS_API_URL + "/flight/busiest_airports/months"
    params = {
        "airport_code": airport_code,
        "num_months" : num_months
    }

    response = requests.get(endpoint, params=params)
    if response.ok:
        busiest_months = response.json()
        print(f"Busiest months for airport {airport_code}:")
        for month in busiest_months:
            month_value = month['_id']
            print(f"Month: {month_value}, Passengers: {month['count']}")
    else:
        print(f"Error: {response}")

def list_busiest_months_airline(airport_code, airline_name):
    endpoint = FLIGHTS_API_URL + "/flight/most_active_months"
    params = {
        "airport_code": airport_code,
        "airline_name" : airline_name
    }

    response = requests.get(endpoint, params=params)
    if response.ok:
        busiest_months = response.json()
        if busiest_months:
            print(f"Traffic by months for airline {airline_name} at airport {airport_code}:")
            for month in busiest_months:
                month_value = month['_id']
                print(f"Month: {month_value}, Flights: {month['count']}")
        else:
            print(f"No data available for airline {airline_name} at airport {airport_code}")
    else:
        print(f"Error: {response}")

def list_busiest_vacation_months(airport_code):
    endpoint = FLIGHTS_API_URL + "/flight/vacation_months"
    params = {
        "airport_code": airport_code
    }

    response = requests.get(endpoint, params=params)
    if response.ok:
        busiest_months = response.json()
        if busiest_months:
            print(f"Busiest vacation/pleasure months for airport {airport_code}:")
            for month in busiest_months:
                month_value = month['_id']
                print(f"Month: {month_value}, Flights: {month['count']}")
        else:
            print(f"No data available for airport {airport_code}")
    else:
        print(f"Error: {response}")

def main():
    log.info(f"Welcome to books catalog. App requests to: {FLIGHTS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search", "bussiest", "months", "airlines", "vacation"]
    parser.add_argument("action", choices=list_of_actions,help="Action to be user for the books library")
    parser.add_argument("--limit", type=int, help="Limit the number of flights returned", default=10)
    parser.add_argument("--airport_code", type=str, default=None)
    parser.add_argument("--airline_name", type=str, default=None)
    args = parser.parse_args()

    if args.action == "search":
        list_flights(args.limit)

    if args.action == "bussiest":
        args.limit = input("Please specify the number of airports to list: ")
        list_busiest_airports(args.limit)

    if args.action == "months":
        args.airport_code = input("Please specify the airport to use: ")
        args.limit = input("Please specify the number of months to list: ")
        list_busiest_airport_months(args.airport_code,args.limit)

    if args.action == "airlines":
        args.airport_code = input("Please specify the airport to use: ")
        args.airline_name = input("Please specify the airline to search: ")
        list_busiest_months_airline(args.airport_code,args.airline_name)
    
    if args.action == "vacation":
        args.airport_code = input("Please specify the airport to use: ")
        list_busiest_vacation_months(args.airport_code)

if __name__ == "__main__":
    main()