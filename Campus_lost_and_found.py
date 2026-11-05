# =====================================================
# PROJECT: CAMPUS LOST & FOUND MANAGEMENT SYSTEM
# =====================================================

import json
import os


# PART 1: PARENT CLASS

class Item:

    def __init__(self, item_id, name, category, location, date):
        self._item_id = item_id
        self.name = name
        self.category = category
        self.location = location
        self.date = date
        self.status = "Open"

    def get_id(self):
        return self._item_id

    def display(self):
        print("-" * 45)
        print("Item ID  :", self._item_id)
        print("Name     :", self.name)
        print("Category :", self.category)
        print("Location :", self.location)
        print("Date     :", self.date)
        print("Status   :", self.status)


# PART 2: CHILD CLASS - LOST ITEM

class LostItem(Item):

    def __init__(self, item_id, name, category,
                 location, date, owner):

        super().__init__(item_id, name, category, location, date)
        self.owner = owner

    def display(self):
        super().display()
        print("Type     : Lost Item")
        print("Reported by:", self.owner)
        print("-" * 45)


# PART 3: CHILD CLASS - FOUND ITEM

class FoundItem(Item):

    def __init__(self, item_id, name, category,
                 location, date, finder):

        super().__init__(item_id, name, category, location, date)
        self.finder = finder

    def display(self):
        super().display()
        print("Type     : Found Item")
        print("Found by :", self.finder)
        print("-" * 45)


# PART 4: ITEM MANAGER CLASS

class ItemManager:

    def __init__(self):
        self.items = []
        self.next_id = 1
        self.filename = "items.json"
        self.load_data()

    # FIND ITEM

    def find_item(self, item_id):

        for item in self.items:
            if item.get_id() == item_id:
                return item

        return None

    # SAVE DATA

    def save_data(self):

        records = []

        for item in self.items:

            if isinstance(item, LostItem):
                item_type = "Lost"
                person = item.owner
            else:
                item_type = "Found"
                person = item.finder

            records.append({
                "id": item.get_id(),
                "name": item.name,
                "category": item.category,
                "location": item.location,
                "date": item.date,
                "status": item.status,
                "type": item_type,
                "person": person
            })

        with open(self.filename, "w") as file:
            json.dump(records, file, indent=4)

    # LOAD DATA

    def load_data(self):

        if not os.path.exists(self.filename):
            return

        try:
            with open(self.filename, "r") as file:
                records = json.load(file)

            for record in records:

                if record["type"] == "Lost":

                    item = LostItem(
                        record["id"],
                        record["name"],
                        record["category"],
                        record["location"],
                        record["date"],
                        record["person"]
                    )

                else:

                    item = FoundItem(
                        record["id"],
                        record["name"],
                        record["category"],
                        record["location"],
                        record["date"],
                        record["person"]
                    )

                item.status = record["status"]
                self.items.append(item)

            if self.items:
                self.next_id = max(
                    item.get_id() for item in self.items
                ) + 1

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("Unable to read saved records.")

    # ADD LOST ITEM

    def add_lost_item(self):

        print("\n========== REPORT LOST ITEM ==========")

        name = input("Enter item name: ").strip()
        category = input("Enter category: ").strip()
        location = input("Where was it lost? ").strip()
        date = input("Enter date: ").strip()
        owner = input("Enter your name: ").strip()

        if not all([name, category, location, date, owner]):
            print("All fields are required!")
            return

        item = LostItem(
            self.next_id, name, category,
            location, date, owner
        )

        self.items.append(item)
        self.next_id += 1
        self.save_data()

        print("\nLost item reported successfully!")
        print("Your Item ID:", item.get_id())

    # ADD FOUND ITEM

    def add_found_item(self):

        print("\n========== REGISTER FOUND ITEM ==========")

        name = input("Enter item name: ").strip()
        category = input("Enter category: ").strip()
        location = input("Where was it found? ").strip()
        date = input("Enter date: ").strip()
        finder = input("Enter your name: ").strip()

        if not all([name, category, location, date, finder]):
            print("All fields are required!")
            return

        item = FoundItem(
            self.next_id, name, category,
            location, date, finder
        )

        self.items.append(item)
        self.next_id += 1
        self.save_data()

        print("\nFound item registered successfully!")
        print("Your Item ID:", item.get_id())

    # VIEW ALL ITEMS

    def view_items(self):

        print("\n========== ALL ITEM RECORDS ==========")

        if not self.items:
            print("No records available.")
            return

        for item in self.items:
            item.display()

    # SEARCH ITEM

    def search_item(self):

        print("\n========== SEARCH ITEM ==========")

        keyword = input(
            "Enter item name, category or location: "
        ).strip().lower()

        if not keyword:
            print("Enter a search term!")
            return

        found = False

        for item in self.items:

            if (keyword in item.name.lower()
                or keyword in item.category.lower()
                or keyword in item.location.lower()):

                item.display()
                found = True

        if not found:
            print("No matching item found.")

    # UPDATE STATUS

    def update_status(self):

        print("\n========== UPDATE ITEM STATUS ==========")

        try:
            item_id = int(input("Enter Item ID: "))
        except ValueError:
            print("Enter a valid ID!")
            return

        item = self.find_item(item_id)

        if item is None:
            print("Item not found!")
            return

        print("\n1. Open")
        print("2. Claimed")

        choice = input("Select status: ")

        if choice == "1":
            item.status = "Open"

        elif choice == "2":
            item.status = "Claimed"

        else:
            print("Invalid choice!")
            return

        self.save_data()
        print("Status updated successfully!")

    # DELETE ITEM

    def delete_item(self):

        print("\n========== DELETE ITEM ==========")

        try:
            item_id = int(input("Enter Item ID: "))
        except ValueError:
            print("Enter a valid ID!")
            return

        item = self.find_item(item_id)

        if item is None:
            print("Item not found!")
            return

        confirm = input(
            "Are you sure? (yes/no): "
        ).strip().lower()

        if confirm == "yes":
            self.items.remove(item)
            self.save_data()
            print("Item deleted successfully!")

        else:
            print("Delete cancelled.")

    # SUMMARY

    def show_summary(self):

        lost = 0
        found = 0
        claimed = 0

        for item in self.items:

            if isinstance(item, LostItem):
                lost += 1
            else:
                found += 1

            if item.status == "Claimed":
                claimed += 1

        print("\n========== ITEM SUMMARY ==========")
        print("Total Items  :", len(self.items))
        print("Lost Items   :", lost)
        print("Found Items  :", found)
        print("Claimed Items:", claimed)


# PART 5: MAIN PROGRAM

def main():

    manager = ItemManager()

    print("=" * 45)
    print("   CAMPUS LOST & FOUND MANAGEMENT")
    print("=" * 45)

    while True:

        print("\n============== MAIN MENU ==============")
        print("1. Report Lost Item")
        print("2. Register Found Item")
        print("3. View All Items")
        print("4. Search Item")
        print("5. Update Item Status")
        print("6. Delete Item")
        print("7. View Summary")
        print("8. Exit")
        print("=" * 42)

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            manager.add_lost_item()

        elif choice == "2":
            manager.add_found_item()

        elif choice == "3":
            manager.view_items()

        elif choice == "4":
            manager.search_item()

        elif choice == "5":
            manager.update_status()

        elif choice == "6":
            manager.delete_item()

        elif choice == "7":
            manager.show_summary()

        elif choice == "8":
            print("\nThank you for using Campus Lost & Found!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Try again.")


# PROGRAM EXECUTION

if __name__ == "__main__":
    main()