import math

def offensive_mode(base_damage, weapon_damage, weapon_skill):
	global offensive
	offensive = base_damage + math.floor(math.floor(1.2*weapon_damage)*((weapon_skill+4)/28))

def balanced_mode(base_damage, weapon_damage, weapon_skill):
	global balanced
	balanced = base_damage + math.floor(weapon_damage * ((weapon_skill + 4) / 28))

def defensive_mode(base_damage, weapon_damage, weapon_skill):
	global defensive
	defensive = base_damage + math.floor(math.ceil(0.6 * weapon_damage) * (weapon_skill + 4) / 28)

def calculate_s(level):
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

def calculate_b(level, s):
    return math.floor((level + 1000) / s - (50 * s)) + (100 * s) - 450

def main_menu():
    print("#" * 40)
    print("#" + " " * 38 + "#")
    print("#" + " " * 9 + "Mark's Tibia Calculators" + " " * 5 + "#")
    print("#" + " " * 38 + "#")
    print("#" * 40)
    print("#" + " " * 3 + "1. Base Damage & Healing" + " " * 11 + "#")
    print("#" + " " * 3 + "2. Max Damage & Healing" + " " * 12 + "#")
    print("#" + " " * 3 + "3. Mana Training Time" + " " * 14 + "#")
    print("#" + " " * 3 + "4. Magic Power" + " " * 21 + "#")
    print("#" + " " * 3 + "5. Speed" + " " * 27 + "#")
    print("#" * 40)
    choice = input("Enter your choice: ")
    if choice == "1":
        base_damage_menu()
    if choice == "2":
    	expected_damage_menu()

def base_damage_menu():
	print("#" * 40)
	print("#" + " " * 38 + "#")
	print("#" + " " * 5 + "Tibia Base Damage & Healing Calc" + " " * 4 + "#")
	print("#" + " " * 38 + "#")
	print("#" * 40)
	level = int(input("Enter player level: "))
	s = calculate_s(level)
	b = calculate_b(level, s)
	base_damage = b + (s - 1) * math.ceil(b / 2)
	print(f"\nPlayer Level: {level}")
	print(f"Base Damage & Healing: {base_damage}")

def expected_damage_menu():
	print ("#" * 40)
	print ("#" + " " * 38 + "#")
	print ("#" + " " * 5 + "Tibia Expected Melee Damage" + " " * 6 + "#")
	print ("#" + " " * 11 + "Weapon Stances:" + " " * 12 + "#")
	print ("#" + " " * 4 + "Offensive, Balanced, Defensive" + " " * 4 + "#")
	print ("#" * 40)
	base_damage = int(input("Enter base damage: "))
	weapon_damage = int(input("Enter weapon damage: "))
	weapon_skill = int(input("Enter weapon skill: "))
	weapon_stance = (input("Enter weapon stance: "))
	if weapon_stance == "offensive":
		offensive_mode(base_damage, weapon_damage, weapon_skill)
		print(f"\nExpected Damage: {offensive}")
	if weapon_stance == "balanced":
		balanced_mode(base_damage, weapon_damage, weapon_skill)
		print(f"\nExpected Damage: {balanced}")
	if weapon_stance == "defensive":
		defensive_mode(base_damage, weapon_damage, weapon_skill)
		print(f"\nExpected Damage: {defensive}")


if __name__ == "__main__":
	main_menu()