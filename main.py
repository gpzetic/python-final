import requests as r, bs4
def get_url(url, key=0, value=0):
    if url[0:8] != 'https://':
        url = 'https://' + url
    try:
        if key == 0:
            page = r.get(url)

        page.raise_for_status()
        if page.status_code != r.codes.ok:
            return 1
        return page
    except Exception as e:
        print(e)
        return 1

def get_input(o, m):
    c = input(m)
    while not c in o:
        c = input('Invalid. ' + m)
    return c

def get_page(url, key=0, value=0):
    if key == 0:
        page = get_url(url)
    else:
        page = get_url(url, key, value)
    print(page)
    if page == 1:
        return
    html = bs4.BeautifulSoup(page.text, 'html.parser')
    a = html.select('a')
    i = html.select('input')
    i += html.select('textarea')
    r = html.select('p')
    #print(len(a))
    if len(i) == 0 or len(a) == 0:
        print('page has no links or no inputs')
        return
    mode = 0
    index = 0
    link_page = 0
    while mode == 0 or mode == 1 or mode == 2:
        print('URL:', url)
        if mode == 0:
            print('Browsing links')
            o = ['w', 's', '', 'b', 'i', 'r']
            link_index = 0
            for n in a:
                if link_index == index:
                    print('>>', end='')
                if 'href' in n.attrs and n.attrs['href'] != '' and n.attrs['href'][0] != '#' and n.text.strip() != '':
                    if abs(index - link_index) < 5:
                        print(n.text.strip())
                    link_index += 1
            c = get_input(o, 'Type "i" to switch to input mode, "r" for read mode\nType "w" to go up, "s" to go down, press Enter to select, "b" back: ')
            if c == '':
                prev_url = url.split('/')[:3]
                print("Visiting relative link from:", '/'.join(prev_url))
                url = a[index].attrs['href']
                if prev_url[-1].endswith('.html') or prev_url[-1].endswith('.php'):
                    prev_url = prev_url[:-1]
                if url[0] == '/':
                    url = '/'.join(prev_url) + url
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
            elif c =='r':
                mode = 2
        elif mode == 1:
            print('Browsing inputs')
            o = ['w', 's', '', 'b', 'a', 'r']
            input_index = 0
            for n in i:
                if input_index == index:
                    print('>>', end='')
                if abs(index - link_index) < 5:
                    if 'title' in n.attrs and n.attrs['title'] != '':
                        print(n.attrs['title'], 'Name:', n.attrs['name'])
                    elif 'aria-label' in n.attrs and n.attrs['aria-label'] != '':
                        print(n.attrs['aria-label'])
                input_index += 1
            c = get_input(o, 'Type "a" to switch to anchor mode, "r" for read mode\nType "w" to go up, "s" to go down, press Enter to select, "b" back: ')
            if c == '':
                inp = input('Enter your input: ')
                el = i[index]
                while el.parent.name != 'form':
                    el = el.parent
                get_page(url + el.parent.attrs['action'] + '?' + i[index].attrs['name'] + '=' + inp)

            elif c == 'w':
                index = (index - 1) % len(a)
            elif c == 's':
                index = (index + 1) % len(a)
            elif c == 'b':
                break
            elif c == 'a':
                mode = 0
            elif c =='r':
                mode = 2
        elif mode == 2:
            print('Read mode')
            o = ['w', 's', 'b', 'a', 'i']
            read_index = 0
            for n in r:
                if read_index == index:
                    print('>>', end='')
                if abs(index - link_index) < 5:
                    print(n.text)
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
            elif c =='i':
                mode = 1
        print('\n'*10)

while True:
    url = input('Enter a URL to browse: ')
    page = ''

    while get_url(url) == 1:
        url = input('Invalid URL, enter a new one: ')    
    get_page(url)

