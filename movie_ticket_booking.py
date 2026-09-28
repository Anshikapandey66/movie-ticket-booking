import csv
import os

MOVIES = {
    1: ("Avengers: Endgame", 250),
    2: ("Pushpa 2", 200),
    3: ("Stree 2", 180),
    4: ("Jawan", 220)
}

BOOKING_FILE = "bookings.csv"


def show_movies():
    print("\n===== AVAILABLE MOVIES =====")

    for number, (movie, price) in MOVIES.items():
        print(f"{number}. {movie} - ₹{price}")


def book_ticket():
    show_movies()

    try:
        choice = int(input("\nSelect movie: "))

        if choice not in MOVIES:
            print("❌ Invalid movie selection.")
            return

        movie, price = MOVIES[choice]
        name = input("Enter your name: ")
        seats = int(input("Number of tickets: "))

        if seats <= 0:
            print("❌ Invalid number of tickets.")
            return

        total = price * seats

        file_exists = os.path.exists(BOOKING_FILE)

        with open(BOOKING_FILE, "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(
                    ["Customer", "Movie", "Tickets", "Total"]
                )

            writer.writerow(
                [name, movie, seats, total]
            )

        print("\n✅ Booking Successful!")
        print(f"Movie: {movie}")
        print(f"Tickets: {seats}")
        print(f"Total Amount: ₹{total}")

    except ValueError:
        print("❌ Please enter a valid number.")


def view_bookings():
    if not os.path.exists(BOOKING_FILE):
        print("\nNo bookings found.")
        return

    print("\n===== BOOKINGS =====")

    with open(BOOKING_FILE, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            print(" | ".join(row))


def main():
    while True:
        print("\n===== MOVIE TICKET BOOKING SYSTEM =====")
        print("1. Show Movies")
        print("2. Book Ticket")
        print("3. View Bookings")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_movies()

        elif choice == "2":
            book_ticket()

        elif choice == "3":
            view_bookings()

        elif choice == "4":
            print("🎬 Thank you for using the system!")
            break

        else:
            print("❌ Invalid choice.")


main()
