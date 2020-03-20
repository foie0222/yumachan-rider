import csv


def make_csv(ticket_list):
    with open('./ticket.csv', 'w') as f:
        writer = csv.writer(f)
        for ticket in ticket_list:
            writer.writerow([ticket.to_csv()])
