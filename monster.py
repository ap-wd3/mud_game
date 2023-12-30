

class Monster:
    def __init__(self, name, description, health, attack, loot, items_required, hint, bonus):
        self.name = name
        self.description = description
        self.health = health
        self.attack = attack
        self.loot = loot
        self.items_required = items_required
        self.hint = hint
        self.bonus = bonus






monsters = {
    'Diet Monster':Monster('Diet Monster',
                           "Born from society's pressure on women to be skinny and obession with dieting and the constant struggle between indulgence and restraint,the Diet Monster feeds on the guilt and confusion surrounding food choices."
                           "It thrives in environments where food is both a source of comfort and anxiety.",
                           100,
                           20,
                           'Self-Acceptance',
                           ['Pizza', 'Jumping Rope'],
                           'To defeat the Diet Monster, you need both pizza and rope. With pizza you can form a healthy relationship with food and with rope you can exercise to keep yourself fit.',
                           20),
    'Insecure Monster':Monster('Insecure Monster',
                               "The Insecure Monster avoids direct conflict,"
                                                    "preferring to undermine its opponents subtly."
                                                    "It attacks by planting seeds of doubt and feeding on the resulting uncertainty and hesitation."
                                                    "It's not particularly strong or aggressive,"
                                                    " but it's elusive and difficult to confront head-on because it plays on the inner fears of its adversaries.",
                               100,
                               20,
                               'Confidence',
                               ['Book'],
                               'To defeat the Insecure Monster, you need a book. With the book you can equip yourself with knowledge and feel secured.',
                               10),
    'Overthinking Monster': Monster('Overthinking Monster',
                                    "Born from the collective anxiety and stress of constant overthinking,"
                                    "this monster embodies the overwhelming flood of thoughts that can paralyze and confuse."
                                    "It lurks in the deepest corners of the mind, growing stronger with indecision and doubt.",
                                    100,
                                    20,
                                    'Serenity',
                                    ['Mirror'],
                                    'To defeat the Insecure Monster, you need a mirror. With the mirror you can have a right percetion on yourself.',
                                    10
                                    ),
    'Balance Monster': Monster('Balance Monster',
                               'Born from the societal pressures and expectations placed on women to excel both in their careers and personal lives,'
                               'the Balance Monster personifies the challenge of achieving a harmonious work-life balance.'
                               'It feeds on the stress and guilt that arise from these conflicting demands.',
                               100,
                               20,
                               'Equality',
                               ['Smart Planner', 'Clock'],
                               'To defeat the Balance Monster, you need a Smart Planner and a Clock. With the Smart Planner and Clock, you can master the work-life balance.',
                               20),
    'Glass Ceiling Monster': Monster('Glass Ceiling Monster',
                                     "Spawned from the invisible barriers that impede women's progress in their careers,"
                                     "this monster embodies the frustration and limitations of the glass ceiling."
                                     "It thrives in environments where inequality and bias go unchecked.",
                                     100,
                                     20,
                                     'Empowerment',
                                     ['Key'],
                                     'To defeat the Glass Ceiling Monster, you need a Key of Ascent Embody. With the Key of Ascent, you can overcome the Glass Ceiling.',
                                     20),
    'Harassment Monster': Monster('Harassment Monster',
                                  'This monster represents the pervasive issue of harassment faced by women in various spheres of life. It grows stronger in environments where such behavior is ignored or normalized.',
                                  100,
                                  20,
                                  'Safe Haven',
                                  ['Pizza', 'Jumping Rope', 'Mirror', 'Book', 'Smart Planner'],
                                  'To defeat the Harassment Monster, you need all the items in the rooms.',
                                  50
                                  )

}