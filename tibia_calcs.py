import math
import json

#different functions for the correct Formulae for Offensive, Balanced, and Defensive Stances
def offensive_mode(base_damage, weapon_damage, weapon_skill):
	offensive = base_damage + math.floor(math.floor(1.2*weapon_damage)*((weapon_skill+4)/28))
	return offensive

def balanced_mode(base_damage, weapon_damage, weapon_skill):
	balanced = base_damage + math.floor(weapon_damage * ((weapon_skill + 4) / 28))
	return balanced

def defensive_mode(base_damage, weapon_damage, weapon_skill):
	defensive = base_damage + math.floor(math.ceil(0.6 * weapon_damage) * (weapon_skill + 4) / 28)
	return defensive

def expected_magic_values(level, base_damage, weapon_damage_min, weapon_damage_max, magic_level, spell_name):
	with open("instantspells.json", "r") as f:
		spell_data = json.load(f)[spell_name]

	spell_x = float(spell_data["Max damage"]["x"]) - float(spell_data["Min damage"]["x"])
	spell_y = float(spell_data["Max damage"]["y"]) - float(spell_data["Min damage"]["y"])

	x = float(spell_data["Min damage"]["x"]) + spell_x * int(magic_level)
	y = float(spell_data["Min damage"]["y"]) + spell_y * int(magic_level)

	magic = math.floor((level * 0.2) + x + y)

	return magic

def expected_healing_values(level, base_damage, magic_level, spell_name):
	with open("healingspells.json", "r") as f:
		spell_data = json.load(f)[spell_name]

	spell_x = float(spell_data["Max healing"]["x"]) - float(spell_data["Min healing"]["x"])
	spell_y = float(spell_data["Max healing"]["y"]) - float(spell_data["Min healing"]["y"])

	x = int(float(spell_data["Min healing"]["x"]) + spell_x * int(magic_level))
	y = int(float(spell_data["Min healing"]["y"]) + spell_y * int(magic_level))

	healing = math.floor((level * 0.2) + x + y)

	return healing

def magic_level_training_time(vocationfactor, vocation_constant, magic_level, percent_to_next):
	trainingtime = vocationfactor * (vocation_constant ** magic_level) * percent_to_next
	return trainingtime

#calculating "s" for the base damage formula
def calculate_s(level):
#	Till level 500: no change, damage and healing +1 every 5 levels
#	As of level 501-1100: damage and healing +1 every 6 levels
#	As of level 1101-1800: damage and healing +1 every 7 levels
#	As of level 1801-2600: damage and healing +1 every 8 levels
#	As of level 2601-3500: damage and healing +1 every 9 levels
#	Above level 3500 it continues with the same logic (steps of 500, 600, 700, etc.)
#the if statements are used to calculate the correct "s" value for the base damage formula from the above info
    if level <= 500:
        return 5
    elif level <= 1100:
        return 6
    elif level <= 1800:
        return 7
    elif level <= 2600:
        return 8
    elif level <= 3500:
        return 9
    else:
        return math.floor((math.sqrt(2 * level + 2025) + 5 / 10))

#calculating "b" for the base damage formula
def calculate_b(level, s):
    return math.floor((level + 1000) / s - (50 * s)) + (100 * s) - 450

#main menu
def main_menu():
	print("#" * 40)
	print("#" + " " * 38 + "#")
	print("#" + " " * 9 + "Mark's Tibia Calculators" + " " * 5 + "#")
	print("#" + " " * 38 + "#")
	print("#" * 40)
	print("#" + " " * 38 + "#")
	print("#" + " " * 3 + "1. Base Damage & Healing" + " " * 11 + "#")
	print("#" + " " * 3 + "2. Melee Expected Damage" + " " * 11 + "#")
	print("#" + " " * 3 + "3. Magic Expected Damage" + " " * 11 + "#")
	print("#" + " " * 3 + "4. Magic Training Time" + " " * 13 + "#")
	print("#" + " " * 38 + "#")
	print("#" * 40)

	while True:
		choice = input("Enter your choice: ")
		if choice == "1":
			base_damage_menu()
			break
		elif choice == "2":
			expected_melee_damage_menu()
			break
		elif choice == "3":
			expected_magic_menu()
			break
		elif choice == "4":
			magic_level_training_menu()
			break
		else:
			print("Invalid choice, try again")
#base damage menu
def base_damage_menu():
	print("#" * 40)
	print("#" + " " * 38 + "#")
	print("#" + " " * 3 + "Tibia Base Damage & Healing Calc" + " " * 3 + "#")
	print("#" + " " * 38 + "#")
	print("#" * 40)
	level = int(input("Enter player level: "))
	s = calculate_s(level)
	b = calculate_b(level, s)
	base_damage = b + (s - 1) * math.ceil(b / 2)
	print(f"\nPlayer Level: {level}")
	print(f"Base Damage & Healing: {base_damage}")

#expected damage menu
def expected_melee_damage_menu():
	print ("#" * 40)
	print ("#" + " " * 38 + "#")
	print ("#" + " " * 5 + "Tibia Expected Melee Damage" + " " * 6 + "#")
	print ("#" + " " * 11 + "Weapon Stances:" + " " * 12 + "#")
	print ("#" + " " * 4 + "Offensive, Balanced, Defensive" + " " * 4 + "#")
	print("#" + " " * 38 + "#")
	print ("#" * 40)
	level = int(input("Enter player level: "))
	s = calculate_s(level)
	b = calculate_b(level, s)
	base_damage = b + (s - 1) * math.ceil(b / 2)
	print(f"\nPlayer Level: {level}")
	print(f"Base Damage & Healing: {base_damage}")
	weapon_damage = int(input("Enter weapon damage: "))
	weapon_skill = int(input("Enter weapon skill level: "))
	offensive_mode(base_damage, weapon_damage, weapon_skill)
	print(f"\nExpected Damage using Offensive:", offensive_mode(base_damage, weapon_damage, weapon_skill))
	balanced_mode(base_damage, weapon_damage, weapon_skill)
	print(f"\nExpected Damage using Balanced:", balanced_mode(base_damage, weapon_damage, weapon_skill))
	defensive_mode(base_damage, weapon_damage, weapon_skill)
	print(f"\nExpected Damage using Defensive:", defensive_mode(base_damage, weapon_damage, weapon_skill))

#expected magic damage menu
def expected_magic_menu():
	print ("#" * 40)
	print ("#" + " " * 38 + "#")
	print ("#" + " " * 5 + "Tibia Expected Magic Damage" + " " * 6 + "#")
	print ("#" + " " * 38 + "#")
	print ("#" * 40)
	#healing or damage
	heal = int(input("Enter 1 for healing, 2 for damage: "))
	if heal == 1:
		level = int(input("Enter player level: "))
		s = calculate_s(level)
		b = calculate_b(level, s)
		base_damage = b + (s - 1) * math.ceil(b / 2)
		print(f"Base Damage: {base_damage}")
		magic_level = str(input("Enter magic level: "))
		spell_name = input("Enter spell name: ")
		print(f"\nExpected Healing using {spell_name}:", expected_healing_values(level, base_damage, magic_level, spell_name))
	else:
		level = int(input("Enter player level: "))
		s = calculate_s(level)
		b = calculate_b(level, s)
		base_damage = b + (s - 1) * math.ceil(b / 2)
		print(f"Base Damage: {base_damage}")
		weapon_damage_min = int(input("Enter minimum weapon damage: "))
		weapon_damage_max = int(input("Enter maximum weapon damage: "))
		magic_level = str(input("Enter magic level: "))
		spell_name = input("Enter spell name: ")
		print(f"Using {spell_name}, expected damage is ", expected_magic_values(level, base_damage, weapon_damage_min, weapon_damage_max, magic_level, spell_name))

def magic_level_training_menu():
	print ("#" * 40)
	print ("#" + " " * 38 + "#")
	print ("#" + " " * 5 + "Tibia Magic Level Training" + " " * 7 + "#")
	print ("#" + " " * 38 + "#")
	print ("#" * 40)

	while True:
		vocation = input("Enter vocation (Sorcerer, Master Sorcerer, Knight, Elite Knight, Paladin, Royal Paladin, Druid, Elder Druid): ")
		if vocation in ["Sorcerer", "Master Sorcerer", "Knight", "Elite Knight", "Paladin", "Royal Paladin", "Druid", "Elder Druid"]:
			break
		else:
			print("Invalid vocation. Please enter a valid vocation")
	#y = a * b(x) * z 
	#y is time needed to train magic level
	#b is vocation constant
	#x is current magic level
	#z percent to next magic level
	#a is vocation factor
	if vocation == "Sorcerer" or "Druid" or "Royal Paladin":
		vocation_factor = 0.67
		vocation_constant = 1.1
	elif vocation == "Master Sorcerer" or "Elder Druid":
		vocation_factor = 0.44
		vocation_constant = 1.1
	elif vocation == "Knight" or "Elite Knight":
		vocation_factor = 1.33
		vocation_constant = 3.0
	elif vocation == "Paladin":
		vocation_factor = 0.88
		vocation_constant = 1.4
	magic_level = int(input("Enter current magic level: "))
	percent_to_next = float(input("Enter percent to next magic level in decimal form: "))
	training_time_hours = magic_level_training_time(vocation_factor, vocation_constant, magic_level, percent_to_next)
	training_time_hours, training_time_minutes = divmod(training_time_hours * 60, 60)
	print(f"\nTime needed to train to next magic level: {int(training_time_hours)} hours, {int(training_time_minutes)} minutes")



#main function call
if __name__ == "__main__":
	main_menu()