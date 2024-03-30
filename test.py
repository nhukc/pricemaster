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
    """Prints the text one word at a time with a delay, making the last two words extra slow."""
    words = text.split()
    for i, word in enumerate(words):
        print(word, end=' ', flush=True)
        if i >= len(words) - 3:  # Extra slow for the last two words
            time.sleep(1)  # Increase the delay for the last two words
        else:
            time.sleep(0.5)  # Regular delay for the other words
    print()  # New line after the sentence

def play_round(offer_made):
    item = inquirer.prompt([
        inquirer.List('item', message="Select an item:", choices=items)
    ])['item']

    action = inquirer.prompt([
        inquirer.List('action', message=f"You've selected the {item}. What will you do?",
                      choices=["Ask The PriceMaster for the price", "Make an offer to The PriceMaster"])
    ])['action']

    if action.startswith("Ask"):
        if offer_made.get(item, None):
            # An offer was already made.
            if random.choice([True, False]) and offer_made.get(item, None) <= 10**11:
                # 50% chance to raise the price by 10x.
                offer_made[item] = 10 * offer_made.get(item, None)
                price_in_words = p.number_to_words(offer_made.get(item, None)).upper() + " DOLLARS"
                print("The PriceMaster demands:", end=' ')
                print_slowly(f"\"{price_in_words}\"")
            else:
                if random.choice([True, False]):
                    # 25% chance to refuse
                    print("The PriceMaster announces:", end=' ')
                    print_slowly("\"THE PRICEMASTER HAS SPOKEN\"")
                else:
                    # 25% chance to provide a new price
                    pricemaster_price = generate_pricemaster_price()
                    offer_made[item] = pricemaster_price
                    price_in_words = p.number_to_words(pricemaster_price).upper() + " DOLLARS"
                    print("The PriceMaster demands:", end=' ')
                    print_slowly(f"\"{price_in_words}\"")
        else:
            # No offers for this item yet.
            pricemaster_price = generate_pricemaster_price()
            offer_made[item] = pricemaster_price
            price_in_words = p.number_to_words(offer_made.get(item, None)).upper() + " DOLLARS"
            print("The PriceMaster demands:", end=' ')
            print_slowly(f"\"{price_in_words}\"")
    else:
        random_offers = sorted(random.sample(range(1, 40), 5))
        offer_speech = [f"${x}" for x in random_offers]
        offered_price = int(inquirer.prompt([
            inquirer.List('offer', message="The PriceMaster demands: \"MAKE ME AN OFFER\"", choices=offer_speech)
        ])['offer'].lstrip('$'))

        if offer_made.get(item, None):
            # An offer was already made.
            if random.choice([True, False]):
                # 50% chance to refuse
                print("The PriceMaster announces:", end=' ')
                print_slowly("\"THE PRICEMASTER HAS SPOKEN\"")
            else:
                if random.choice([True, False]):
                    # 25% chance to raise the provided price by an order of magnitude.
                    magnitude = random.choice([3, 6, 9])
                    offer_made[item] = offered_price * (10 ** magnitude)
                    price_in_words = p.number_to_words(offer_made.get(item, None)).upper() + " DOLLARS"
                    print("The PriceMaster demands:", end=' ')
                    print_slowly(f"\"{price_in_words}\"")
                else:
                    # 25% chance to provide a new price
                    pricemaster_price = generate_pricemaster_price()
                    offer_made[item] = pricemaster_price
                    price_in_words = p.number_to_words(pricemaster_price).upper() + " DOLLARS"
                    print("The PriceMaster demands:", end=' ')
                    print_slowly(f"\"{price_in_words}\"")
        else:
            if random.choice([True, False]):
                # 50% chance to raise the provided price by an order of magnitude.
                magnitude = random.choice([3, 6, 9])
                offer_made[item] = offered_price * (10 ** magnitude)
                price_in_words = p.number_to_words(offer_made.get(item, None)).upper() + " DOLLARS"
                print("The PriceMaster demands:", end=' ')
                print_slowly(f"\"{price_in_words}\"")
            else:
                # 50% chance to provide a random price
                pricemaster_price = generate_pricemaster_price()
                offer_made[item] = pricemaster_price
                price_in_words = p.number_to_words(pricemaster_price).upper() + " DOLLARS"
                print("The PriceMaster demands:", end=' ')
                print_slowly(f"\"{price_in_words}\"")

def game_loop():
    offer_made = {}  # Initialize a dictionary to track offers
    while True:
        play_round(offer_made)

try:
    game_loop()
except KeyboardInterrupt:
    print("\nGame exited by the user.")

