

class Monster:
    def __init__(self, name, description, health, attack, loot, items_required, hint, bonus, words):
        self.name = name
        self.description = description
        self.health = health
        self.attack = attack
        self.loot = loot
        self.items_required = items_required
        self.hint = hint
        self.bonus = bonus
        self.words = words

monsters = {
    'Diet Monster':Monster('Diet Monster',
                           "The Diet Monster is created by society's push for women to be thin and the intense focus on dieting. It grows in the battle between wanting to enjoy food and needing to control it. This creature feeds on the mixed feelings and guilt about what to eat. It lives where food is both comforting and worrisome.",
                           100,
                           20,
                           'Self-Acceptance',
                           ['Pizza', 'Jumping Rope'],
                           'To defeat the Diet Monster, you need both pizza and jumping rope. With pizza you can form a healthy relationship with food and with rope you can exercise to keep yourself fit.',
                           20,
                           "Why bother trying to eat healthy? You never stick to it anyway. You don't have the willpower like others do."),
    'Insecure Monster':Monster('Insecure Monster',
                               "The Insecure Monster stays away from open fights and likes to weaken its enemies in sneaky ways. It attacks by causing doubt and feeding on the uncertainty and pause that follow. This monster isn't very strong or bold, but it's hard to face directly because it uses the deep fears of its opponents against them.",
                               100,
                               20,
                               'Confidence',
                               ['Book'],
                               'To defeat the Insecure Monster, you need a book. With the book you can equip yourself with knowledge and feel secured.',
                               10,
                               "Are you really good enough for this? Think about all the times you've failed before. Maybe you're just not cut out for success like others are."
                               ),
    'Overthinking Monster': Monster('Overthinking Monster',
                                    "This monster comes from the shared worry and stress of overthinking too much. It represents the rush of thoughts that can stop and confuse someone. It hides in the deepest parts of the mind, getting stronger from not being able to decide and from doubt.",
                                    100,
                                    20,
                                    'Serenity',
                                    ['Mirror'],
                                    'To defeat the Insecure Monster, you need a mirror. With the mirror you can have a right percetion on yourself.',
                                    10,
                                    "What if you make the wrong decision? You know how every little choice can go badly. It's probably safer not to decide at all."
                                    ),
    'Balance Monster': Monster('Balance Monster',
                               "The Balance Monster comes from the pressures and expectations society puts on women to be great in both their work and personal lives. It represents the struggle to find a good balance between work and life. This monster grows stronger from the stress and guilt that come from these competing demands.",
                               100,
                               20,
                               'Equality',
                               ['Smart Planner', 'Clock'],
                               'To defeat the Balance Monster, you need a Smart Planner and a Clock. With the Smart Planner and Clock, you can master the work-life balance.',
                               20,
                               "You'll never get this balance right. If you focus on work, your personal life suffers, and if you relax a bit, your career falls behind. It's impossible to manage both successfully."),
    'Glass Ceiling Monster': Monster('Glass Ceiling Monster',
                                     "This monster comes from the unseen obstacles that stop women from moving forward in their careers. It symbolizes the frustration and limits of the glass ceiling. This creature gets stronger in places where inequality and unfairness are ignored.",
                                     100,
                                     20,
                                     'Empowerment',
                                     ['Key'],
                                     'To defeat the Glass Ceiling Monster, you need a Key of Ascent. With the Key of Ascent, you can climb to the top of your career ladder.',
                                     20,
                                     "Why strive for more when you're just going to hit the ceiling? You've seen others try and fail. It's just not meant for someone like you."),
    'Harassment Monster': Monster('Harassment Monster',
                                  "This monster stands for the widespread problem of harassment that women face in different areas of life. It becomes more powerful in places where this kind of behavior is overlooked or seen as normal.",
                                  100,
                                  20,
                                  'Safe Haven',
                                  ['Pizza', 'Key', 'Mirror', 'Book', 'Clock'],
                                  'To defeat the Harassment Monster, you need a lot of items which will make you stronger to say no to the harassment and fight against the monster.',
                                  50,
                                  "It's just the way things are, why make a fuss? Speaking up will only make it worse for you. Better to stay quiet and not rock the boat."
                                  )

}