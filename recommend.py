import json
from random import choice, randint

class Recommend():
	def build_dict(self, users_book_list, user_book_list):
		"""
		Expecting  [{"name":"tom", "books":["bok1", "bok2"]},{"name":"eva", "books":["bok1"] } ]

		"""

		d = {}
		i = 0
		for user in users_book_list:
			for book in user["books"]:
				if book not in d.values():
					d[i] = book
					i += 1


		for book in user_book_list:
			if book not in d.values():
				d[i] = book
				i += 1

		matrix = []
		self.user = []
		for i in xrange(len(d)):
			if d[i] in user_book_list: 
				self.user.append(1)
			else:
				self.user.append(0)

		for i in xrange(len(users_book_list)):
			row = []
			for j in xrange(len(d)):
				if d[j] in users_book_list[i]["books"]: 
					row.append(1)
				else:
					row.append(0)
			matrix.append(row)

		self.matrix = matrix
		self.book_dictionary = d

	def compare(self):
		greatest = 0
		greatest_user = None
		for user in self.matrix:
			total = 0
			for i in xrange(len(self.user)):
				if self.user[i] == 1 and user[i] == 1: 
					total += 1
			if total > greatest:
				greatest = total
				greatest_user = user
		if greatest_user is None:
			return choice(self.user)							# Returns random user if none is good match
		
		recommendations = []
		for i in xrange(len(self.user)):
			if self.user[i] == 0 and greatest_user[i] == 1:
				recommendations.append( self.book_dictionary[i])
		if len(recommendations) == 0:
			for i in range(4):									# Add random book if it doesn't find any
				recommendations.append( self.book_dictionary[randint(0, len(book_dictionary)-1)])
		return recommendations
				
		
if __name__ == "__main__":
	print "Running som tests!"
	print "------------------"
	r = Recommend()
	r.build_dict([{"name":"tom", "books":["bok1", "bok2", "bok3"]}, {"name":"eva", "books":["bok1", "bok4"] } ])
	r.build_user(["bok1", "bok2"])
	r.compare()

