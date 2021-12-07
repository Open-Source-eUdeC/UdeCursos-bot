def Clip():
    clippings = []
    with open('data/clippings.txt') as file:
        unwanted = ['(', ')', '"', '«', '»']
        row = 0
        for line in file:
            if  row == 0: # Book & Author
                if '-' in line:
                    line = line.split(' - ')
                    book = line[0].strip()
                    author = line[1].strip()
                elif '(' in line:
                    line = line.split('(')
                    book = line[0].strip()
                    author = line[1].strip()
                    author = author.split(')')[0]
                else:
                    book, author = line, line            
                row += 1

            elif row == 1: # Highlight page and date
                page, date = line, line
                # line = line.split('|')
                # page = line[0].strip().split(' ')[-1].split('-')[-1]            
                # date = line[1].strip()
                row += 1
            elif row == 2: # Empty line
                row += 1
                continue
            elif row == 3: # Highlight
                highlight = line
                for char in unwanted:
                    highlight = highlight.replace(char, '')

                highlight = (highlight[0].upper() + highlight[1:]).strip()
                if highlight[-1] == '.':
                    pass
                else:
                    highlight = highlight + '.'
                row += 1
            elif row == 4: # Separator and end of clipping
                out = {
                    'book': book,
                    'page': page,
                    'author': author,
                    'date': date,
                    'highlight': highlight   
                }
                clippings.append(out)
                row = 0
    return clippings
