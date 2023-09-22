import random
import time

# Reseeding the random number generator
random.seed(time.time())


class Field:
    def __init__(self, owner):
        self.owner = owner
        self.corn_generation = 10

    def generate_corn(self):
        self.owner.corn += self.corn_generation

    def cycle(self):
        self.generate_corn()


class Agent:
    MAX_HUNGER = 100
    CORN_PRICE = 2  # Arbitrary price for corn

    def __init__(self, cash, corn):
        self.cash = cash
        self.corn = corn
        self.hunger = 0
        self.fields = []  # List to hold multiple fields

    def increase_hunger(self):
        self.hunger += 10
        if self.hunger >= Agent.MAX_HUNGER:
            return True
        return False

    def consume_corn(self, amount):
        if self.corn >= amount:
            self.corn -= amount
            self.hunger -= amount
            self.hunger = max(0, self.hunger)

    def transact(self, other_agent):
        if self.hunger > 50 and self.cash >= Agent.CORN_PRICE:
            if other_agent.corn > 10:
                self.cash -= Agent.CORN_PRICE
                other_agent.cash += Agent.CORN_PRICE
                self.corn += 10
                other_agent.corn -= 10

    def seek_employment(self, other_agent):
        if self.cash < 10:
            self.cash += 10
            other_agent.cash -= 10

    def cycle(self):
        is_dead = self.increase_hunger()
        if is_dead:
            return True

        self.consume_corn(10)
        return False


if __name__ == "__main__":
    random.seed()  # Reseeding the random generator
    num_agents = 10
    agents = [Agent(100, 50) for _ in range(num_agents)]
    num_fields = 5
    fields = []

    for _ in range(num_fields):
        lucky_agent = random.choice(agents)
        field = Field(lucky_agent)
        fields.append(field)
        lucky_agent.fields.append(field)

    months = 50
    for month in range(months):
        print(f"Simulating month {month + 1}...")
        for agent in agents:
            for field in agent.fields:
                field.cycle()

            is_dead = agent.cycle()
            if is_dead:
                agents.remove(agent)
                print("Agent has died.")
                continue  # Skip the below transactions for this dead agent

            # Attempting transactions or employment
            another_agent = random.choice([a for a in agents if a != agent])
            agent.transact(another_agent)
            agent.seek_employment(another_agent)

        print(f"{len(agents)} agents remaining.")

    print("Simulation complete.")
