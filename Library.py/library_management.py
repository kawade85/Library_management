#LibraryItem: Represents a library item with attributes and methods for checking out and returning items.
#Library: Manages a collection of LibraryItem objects, allowing you to add, check out, return, and search for items.
#LibraryApp: This class creates the GUI using Tkinter and handles user interactions.

#GUI Components:

 #   Frames: Used to organize UI elements.
 #   Labels, Entry fields, and Buttons: For user inputs and actions (adding items, checking out, returning, and searching).
 #   Text Widget: Displays search results.

# Adding an item to the library requires entering the title, author, and category.
# Checking out an item changes its status to checked out and sets a due date.
# Returning an item checks its status and calculates any overdue fines.
# Searching items displays results based on title, author, or category.



import tkinter as tk  # Import the Tkinter library for GUI
from tkinter import messagebox  # Import messagebox for pop-up messages
from datetime import datetime, timedelta  # Import date/time handling for due dates

class LibraryItem:
    def __init__(self, title, author, category):     #class definition
        self.title = title  # Set the title of the item
        self.author = author  # Set the author of the item
        self.category = category  # Set the category of the item
        self.is_checked_out = False  # Item starts as not checked out
        self.due_date = None  # Due date starts as None

    def check_out(self):
        if not self.is_checked_out:  # Check if the item is not already checked out
            self.is_checked_out = True  # Mark the item as checked out
            self.due_date = datetime.now() + timedelta(days=7)  # Set due date to 7 days from now
            return True  # Return True indicating successful checkout
        return False  # Return False if item was already checked out

    def return_item(self):
        if self.is_checked_out:  # Check if the item is currently checked out
            self.is_checked_out = False  # Mark the item as returned
            self.due_date = None  # Clear the due date
            return True  # Return True indicating successful return
        return False  # Return False if item was not checked out

    def is_overdue(self):
        return self.is_checked_out and datetime.now() > self.due_date  # Check if the item is overdue

    def __str__(self):
        return f"{self.title} by {self.author} ({self.category}) - {'Checked Out' if self.is_checked_out else 'Available'}"  # String representation of the item

class Library:
    def __init__(self):
        self.items = []           #...... Initialize an empty list to hold library items

    def add_item(self, item):
        self.items.append(item)             # Add a new item to the library's item list

    def check_out_item(self, title):
        for item in self.items:           # Loop through all items in the library
            if item.title.lower() == title.lower() and not item.is_checked_out:     # Check for matching title and availability
                if item.check_out():       # Attempt to check out the item
                    return item            # Return the item if checkout is successful
        return None                        # Return None if item is not found or not available

    def return_item(self, title):
        for item in self.items:               # Loop through all items in the library
            if item.title.lower() == title.lower() and item.is_checked_out:      # Check for matching title and checked out status
                item.return_item()            # Return the item
                overdue_days = (datetime.now() - item.due_date).days        # Calculate overdue days
                fine = max(0, overdue_days)  # Set fine; 70Rs per day, ensuring no negative fines
                return item, fine            # Return the item and the calculated fine
        return None, 0                       # Return None and 0 if item is not found or not checked out

    def search_items(self, search_term):
        return [item for item in self.items 
        if (search_term.lower() in item.title.lower() or  # Check if search term matches title
            search_term.lower() in item.author.lower() or  # Check if search term matches author
            search_term.lower() in item.category.lower())]  # Check if search term matches category

class LibraryApp:
    def __init__(self, root):
        self.library = Library()       # Creating an instance of the Library class
        self.root = root               # Creating the main window
        self.root.title("***** Library Management System *****")  # Set the window title

        self.setup_ui()          #..... Calling method to set up the user interface

    def setup_ui(self):
        # Adding Item Frame
        frame_add = tk.Frame(self.root)  # Create a frame for adding items
        frame_add.pack(pady=10)          # vertical padding

        tk.Label(frame_add, text="Title:").grid(row=0, column=0)     # Label for title
        self.title_entry = tk.Entry(frame_add)                       # Entry field for title
        self.title_entry.grid(row=0, column=1)                       # Position the title entry

        tk.Label(frame_add, text="Author:").grid(row=1, column=0)    # Label for author
        self.author_entry = tk.Entry(frame_add)                      # Entry field for author
        self.author_entry.grid(row=1, column=1)                      # Position the author entry

        tk.Label(frame_add, text="Category:").grid(row=2, column=0)  # Label for category
        self.category_entry = tk.Entry(frame_add)                    # Entry field for category
        self.category_entry.grid(row=2, column=1)                    # Position the category entry

        tk.Button(frame_add, text="Add Item", command=self.add_item).grid(row=3, columnspan=2, pady=5)  # Button to add item

        # Check Out Frame
        frame_checkout = tk.Frame(self.root)       # Creating a frame for checking out items
        frame_checkout.pack(pady=10)               # vertical padding

        tk.Label(frame_checkout, text="Checkout Title:").grid(row=0, column=0)      # Label for checkout title
        self.checkout_entry = tk.Entry(frame_checkout)                              # Entry field for checkout title
        self.checkout_entry.grid(row=0, column=1)                                   # Position the checkout entry

        tk.Button(frame_checkout, text="Check Out", command=self.check_out_item).grid(row=1, columnspan=2, pady=5)  # Button to check out item

        # Return Frame
        frame_return = tk.Frame(self.root)               # Creating a frame for returning items
        frame_return.pack(pady=10)                       # vertical padding

        tk.Label(frame_return, text="Return Title:").grid(row=0, column=0)               # Label for return title
        self.return_entry = tk.Entry(frame_return)                                       # Entry field for return title
        self.return_entry.grid(row=0, column=1)                                          # Position the return entry

        tk.Button(frame_return, text="Return", command=self.return_item).grid(row=1, columnspan=2, pady=5)  # Button to return item

        # Search Frame
        frame_search = tk.Frame(self.root)  # Create a frame for searching items
        frame_search.pack(pady=10)          # Pack the frame with some vertical padding

        tk.Label(frame_search, text="Search:").grid(row=0, column=0)  # Label for search
        self.search_entry = tk.Entry(frame_search)                    # Entry field for search
        self.search_entry.grid(row=0, column=1)                       # Position the search entry

        tk.Button(frame_search, text="Search", command=self.search_items).grid(row=1, columnspan=2, pady=5)  # Button to search items

        # Results Area
        self.results_text = tk.Text(self.root, width=50, height=10)  # Text widget to display search results
        self.results_text.pack(pady=10)                              # Pack the text widget with some vertical padding

    def add_item(self):
        title = self.title_entry.get()             # Get the title from the entry
        author = self.author_entry.get()           # Get the author from the entry
        category = self.category_entry.get()       # Get the category from the entry

        if title and author and category:          # Check if all fields are filled
            item = LibraryItem(title, author, category)  # Create a new LibraryItem
            self.library.add_item(item)                  # Add the item to the library
            messagebox.showinfo("Success", f"Added: {item}")  # Show success message
            self.clear_entries()                              # Clear the entry fields
        else:
            messagebox.showerror("Error", "All fields are required.")  # Show error if fields are empty

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)           # Clear title entry
        self.author_entry.delete(0, tk.END)          # Clear author entry
        self.category_entry.delete(0, tk.END)        # Clear category entry
        self.checkout_entry.delete(0, tk.END)        # Clear checkout entry
        self.return_entry.delete(0, tk.END)          # Clear return entry
        self.search_entry.delete(0, tk.END)          # Clear search entry

    def check_out_item(self):
        title = self.checkout_entry.get()           # Get the title to check out
        item = self.library.check_out_item(title)   # Attempt to check out the item

        if item:                # If item was successfully checked out
            messagebox.showinfo("Success", f"Checked out: {item.title}")  # Show success message
        else:
            messagebox.showerror("Error", "Item not available for checkout.")  # Show error if not available

    def return_item(self):
        title = self.return_entry.get()               # Get the title to return
        item, fine = self.library.return_item(title)  # Attempt to return the item and get fine

        if item: 
            messagebox.showinfo("Success", f"Returned: {item.title}. Fine: ${fine:.2f}")
        else:
            messagebox.showerror("Error", "Item not found or not checked out.")

    def search_items(self):
        search_term = self.search_entry.get()
        results = self.library.search_items(search_term)

        self.results_text.delete(1.0, tk.END)  # Clear previous results
        if results:
            for item in results:
                self.results_text.insert(tk.END, str(item) + "\n")
        else:
            self.results_text.insert(tk.END, "No items found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
