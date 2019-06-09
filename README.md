# dayzLootEditor
Visualize loot as list from database Edit and update types.xml
Built opon a a mysql database mostly generated and some manual editing
written in python.
types.xml needs to be in working directory

packages to install:
pyodbc

## Features
Press Enter to search by name or update entries to database!
![screenshot of application](images/2019-06-05_14-23-51.png)

### item searching
![search by name](images/searching.png)
search for items that contain the input in the name tag

### view linked items
select an item and click "view linked items":
it will show all items that can be attached to the item or are assossiated with it like ammo types, mags... this works for all supported item types

#### items that are linked to the FAL
![](images/linkedToFAL.png)

#### guns that are assosiated with 556 Ammo
![](images/linkedTo556Ammo.png)

### overall loot info

![](images/2019-06-05_14-23-41.png)

this shows overall nominal added up for all gun, mags... as well as the change since you started the programm. So you can check if you overall increased or decreased the loot count

### supported categories:
All items of the game are loaded and found if searched but the sorting only works for these types of items

![weapons, gun, ammo, mag, attachment, optic](images/2019-06-05_14-24-52.png)

## To do:

- [ ] Beeing able to add paste in new items and assossiate these items with a mod that can be activated and deactivated
- [ ] doing item assossiation inside of the app (most is automatic)
- [ ] guns can be assinged an ammo type which creates automatic assossiations
- [ ] support for all item types
- [ ] drop percentages (not in types.xml)
- [ ] loot overall droprate in percent adjusts nominal, min and restock
- [x] enter hotkey: when editing name -> search, nominal... -> update sel, selecting -> select matching
- [ ] loading types.xml and then generating all database from that (including finding ammo for typical guns)
- [ ] loading database with all links allready included
- [ ] 60round stanag is not implemented

## crazy ideas:

- [ ] creating online database for all mods where people can add their itemsmods types.xml entries and a checkbox in app for a specific mod to add to types xml.
- [ ] simulation of loot in game over time without having to run the game. graph for all items
