
print(r"""
    

                                                                      
                                                                      
________  _______ __________ ____  __.__      ____________________ 
\______ \ \   _  \\______   \    |/ _/  \    /  \_____  \______   \
 |    |  \/  /_\  \|       _/      < \   \/\/   / _(__  <|    |  _/
 |    `   \  \_/   \    |   \    |  \ \        / /       \    |   \
/_______  /\_____  /____|_  /____|__ \ \__/\  / /______  /______  /
        \/       \/       \/        \/      \/         \/       \/                                

                 All your OSINT links in one place
                         by Wali & Subhan                             
                                                                      

""")


import search_links, facebook, x, linkedin, instagram, github, communities, emailaddresses, usernames, documents, images

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
            
def show_linkedin_menu():
    while True:
        print("\n====== LinkedIn ======")
        print("1. Username")
        print("2. Company")
        print("3. Keywords")
        print("4. Post URL")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            uname = input("Enter LinkedIn username: ")
            links = linkedin.li_profile_links(uname)

        elif choice == "2":
            cname = input("Enter Company name: ")
            links = linkedin.li_company_links(cname)

        elif choice == "3":
            term = input("Enter search keyword: ")
            links = linkedin.li_search_links(term)

        elif choice == "4":
            post_url = input("Enter LinkedIn post URL: ")
            links = linkedin.linkedin_post_upload_date(post_url)

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
            continue

        print("\n====== Generated Links ======")
        for name, url in links.items():
            print(f"[+] {name:<25} {url}")

def show_github_menu():
    while True:
        print("\n====== GitHub ======")
        print("1. Username")
        print("2. Repository")
        print("3. Keyword")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter GitHub username: ").strip()
            links = github.gh_user_links(username)

        elif choice == "2":
            owner = input("Enter repo owner (username/org): ").strip()
            repo = input("Enter repo name: ").strip()
            links = github.gh_repo_links(owner, repo)

        elif choice == "3":
            term = input("Enter search term: ").strip()
            links = github.gh_search_links(term)

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
            continue

        print("\n====== Generated Links ======")
        for name, url in links.items():
            print(f"[+] {name:<25} {url}")

def show_instagram_menu():
    while True:
        print("\n====== Instagram ======")
        print("1. Username")
        print("2. IG User ID")
        print("3. Username + Search Terms")
        print("4. Usernames")
        print("5. Search Terms")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter Instagram username: ")
            links = instagram.instagram_username_links(username)
        elif choice == "2":
            user_id = input("Enter Instagram User ID: ")
            links = instagram.instagram_user_id_links(user_id)
        elif choice == "3":
            username = input("Enter Instagram username: ")
            term = input("Enter search terms: ")
            links = instagram.instagram_username_term_links(username, term)
        elif choice == "4":
            username1 = input("Enter first Instagram username: ")
            username2 = input("Enter second Instagram username: ")
            links = instagram.instagram_username_association_links(username1, username2)
        elif choice == "5":
            term = input("Enter search terms: ")
            links = instagram.instagram_term_only_links(term)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            continue

        print("\n====== Generated Links ======")
        for name, url in links.items():
            print(f"[+] {name:<25} {url}")

def show_communities_menu():
    while True:
        print("\n====== Communities ======")
        print("1. Username")
        print("2. Search Terms")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            links = communities.community_user_links(username)
        elif choice == "2":
            term = input("Enter search terms: ")
            links = communities.community_search_links(term)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            continue

        print("\n====== Generated Links ======")
        for community, urls in links.items():
            print(f"\n====== {community} ======")
            for name, url in urls.items():
                print(f"[+] {name:<25} {url}")


def show_images_menu():
    while True:
        print("\n====== Images ======")
        print("1. Reverse Image Search")
        print("2. Images Search")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            image_url = input("Enter image URL: ")
            results = images.reverse_image_search(image_url)
        elif choice == "2":
            term = input("Enter search term: ")
            results = images.image_keyword_search(term)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")
            continue

        for category, links in results.items():
            print(f"\n====== {category} ======")
            for name, url in links.items():
                print(f"[+] {name:<25} {url}")


def main():
    while True:
        print("\n====== Main Menu ======")
        print("1. Search Engines")
        print("2. Facebook")
        print("3. X")
        print("4. Linkedin")
        print("5. Instagram")
        print("6. GitHub")
        print("7. Communities")
        print("8. Emails")
        print("9. Usernames")
        print("10. Documents")
        print("11. Images")
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
            
        elif choice == "4":
            show_linkedin_menu()
            
        elif choice == "5":
            show_instagram_menu()

        elif choice == "6":
            show_github_menu()

        elif choice == "7":
            show_communities_menu()
            
        elif choice == "8":
            email = input("Enter email address: ")
            links = emailaddresses.email_osint_links(email)
            print("\n====== Generated Links ======")
            for name, url in links["Email OSINT"].items():
                print(f"[+] {name:<25} {url}")
            
        elif choice == "9":
            uname = input("Enter username: ").strip()
            if not uname:
                print("Empty username. Try again.")
                continue

            results = usernames.username_osint_links(uname)
            if "error" in results:
                print("Error:", results["error"])
                continue

            print(f"\n=== Generated Links ===")
            for site in sorted(results.keys()):
                print(f"[+] {site:<25} {results[site]}")

        elif choice == "10":
            term = input("Enter search terms: ")
            links = documents.document_links(term)
            print("\n====== Generated Links ======")
            for name, url in links["Documents"].items():
                print(f"[+] {name:<25} {url}")

        elif choice == "11":
            show_images_menu()

        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass  
