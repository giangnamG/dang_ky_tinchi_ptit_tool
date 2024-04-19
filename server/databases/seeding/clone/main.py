
def get(filename):
    with open(filename, 'rb') as f:
        contents = f.readlines()
    subjects = []
    for line in contents:
        line = line.decode('utf-8')
        if '#' not in line and '-' not in line and '+' not in line and len(line) > 1:
            subject = line.replace('\r','').split(',')
            if len(subject) == 3:
                subjects.append({
                    'NameSubjects' : subject[0].strip(),
                    'CodeSubjects' : subject[1].strip(),
                    'STC' : subject[2].strip(),
                })
    return subjects