"""
Web crawler is a computer program that is used to search and automatically index website content and other information over the internet.
These programs are most commonly used to create entries for a search engine index. 
Here is one of the most basic form of a web crawler, which is finding all the web links referred to by an HTML page recursively."""
"""
Open a terminal on your text editor. 
Move to the location of the file.
Ensure that you have installed all the required libraries beforehand for the proper functioning of the code.
Finally, type the following command on your terminal. 
(Some websites require a certain certificates before getting access to their data. Care has to be taken while choosing the website to be crawled.)
Usage: python main.py -u <complete address of the website to be crawled> -t <depth/threshold of recursiveness>  -o <output file name>
-u: for the URL, If not given then the code will print an error on the command line.
-t: for the threshold of recursiveness. It must be greater than 0. The code gives an error for an invalid threshold.
-o: For an output file. If not provided then by default, the result will be printed on the command line.
"""

# argparse is a powerful library to create command -line interfaces for Python scripts and applications and handling argument parsing.
import argparse

# requests library is widely used for various web-related tasks, including API integration, web scraping and interacting with web services.
import requests

# urllib is useful for tasks involving URL manipulation, data retrieval and web scraping.
from urllib.parse import urlparse, urljoin

# bs4 provides a convenient way to extract data from web pages by navigating the HTML structure and locating specific elements based on their tags, attributes or contents.
from bs4 import BeautifulSoup

# The sys library in Python provides access to some variables and functions that interact with the Python interpreter.
import sys

# The os library in Python provides a way to interact with the operating system and perform various system-related tasks.
import os

# For regular expressions. For working with powerful patterns used to match and manipulate things.
import re


file_counts = {             # a dictionary to store the number of files of each type
    'html': 0,
    'css' : 0,
    'jpg' : 0, 
    'js' : 0
}

links = {}                  # a set to store the links crawled by the program. A list is not used so as to automatically delete same links.

MIN_DEPTH = 1               # defined the Minimum recursive depth which the code should go into

visited_urls = set()        # initialize a set named visited_urls to store all the links that have been crawled and stored by the program.


def is_internal_link(url, base_url):
    """This function checks if the url given as argument is in the domain of the base url. It returns True or False correspondingly."""
    return url.startswith(base_url)


def scrape(site, depth, base_url):
    """This is the main recursive function controlling the program."""
    
    if depth < MIN_DEPTH:           # If depth==0 satisfies, we will stop the recursion as we have moved to the desired depth.
        return
    # Print statements to enhance the beauty of the output to be produced.
    
    print(f"At recursion level {depth}:")
    print("Crawling:", site)
    print("-" * 30)
    
    # The code for requesting the access to the site. This is embedded in a try-exception block.
    try:
        r = requests.get(site)
    except requests.exceptions.RequestException:
        #Certain sites require the use of security certificates to their file. On crawling such links, the code will keep running but will produce an error message, so that user can get insights from it.
        print("Error occurred while crawling:", site)
        print("-" * 30)
        return
    
    # This line is creating a BeautifulSoup object named s by parsing the HTML content of the response obtained from the requests.get() method.
    s = BeautifulSoup(r.text, "html.parser")
    
    # The dictionary variable file_counts_local stores the number of files of each type. It is a local variable and so is created whenever the function is called.
    file_counts_local = {
        'html':0,
        'css':0,
        'jpg':0,
        'js':0
    }
    
    # This is also a local variable list storing the links of this function call.
    links_local = []
    
    for i in s.find_all("a"):
        # This will search for the a href tag in the html code.
        if 'href' in i.attrs:
            # Checks if the <a> tag has the attribute href and retrieves the value of the 'href' attribute and assigns it to the variable 'href'.
            href = i.attrs['href']
            link = urljoin(site, href)      # Will join the base site and the relative url.
            if link not in visited_urls:
                # Checking the presence of the url in the set visited_urls to avoid processing the same url multiple times.
                visited_urls.add(link)
                print(link)
                links_local.append(link)            # Appends the link to the local list created earlier.
    
    for img in s.find_all("img"):
        # Checks for the img tag.
        if 'src' in img.attrs:
            # Check for the presence of the src attribute in the img tag and stores it in the src variable.
            src = img.attrs['src']
            link = urljoin(site, src)
            if link not in visited_urls:
                visited_urls.add(link)
                print(link)
    
    # Code for <link> tags (CSS stylesheets)
    for i in s.find_all("link"):
        if 'href' in i.attrs:
            href = i.attrs['href']
            link = urljoin(site, href)
            if link not in visited_urls:
                visited_urls.add(link)
                print(link)
                links_local.append(link)

    # This will search for javascript links.
    for i in s.find_all("script"):
        if 'src' in i.attrs:
            src = i.attrs['src']
            link = urljoin(site, src)
            if link not in visited_urls:
                visited_urls.add(link)
                print(link)
                links_local.append(link)
    
    # This will search for internal css style sheets.
    for i in s.find_all("style"):
        style_content = i.string
        if style_content:
            css_urls = re.findall(r'url\((.*?)\)', style_content)
            for css_url in css_urls:
                link = urljoin(site, css_url)
                if link not in visited_urls:
                    visited_urls.add(link)
                    print(link)
                    links_local.append(link)
    
    # Code for <video> tags
    for i in s.find_all("video"):
        if 'src' in i.attrs:
            src = i.attrs['src']
            link = urljoin(site, src)
            if link not in visited_urls:
                visited_urls.add(link)
                print(link)
                links_local.append(link)

    # Code for <audio> tags
    for i in s.find_all("audio"):
        if 'src' in i.attrs:
            src = i.attrs['src']
            link = urljoin(site, src)
            if link not in visited_urls:
                visited_urls.add(link)
                print(link)
                links_local.append(link)   


    # This will loop through all the links and then update the arrray file_counts and file_counts_local.
    for link in links_local:
        extension = os.path.splitext(link)[1][1:]
        if extension in file_counts:
            file_counts[extension] += 1
            file_counts_local[extension] += 1
    
    # This will update the links list for the current recursive depth.
    links[depth] = links_local

    # This will print the total number of files found for the array.
    print("Total files found:", sum(file_counts_local.values()))

    # This part of the code will print additional information for the website. Corresponding to each extension, it will print the count and links associated.
    for extension, count in file_counts_local.items():
        if count > 0:
            print(f"{extension.upper()}: {count}")
            for link in links_local:
                if os.path.splitext(link)[1][1:] == extension:
                    print(link)
    print("\n")

    # This part of the code checks if the link is internal or not. If it is, then it will recursively call the function on that link with the depth decreased by one.
    for link in links_local:
        if is_internal_link(link, base_url):
            scrape(link, depth -1, base_url)


# This part of the code is to comprehend the command line argument using a python library.
# Creates an argument parser object named parser with the description "Web Crawler"
parser = argparse.ArgumentParser(description="Web Crawler")

# Adds an argument -u or --url to the parser. It specifies that the argument should be a string representing the website URL. The help parameter provides a description of the argument.
parser.add_argument("-u", "--url", type=str, help="Website URL")

# Adds an argument -t or --threshold to the parser. It specifies that the argument should be an integer representing the recursion threshold. Again, the help parameter provides a description.
parser.add_argument("-t", "--threshold", type=int, help="Recursion threshold")

# Adds an argument -o or --output to the parser. It specifies that the argument should be a string representing the output file name. The help parameter provides a description.
parser.add_argument("-o", "--output", type=str, help="Output file name")

# Parses the command-line arguments provided when running the script and stores the values in the args object. The values can be accessed using dot notation, such as args.url, args.threshold, and args.output.
args = parser.parse_args()

if __name__ == "__main__":
    # Produces an error if the url is not provided.
    
    if not args.url:
        print("Error: Website URL not provided.")
        exit(1)
    # Choses a default threshold value if not provided.
    
    if args.threshold is None:
        default_threshold = 10
        args.threshold = default_threshold
    # Produces an error message if the threshold provided is not positive.
    
    if args.threshold <= 0:
        print("Error: Invalid recursion threshold.")
        exit(1)
    
    # Removes any trailing slashes (/) from the URL. This is done to ensure consistency in the URL format.
    base_url = args.url.rstrip("/")
    
    # Adding the base_url ensures that the program starts crawling from the specified URL and avoids processing it again during recursive calls.
    visited_urls.add(base_url)
    
    # This if loop will run if the user has provided an output file.
    if args.output:
        
        # Code for opening the file in write mode. This will remove any output previously written.
        with open(args.output, 'w') as f:
            sys.stdout = f                  # Redirects the standard output to the file object 'f'.          
            scrape(base_url, args.threshold, base_url)              # The main function is called and its output will be written to f.
            sys.stdout = sys.__stdout__                             # Restores the standard output back to the original value, which is the console.
            # Any print statements after this line will be displayed on the console.
        print("Web crawler output saved to", args.output)                   # Display message on the terminal after the task is completed.
    
    else:
        scrape(base_url, args.threshold, base_url)                  # Function call with suitable arguments.
        print("Web crawler output:")

        for depth, level_links in links.items():                # Accessing the dictionary and printing the summary of the links crawled at each recursive level.
            print(f"At recursion level {depth}:")
            print("Total files found:", len(level_links))
            for link in level_links:
                print(link)


"""This is the end of the code. Thank You."""