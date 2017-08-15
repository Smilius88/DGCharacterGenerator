import random
from models import Stats, Skills, Character


def make_character(stats, profession, background, professional_skills, background_skills, base_skills):
	prof_skills = make_professional_skills(professional_skills[profession]["Skills"])
	char_background = make_background_skills(background_skills[background], base_skills.keys())
	char_stats = Stats(*stats)
	char_skills = Skills(base_skills)
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
