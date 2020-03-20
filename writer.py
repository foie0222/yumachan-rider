def make_csv(ticket_list, timestamp):
    with open('./ticket_' + timestamp + '.csv', 'w') as f:
        for ticket in ticket_list:
            f.write(ticket.to_csv() + '\n')
