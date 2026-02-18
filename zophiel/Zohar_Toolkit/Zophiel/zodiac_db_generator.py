import json
from lunarcalendar import Converter, Solar, Lunar
import datetime

def get_chinese_zodiac(year):
    # Zodiac Animals
    animals = ['Rat', 'Ox', 'Tiger', 'Rabbit', 'Dragon', 'Snake', 'Horse', 'Goat', 'Monkey', 'Rooster', 'Dog', 'Pig']
    # Heavenly Stems (Elements)
    elements = ['Metal', 'Metal', 'Water', 'Water', 'Wood', 'Wood', 'Fire', 'Fire', 'Earth', 'Earth']
    
    # Calculate Animal (Base 1900 was Rat)
    # 1900 % 12 = 4. Rat is index 0. So (year - 1900) % 12 should work.
    animal_index = (year - 1900) % 12
    animal = animals[animal_index]
    
    # Calculate Element (Base 1900 was Metal)
    # 1900 % 10 = 0. Metal is index 0.
    element_index = (year - 1900) % 10
    element = elements[element_index]
    
    return animal, element

def generate_zodiac_db():
    database = []
    
    for year in range(1900, 2045):
        # Find Lunar New Year (1st Month, 1st Day)
        # Note: lunarcalendar library might need specific handling to find the solar date of the lunar new year
        # The Converter converts Solar to Lunar and vice versa.
        # We need the Solar date of Lunar(year, 1, 1)
        
        try:
            # Create a Lunar object for the 1st day of the 1st month of the given lunar year?
            # No, Converter.Lunar2Solar takes (lunar_year, lunar_month, lunar_day)
            # But wait, does the library use 1900 as base?
            
            solar_date = Converter.Lunar2Solar(Lunar(year, 1, 1))
            date_str = f"{solar_date.year}-{solar_date.month:02d}-{solar_date.day:02d}"
            
            animal, element = get_chinese_zodiac(year)
            
            entry = {
                "year": year,
                "lunar_new_year_date": date_str,
                "animal": animal,
                "element": element,
                "full_sign": f"{element} {animal}"
            }
            database.append(entry)
            
        except Exception as e:
            print(f"Error for year {year}: {e}")
            continue

    with open('c:/Users/kille/Documents/trae_projects/osint_links/Intelligence_Reports/CHINESE_ZODIAC_DB_1900_2044.json', 'w') as f:
        json.dump(database, f, indent=4)
    
    print("Database generated successfully.")

if __name__ == "__main__":
    generate_zodiac_db()
