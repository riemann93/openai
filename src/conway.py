import random
import time

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
    CORN_PRICE = 2

    def __init__(self, cash, corn):
        self.cash = cash
        self.corn = corn
        self.hunger = 0
        self.fields = []
        self.workers = []

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
        # Placeholder: Should link to actual work
        if self.cash < 10 and other_agent.cash >= 10:
            self.workers.append(other_agent)
            self.cash -= 10
            other_agent.cash += 10

    def post_job(self, market, salary):
        market.post_job_offer(self, salary)

    def list_corn(self, market, price, amount):
        market.list_corn_for_sale(self, price, amount)

    def find_job(self):
        pass
    def buy_corn(self):
        pass

    def cycle(self):
        is_dead = self.increase_hunger()
        if is_dead:
            return True
        if self.hunger > 50:
            self.consume_corn(10)
        return False




class JobOffer:
    def __init__(self, employer, salary):
        self.employer = employer
        self.salary = salary


class CornForSale:
    def __init__(self, seller, price, amount):
        self.seller = seller
        self.price = price
        self.amount = amount


class Market:
    def __init__(self):
        self.corn_price = Agent.CORN_PRICE
        self.current_salary = 10  # Just an initial value
        self.job_offers = []
        self.corn_for_sale = []

    def post_job_offer(self, employer, salary):
        job_offer = JobOffer(employer, salary)
        self.job_offers.append(job_offer)

    def list_corn_for_sale(self, seller, price, amount):
        corn_offer = CornForSale(seller, price, amount)
        self.corn_for_sale.append(corn_offer)

    def update_market(self):
        # Logic for updating the corn_price and current_salary
        # Here you can add whatever you want to change these values over time
        pass

def distribute_fields():
    for _ in range(num_fields):
        lucky_agent = random.choice(agents)
        field = Field(lucky_agent)
        fields.append(field)
        lucky_agent.fields.append(field)


if __name__ == "__main__":
    num_agents = 10
    agents = [Agent(100, 50) for _ in range(num_agents)]
    num_fields = 5
    fields = []
    market = Market()

    distribute_fields()

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
                continue

            another_agent = random.choice([a for a in agents if a != agent])
            agent.transact(another_agent)
            agent.seek_employment(another_agent)

        print(f"{len(agents)} agents remaining.")

    print("Simulation complete.")
