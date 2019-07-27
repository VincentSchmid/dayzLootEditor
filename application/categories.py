from enum import Enum

gunSubTypesDict = {
               "Sidearms": [],
               "Pistols": [],
               "Rifles": [],
               "Shotguns": [],
               "Submachine Guns": [],
               "Assault Rifles": [],
               "Light Machine Guns": [],
               "Sniper Rifles": [],
               "Anti Material Rifles": []
                }

clothingSubTypesDict = {
                    "Glasses": ["glasses", "goggles"],
                    "Armbands": ["armband"],
                    "Gloves": ["gloves"],
                    "Hats & Caps": ["hat", "cap", "bandana", "hood"],
                    "Helmets": ["helm"],
                    "Masks": ["mask", "balaclava"],
                    "Shirts": ["shirt", "blouse"],
                    "Hoodies & Sweater": ["hoodie", "sweater"],
                    "Vests": ["vest"],
                    "Jackets & Coats": ["coat", "jacket", "suit"],
                    "Skirts & Dresses": ["skirt", "dress_"],
                    "Pants": ["pants", "breeches", "jeans"],
                    "Shoes & Boots": ["shoes", "sneakers", "boots", "wellies"],
                    "Ghillie": ["ghillie"],
                    "Holster & Pouches": ["holster", "pouch"],
                    "Bags": ["bag"],
                    "Handmade": []
                    }

foodSubTypesDict = {
                "Vegetables": [],
                "Packaged Food": ["can", "cereal", "powdered"],
                "Meat": ["meat", "lard"],
                "Drinks": ["sodacan", "bottle", "canteen"],
                "Medical Supplies": [],
                "Medications": [],
                "Money Exchange": []
                }

miscSubTypesDict = {
                "Tools (small)": [],
                "Tools (big)": [],
                "Electronics": [],
                "Fire & Lights": ["chemlight", "flare", "flashlight", "ablegas", "torch", "spotlight"],
                "Cooking & Hunting Supplies": [],
                "Hardware Supplies": ["tent", "barrel", "canister", "handcuff", "netting", "seachest"],
                "Seeds & Lime": ["seeds"]
                }

weaponSubTypesDict = {
                 "gun": gunSubTypesDict,
                 "ammo": {},
                 "optic": {},
                 "mag": {},
                 "attachment": {}
                  }

categoriesDict = {"weapons": weaponSubTypesDict,
                  "containers": clothingSubTypesDict,
                  "clothes": clothingSubTypesDict,
                  "food": foodSubTypesDict,
                  "tools": miscSubTypesDict,
                  "vehicles": {},
                  "vehiclesparts": {}}

weaponSubTypes = list(weaponSubTypesDict.keys())
categories = list(categoriesDict.keys())

usages = ["Military",
          "Prison",
          "School",
          "Coast",
          "Village",
          "Industrial",
          "Medic",
          "Police",
          "Hunting",
          "Town",
          "Farm",
          "Firefighter",
          "Office"]

usagesAbr = ["Mil.",
             "Pris.",
             "School",
             "Coast",
             "Vil.",
             "Ind.",
             "Med.",
             "Pol.",
             "Hunt.",
             "Town",
             "Farm",
             "Firef.",
             "Office"]

tiers = ["Tier1", "Tier2", "Tier3", "Tier4"]

tags = ["shelves", "floor"]

flags = ["count_in_cargo",
         "count_in_hoarder",
         "count_in_map",
         "count_in_player",
         "crafted",
         "deloot"]