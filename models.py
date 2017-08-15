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
	def __init__(self, base_skills):
		self.skills = dict()
		for skill, base in base_skills.iteritems():
			self.skills[skill] = (False, base)
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
	def add_professional_skills_package(self, professional_skills):
			for skill, val in professional_skills.iteritems():
				self.skills[skill] = (True, val)
	def add_bonus_skills_package(self, bonus_skills):
			for skill in bonus_skills:
				if skill in self.skills.keys():
					_, stat = self.skills[skill]
					self.skills[skill] = (True, stat + 20)
				elif self.__match_optional_skill(skill):
					self.skills[skill] = (True, 20)
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
