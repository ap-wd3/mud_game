class Character:
    def __init__(self, name, bmi_category, hair_length, hair_color):
        self.name = name
        self.bmi_category = bmi_category
        self.hair_length = hair_length
        self.hair_color = hair_color

    def view_character(self):
        return (f"Name: {self.name}, "
                f"BMI Category: {self.bmi_category}, "
                f"Hair: {self.hair_length} & {self.hair_color}")

    def to_dict(self):
        """Convert the Character object to a dictionary."""
        return {
            'name': self.name,
            'bmi_category': self.bmi_category,
            'hair_length': self.hair_length,
            'hair_color': self.hair_color
        }
