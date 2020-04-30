import sys
sys.path.append("..")

import unittest
from modules import pet_shop as ps

class TestPetShop(unittest.TestCase):

    def setUp(self):
        self.customers = [
            {
                "name": "Alice",
                "pets": [],
                "cash": 1000
            },
            {
                "name": "Bob",
                "pets": [],
                "cash": 50
            },
            {
                "name": "Jack",
                "pets": [],
                "cash": 100
            }
        ]

        self.new_pet = {
            "name": "Bors the Younger",
            "pet_type": "cat",
            "breed": "Cornish Rex",
            "price": 100
        }

        self.pet_shop = {
            "pets": [
                {
                    "name": "Sir Percy",
                    "pet_type": "cat",
                    "breed": "British Shorthair",
                    "price": 500
                },
                {
                    "name": "King Bagdemagus",
                    "pet_type": "cat",
                    "breed": "British Shorthair",
                    "price": 500
                },
                {
                    "name": "Sir Lancelot",
                    "pet_type": "dog",
                    "breed": "Pomsky",
                    "price": 1000,
                },
                {
                    "name": "Arthur",
                    "pet_type": "dog",
                    "breed": "Husky",
                    "price": 900,
                },
                {
                    "name": "Tristan",
                    "pet_type": "cat",
                    "breed": "Basset Hound",
                    "price": 800,
                },
                {
                    "name": "Merlin",
                    "pet_type": "cat",
                    "breed": "Egyptian Mau",
                    "price": 1500,
                }
            ],
            "admin": {
                "total_cash": 1000,
                "pets_sold": 0,
            },
            "name": "Camelot of Pets"
        }

    def test_pet_shop_name(self):
        name = ps.pet_shop_name(self.pet_shop)
        self.assertEqual("Camelot of Pets", name)


    def test_total_cash(self):
        sum = ps.total_cash(self.pet_shop)
        self.assertEqual(1000, sum)

    def test_add_or_remove_cash__add(self):
        ps.add_or_remove_cash(self.pet_shop,10)
        cash = ps.total_cash(self.pet_shop)
        self.assertEqual(1010, cash)

    def test_add_or_remove_cash__remove(self):
        ps.add_or_remove_cash(self.pet_shop,-10)
        cash = ps.total_cash(self.pet_shop)
        self.assertEqual(990, cash)

    def test_pets_sold(self):
        sold = ps.pets_sold(self.pet_shop)
        self.assertEqual(0, sold)

    def test_increase_pets_sold(self):
        ps.increase_pets_sold(self.pet_shop,2)
        sold = ps.pets_sold(self.pet_shop)
        self.assertEqual(2, sold)

    def test_stock_count(self):
        count = ps.stock_count(self.pet_shop)
        self.assertEqual(6, count)

    def test_all_pets_by_breed__found(self):
        pets = ps.pets_by_breed(self.pet_shop, "British Shorthair")
        self.assertEqual(2, len(pets))

    def test_all_pets_by_breed__not_found(self):
        pets = ps.pets_by_breed(self.pet_shop, "Dalmation")
        self.assertEqual(0, len(pets))

    def test_find_pet_by_name__returns_pet(self):
        pet = ps.find_pet_by_name(self.pet_shop, "Arthur")
        self.assertEqual("Arthur", pet["name"])

    def test_find_pet_by_name__returns_None(self):
        pet = ps.find_pet_by_name(self.pet_shop, "Fred")
        self.assertIsNone(pet)

    def test_remove_pet_by_name(self):
        ps.remove_pet_by_name(self.pet_shop, "Arthur")
        pet = ps.find_pet_by_name(self.pet_shop,"Arthur")
        self.assertIsNone(pet)

    def test_add_pet_to_stock(self):
        ps.add_pet_to_stock(self.pet_shop, self.new_pet)
        count = ps.stock_count(self.pet_shop)
        self.assertEqual(7, count)

    def test_customer_cash(self):
        cash = ps.customer_cash(self.customers[0])
        self.assertEqual(1000, cash)

    def test_remove_customer_cash(self):
        customer = self.customers[0]
        ps.remove_customer_cash(customer, 100)
        self.assertEqual(900, customer["cash"])

    def test_customer_pet_count(self):
        count = ps.customer_pet_count(self.customers[0])
        self.assertEqual(0, count)

    def test_add_pet_to_customer(self):
        customer = self.customers[0]
        ps.add_pet_to_customer(customer, self.new_pet)
        self.assertEqual(1, ps.customer_pet_count(customer))

    # --- OPTIONAL ---

    def test_customer_can_afford_pet__sufficient_funds(self):
        customer = self.customers[0]
        can_buy_pet = ps.customer_can_afford_pet(customer, self.new_pet)
        self.assertEqual(True, can_buy_pet)

    def test_customer_can_afford_pet__insufficient_funds(self):
        customer = self.customers[1]
        can_buy_pet = ps.customer_can_afford_pet(customer, self.new_pet)
        self.assertEqual(False, can_buy_pet)

    def test_customer_can_afford_pet__exact_funds(self):
        customer = self.customers[2]
        can_buy_pet = ps.customer_can_afford_pet(customer, self.new_pet)
        self.assertEqual(True, can_buy_pet)

    # These are 'integration' tests so we want multiple asserts.
    # If one fails the entire test should fail
    #
    def test_sell_pet_to_customer__pet_found(self):
        customer = self.customers[0]
        pet = ps.find_pet_by_name(self.pet_shop,"Arthur")

        ps.sell_pet_to_customer(self.pet_shop, pet, customer)

        self.assertEqual(1, ps.customer_pet_count(customer))
        self.assertEqual(1, ps.pets_sold(self.pet_shop))
        self.assertEqual(100, ps.customer_cash(customer))
        self.assertEqual(1900, ps.total_cash(self.pet_shop))

    def test_sell_pet_to_customer__pet_not_found(self):
        customer = self.customers[0]
        pet = ps.find_pet_by_name(self.pet_shop,"Dave")

        ps.sell_pet_to_customer(self.pet_shop, pet, customer)

        self.assertEqual(0, ps.customer_pet_count(customer))
        self.assertEqual(0, ps.pets_sold(self.pet_shop))
        self.assertEqual(1000, ps.customer_cash(customer))
        self.assertEqual(1000, ps.total_cash(self.pet_shop))

    def test_sell_pet_to_customer__insufficient_funds(self):
        customer = self.customers[1]
        pet = ps.find_pet_by_name(self.pet_shop,"Arthur")

        ps.sell_pet_to_customer(self.pet_shop, pet, customer)

        self.assertEqual(0, ps.customer_pet_count(customer))
        self.assertEqual(0, ps.pets_sold(self.pet_shop))
        self.assertEqual(50, ps.customer_cash(customer))
        self.assertEqual(1000, ps.total_cash(self.pet_shop))

if __name__ == '__main__':
    unittest.main()
