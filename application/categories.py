from enum import Enum

weaponSubTypes = ["gun", "ammo", "optic", "mag", "attachment"]

gunSubTypes = {"Sidearms", "Pistols" "Rifles", "Shotguns", "Submachine Guns", "Assault Rifles", "Light Machine Guns",
               "Sniper Rifles", "Anti Material Rifles"}

clothingSubTypes = ["Glasses", "Armbands", "Gloves", "Hats & Caps", "Helmets", "Masks", "Shirts", "Hoodies & Sweater",
                     "Vests", "Jackets & Coats", "Skirts & Dresses", "Pants", "Shoes & Boots", "Ghillie",
                     "Holster & Pouches", "Bags", "Handmade"]

foodSubTypes = ["Vegetables", "Packaged Food", "Meat", "Drinks", "Medical Supplies", "Medications", "Money Exchange"]

MiscSubTypes = ["Tools (small)", "Tools (big)", "Electronics", "Fire & Lights", "Cooking & Hunting Supplies",
                "Hardware Supplies", "Seeds & Lime"]

categories = ["weapons", "containers", "clothes", "food", "tools", "vehicles", "vehiclesparts"]

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