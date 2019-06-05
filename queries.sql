select item2
from
    (select *
     from items
              join itemcombos i on name = item1
     WHERE name = 'AKM') as attachments;

select name, nominal, min, restock, lifetime
from items
where type = 'gun';

select name, nominal, min
from items
where type = 'mag';

select name, ingameName
from items
where type = 'optic';

select name
from items
where type = 'attachment' or type = 'optic';

#supressors
select name
from items
where name LIKE '%suppressor%'

#Select ammo type
select name
from items
where
        type = 'ammo'
  and name LIKE '%308%';

#select gun
select name
from items
where name LIKE '%m4%'
  and type = 'gun';

#select mag
select name
from items
WHERE name LIKE'%stanag%'
  and type = 'mag';

#select optic
select name
from items
WHERE name LIKE '%acog%'
  and type = 'optic';

#get weapon and corresponding items with relevant values
select name, nominal, min, restock, lifetime, count_in_cargo as cargo, count_in_player as player
from items
         join
     (select item2
      FROM (select name, item2
            from items
                     join itemcombos i on items.name = i.item1
            where name LIKE '%awm%') as accessoire
     ) as item2 on name = item2.item2;

#get accessoir and see to what weapon it corresponds to
select item2, name, type, nominal, min, lifetime, restock
from (select item1, item2, items.*
      from itemcombos
               join items on name = item1
      where item2 LIKE '%556%'
     ) as accessoire
group by name;

#nominal of all guns
select SUM(nominal)
from items
where type = 'gun';

#nominal of all guns in military
select SUM(nominal)
from items
where type = 'gun'
  and Military = 1;

#nominal of all guns tier4
select SUM(nominal)
from items
where type = 'gun'
  and Tier4 = 1;

select name
from items
where type = 'gun'
  and nominal = 0

select name
from items
WHERE name NOT IN
      (SELECT item2
       FROM itemcombos)
  AND type = 'optic';


