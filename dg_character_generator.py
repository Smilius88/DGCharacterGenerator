import json, random, argparse
from sys import argv
from CharacterCreationService import make_character

BASE_SKILLS_JSON = "base_skills.json"
PROFESSIONAL_SKILLS_JSON = "professional_skills.json"
BACKGROUND_SKILLS_JSON = "bonus_skills.json"

def make_professional_aliases():
	aliases = {
		'random': set(['random']),
		'Physician': set(['physician', 'doctor']),
		'Intelligence Case Officer': set(['intelligence case officer', 'spy', 'intelligence agent', 'case officer']),
		'Special Operator': set(['special operator', 'special forces', 'operator', 'specfor']),
		'Foreign Service Officer': set(['foreign service officer', 'foreign service']),
		'Media Specialist': set(['media specialist', 'pr', 'advertising agent', 'journalist', 'reporter']),
		'Firefighter': set(['firefighter']),
		'Nurse / Paramedic': set(['nurse', 'paramedic', 'nurse/paramedic', 'nurse / paramedic']),
		'Police Officer': set(['cop', 'police officer', 'detective']),
		'Scientist': set(['scientist', 'physicist', 'mathematician', 'biologist']),
		'Pilot / Sailor': set(['pilot', 'sailor', 'sailor / pilot', 'sailor/pilot', 'airplane pilot', 'captain']),
		'Program Manager': set(['program manager', 'manager', 'office manager', 'bureaucrat']),
		'Federal Agent': set(['federal agent', 'fed']),
		'Anthropologist / Historian': set(['anthropologist', 'historian', 'anthropologist/historian', 'anthropologist / historian']),
		'Lawyer / Business Executive': set(['lawyer', 'business executive', 'executive', 'lawyer / business executive', 'CEO', 'lawyer/business executive']),
		'Criminal': set(['crook', 'criminal', 'gangster', 'forger', 'hit man', 'mafia']),
		'Computer Scientist / Engineer': set(['computer scientist', 'hacker', 'engineer', 'computer scientist / engineer', 'computer scientist/engineer'])
	}
	return aliases

def make_background_aliases():
	aliases = {
		'random': set(['random']),
		'Social Worker or Criminal Justice Degree': set(['social worker', 'criminal justice degree', 'socialworker', 'social worker / criminal justice degree', 'social worker/criminal justice degree', 'criminal justice major']),
		'Black Bag Training': set(['spook', 'black bag training', 'black bag ops', 'black bag', 'spy']),
		'Firefighter': set(['firefighter']),
		'Nurse, Paramedic, or Pre-Med': set(['nurse', 'paramedic', 'pre-med', 'nurse, paramedic, or pre-med', 'premed', 'nurse, paramedic or pre-med']),
		'Science Grad Student': set(['science grad student', 'tech major', 'engineering grad student', 'nerd']),
		'Soldier or Marine': set(['soldier', 'army', 'marine', 'marines', 'soldier or marine', 'soldier / marine', 'soldier/marine']),
		'Interrogator': set(['interrogator']),
		'Artist, Actor, or Musician': set(['artist', 'actor', 'musician', 'writer', 'artist, actor, or musician', 'artist, actor or musician']),
		'Military Officer': set(['military officer', 'officer', 'major', 'leiutenant']),
		'Bureaucrat': set('bureaucrat'),
		'MBA': set(['mba', 'ceo']),
		'Police Officer': set(['cop', 'police officer', 'detective']),
		'Gangster or Deep Cover': set(['mafia', 'crook', 'criminal', 'deep cover', 'undercover agent', 'undercover', 'gangster or deep cover', 'gangster/deep cover', 'gangster / deep cover']),
		'Translator': set('translator'),
		'Photographer': set(['photographer', 'photojournalist']),
		'Pilot or Sailor':  set(['pilot', 'sailor', 'sailor / pilot', 'sailor/pilot', 'airplane pilot', 'captain', 'pilot or sailor']),
		'Combat Veteran': set(['veteran', 'combat veteran']),
		'Outdoorsman': set(['outdoorsman']),
		'Athlete': set(['athlete']),
		'Liberal Arts Degree': set(['philosopher', 'liberal arts major', 'liberal arts degree', 'historian']),
		'Clergy': set(['clergy', 'priest', 'rabbi', 'imam']),
		'Urban Explorer': set(['urban explorer']),
		'Counselor': set(['counselor']),
		'Author, Editor, or Journalist': set(['author', 'editor', 'journalist', 'author, editor, or journalist', 'author, editor or journalist']),
		'Blue-Collar Worker': set(['blue collar worker', 'factory worker']),
		'Computer Enthusiast or Hacker': set(['computer enthusiast', 'hacker', 'computer enthusiast or hacker', 'computer scientist']),
		'Criminalist': set(['criminalist', 'forensics', 'csi']),
		'Occult Investigator or Conspiracy Theorist': set(['occult investigator', 'paranormal investigator', 'parapsychologist', 'conspiracy theorist', 'occult investigator or conspiracy theorist'])
	}
	return aliases

def alias_map(user_input, aliases):
	user_input_standardized = user_input.lower().strip()
	for key, value in aliases.iteritems():
		if user_input_standardized in value:
			return key
	raise Exception("Unidentified profession: %s" % user_input)

def optimize_profession(stats, profession_dict):
	stats_map = dict(zip(("STR", "CON", "DEX", "INT", "POW", "CHA"), stats))
	maximum, ans = 0, []
	for key in profession_dict.keys():
		ranking = 1
		if "Recommended Stats" in profession_dict[key]:
			rec_stats = profession_dict[key]["Recommended Stats"]
			total = [stats_map[stat] for stat in rec_stats]
			ranking = sum(total)/float(len(total))
		if ranking > maximum:
			maximum = ranking
			ans = [key]
		elif ranking == maximum:
			ans.append(key)
	return random.choice(ans)

def roll_stat():
	from random import randint
	dice = [randint(1,6) for _ in xrange(4)]
	dice.sort()
	return sum(dice[1:])


def make_parser():
	parser = argparse.ArgumentParser(description = 'Generates random PCs for Delta Green.')
	parser.add_argument('--make', '-m', nargs = '?', default = 1, help = "The number of PCs to generate. The default is 1", dest = 'num')
	parser.add_argument('--profession', '-p', nargs = '?', default = 'random', help = 'Give this profession to all the PCs generated.', dest ='prof_string')
	parser.add_argument('--background', '-b', nargs = '?', default = 'random', help = 'Give this background to all the PCs generated.', dest = 'backgr_string')
	parser.add_argument('--optimize', '-o', action = 'store_true', help = 
			'If selected, this will attempt to opmtimize the PC. If a profession is selected, it will generate several characters (currently 5) and choose ' +
			'the one with the most appropriate stats. If the profession is randomized, a profession suited to the stats will be selected.', dest = 'optimize')
	return parser

# Parse JSON, handle invoke randomization
def main(num,  profession, background, optimize):

	base_stats, professional_skills, background_skills = None, None, None

	with open(BASE_SKILLS_JSON) as ifile:
		base_stats = json.loads(ifile.read())
	with open(PROFESSIONAL_SKILLS_JSON) as ifile:
		professional_skills = json.loads(ifile.read())
	with open(BACKGROUND_SKILLS_JSON) as ifile:
		background_skills = json.loads(ifile.read())

	char_stats = tuple(roll_stat() for _ in xrange(6))
	if profession == "random":
		if optimize:
			profession = optimize_profession(char_stats, professional_skills)
		else:
			profession = random.choice(professional_skills.keys())
	if background == "random":
		background = random.choice(background_skills.keys())


	print '\n'
	print make_character(char_stats, profession, background, professional_skills, background_skills, base_stats)
	print '\n'

if __name__ == "__main__":
	parser = make_parser()
	args = parser.parse_args()
	bg_alias = make_background_aliases()
	prof_alias = make_professional_aliases()
	profession = alias_map(args.prof_string, prof_alias)
	background = alias_map(args.backgr_string, bg_alias)
	main(args.num, profession, background, args.optimize)


