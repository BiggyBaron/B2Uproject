with open("./index.html", "r") as file:
    lines = file.readlines()
    for line in lines:
        if 'id="' in line:
            id = line.split('id="')[1].split('"')[0]
            print('var ' + id + ' = document.getElementById("' + id + '");')