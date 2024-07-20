import requests
from bs4 import BeautifulSoup
import re
import PyPDF2
import urllib.parse
import urllib3
import colorama
import pyshorteners
import os
import time
import fade
import sys
import os
import colorama
colorama.init(autoreset=True)
from colorama import Fore, Style, Back

def clear_screen():
    # Clear screen for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear screen for Linux and macOS
    else:
        os.system('clear')

def press_any_key_to_continue():
    print(Back.CYAN + Fore.RED + "Press any key to continue...")
    
    try:
        # for Windows
        import msvcrt
        msvcrt.getch()
    except ImportError:
        # for Unix-like systems (Linux, macOS)
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def setup_project():
    current_dir = os.getcwd()
    templates_path = os.path.join(current_dir, 'templates')

    if not os.path.exists(templates_path):
        os.makedirs(templates_path)
        print(f"Created 'templates' folder at {templates_path}")
    else:
        print(f"'templates' folder already exists at {templates_path}")

    library_path = os.path.join(current_dir, 'library')

    if not os.path.exists(library_path):
        os.makedirs(library_path)
        print(f"Created 'library' folder at {library_path}")
    else:
        print(f"'library' folder already exists at {library_path}")

    # Your library creation code goes here
class EvilEbookSearch:
    def __init__(self):
        # Disable SSL warnings
        urllib3.disable_warnings()
        # Initialize colorama for colored console output
        # Lists to store URLs
        self.filtered_urls = []
        self.verified_urls = []

    def extract_url(self, input_string):
        # Extract URL from Google search result
        regex = r"/url\?q=(.*?)&sa="
        match = re.search(regex, input_string)
        if match:
            url = match.group(1)
            url = url.replace("%25", "%")
            return url
        else:
            return None

    def check_site_connection(self, site):
        # Check if a site is accessible
        try:
            if requests.get(site, verify=False, timeout=3).status_code == 200:
                return True
            else:
                return False
        except:
            return False

    def shorten_url(self, site):
        # Shorten URL using pyshorteners
        type_tiny = pyshorteners.Shortener()
        short_url = type_tiny.tinyurl.short(site)
        return short_url

    def search_books(self, query):
        # Search for PDF links related to the given query
        page = requests.get("https://www.google.dz/search?q=" + urllib.parse.quote_plus(query) + "+type=pdf", timeout=3)
        soup = BeautifulSoup(page.content, features="html.parser")
        links = soup.findAll("a")
        
        for i in links:
            urls = i.get("href")
            if ".pdf" in urls:
                self.filtered_urls.append(str(self.extract_url(urls)))

    def get_pdf_title(self, pdf_url):
        # Get the title and number of pages from a PDF
        try:
            response = requests.get(pdf_url, timeout=3, verify=False)
            with open("temp.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)

            with open("temp.pdf", "rb") as pdf_document:
                pdf_reader = PyPDF2.PdfReader(pdf_document)
                title = pdf_reader.metadata.title
                pages = len(pdf_reader.pages)

            os.remove("temp.pdf")
            return [str(title), pages]
        except:
            return ["None", "Unknown"]

    def display_results(self, query):  # Add 'query' as a parameter
        # Display search results with verified connections
        results = len(self.verified_urls)
        choices = []

        for i in range(results):
            choices.append(i)

        if results == 0:
            print(colorama.Fore.RED + f"NO RESULTS FOUND for {query.upper()}" + colorama.Fore.RESET)
        else:
            print("\n")
            print(colorama.Fore.GREEN + f"Total PDF Book Links Found For {query.upper()}" + colorama.Fore.RESET)
            list_choice = 0
            for book in self.verified_urls:
                try:
                    newlink = str(self.shorten_url(book))
                except:
                    newlink = str(book)
                r = self.get_pdf_title(book)
                t = ""
                t = book
                choices[list_choice] = [t, r[0], r[1]]
                print("[" + str(list_choice) + "] " + colorama.Fore.GREEN + "Verified Connection: " +
                      colorama.Fore.RESET + newlink + " | Title: " + str(r[0]) + " | Pages: " + str(r[1]))
                list_choice += 1

    def download_pdf(self, pdf_url, series_name):
        # Download PDF file and save to the specified directory structure
        try:
            response = requests.get(pdf_url, timeout=5)
            title, _ = self.get_pdf_title(pdf_url)
            
            # Create library directory if not exists
            library_dir = "./library/"
            if not os.path.exists(library_dir):
                os.makedirs(library_dir)

            # Create series folder if not exists
            series_dir = os.path.join(library_dir, series_name)
            if not os.path.exists(series_dir):
                os.makedirs(series_dir)

            # Save PDF file in series folder with title as filename
            filename = os.path.join(series_dir, f"{title}.pdf")
            with open(filename, "wb") as pdf_file:
                pdf_file.write(response.content)
            return filename
        except:
            return None

    def run(self):
        while True:
            self.verified_urls = []
            self.filtered_urls = []
            clear_screen()
            # Start menu with ASCII logo and purple fade
            logo = """
▓█████ ██▒   █▓ ██▓ ██▓    ▓█████  ▄▄▄▄    ▒█████   ▒█████   ██ ▄█▀
▓█   ▀▓██░   █▒▓██▒▓██▒    ▓█   ▀ ▓█████▄ ▒██▒  ██▒▒██▒  ██▒ ██▄█▒ 
▒███   ▓██  █▒░▒██▒▒██░    ▒███   ▒██▒ ▄██▒██░  ██▒▒██░  ██▒▓███▄░ 
▒▓█  ▄  ▒██ █░░░██░▒██░    ▒▓█  ▄ ▒██░█▀  ▒██   ██░▒██   ██░▓██ █▄ 
░▒████▒  ▒▀█░  ░██░░██████▒░▒████▒░▓█  ▀█▓░ ████▓▒░░ ████▓▒░▒██▒ █▄
░░ ▒░ ░  ░ ▐░  ░▓  ░ ▒░▓  ░░░ ▒░ ░░▒▓███▀▒░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▒ ▓▒
 ░ ░  ░  ░ ░░   ▒ ░░ ░ ▒  ░ ░ ░  ░▒░▒   ░   ░ ▒ ▒░   ░ ▒ ▒░ ░ ░▒ ▒░
   ░       ░░   ▒ ░  ░ ░      ░    ░    ░ ░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░░ ░ 
   ░  ░     ░   ░      ░  ░   ░  ░ ░          ░ ░      ░ ░  ░  ░   
           ░                            ░                          
        Original By DEA"""
            print(fade.purplepink(logo))
            print(fade.purplepink("[1] Download Ebook\n[2] Run Library\n[3] Show Author\n[4] Exit"))
            texter = Fore.MAGENTA + "[$](EvilEbook)~>"
            choice = input(texter)

            if choice == '1':
                clear_screen()
                query = input("Enter Book>>>")

                self.search_books(query)

                if not self.filtered_urls:
                    print(colorama.Fore.RED + "No PDF links found for the given query." + colorama.Fore.RESET)
                else:
                    print(colorama.Fore.GREEN + f"Found Book PDF Links For {query.upper()}" + colorama.Fore.RESET)
                    print(colorama.Fore.GREEN + "Checking Connections To Servers" + colorama.Fore.RESET)
                    amount = len(self.filtered_urls)
                    counter = 1
                    for x in self.filtered_urls:
                        clear_screen()
                        print(colorama.Fore.GREEN + f"Found Book PDF Links For {query.upper()}" + colorama.Fore.RESET)
                        print(colorama.Fore.GREEN + "Checking Connections To Servers" + colorama.Fore.RESET)
                        print(str(counter) + "/" + str(amount) + " Found EBooks")
                        for i in range(counter):
                            print(colorama.Fore.GREEN + "Found A Clean Connection" + colorama.Fore.RESET)
                        if self.check_site_connection(x):
                            self.verified_urls.append(x)
                        counter += 1

                    self.display_results(query)  # Pass query to display_results

                    download = input("Would you like to download one(y/n)>>>")
                    if download.lower() == "y":
                        chs = input("Enter The Number Of The Book You Want To Download>>>")
                        try:
                            chs = int(chs)
                            if 0 <= chs < len(self.verified_urls):
                                series_name = input("Enter Series Name>>>")
                                print("Downloading...")
                                try:
                                    downloaded_file = self.download_pdf(self.verified_urls[chs], series_name)
                                    if downloaded_file:
                                        print(f"Download Success! Book saved at: {downloaded_file}")
                                    else:
                                        print("ERROR! Download Failed")
                                except Exception as e:
                                    print(f"ERROR! Download Failed: {e}")
                            else:
                                print("ERROR! Invalid Book Number")
                        except ValueError:
                            print("ERROR! Not a Valid Number")
                    else:
                        print("Thanks For Using EvilEbook")
            elif choice == '2':
                clear_screen()
                try:
                    import sys
                    import subprocess
                    import base64
                    print("Press Ctrl + C To Stop")
                    with open("./app.py", "w") as f:
                        f.write(base64.b64decode("ZnJvbSBmbGFzayBpbXBvcnQgRmxhc2ssIHJlbmRlcl90ZW1wbGF0ZSwgc2VuZF9maWxlCmltcG9ydCBvcwppbXBvcnQgcmFuZG9tCmZyb20gUHlQREYyIGltcG9ydCBQZGZSZWFkZXIKaW1wb3J0IHJlCgphcHAgPSBGbGFzayhfX25hbWVfXykKCmRlZiBnZXRfYm9va3MoKToKICAgIGJvb2tzID0gW10gCiAgICBmb3Igc2VyaWVzIGluIG9zLmxpc3RkaXIoJ2xpYnJhcnknKToKICAgICAgICBpZiBvcy5wYXRoLmlzZGlyKG9zLnBhdGguam9pbignbGlicmFyeScsIHNlcmllcykpOgogICAgICAgICAgICBmb3IgYm9vayBpbiBvcy5saXN0ZGlyKG9zLnBhdGguam9pbignbGlicmFyeScsIHNlcmllcykpOgogICAgICAgICAgICAgICAgaWYgYm9vay5lbmRzd2l0aCgnLnBkZicpOgogICAgICAgICAgICAgICAgICAgIGZpbGVuYW1lID0gb3MucGF0aC5zcGxpdGV4dChib29rKVswXSAgIyByZW1vdmUgLnBkZiBleHRlbnNpb24KICAgICAgICAgICAgICAgICAgICB0aXRsZSA9IHJlLnN1YihyJ15Cb29rXGQrJywgJycsIHN0cihmaWxlbmFtZSkpCiAgICAgICAgICAgICAgICAgICAgdGl0bGUgPSB0aXRsZS5yZXBsYWNlKCItIiwgIiAiKQogICAgICAgICAgICAgICAgICAgIGlmIGxlbih0aXRsZSkgPiAyMzoKICAgICAgICAgICAgICAgICAgICAgICAgdGl0bGUgPSB0aXRsZS5zdHJpcCgpWzoyM10gKyAnLi4uJyAgIyByZW1vdmUgIkJvb2siIGZvbGxvd2VkIGJ5IGEgbnVtYmVyCiAgICAgICAgICAgICAgICAgICAgcGF0aCA9IG9zLnBhdGguam9pbignbGlicmFyeScsIHNlcmllcywgYm9vaykKICAgICAgICAgICAgICAgICAgICBpZiAiQm9vayIgaW4gc3RyKHRpdGxlKToKICAgICAgICAgICAgICAgICAgICAgICAgcGFzcwogICAgICAgICAgICAgICAgICAgIGJvb2tzLmFwcGVuZCh7CiAgICAgICAgICAgICAgICAgICAgICAgICd0aXRsZSc6IHRpdGxlLAogICAgICAgICAgICAgICAgICAgICAgICAnc2VyaWVzJzogc2VyaWVzLAogICAgICAgICAgICAgICAgICAgICAgICAnYm9vayc6IGJvb2ssCiAgICAgICAgICAgICAgICAgICAgICAgICdwcmV2aWV3JzogcmFuZG9tX2NvbG9yKCkKICAgICAgICAgICAgICAgICAgICB9KQogICAgcmV0dXJuIGJvb2tzCgoKCgppbXBvcnQgcmFuZG9tCgpkZWYgcmFuZG9tX2NvbG9yKCk6CiAgICAjIEdlbmVyYXRlIGEgcmFuZG9tIGNvbG9yIGdyYWRpZW50CiAgICByMSwgZzEsIGIxID0gW3JhbmRvbS5yYW5kaW50KDU0LCAyMDApIGZvciBfIGluIHJhbmdlKDMpXSAgIyBsaW1pdHMgYnJpZ2h0bmVzcyB0byBhIHJhbmdlIG9mIDU0LTIwMAogICAgcjIsIGcyLCBiMiA9IFtyYW5kb20ucmFuZGludCg1NCwgMjAwKSBmb3IgXyBpbiByYW5nZSgzKV0KICAgIHJldHVybiBmImxpbmVhci1ncmFkaWVudCh0byByaWdodCwgcmdiYSh7cjF9LCB7ZzF9LCB7YjF9LCAxKSwgcmdiYSh7cjJ9LCB7ZzJ9LCB7YjJ9LCAxKSkiCgoKQGFwcC5yb3V0ZSgnLycpCmRlZiBpbmRleCgpOgogICAgYm9va3MgPSBnZXRfYm9va3MoKQogICAgcmV0dXJuIHJlbmRlcl90ZW1wbGF0ZSgnaW5kZXguaHRtbCcsIGJvb2tzPWJvb2tzKQoKQGFwcC5yb3V0ZSgnL3JlYWQvPHNlcmllcz4vPGJvb2s+JykKZGVmIHJlYWRfYm9vayhzZXJpZXMsIGJvb2spOgogICAgcGF0aCA9IG9zLnBhdGguam9pbignbGlicmFyeScsIHNlcmllcywgYm9vaykKICAgIHJldHVybiBzZW5kX2ZpbGUocGF0aCwgZG93bmxvYWRfbmFtZT1ib29rLCBhc19hdHRhY2htZW50PUZhbHNlKQoKaWYgX19uYW1lX18gPT0gJ19fbWFpbl9fJzoKICAgIGFwcC5ydW4oZGVidWc9RmFsc2UsIGhvc3Q9IjAuMC4wLjAiKQo=").decode("utf-8"))
                        f.close()
                    setup_project()
                    with open("./templates/index.html", "w") as f:
                        f.write(base64.b64decode("PCFET0NUWVBFIGh0bWw+CjxodG1sPgogIDxoZWFkPgogICAgPG1ldGEgY2hhcnNldD0idXRmLTgiPgogICAgPHRpdGxlPkxpYnJhcnk8L3RpdGxlPgogICAgPHNjcmlwdCBzcmM9Imh0dHBzOi8va2l0LmZvbnRhd2Vzb21lLmNvbS9hY2Y2OTE5MTRmLmpzIiBjcm9zc29yaWdpbj0iYW5vbnltb3VzIj48L3NjcmlwdD4KICAgIDxzdHlsZT4KICAgICAgLyogU2Nyb2xsIGJhciBzdHlsZSAqLwo6Oi13ZWJraXQtc2Nyb2xsYmFyIHsKICB3aWR0aDogMTNweDsKfQoKOjotd2Via2l0LXNjcm9sbGJhci10cmFjayB7CiAgYmFja2dyb3VuZDogIzJmMzEzNjsKICBib3JkZXItcmFkaXVzOiAxMHB4Owp9Cgo6Oi13ZWJraXQtc2Nyb2xsYmFyLXRodW1iIHsKICBiYWNrZ3JvdW5kLWNvbG9yOiAjNzI4OWRhOwogIGJvcmRlci1yYWRpdXM6IDEwcHg7CiAgYm9yZGVyOiAycHggc29saWQgIzJmMzEzNjsKfQoKOjotd2Via2l0LXNjcm9sbGJhci10aHVtYjpob3ZlciB7CiAgYmFja2dyb3VuZC1jb2xvcjogIzcyODlkYTsKfQoKI3Njcm9sbC10by10b3AgewogIGRpc3BsYXk6IG5vbmU7CiAgcG9zaXRpb246IGZpeGVkOwogIGJvdHRvbTogMjBweDsKICByaWdodDogMzBweDsKICB6LWluZGV4OiA5OTsKICBmb250LXNpemU6IDE4cHg7CiAgYm9yZGVyOiBub25lOwogIG91dGxpbmU6IG5vbmU7CiAgYmFja2dyb3VuZC1jb2xvcjogIzcyODlkYTsKICBjb2xvcjogI2ZmZjsKICBjdXJzb3I6IHBvaW50ZXI7CiAgcGFkZGluZzogMTVweDsKICBib3JkZXItcmFkaXVzOiAxMHB4OwogIGZvbnQtZmFtaWx5OiBzYW5zLXNlcmlmOwogIHRleHQtYWxpZ246IGNlbnRlcjsKICBib3gtc2hhZG93OiAwcHggMnB4IDVweCByZ2JhKDAsIDAsIDAsIDAuNSk7Cn0KCgoKI3Njcm9sbC10by10b3A6aG92ZXIgewogIGJhY2tncm91bmQtY29sb3I6ICM2NzdiYzQ7Cn0KCiNzY3JvbGwtdG8tdG9wLWljb24gewogIGZvbnQtZmFtaWx5OiAiRm9udCBBd2Vzb21lIDUgRnJlZSI7CiAgZm9udC13ZWlnaHQ6IDkwMDsKfQoKI3Njcm9sbC10by10b3Auc2hvdyB7CiAgZGlzcGxheTogYmxvY2s7Cn0KICAgICAgYm9keSB7CiAgICAgICAgZm9udC1mYW1pbHk6IHNhbnMtc2VyaWY7CiAgICAgICAgYmFja2dyb3VuZC1jb2xvcjogIzM2MzkzZjsKICAgICAgICBtYXJnaW46IDA7CiAgICAgICAgcGFkZGluZzogMDsKICAgICAgfQoKICAgICAgLmNvbnRhaW5lciB7CiAgICAgICAgZGlzcGxheTogZmxleDsKICAgICAgICBmbGV4LXdyYXA6IHdyYXA7CiAgICAgICAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7CiAgICAgICAgZ2FwOiAycmVtOwogICAgICAgIHBhZGRpbmc6IDJyZW07CiAgICAgIH0KCiAgICAgIC5ib29rIHsKICAgICAgICB3aWR0aDogMjAwcHg7CiAgICAgICAgaGVpZ2h0OiAzMDBweDsKICAgICAgICBib3JkZXItcmFkaXVzOiAxMHB4OwogICAgICAgIHBvc2l0aW9uOiByZWxhdGl2ZTsKICAgICAgICBvdmVyZmxvdzogaGlkZGVuOwogICAgICB9CgogICAgICAuYm9vazpiZWZvcmUgewogICAgICAgIGNvbnRlbnQ6ICIiOwogICAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTsKICAgICAgICB0b3A6IDA7CiAgICAgICAgbGVmdDogMDsKICAgICAgICByaWdodDogMDsKICAgICAgICBib3R0b206IDA7CiAgICAgICAgYmFja2dyb3VuZC1pbWFnZTogdmFyKC0tZ3JhZGllbnQpOwogICAgICAgIGJhY2tncm91bmQtc2l6ZTogY292ZXI7CiAgICAgICAgYmFja2dyb3VuZC1wb3NpdGlvbjogY2VudGVyIGNlbnRlcjsKICAgICAgICB6LWluZGV4OiAtMTsKICAgICAgICAKICAgICAgfQoKICAgICAgLmJvb2s6YWZ0ZXIgewogICAgICAgIGNvbnRlbnQ6ICIiOwogICAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTsKICAgICAgICBib3R0b206IDA7CiAgICAgICAgbGVmdDogMDsKICAgICAgICByaWdodDogMDsKICAgICAgICBoZWlnaHQ6IDEwMHB4OwogICAgICAgIGJhY2tncm91bmQtY29sb3I6IHJnYmEoMjU1LCAyNTUsIDI1NSwgMC41Mik7CiAgICAgICAgYmFja2Ryb3AtZmlsdGVyOiBibHVyKDEwcHgpOwogICAgICAgIHotaW5kZXg6IDI7CiAgICAgIH0KCiAgICAgIC5ib29rIGgyIHsKICAgICAgICBmb250LXNpemU6IDEuNXJlbTsKICAgICAgICBjb2xvcjogIzhlNTRlOTsKICAgICAgICBtYXJnaW46IDA7CiAgICAgICAgcGFkZGluZzogMC41cmVtOwogICAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTsKICAgICAgICB0b3A6IDIwMHB4OwogICAgICAgIGxlZnQ6IDA7CiAgICAgICAgcmlnaHQ6IDA7CiAgICAgICAgei1pbmRleDogMzsKICAgICAgICB0ZXh0LWFsaWduOiBjZW50ZXI7CiAgICAgICAgCiAgICAgIH0KCiAgICAgIC5ib29rIGgzIHsKICAgICAgICBmb250LXNpemU6IDAuOHJlbTsKICAgICAgICBjb2xvcjogIzhlNTRlOTsKICAgICAgICBtYXJnaW46IDA7CiAgICAgICAgcGFkZGluZzogMC41cmVtOwogICAgICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTsKICAgICAgICBib3R0b206IDA7CiAgICAgICAgbGVmdDogMDsKICAgICAgICByaWdodDogMDsKICAgICAgICB6LWluZGV4OiAzOwogICAgICAgIHRleHQtYWxpZ246IGNlbnRlcjsKICAgICAgfQoKICAgICAgLmJvb2sgYSB7CiAgICAgICAgZGlzcGxheTogYmxvY2s7CiAgICAgICAgaGVpZ2h0OiAxMDAlOwogICAgICAgIHdpZHRoOiAxMDAlOwogICAgICAgIHBvc2l0aW9uOiByZWxhdGl2ZTsKICAgICAgICB6LWluZGV4OiAzOwogICAgICB9CgogICAgICAuYm9vayBhOmhvdmVyOmJlZm9yZSB7CiAgICAgICAgb3BhY2l0eTogMC41OwogICAgICB9CiAgICA8L3N0eWxlPgogIDwvaGVhZD4KICA8Ym9keT4KICAgIDxjZW50ZXI+PGgxIHN0eWxlPSJmb250LXNpemU6IDQwcHg7IGNvbG9yOiAjOGU1NGU5OyI+WW91ciBEb3dubG9hZGVkIEJvb2tzPC9oMT48L2NlbnRlcj4KICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgIHslIGZvciBib29rIGluIGJvb2tzICV9CiAgICAgICAgPGRpdiBjbGFzcz0iYm9vayIgc3R5bGU9Ii0tZ3JhZGllbnQ6IHt7IGJvb2sucHJldmlldyB9fTsiPgogICAgICAgICAgPGEgaHJlZj0ie3sgdXJsX2ZvcigncmVhZF9ib29rJywgc2VyaWVzPWJvb2suc2VyaWVzLCBib29rPWJvb2suYm9vaykgfX0iPgogICAgICAgICAgICA8aDIgY2xhc3M9ImJvb2stdGl0bGUiPnt7IGJvb2sudGl0bGUgfX08L2gyPgogICAgICAgICAgICA8aDMgY2xhc3M9ImJvb2stc2VyaWVzIj57eyBib29rLnNlcmllcyB9fTwvaDM+CiAgICAgICAgICA8L2E+CiAgICAgICAgPC9kaXY+CiAgICAgIHslIGVuZGZvciAlfQogICAgPC9kaXY+CiAgICA8YnV0dG9uIGlkPSJzY3JvbGwtdG8tdG9wIiBvbmNsaWNrPSJzY3JvbGxUb1RvcCgpIj4KICAgICAgPHNwYW4gaWQ9InNjcm9sbC10by10b3AtaWNvbiI+PGkgY2xhc3M9ImZhLXNoYXJwIGZhLXNvbGlkIGZhLWFuZ2xlLXVwIj48L2k+PC9zcGFuPgogICAgPC9idXR0b24+CiAgICA8c2NyaXB0Pgpjb25zdCBidXR0b24gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic2Nyb2xsLXRvLXRvcCIpOwoKd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoInNjcm9sbCIsIGZ1bmN0aW9uICgpIHsKICBpZiAod2luZG93LnBhZ2VZT2Zmc2V0ID4gMzAwKSB7CiAgICBidXR0b24uY2xhc3NMaXN0LmFkZCgic2hvdyIpOwogIH0gZWxzZSB7CiAgICBidXR0b24uY2xhc3NMaXN0LnJlbW92ZSgic2hvdyIpOwogIH0KfSk7CgpidXR0b24uYWRkRXZlbnRMaXN0ZW5lcigiY2xpY2siLCBmdW5jdGlvbiAoKSB7CiAgd2luZG93LnNjcm9sbFRvKHsKICAgIHRvcDogMCwKICAgIGJlaGF2aW9yOiAic21vb3RoIiwKICB9KTsKfSk7CgoKICAgIDwvc2NyaXB0PgogIDwvYm9keT4KPC9odG1sPgo=").decode("utf-8"))
                        f.close()
                    py = sys.executable
                    file = os.path.abspath(os.path.join(os.path.dirname(__file__), "app.py"))
                    command = "" + py + ' "' + file + '"'
                    print(command)
                    subprocess.run(command, check=True)
                except KeyboardInterrupt:
                    print("Stopped Live Server")
                    press_any_key_to_continue()
                
            elif choice == '3':
                clear_screen()
                auther = """
• ▌ ▄ ·.  ▄▄▄·▄▄▄▄▄▄▄▄▄ ▄· ▄▌     ▄▄·  ▄▄▄· ▄ •▄ ▄▄▄ ..▄▄ · 
·██ ▐███▪▐█ ▀█•██ •██  ▐█▪██▌    ▐█ ▌▪▐█ ▀█ █▌▄▌▪▀▄.▀·▐█ ▀. 
▐█ ▌▐▌▐█·▄█▀▀█ ▐█.▪▐█.▪▐█▌▐█▪    ██ ▄▄▄█▀▀█ ▐▀▀▄·▐▀▀▪▄▄▀▀▀█▄
██ ██▌▐█▌▐█ ▪▐▌▐█▌·▐█▌· ▐█▀·.    ▐███▌▐█ ▪▐▌▐█.█▌▐█▄▄▌▐█▄▪▐█
▀▀  █▪▀▀▀ ▀  ▀ ▀▀▀ ▀▀▀   ▀ •     ·▀▀▀  ▀  ▀ ·▀  ▀ ▀▀▀  ▀▀▀▀ """
                print(fade.purplepink(auther))
                press_any_key_to_continue()
            elif choice == '4':
                clear_screen()
                print("Exiting EvilEbook. Goodbye!")
                break
                

# Instantiate the EvilEbookSearch class and run the search
evil_ebook_search = EvilEbookSearch()
evil_ebook_search.run()
