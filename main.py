import requests as r, bs4
# Function to return the page from a url
# Displays an error and returns to main URL input
# if there is an error in the URL
def get_url(url, key=0, value=0):
    # if the first 8 characters of the url dont contain http then add it
    if url[0:8] != 'https://':
        url = 'https://' + url
    try:
        if key == 0:
            page = r.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"})

    # find the status of the page, if it is ok then return page, if not return 1 for error
        page.raise_for_status()
        if page.status_code != r.codes.ok:
            return 1
        return page
    # general exception, print the error and return 1 for error
    except Exception as e:
        print(e)
        return 1

# Takes in an array of valid characters and checks if the user types
# a correct input, such as "s", "w" and displays a message with the user's
# options
def get_input(o, m):
    c = input(m)
    # while the user input is not in the array, say it is invalid
    while not c in o:
        c = input('Invalid. ' + m)
    return c

# Takes in a url for a website and first converts it into arrays of
# HTML elements
def get_page(url, key=0, value=0):
    if key == 0:
        page = get_url(url)
    else:
        page = get_url(url, key, value)
    print(page)
    # the above function returns 1 if error, so if page is error, then return to first function
    if page == 1:
        return

    print('\033[2J')

    # Convert the page text with html.parser to the elements
    html = bs4.BeautifulSoup(page.text, 'html.parser')
    # Select all the links from the page
    a = html.select('a')
    # inputs
    i = html.select('input')
    i += html.select('textarea')
    r = html.select('h1')
    r += html.select('h2')
    r += html.select('h3')
    r += html.select('p')
    r += html.select('span')
    print(r)
    #print(len(a))
    # Return to main URL input if there are no links
    if len(i) == 0 and len(a) == 0:
        print('Page has no links and no inputs')
        return
    mode = 0
    index = 0
    # Recursive loop to save pages
    while mode == 0 or mode == 1 or mode == 2:
        print('URL:', url)
        if mode == 0:
            print('Browsing links')
            if len(a) == 0:
                print("No links found")
            # the list of valid inputs
            o = ['w', 's', '', 'b', 'i', 'r']
            link_index = 0
            # for every a tag in a array, if href is in the attributes
            # and isnt blank and it isnt an id and remove whitespace isnt blank
            for n in a:
                if 'href' in n.attrs and n.attrs['href'] != '' and n.attrs['href'][0] != '#' and n.text.strip() != '':
                    # then for printing the links and underlining for the console
                    if abs(index - link_index) < 5:
                        print(link_index + 1, end=': ')
                        if link_index == index:
                            print('>>\033[4m', end='')
                        print(n.text.strip())
                        if link_index == index:
                            print('\033[24m', end='')
                    link_index += 1
                    # add one to link_index every valid link
            c = get_input(o, 'Type "i" to switch to input mode, "r" for read mode\nType "w" to go up, "s" to go down, press Enter to select, "b" back: ')

            if c == '' and len(a) != 0:
                if len(a[index].attrs['href']) == 0:
                    print("Invalid link")
                    continue
                prev_url = url.split('/')[:3]
                print("Visiting relative link from:", '/'.join(prev_url))
                url = a[index].attrs['href']
                if prev_url[-1].endswith('.html') or prev_url[-1].endswith('.php'):
                    prev_url = prev_url[:-1]
                if url[0] == '/':
                    url = '/'.join(prev_url[:-1]) + url
                elif url[0] != 'h':
                    url = '/'.join(prev_url) + '/' + url
                get_page(url)
            elif c == 'w':
                index = (index - 1) % len(a)
            elif c == 's':
                index = (index + 1) % len(a)
            elif c == 'b':
                break
            elif c == 'i':
                mode = 1
                index = 0
            elif c =='r':
                mode = 2
                index = 0
        elif mode == 1:
            print('Browsing inputs')
            if len(i) == 0:
                print("No inputs found")
            o = ['w', 's', '', 'b', 'a', 'r']
            input_index = 0
            name = ''
            for n in i:
                out = ''
                if 'name' in n.attrs:
                    if 'type' in n.attrs and (n.attrs['type'] == 'hidden' or n.attrs['type'] == 'button' or n.attrs['type'] == 'submit'):
                        continue
                    elif 'value' in n.attrs and n.attrs['value'] != '':
                        out = n.attrs['value']
                    elif 'title' in n.attrs:
                        out = n.attrs['title']
                    elif n.text != '':
                        out = n.text
                    else:
                        continue
                    input_index += 1
                if abs(index - input_index) < 5 and out != '':
                    print(input_index, end=': ')
                    if input_index == index:
                        print('>>\033[4m', end='')
                        name = n.attrs['name']
                    print(n.name, "variable:", n.attrs['name'], end=': ')
                    print(out)
                    if input_index == index:
                        print('\033[24m', end='')
            c = get_input(o, 'Type "a" to switch to anchor mode, "r" for read mode\nType "w" to go up, "s" to go down, press Enter to select, "b" back: ')
            if c == '' and len(i) != 0:
                inp = input('Enter your input: ')
                el = i[index]
                while el.parent.name != 'form':
                    el = el.parent
                get_page(url + el.parent.attrs['action'] + '?' + name + '=' + inp)

            elif c == 'w':
                index = (index - 1) % len(a)
            elif c == 's':
                index = (index + 1) % len(a)
            elif c == 'b':
                break
            elif c == 'a':
                mode = 0
                index = 0
            elif c =='r':
                mode = 2
                index = 0
        elif mode == 2:
            print('Read mode')
            if len(r) == 0:
                print("No readable text")
            o = ['w', 's', 'b', 'a', 'i']
            read_index = 0
            for n in r:
                if n.text.strip() != '':
                    if abs(index - link_index) < 5:
                        if read_index == index:
                            print('>>', end='')
                        print(n.text.strip())
                    read_index += 1
            c = get_input(o, 'Type "a" to switch to anchor mode, "i" for input mode\nType "w" to go up, "s" to go down, "b" back: ')
            if c == 'w':
                index = (index - 1) % len(a)
            elif c == 's':
                index = (index + 1) % len(a)
            elif c == 'b':
                break
            elif c == 'a':
                mode = 0
                index = 0
            elif c =='i':
                mode = 1
                index = 0
        print('\033[2J')

while True:
    url = input('Enter a URL to browse: ')
    while get_url(url) == 1:
        url = input('Invalid URL, enter a new one: ')
    get_page(url)

