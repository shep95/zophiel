from lunarcalendar import Converter, Solar, Lunar

# User's Solar Date
solar_date = Solar(2005, 9, 26)
lunar_date = Converter.Solar2Lunar(solar_date)

print(f"Solar: {solar_date}")
print(f"Lunar: {lunar_date}")
print(f"Lunar Year: {lunar_date.year}")
print(f"Lunar Month: {lunar_date.month}")
print(f"Lunar Day: {lunar_date.day}")
