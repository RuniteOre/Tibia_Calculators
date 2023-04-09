package main

import (
	"fmt"
	"math"
	"os"
	"strings"
	"encoding/json"
	"bufio"
)

func offensiveMode(baseDmg, wepDmg, wepSkill int) int {
	return baseDmg + int(math.Floor(1.2*float64(wepDmg)*((float64(wepSkill)+4)/28)))
}

func balancedMode(baseDmg, wepDmg, wepSkill int) int {
	return baseDmg + int(math.Floor(float64(wepDmg) * ((float64(wepSkill) + 4) / 28)))
}

func defensiveMode(baseDmg, wepDmg, wepSkill int) int {
	return baseDmg + int(math.Floor(math.Ceil(0.6 * float64(wepDmg)) * (float64(wepSkill) + 4) / 28))
}

func magicLevelTrainingTime(vocationfactor, vocation_constant float64, magic_level int, percent_to_next float64) float64 {
	return vocationfactor * math.Pow(vocation_constant, float64(magic_level)) * percent_to_next
}

func expectedMagicValues(level, base_damage, magic_level int, spell_name string) int {
	var spell_data map[string]map[string]map[string]float64
	spell_x := 0.0
	spell_y := 0.0
	x := 0.0
	y := 0.0
	magic := 0.0

	f, err := os.Open("instantspells.json")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	decoder := json.NewDecoder(f)
	err = decoder.Decode(&spell_data)
	if err != nil {
		panic(err)
	}

	spell_x = spell_data[spell_name]["Max damage"]["x"] - spell_data[spell_name]["Min damage"]["x"]
	spell_y = spell_data[spell_name]["Max damage"]["y"] - spell_data[spell_name]["Min damage"]["y"]

	x = spell_data[spell_name]["Min damage"]["x"] + spell_x * float64(magic_level)
	y = spell_data[spell_name]["Min damage"]["y"] + spell_y * float64(magic_level)

	magic = math.Floor((float64(level) * 0.2) + x + y)

	return int(magic)
}

func expectedHealingValues(level, base_damage, magic_level int, spell_name string) int {
	var spell_data map[string]map[string]map[string]float64
	spell_x := 0.0
	spell_y := 0.0
	x := 0.0
	y := 0.0
	healing := 0.0

	f, err := os.Open("healingspells.json")
	if err != nil {
		panic(err)
	}
	defer f.Close()

	decoder := json.NewDecoder(f)
	err = decoder.Decode(&spell_data)
	if err != nil {
		panic(err)
	}

	spell_x = spell_data[spell_name]["Max healing"]["x"] - spell_data[spell_name]["Min healing"]["x"]
	spell_y = spell_data[spell_name]["Max healing"]["y"] - spell_data[spell_name]["Min healing"]["y"]

	x = float64(spell_data[spell_name]["Min healing"]["x"]) + spell_x * float64(magic_level)
	y = float64(spell_data[spell_name]["Min healing"]["y"]) + spell_y * float64(magic_level)

	healing = math.Floor((float64(level) * 0.2) + x + y)

	return int(healing)
}

func calculateS(level int) int {
/*
	Till level 500: no change, damage and healing +1 every 5 levels
	As of level 501-1100: damage and healing +1 every 6 levels
	As of level 1101-1800: damage and healing +1 every 7 levels
	As of level 1801-2600: damage and healing +1 every 8 levels
	As of level 2601-3500: damage and healing +1 every 9 levels
	Above level 3500 it continues with the same logic (steps of 500, 600, 700, etc.)
	the if statements are used to calculate the correct "s" value for the base damage formula from the above info
*/
	if level <= 500 {
		return 5
	} else if level <= 1100 {
		return 6
	} else if level <= 1800 {
		return 7
	} else if level <= 2600 {
		return 8
	} else if level <= 3500 {
		return 9
	} else {
		return int(math.Floor((math.Sqrt(2 * float64(level) + 2025) + 5 / 10)))
	}
}

func calculateB(level, s int) int {
	return int(math.Floor(float64(level + 1000) / float64(s) - (50 * float64(s)))) + (100 * s) - 450
}

func mainMenu() {
	fmt.Println("########################################")
	fmt.Println("#                                      #")
	fmt.Println("#          Mark's Tibia Calculators    #")
	fmt.Println("#                                      #")
	fmt.Println("########################################")
	fmt.Println("#                                      #")
	fmt.Println("#          1. Base Damage & Healing    #")
	fmt.Println("#          2. Melee Expected Damage    #")
	fmt.Println("#          3. Magic Expected Damage    #")
	fmt.Println("#          4. Magic Training Time      #")
	fmt.Println("#                                      #")
	fmt.Println("########################################")
	var option int

	for true {
		fmt.Print("Enter your choice: ")
		fmt.Scanln(&option)

		if option == 1 {
			baseDamageMenu()
			break
		} else if option == 2 {
			meleeExpectedDamageMenu()
			break
		} else if option == 3 {
			expectedMagicMenu()
			break
		} else if option == 4 {
			magicTrainingTimeMenu()
			break
		} else {
			fmt.Println("Invalid choice, try again")
		}
	}
}

func baseDamageMenu() {
	var level int
	fmt.Println("########################################")
	fmt.Println("#                                      #")
	fmt.Println("#        Tibia Base Damage & Healing   #")
	fmt.Println("#                                      #")
	fmt.Println("########################################")
	fmt.Print("Enter player level: ")
	fmt.Scanln(&level)
	s := calculateS(level)
	b := calculateB(level, s)
	baseDamage := b + (s - 1) * int(math.Ceil(float64(b) / 2))
	fmt.Printf("\nPlayer Level: %d\n", level)
	fmt.Printf("Base Damage & Healing: %d\n", baseDamage)
}

func meleeExpectedDamageMenu() {
	var level, weaponDamage, weaponSkill int
	fmt.Println("########################################")
	fmt.Println("#                                      #")
	fmt.Println("#      Tibia Expected Melee Damage     #")
	fmt.Println("#                                      #")
	fmt.Println("########################################")
	fmt.Println("#                                      #")
	fmt.Println("#       Weapon Stances:                #")
	fmt.Println("#       Offensive, Balanced, Defensive #")
	fmt.Println("#                                      #")
	fmt.Println("########################################")
	fmt.Print("Enter player level: ")
	fmt.Scanln(&level)
	s := calculateS(level)
	b := calculateB(level, s)
	baseDamage := b + (s - 1) * int(math.Ceil(float64(b) / 2))
	fmt.Printf("\nPlayer Level: %d\n", level)
	fmt.Printf("Base Damage & Healing: %d\n", baseDamage)
	fmt.Print("Enter weapon damage: ")
	fmt.Scanln(&weaponDamage)
	fmt.Print("Enter weapon skill level: ")
	fmt.Scanln(&weaponSkill)
	offensive := offensiveMode(baseDamage, weaponDamage, weaponSkill)
	fmt.Printf("\nExpected Damage using Offensive: %d\n", offensive)
	balanced := balancedMode(baseDamage, weaponDamage, weaponSkill)
	fmt.Printf("\nExpected Damage using Balanced: %d\n", balanced)
	defensive := defensiveMode(baseDamage, weaponDamage, weaponSkill)
	fmt.Printf("\nExpected Damage using Defensive: %d\n", defensive)
}

func expectedMagicMenu() {
	var heal, level, magicLevel int
	var spellName string
	fmt.Println("########################################")
	fmt.Println("#                                      #")
	fmt.Println("#     Tibia Expected Magic Damage      #")
	fmt.Println("#                                      #")
	fmt.Println("########################################")
	fmt.Print("Enter 1 for healing, 2 for damage: ")
	fmt.Scanln(&heal)
	if heal != 1 && heal != 2 {
		return
	}
	fmt.Print("Enter player level: ")
	fmt.Scanln(&level)
	s := calculateS(level)
	b := calculateB(level, s)
	baseDamage := b + (s - 1) * int(math.Ceil(float64(b) / 2))
	fmt.Println("Base Damage:", baseDamage)
	fmt.Print("Enter magic level: ")
	fmt.Scanln(&magicLevel)
	fmt.Print("Enter spell name: ")
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	spellName = scanner.Text()
	if heal == 1 {
		healing := expectedHealingValues(level, baseDamage, magicLevel, spellName)
		fmt.Println()
		fmt.Printf("Expected Healing using %s: %d\n", spellName, healing)
	} else {
		damage := expectedMagicValues(level, baseDamage, magicLevel, spellName)
		fmt.Println()
		fmt.Printf("Expected Damage using %s: %d\n", spellName, damage)
	}
}

func magicTrainingTimeMenu() {
	var vocation string
	fmt.Println("########################################")
	fmt.Println("#                                      #")
	fmt.Println("#        Tibia Magic Level Training    #")
	fmt.Println("#                                      #")
	fmt.Println("########################################")
	for true {
		fmt.Print("Enter vocation (Sorcerer, Master Sorcerer, Knight, Elite Knight, Paladin, Royal Paladin, Druid, Elder Druid): ")
		vocation = strings.ToLower(vocation)
		fmt.Scanln(&vocation)
		if vocation == "sorcerer" || vocation == "master sorcerer" || vocation == "knight" || vocation == "elite knight" || vocation == "paladin" || vocation == "royal paladin" || vocation == "druid" || vocation == "elder druid" {
			break
		} else {
			fmt.Println("Invalid vocation. Please enter a valid vocation")
		}
	}
	var vocationFactor, vocationConstant float64
	if vocation == "sorcerer" || vocation == "druid" || vocation == "royal paladin" {
		vocationFactor = 0.67
		vocationConstant = 1.1
	} else if vocation == "master sorcerer" || vocation == "elder druid" {
		vocationFactor = 0.44
		vocationConstant = 1.1
	} else if vocation == "knight" || vocation == "elite knight" {
		vocationFactor = 1.33
		vocationConstant = 3.0
	} else if vocation == "paladin" {
		vocationFactor = 0.88
		vocationConstant = 1.4
	}
	var magicLevel int
	var percentToNext float64
	fmt.Print("Enter current magic level: ")
	fmt.Scanln(&magicLevel)
	fmt.Print("Enter percent to next magic level in decimal form: ")
	fmt.Scanln(&percentToNext)
	trainingTimeTotalMinutes := magicLevelTrainingTime(vocationFactor, vocationConstant, magicLevel, percentToNext)
	trainingTimeHours := int(math.Floor(trainingTimeTotalMinutes / 60))
	trainingTimeMinutes := int(trainingTimeTotalMinutes) % 60
	fmt.Printf("\nTime needed to train to next magic level: %d hours, %d minutes\n", int(trainingTimeHours), int(trainingTimeMinutes))
}

func main() {
	mainMenu()
}