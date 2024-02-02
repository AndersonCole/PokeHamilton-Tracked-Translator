import regex as re
'''
Data is in the following order
Name|IvRange|LevelRange|StatRange|PvpIvs|Gender
if no gender, col is blank
if there are no pvpivs, gender fills that col
if no pvpivs or gender, cols are blank
'''
seenForms = []

def translateFormName(formName):
    global seenForms
    if formName not in seenForms:
        seenForms.append(formName)

    match formName:
        case 'Alolan':
            formName = 'Alola'
        case 'Plant Cloak':
            formName = 'Plant_Cloak'
        case 'Sandy Cloak':
            formName = 'Sandy_Cloak'
    return formName

tracked_data = []

with open('anderson4990.txt', 'r') as file:
    for line in file:
        tracked_line = re.split(r'[|]', line)
        if 'distance' in tracked_line[1]:
            tracked_line.pop(1)
        if 'cp: ' in tracked_line[2]:
            tracked_line.pop(2)
        tracked_line_stripped = []
        for tracked_field in tracked_line:
            tracked_line_stripped.append(tracked_field.strip())

        tracked_data.append(tracked_line_stripped)

tracking_string = ''

for mon in tracked_data:
    tracking_string += '!track '

    #mon name and form
    mon_name = re.split(r'\*\*', mon[0])
    for index, name in enumerate(mon_name):
        if name == '':
            mon_name.pop(index)
    tracking_string += f'{mon_name[0]} '
    if len(mon_name) > 1:
        tracking_string += f'form{translateFormName(mon_name[1].strip())} '

    #IvRange
    if mon[1] == 'iv: 100%-100%':
        tracking_string += 'iv100 '

    #LevelRange
    if mon[2] != 'level: 0-40':
        level_range = re.split(r'\-', mon[2][7:])
        tracking_string += f'level{level_range[0]} maxLevel{level_range[1]} '

    #StatRange
    if mon[3] != 'stats: 0/0/0 - 15/15/15':
        stat_range = re.split(r'\s\-\s', mon[3][7:])
        min_range = re.split(r'\/', stat_range[0])
        max_range = re.split(r'\/', stat_range[1])
        tracking_string += f'atk{min_range[0]} def{min_range[1]} sta{min_range[2]} maxatk{max_range[0]} maxdef{max_range[1]} maxsta{max_range[2]} '

    #PvpIvs or gender
    if len(mon) > 4:
        if 'pvp ranking' in mon[4]:
            tracking_string += f'{mon[4][13:18]}1 '
        else:
            #gender
            tracking_string += f'{mon[4][15:]}'
    
    #Gender
    if len(mon) > 5:
        tracking_string += f'{mon[5][15:]}'

    tracking_string += '\n'

print(seenForms)

with open('tracked_commands.txt', 'w') as file:
    file.write(tracking_string)