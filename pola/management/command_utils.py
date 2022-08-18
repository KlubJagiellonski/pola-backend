def ask_yes_no(question):
    confirm = input(question)
    while True:
        if confirm not in ('Y', 'n', 'yes', 'no'):
            confirm = input('Please enter either "yes" or "no": ')
            continue
        if confirm in ('Y', 'yes'):
            return True
        else:
            return False
