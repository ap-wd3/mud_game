import os

os.system("")

class ConfidenceBar:
    symbol_remaining: str = "▮"
    symbol_lost: str = "_"
    barrier: str = "|"
    def __init__(self,
                 entity,
                 length: int = 20,
                 id_colored: bool = True,
                 color: str = ""):
        self.entity = entity
        self.length = length
        self.max_value = entity.confidence_max
        self.current_value = entity.confidence_max

        self.is_colored = id_colored
        self.color = color

    def update(self):
        self.current_value = self.entity.health

    def draw(self):
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        print(f"{self.entity.name}'s HEALTH: {self.entity.confidence}/{self.entity.confidence_max}")
        print(f"{self.barrier}"
              f"{self.color if self.is_colored else ''}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors['default'] if self.is_colored else ''}"
              f"{self.barrier}")