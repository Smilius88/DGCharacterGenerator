import random, json
from models import Stats, Skills, Character

BASE_SKILLS_JSON = "base_skills.json"
PROFESSIONAL_SKILLS_JSON = "professional_skills.json"
BACKGROUND_SKILLS_JSON = "bonus_skills.json"

def make_random_character(choose_profession):
	base_stats, professional_skills, background_skills = None, None, None
	with open(BASE_SKILLS_JSON) as ifile:
		base_stats = json.loads(ifile.read())
	with open(PROFESSIONAL_SKILLS_JSON) as ifile:
		professional_skills = json.loads(ifile.read())
	with open(BACKGROUND_SKILLS_JSON) as ifile:
		background_skills = json.loads(ifile.read())

	def roll_stat():
		from random import randint
		dice = [randint(1,6) for _ in xrange(4)]
		dice.sort()
		return sum(dice[1:])

	stats = tuple(roll_stat() for _ in xrange(6))
	char_stats = Stats(*stats)
	profession = ""
	if choose_profession:
		profession = optimize_profession(char_stats, professional_skills)
	else:
		profession = random.choice(professional_skills.keys())
	prof_skills = make_professional_skills(professional_skills[profession]["Skills"])
	background = random.choice(background_skills.keys())
	char_background = make_background_skills(background_skills[background], base_stats.keys())
	char_skills = Skills(base_stats)
	char_skills.add_professional_skills_package(prof_skills)
	char_skills.add_bonus_skills_package(char_background)
	bonds = professional_skills[profession]["Bonds"]
	character = Character(char_stats, char_skills, profession, bonds, background)
	return character

def make_professional_skills(professional_skills):
	skills  = dict()
	for key, value in professional_skills.iteritems():
		unique_choices = []
		if key == "Choose":
			num = value[0]
			choices = value[1]
			c = random.sample(choices.keys(), num)
			for sk in c:
				skills[sk] = choices[sk]
		elif key == "Choose Unique":
			unique_choices.append(value)
		else:
			skills[key] = value
	for choice in unique_choices:
		num = choice[0]
		choices = choice[1]
		uc = set(choices.keys()) - set(skills.keys())
		c = random.sample(uc, num)
		for sk in c:
			skills[sk] = choices[sk]
	return skills

def make_background_skills(background_skills, profession_list):
	skills = []
	skill_strings = filter(lambda x: type(x) == str, background_skills)
	for item in background_skills:
		if type(item) == list:
			num = item[1]
			if item[0] == "Any":
				options = set(profession_list) - set(skill_strings)
				skills.extend(random.sample(options, num))
			elif item[0] == "Choose":
				skills.extend(random.sample(item[2], num))
		else:
			skills.append(item)
	return skills

def optimize_profession(stats, profession_dict):
	def map_stats(key, stats):
		if key == "STR":
			return stats.str
		elif key == "CON":
			return stats.con
		elif key == "DEX":
			return stats.dex
		elif key == "INT":
			return stats.int
		elif key == "POW":
			return stats.pow
		elif key == "CHA":
			return stats.cha
	maximum, ans = 0, []
	for key in profession_dict.keys():
		ranking = 1
		if "Recommended Stats" in profession_dict[key]:
			rec_stats = profession_dict[key]["Recommended Stats"]
			total = [map_stats(stat, stats) for stat in rec_stats]
			ranking = sum(total)/float(len(total))
		if ranking > maximum:
			maximum = ranking
			ans = [key]
		elif ranking == maximum:
			ans.append(key)
	return random.choice(ans)

print '\n'
print make_random_character(True)
print '\n'


