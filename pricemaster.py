import random
import inquirer
import inflect
import time  # Importing the time module

p = inflect.engine()

items = [
    "Old Lawn Mower",
    "Vintage Lamp",
    "Box of Mismatched Socks",
    "Collection of Used Books",
    "Rusty Bicycle"
]

def generate_pricemaster_price():
    magnitude = random.choice([3, 6, 9])
    base_price = random.randint(1, 1000)
    price = base_price * (10 ** magnitude)
    return price

def print_slowly(text):
    """Prints the text with a varying delay, increasing for the last two words."""
    words = text.split()
    for i, word in enumerate(words):
        print(word, end=' ', flush=True)
        time.sleep(1 if i >= len(words) - 3 else 0.5)
    print()  # New line after the sentence

def say_price(price):
    price_in_words = p.number_to_words(price).upper() + " DOLLARS"
    print("The PriceMaster demands:", end=' ')
    print_slowly(f"\"{price_in_words}\"")

def handle_ask(item, previous_price):
    if previous_price:
        # An offer was already made.
        if random.choice([True, False]) and new_price <= 10**11:
            # 50% chance to raise the price by an order of magnitude.
            new_price = 10**3 * previous_price
            say_price(new_price)
            return new_price
        else:
            if random.choice([True, False]):
                # 25% chance to refuse
                print("The PriceMaster announces:", end=' ')
                print_slowly("\"THE PRICEMASTER HAS SPOKEN\"")
                return previous_price
            else:
                # 25% chance to provide a new price
                new_price = generate_pricemaster_price()
                say_price(new_price)
                return new_price
    else:
        # No offers for this item yet.
        new_price = generate_pricemaster_price()
        say_price(new_price)
        return new_price

def handle_offer(item, previous_price):
    random_offers = sorted(random.sample(range(1, 40), 5))
    offer_speech = [f"${x}" for x in random_offers]
    offered_price = int(inquirer.prompt([
        inquirer.List('offer', message="The PriceMaster demands: \"MAKE ME AN OFFER\"", choices=offer_speech)
    ])['offer'].lstrip('$'))

    if previous_price:
        # An offer was already made.
        if random.choice([True, False]):
            # 50% chance to refuse
            print("The PriceMaster announces:", end=' ')
            print_slowly("\"THE PRICEMASTER HAS SPOKEN\"")
            return previous_price
        else:
            if random.choice([True, False]):
                # 25% chance to raise the provided price by an order of magnitude.
                magnitude = random.choice([3, 6, 9])
                new_price = offered_price * (10 ** magnitude)
                say_price(new_price)
                return new_price
            else:
                # 25% chance to provide a new price
                new_price = generate_pricemaster_price()
                say_price(new_price)
                return new_price
    else:
        if random.choice([True, False]):
            # 50% chance to raise the provided price by an order of magnitude.
            magnitude = random.choice([3, 6, 9])
            new_price = offered_price * (10 ** magnitude)
            say_price(new_price)
            return new_price
        else:
            # 50% chance to provide a random price
            new_price = generate_pricemaster_price()
            say_price(new_price)
            return new_price

def play_round(offer_made):
    item = inquirer.prompt([
        inquirer.List('item', message="Select an item:", choices=items)
    ])['item']

    action = inquirer.prompt([
        inquirer.List('action', message=f"You've selected the {item}. What will you do?",
                      choices=["Ask The PriceMaster for the price", "Make an offer to The PriceMaster"])
    ])['action']

    if action.startswith("Ask"):
        price = handle_ask(item, offer_made.get(item, None))
        offer_made[item] = price
    else:
        price = handle_offer(item, offer_made.get(item, None))
        offer_made[item] = price

def game_loop():
    offer_made = {}  # Initialize a dictionary to track offers
    while True:
        play_round(offer_made)

try:
    game_loop()
except KeyboardInterrupt:
    print("\nGame exited by the user.")

