class Weapon:
    def __init__(self, name, weapon_type, damage, value):
        self.name = name
        self.weapon_type = weapon_type
        self.damage = damage
        self.value = value


fists = Weapon(name="Fists",
              weapon_type="blunt",
              damage=2,
              value=0)

short_bow = Weapon(name="Short Bow",
                   weapon_type="ranged",
                   damage=4,
                   value=8)
