# TASK 04: FLIGHT BOOKING CONSOLE APPLICATION — OOP

from abc import ABC, abstractmethod


class Flight:
    """Stores flight details and controls seat availability."""

    def __init__(self, code, airline, source, destination, available_seats, base_fare):
        self.__code = code
        self.__airline = airline
        self.__source = source
        self.__destination = destination
        self.__available_seats = available_seats
        self.__base_fare = base_fare

    @property
    def code(self):
        return self.__code

    @property
    def airline(self):
        return self.__airline

    @property
    def source(self):
        return self.__source

    @property
    def destination(self):
        return self.__destination

    @property
    def available_seats(self):
        return self.__available_seats

    @property
    def base_fare(self):
        return self.__base_fare

    def has_seats(self, ticket_count):
        return 0 < ticket_count <= self.__available_seats

    def reserve_seats(self, ticket_count):
        """Change seats only after the system has validated a booking."""
        if not self.has_seats(ticket_count):
            return False
        self.__available_seats -= ticket_count
        return True

    def display(self):
        print(
            f"{self.code:<8} | {self.airline:<18} | "
            f"{self.source} to {self.destination} | "
            f"Seats: {self.available_seats} | Fare: Rs. {self.base_fare:.2f}"
        )


class Passenger(ABC):
    """Abstract base class for passenger categories."""

    def __init__(self, name, age):
        self._name = name.strip()
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @abstractmethod
    def get_discount_percentage(self):
        """Return this passenger category's discount percentage."""
        pass

    @property
    @abstractmethod
    def passenger_type(self):
        pass


class RegularPassenger(Passenger):
    def get_discount_percentage(self):
        return 0.0

    @property
    def passenger_type(self):
        return "Regular"


class StudentPassenger(Passenger):
    def get_discount_percentage(self):
        return 10.0

    @property
    def passenger_type(self):
        return "Student"


class Booking:
    """Stores the details and fare breakdown of one confirmed booking."""

    def __init__(self, booking_id, flight, passenger, ticket_count):
        self.booking_id = booking_id
        self.flight = flight
        self.passenger = passenger
        self.ticket_count = ticket_count

        self.subtotal = flight.base_fare * ticket_count
        self.discount_percentage = passenger.get_discount_percentage()
        self.discount_amount = self.subtotal * self.discount_percentage / 100
        self.total_fare = self.subtotal - self.discount_amount

    def display_summary(self):
        print("\n========== BOOKING SUMMARY ==========")
        print(f"Booking ID          : {self.booking_id}")
        print(f"Passenger           : {self.passenger.name}")
        print(f"Age                 : {self.passenger.age}")
        print(f"Passenger type      : {self.passenger.passenger_type}")
        print(f"Flight code         : {self.flight.code}")
        print(f"Airline             : {self.flight.airline}")
        print(f"Route               : {self.flight.source} to {self.flight.destination}")
        print(f"Tickets             : {self.ticket_count}")
        print(f"Base fare per ticket: Rs. {self.flight.base_fare:.2f}")
        print(f"Subtotal            : Rs. {self.subtotal:.2f}")
        print(
            f"Discount ({self.discount_percentage:.0f}%)      : "
            f"Rs. {self.discount_amount:.2f}"
        )
        print(f"Final amount        : Rs. {self.total_fare:.2f}")
        print("=====================================")


class FlightBookingSystem:
    """Manages flights, bookings, input validation, and the menu."""

    def __init__(self):
        self.flights = [
            Flight("PN101", "Kiran Air", "Pune", "Delhi", 20, 4000),
            Flight("MB202", "Sky Connect", "Mumbai", "Bengaluru", 25, 3500),
            Flight("PN303", "Kiran Air", "Pune", "Hyderabad", 18, 3000),
        ]
        self.bookings = []
        self.next_booking_number = 1001

    def display_flights(self):
        print("\n================ AVAILABLE FLIGHTS ================")
        print("Code     | Airline            | Route                 | Seats | Base Fare")
        print("-" * 75)
        for flight in self.flights:
            flight.display()
        print("=" * 75)

    def find_flight_by_code(self, flight_code):
        for flight in self.flights:
            if flight.code.lower() == flight_code.strip().lower():
                return flight
        return None

    def validate_booking_details(self, flight, name, age, ticket_count):
        if flight is None:
            return "Invalid flight code."
        if not name.strip():
            return "Passenger name cannot be blank."
        if age <= 0:
            return "Age must be greater than 0."
        if ticket_count <= 0:
            return "Number of tickets must be greater than 0."
        if not flight.has_seats(ticket_count):
            return f"Not enough seats. Available seats: {flight.available_seats}."
        return None

    @staticmethod
    def read_positive_integer(prompt):
        while True:
            try:
                value = int(input(prompt).strip())
                if value > 0:
                    return value
                print("Please enter a number greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a whole number.")

    def book_flight(self):
        self.display_flights()
        flight_code = input("Enter flight code: ").strip()
        flight = self.find_flight_by_code(flight_code)

        name = input("Enter passenger name: ").strip()
        age = self.read_positive_integer("Enter passenger age: ")

        while True:
            passenger_type = input("Passenger type (Regular/Student): ").strip().lower()
            if passenger_type in ("regular", "student"):
                break
            print("Invalid passenger type. Enter Regular or Student.")

        ticket_count = self.read_positive_integer("Enter number of tickets: ")

        error = self.validate_booking_details(flight, name, age, ticket_count)
        if error:
            print(f"Booking failed: {error}")
            print("No booking was created and seat counts remain unchanged.")
            return

        if passenger_type == "student":
            passenger = StudentPassenger(name, age)
        else:
            passenger = RegularPassenger(name, age)

        # Reserve seats only after all validation has succeeded.
        if not flight.reserve_seats(ticket_count):
            print("Booking failed: seats are no longer available.")
            return

        booking = Booking(
            f"BK{self.next_booking_number}", flight, passenger, ticket_count
        )
        self.next_booking_number += 1
        self.bookings.append(booking)

        print("\nBooking confirmed!")
        booking.display_summary()

    def view_latest_booking(self):
        if not self.bookings:
            print("\nNo confirmed booking exists yet. Please book a flight first.")
            return
        self.bookings[-1].display_summary()

    def run(self):
        print("Welcome to Kiran Air Booking")
        while True:
            print("\n1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.display_flights()
            elif choice == "2":
                self.book_flight()
            elif choice == "3":
                self.view_latest_booking()
            elif choice == "4":
                print("Thank you for using Kiran Air Booking!")
                break
            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        system = FlightBookingSystem()
        system.run()
    except (EOFError, KeyboardInterrupt):
        print("\nApplication closed. Goodbye!")
