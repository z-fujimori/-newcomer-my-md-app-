import html

def markdown_to_html(base_text):
    print("ベース: ", base_text)
    lines = base_text.splitlines()
    print("", lines)

    return_text = "<div>"
    return_text = analyser(return_text, lines, index=0 )
    return_text += "</div>"

    return return_text

def analyser(return_text, lines, index):
    if len(lines) <= index:
        return return_text
    
    line = lines[index]
    line_split = line.split(' ')
    if line_split[0] == "#":
        return_line = h1(line[2:])
    elif line_split[0] == "##":
        return_line = h2(line[3:])
    elif line_split[0] == "-" or line_split[0] == "・":
        return_line, index = ul_li("<ul>", lines, index)
    elif line_split[0] == "```":
        if not len(line_split) == 1:
            text = f"<div class='code_block'><div class='code_block_title'>{line[4:]}</div><br><per><code>"
        else:
            text = f"<div class='code_block'><per><code>"
        return_line, index = code_block(text, lines, index+1)
        return_line += "</code></per></div>"
    else:
        return_line = nomal_row(line)
    return_text += return_line
    return analyser(return_text, lines, index+1)
 
def h1(text):
    return "<h1>" + text + "</h1><hr>"
def h2(text):
    return "<h2>" + text + "</h2>"
def p(text):
    return "<p>" + text + "</p>"
def nomal_row(text):
    return text + "<br>"
def ul_li(text, lines, index):
    if len(lines) <= index:
        return text, index
    line = lines[index]
    if line == '':
        text += "</ul>"
        return text, index
    if line.split(' ')[0] == '-' or line.split(' ')[0] == '・':
        text += li(line[2:])
    else:
        text += nomal_row(line)
    return ul_li(text, lines, index+1) 
    
    ul_li(retun_text, lines)
def li(text):
    return f"<li>{text}</li>"
def code_block(text, lines, index):
    if len(lines) <= index:
        return text, index 
    line = lines[index]   
    if line == "```":
        return text, index
    text += nomal_row(html.escape(line))
    return code_block(text, lines, index+1)

