class Stats:
	def __init__(self, strn, con, dex, intl, powr, char):
		self.str, self.con, self.dex, self.int, self.pow, self.cha = strn, con, dex, intl, powr, char
		self.hp = (self.str + self.con + 1)/2
		self.san = 5 * self.pow
		self.bp = self.san - self.pow
		self.wp = self.pow
	def __repr__(self):
		return "STR: %d, CON %d, DEX %d, INT %d, POW %d, CHA %d" % (self.str, self.con, self.dex, self.int, self.pow, self.cha)
	def __str__(self):
		stats_str = self.__repr__()
		return '''Base Stats:\n%s\n\nDerived Stats:\nHP: %d, Sanity: %d, Breaking Point: %d, Willpower: %d''' % (stats_str, self.hp, self.san, self.bp, self.wp)

class Skills:
	def __init__(self, base_skills, professional_skills, bonus_skills):
		self.skills = dict()
		for skill, base in base_skills.iteritems():
			self.skills[skill] = (False, base)
		self.__add_professional_skills_package(professional_skills)
		self.__add_bonus_skills_package(bonus_skills)
		self.__combine_bucket_skills()

	def __repr__(self):
		skill_strings = []
		for key, val in self.skills.iteritems():
			dirty, stat = val
			if dirty:
				skill_strings.append("%s: %d" % (key, stat))
		skill_strings.sort()
		return '\n'.join(skill_strings)
	def __match_optional_skill(self, skill):
		new = [token.strip() for token in skill.split('(')]
		return new[0] in self.skills
	def __add_professional_skills_package(self, professional_skills):
			for skill, val in professional_skills.iteritems():
				self.skills[skill] = (True, val)
	def __add_bonus_skills_package(self, bonus_skills):
			for skill in bonus_skills:
				if skill in self.skills.keys():
					_, stat = self.skills[skill]
					self.skills[skill] = (True, stat + 20)
#				elif self.__match_optional_skill(skill):
				else:
					self.skills[skill] = (True, 20)
	def __combine_bucket_skills(self):
		bucket_dict = {
			"Art": {'generic': [], 'specific':[]},
			"Craft": {'generic': [], 'specific':[]},
			"Foreign Language": {'generic': [], 'specific':[]},
			"Military Science": {'generic': [], 'specific':[]},
			"Pilot": {'generic': [], 'specific':[]},
			"Science": {'generic': [], 'specific':[]}
		}
		for skill in self.skills.keys():
			tup = tuple(st.strip(" ()") for st in skill.split("("))
			if tup[0] in bucket_dict:
				if self.skills[skill][0] and (len(tup) == 1 or tup[1] not in ['Choose Another', 'Choose a Third']):
					if (len(tup) == 1 or tup[1] == 'Choose One'):
						bucket_dict[tup[0]]['generic'].append(skill)
					else:
						bucket_dict[tup[0]]['specific'].append(skill)
		for key, value in bucket_dict.iteritems():
			if value['generic'] and value['specific']:
				for skill in value['generic']:
					guard = 90
					while guard >= 80 and value['specific']:
						maximum_skill = max(value['specific'], key = lambda x: self.skills[x][1])
						guard =  self.skills[maximum_skill][1]
						if self.skills[maximum_skill][1] >= 80:
							value['specific'].remove(maximum_skill)
					if not value['generic']:
						pass
					else:
						self.skills[maximum_skill] = (True, self.skills[maximum_skill][1] + self.skills[skill][1])
						self.skills[skill] = (False, 0)
	def __getitem__(self, key):
		return self.skills[key]

class Character:
	def __init__(self, stats, skills, profession, bonds, background, veteran = False):
		self.stats, self.skills, self.profession, self.bonds, self.background = stats, skills, profession, bonds, background
	def __repr__(self):
		return "Profession: %s\nBackground: %s\nBonds: %d" % (self.profession, self.background, self.bonds)
	def __str__(self):
		char_repr = self.__repr__()
		stat_str = self.stats.__str__()
		skill_str = self.skills.__repr__()
		repr_str = "%s\n\n%s\n\nSkill Percentages:\n%s" % (char_repr, stat_str, skill_str)
		return repr_str
