def make_csv(ticket_list):
    with open('./ticket.csv', 'w') as f:
        for ticket in ticket_list:
            f.write(ticket.to_csv() + '\n')
