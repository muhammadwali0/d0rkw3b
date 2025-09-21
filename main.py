
print(r"""
    

                                                                      
                                                                      
________  _______ __________ ____  __.__      ____________________ 
\______ \ \   _  \\______   \    |/ _/  \    /  \_____  \______   \
 |    |  \/  /_\  \|       _/      < \   \/\/   / _(__  <|    |  _/
 |    `   \  \_/   \    |   \    |  \ \        / /       \    |   \
/_______  /\_____  /____|_  /____|__ \ \__/\  / /______  /______  /
        \/       \/       \/        \/      \/         \/       \/                                

                All your OSINT links in one place
                        by Muhammad Wali                               
                                                                      

""")

import search_links
import facebook
import x

def show_facebook_menu():
    while True:
        print("\n====== Facebook ======")
        print("1. FB Username")
        print("2. FB Number")
        print("3. Search Terms")
        print("4. Facebook User ID")
        print("5. Facebook Location ID")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter Facebook username: ")
            links = facebook.fb_username_links(username)
        elif choice == "2":
            number = input("Enter Facebook phone number: ")
            links = facebook.fb_number_links(number)
        elif choice == "3":
            term = input("Enter search terms: ")
            links = facebook.fb_search_term_links(term)
        elif choice == "4":
            user_id = input("Enter Facebook user ID: ")
            links = facebook.fb_user_id_links(user_id)
        elif choice == "5":
            location_id = input("Enter Facebook location ID: ")
            links = facebook.fb_location_links(location_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            continue

        print("\n====== Generated Links ======")
        for name, url in links.items():
            print(f"[+] {name:<25} {url}")

def show_x_menu():
    while True:
        print("\n====== X ======")
        print("1. Username")
        print("2. Username by Year")
        print("3. X User ID")
        print("4. Real Name")
        print("5. List Number")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter X username: ")
            links = x.x_username_links(username)
        elif choice == "2":
            username = input("Enter X username: ")
            year = input("Enter year (e.g. 2024): ")
            links = x.x_username_by_year(username, year)
        elif choice == "3":
            user_id = input("Enter X user ID: ")
            links = x.x_user_id_links(user_id)
        elif choice == "4":
            name = input("Enter real name: ")
            links = x.x_real_name_links(name)
        elif choice == "5":
            list_id = input("Enter list ID: ")
            links = x.x_list_links(list_id)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            continue

        print("\n====== Generated Links ======")
        for name, url in links.items():
            print(f"[+] {name:<25} {url}")

def main():
    while True:
        print("\n====== Main Menu ======")
        print("1. Search Engines")
        print("2. Facebook")
        print("3. X")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            search_terms = input("Enter search terms: ")
            engines, tor_engines = search_links.generate_links(search_terms)

            print("\n====== Clear Web Search Engines ======")
            for name, url in engines.items():
                print(f"[+] {name:<15} {url}")

            print("\n====== Tor Links ======")
            for name, url in tor_engines.items():
                print(f"[+] {name:<15} {url}")

        elif choice == "2":
            show_facebook_menu()

        elif choice == "3":
            show_x_menu()

        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass  
