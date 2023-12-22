class Character:
    def __init__(self, name, hair_length, hair_color, eye_color):
        self.name = name
        self.hair_length = hair_length
        self.hair_color = hair_color
        self.eye_color = eye_color

    def view_character(self):
        return (f"Name: {self.name}, "
                f"Hair Length: {self.hair_length}, "
                f"Hair Color: {self.hair_color},"
                f"Eye Color: {self.eye_color}")

    def to_dict(self):
        return {
            'name': self.name,
            'hair_length': self.hair_length,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color
        }
