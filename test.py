from server import PersonDatabase

p = PersonDatabase("Database/user.db")
print(p.check_score_by_global(4, 4.87))
print(p.check_score_by_username("lbehrens2", 4, 4.63))

