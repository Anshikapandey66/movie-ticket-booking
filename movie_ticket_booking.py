import csv
import os
import random

FILE = "bookings.csv"

movies = {
    1: ("Pushpa 2", 200),
    2: ("Stree 2", 180),
    3: ("Jawan", 220),
    4: ("Avengers: Endgame", 250)
}

shows = {
    1: "10:00 AM",
    2: "01:00 PM",
    3: "04:00 PM",
    4: "07:00 PM"
}

seats = [
    "A1", "A2", "A3", "A4",
    "B1", "B2", "B3", "B4",
    "C1", "C2", "C3", "C4"
]


def generate_booking_id():
    return "BK" + str(random.randint(1000, 9999))


def show_movies():
    print("\n===== AVAILABLE MOVIES =====")

    for number, (movie, price) in movies.items():
        print(f"{number}. {movie} - ₹{price}")


def get_booked_seats(movie, show):
    booked = []

    if not os.path.exists(FILE):
        return booked

    with open(FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if (row["Movie"] == movie and
                    row["Show"] == show and
                    row["Status"] == "Booked"):
                booked.append(row["Seat"])

    return booked


def book_ticket():

    show_movies()

    try:
        movie_choice = int(input("\nSelect movie: "))

        if movie_choice not in movies:
            print("❌ Invalid movie.")
            return

        movie, price = movies[movie_choice]

        print("\n===== SHOW TIMINGS =====")

        for number, time in shows.items():
            print(f"{number}. {time}")

        show_choice = int(input("Select show: "))

        if show_choice not in shows:
            print("❌ Invalid show.")
            return

        show = shows[show_choice]

        booked_seats = get_booked_seats(movie, show)

        available_seats = [
            seat for seat in seats
            if seat not in booked_seats
        ]

        print("\n===== AVAILABLE SEATS =====")
        print(" ".join(available_seats))

        seat = input("Select seat: ").upper()

        if seat not in seats:
            print("❌ Invalid seat.")
            return

        if seat in booked_seats:
            print("❌ Seat already booked.")
            return

        name = input("Enter customer name: ")

        gst = price * 0.18
        total = price + gst

        booking_id = generate_booking_id()

        file_exists = os.path.exists(FILE)

        with open(FILE, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "Booking ID",
                    "Customer",
                    "Movie",
                    "Show",
                    "Seat",
                    "Price",
                    "GST",
                    "Total",
                    "Status"
                ])

            writer.writerow([
                booking_id,
                name,
                movie,
                show,
                seat,
                price,
                round(gst, 2),
                round(total, 2),
                "Booked"
            ])

        print("\n🎉 BOOKING CONFIRMED!")
        print("----------------------------")
        print(f"Booking ID : {booking_id}")
        print(f"Customer   : {name}")
        print(f"Movie      : {movie}")
        print(f"Show       : {show}")
        print(f"Seat       : {seat}")
        print(f"Ticket     : ₹{price}")
        print(f"GST (18%)  : ₹{gst:.2f}")
        print(f"Total      : ₹{total:.2f}")
        print("----------------------------")

    except ValueError:
        print("❌ Please enter a valid number.")


def search_booking():

    booking_id = input("\nEnter Booking ID: ").upper()

    if not os.path.exists(FILE):
        print("❌ No bookings found.")
        return

    with open(FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Booking ID"] == booking_id:

                print("\n===== BOOKING DETAILS =====")
                print(f"Booking ID : {row['Booking ID']}")
                print(f"Customer   : {row['Customer']}")
                print(f"Movie      : {row['Movie']}")
                print(f"Show       : {row['Show']}")
                print(f"Seat       : {row['Seat']}")
                print(f"Total      : ₹{row['Total']}")
                print(f"Status     : {row['Status']}")
                return

    print("❌ Booking not found.")


def cancel_ticket():

    booking_id = input("\nEnter Booking ID: ").upper()

    if not os.path.exists(FILE):
        print("❌ No bookings found.")
        return

    rows = []

    found = False

    with open(FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Booking ID"] == booking_id:

                if row["Status"] == "Cancelled":
                    print("❌ Ticket already cancelled.")
                    return

                row["Status"] = "Cancelled"
                found = True

            rows.append(row)

    if found:

        with open(FILE, "w", newline="") as file:

            fieldnames = [
                "Booking ID",
                "Customer",
                "Movie",
                "Show",
                "Seat",
                "Price",
                "GST",
                "Total",
                "Status"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(rows)

        print("✅ Ticket cancelled successfully.")

    else:
        print("❌ Booking ID not found.")


def booking_summary():

    if not os.path.exists(FILE):
        print("\nNo bookings available.")
        return

    total_bookings = 0
    revenue = 0

    with open(FILE, "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Status"] == "Booked":

                total_bookings += 1
                revenue += float(row["Total"])

    print("\n===== BOOKING SUMMARY =====")
    print(f"Total Active Bookings : {total_bookings}")
    print(f"Total Revenue         : ₹{revenue:.2f}")


def main():

    while True:

        print("\n================================")
        print("   🎬 MOVIE TICKET BOOKING")
        print("================================")

        print("1. View Movies")
        print("2. Book Ticket")
        print("3. Search Booking")
        print("4. Cancel Ticket")
        print("5. Booking Summary")
        print("6. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            show_movies()

        elif choice == "2":
            book_ticket()

        elif choice == "3":
            search_booking()

        elif choice == "4":
            cancel_ticket()

        elif choice == "5":
            booking_summary()

        elif choice == "6":
            print("\n🎬 Thank you for using Movie Booking System!")
            break

        else:
            print("❌ Invalid choice.")


main()
