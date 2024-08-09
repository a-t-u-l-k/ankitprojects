from datetime import datetime, timedelta
import random
from colorama import Fore, Style, init
from dateutil.relativedelta import relativedelta

# Initialize colorama
init()

# Define the Tithis and their descriptions for Shukla and Krishna Paksha
TITHIS = {
    "Prathama": "First lunar day; good for new beginnings.",
    "Dwitiya": "Second day; good for foundation ceremonies.",
    "Tritiya": "Third day; favorable for cutting hair and nails.",
    "Chaturthi": "Fourth day; good for removing obstacles.",
    "Panchami": "Fifth day; favorable for medicine and surgery.",
    "Shashthi": "Sixth day; good for celebrations and festivals.",
    "Saptami": "Seventh day; favorable for journeys and purchases.",
    "Ashtami": "Eighth day; good for defense and fortification.",
    "Navami": "Ninth day; suitable for destruction of enemies.",
    "Dasami": "Tenth day; favorable for virtuous activities.",
    "Ekadasi": "Eleventh day; ideal for fasting and spiritual practices.",
    "Dvadasi": "Twelfth day; good for religious ceremonies.",
    "Trayodasi": "Thirteenth day; suitable for friendships and festivities.",
    "Chaturdashi": "Fourteenth day; good for rituals involving spirits.",
    "Amavasya": "New Moon day; good for ancestral rituals.",
    "Purnima": "Full Moon day; good for celebrations and sacrifices.",
}

# Define the sequence for Shukla Paksha and Krishna Paksha
TITHIS_SHUKLA_PAKSHA = [
    "Prathama", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", 
    "Ashtami", "Navami", "Dasami", "Ekadasi", "Dvadasi", "Trayodasi", "Chaturdashi", "Purnima"
]

TITHIS_KRISHNA_PAKSHA = [
    "Prathama", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", 
    "Ashtami", "Navami", "Dasami", "Ekadasi", "Dvadasi", "Trayodasi", "Chaturdashi", "Amavasya"
]

FESTIVALS = {
    "January 1": "New Year's Day (International)",
    "January 26": "Republic Day (India)",
    "February 14": "Valentine's Day (International)",
    "March 8": "International Women's Day",
    "April 14": "Ambedkar Jayanti (India)",
    "May 1": "International Workers' Day",
    "June 21": "International Yoga Day",
    "August 15": "Independence Day (India)",
    "October 2": "Gandhi Jayanti (India)",
    "December 25": "Christmas Day (International)",
    "Diwali": "Festival of Lights (India, dates vary)",
    "Holi": "Festival of Colors (India, dates vary)",
    "Navratri": "Nine Nights Festival (India, dates vary)",
    "Eid-ul-Fitr": "End of Ramadan (International, dates vary)",
    "Eid-ul-Adha": "Festival of Sacrifice (International, dates vary)",
    "Thanksgiving": "Thanksgiving Day (International, USA)",
    "Halloween": "Halloween (International)",
    "Lunar New Year": "Chinese New Year (International, dates vary)",
    "Good Friday": "Christian holiday (International, dates vary)",
    "Hanukkah": "Jewish Festival of Lights (International, dates vary)",
    "Pongal": "Harvest Festival (India, dates vary)",
    "Onam": "Harvest Festival (India, dates vary)",
    "Baisakhi": "Harvest Festival (India, dates vary)",
    "Guru Nanak Jayanti": "Guru Nanak's Birthday (India, dates vary)",
    "Raksha Bandhan": "Festival celebrating sibling bonds (India, dates vary)",
}

def get_random_color():
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.LIGHTBLACK_EX]
    return random.choice(colors)

def print_error_message(message):
    print(Fore.RED + Style.BRIGHT + "ERROR: " + message + Style.RESET_ALL)

def print_info_message(message):
    print(Fore.CYAN + Style.BRIGHT + "INFO: " + message + Style.RESET_ALL)

def calculate_paksha_and_tithi(date):
    """ Calculate Tithi and Paksha based on the given date. """
    base_date = datetime(2024, 1, 1)  # Adjust the base date as per your reference
    delta_days = (date - base_date).days
    
    # Example calculation adjustments for Paksha and Tithis
    paksha_index = (delta_days // 15) % 2  # 0 for Shukla Paksha, 1 for Krishna Paksha
    day_in_paksha = delta_days % 15
    
    if paksha_index == 0:  # Shukla Paksha
        paksha = "Shukla Paksha"
        tithi = TITHIS_SHUKLA_PAKSHA[day_in_paksha]
    else:  # Krishna Paksha
        paksha = "Krishna Paksha"
        tithi = TITHIS_KRISHNA_PAKSHA[day_in_paksha]
    
    tithi_description = TITHIS.get(tithi, "No Description Available")
    return paksha, tithi, tithi_description

def print_single_day(date):
    paksha, tithi, description = calculate_paksha_and_tithi(date)
    color = get_random_color()
    print(color + f"Date: {date.strftime('%d-%m-%Y')}, Paksha: {paksha}, Tithi: {tithi}")
    print("Description:", description[:100] + "..." if len(description) > 100 else description + Style.RESET_ALL)

def view_tithis():
    while True:
        date_input = input("Enter the date (ddmmyyyy): ")
        try:
            date = datetime.strptime(date_input, "%d%m%Y")
            print_single_day(date)
            
            # Options to continue or go back
            print(Fore.YELLOW + "1. View another date" + Style.RESET_ALL)
            print(Fore.YELLOW + "2. Go back to the main menu" + Style.RESET_ALL)
            
            choice = input("Enter your choice: ")
            if choice == '2':
                break
            elif choice != '1':
                print_error_message("Invalid choice. Please enter 1 or 2.")
        
        except ValueError:
            print_error_message("Invalid date format. Please use ddmmyyyy.")

def display_month_calendar():
    while True:
        year_input = input("Enter the year (yyyy): ")
        month_input = input("Enter the month (1-12): ")
        
        try:
            year = int(year_input)
            month = int(month_input)
            
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")
            
            # Calculate the first and last day of the month
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
            
            print(Fore.GREEN + f"Calendar for {first_day.strftime('%B %Y')}:" + Style.RESET_ALL)
            print("Mo Tu We Th Fr Sa Su")
            
            # Print leading spaces for the first day of the month
            first_weekday = first_day.weekday()
            for _ in range(first_weekday):
                print("   ", end="")

            current_date = first_day
            while current_date <= last_day:
                date_str = current_date.strftime("%d")
                color = get_random_color()
                print(color + f"{date_str:2} " + Style.RESET_ALL, end="")
                if current_date.weekday() == 6:  # Sunday
                    print()
                current_date += timedelta(days=1)
            
            print("\nOptions:")
            print(Fore.YELLOW + "1. Search for a different month or year" + Style.RESET_ALL)
            print(Fore.YELLOW + "2. Go back to the main menu" + Style.RESET_ALL)

            choice = input("Enter your choice: ")
            if choice == '2':
                break
            elif choice != '1':
                print_error_message("Invalid choice. Please enter 1 or 2.")
        
        except ValueError:
            print_error_message("Invalid input. Please enter a valid year and month.")

def add_days():
    base_date_input = input("Enter the base date (ddmmyyyy): ")
    try:
        base_date = datetime.strptime(base_date_input, "%d%m%Y")
        days_to_add = int(input("Enter the number of days to add: "))
        new_date = base_date + timedelta(days=days_to_add)
        print(Fore.GREEN + f"New date after adding days: {new_date.strftime('%d-%m-%Y')}" + Style.RESET_ALL)
    
    except ValueError:
        print_error_message("Invalid date format or number of days. Please use ddmmyyyy for date and integer for days.")

def subtract_days():
    base_date_input = input("Enter the base date (ddmmyyyy): ")
    try:
        base_date = datetime.strptime(base_date_input, "%d%m%Y")
        days_to_subtract = int(input("Enter the number of days to subtract: "))
        new_date = base_date - timedelta(days=days_to_subtract)
        print(Fore.GREEN + f"New date after subtracting days: {new_date.strftime('%d-%m-%Y')}" + Style.RESET_ALL)
    
    except ValueError:
        print_error_message("Invalid date format or number of days. Please use ddmmyyyy for date and integer for days.")

def calculate_age():
    date_of_birth_input = input("Enter your date of birth (ddmmyyyy): ")
    try:
        date_of_birth = datetime.strptime(date_of_birth_input, "%d%m%Y")
        now = datetime.now()
        age = relativedelta(now, date_of_birth)
        print(Fore.GREEN + f"Age: {age.years} years, {age.months} months, {age.days} days, {age.hours} hours, and {age.seconds} seconds" + Style.RESET_ALL)
    
    except ValueError:
        print_error_message("Invalid date format. Please use ddmmyyyy.")

def show_festivals():
    date_input = input("Enter the date (ddmmyyyy): ")
    try:
        date = datetime.strptime(date_input, "%d%m%Y")
        date_str = date.strftime("%B %d")
        festival = FESTIVALS.get(date_str, "No major festivals on this date.")
        print(Fore.GREEN + f"Festivals and holidays for {date_str}: {festival}" + Style.RESET_ALL)
    
    except ValueError:
        print_error_message("Invalid date format. Please use ddmmyyyy.")

def display_current_time():
    now = datetime.now()
    print(Fore.GREEN + f"Current Date: {now.strftime('%d-%m-%Y')}, Day: {now.strftime('%A')}, Time: {now.strftime('%H:%M:%S')}" + Style.RESET_ALL)

def main_menu():
    while True:
        display_current_time()
        print(Fore.MAGENTA + Style.BRIGHT + "Main Menu:" + Style.RESET_ALL)
        print(Fore.RED + "1. View Tithis and Pakshas" + Style.RESET_ALL)
        print(Fore.BLUE + "2. Display Calendar" + Style.RESET_ALL)
        print(Fore.GREEN + "3. Add Days to a Date" + Style.RESET_ALL)
        print(Fore.YELLOW + "4. Subtract Days from a Date" + Style.RESET_ALL)
        print(Fore.CYAN + "5. Calculate Age" + Style.RESET_ALL)
        print(Fore.MAGENTA + "6. Show Festivals and Special Days" + Style.RESET_ALL)
        print(Fore.RED + "7. Exit" + Style.RESET_ALL)
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_tithis()
        elif choice == '2':
            display_month_calendar()
        elif choice == '3':
            add_days()
        elif choice == '4':
            subtract_days()
        elif choice == '5':
            calculate_age()
        elif choice == '6':
            show_festivals()
        elif choice == '7':
            print(Fore.GREEN + "Exiting program. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print_error_message("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main_menu()
