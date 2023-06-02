class bcolors:
	HEADER = '\033[95m'
	NORMAL = '\033[39m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	PASS = '\033[32m'
	#WARNING = '\033[91m'
	WARNING = '\033[33m'
	FAIL = '\033[31m'
	ENDC = '\033[0m'
	BOLD = '\033[01m'
	UNDERLINE = '\033[4m'
	TEST1 = '\033[41m'
	TEST2 = '\033[42m'
	TEST3 = '\033[43m'
	TEST4 = '\033[44m'
	TEST5 = '\033[45m'
	TEST6 = '\033[46m'
	TEST7 = '\033[47m'
	TEST8 = '\033[48m'
	TEST9 = '\033[49m'
	TEST0 = '\033[50m'


def disable(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''
#num: fg/bg

#11m: Nothing
#12m: Nothing

#21m: Nothing
#22m: Nothing

#31m: white/Red
#32m: white/Green
#33m: white/Yellow
#34m: White/Blue
#35m: White/Purple
#36m: White/Teal
#37m: White/Grey
#38m: White/Black
#39m: White/Black
#40m: Black/Black
#41m: Red/Black
#42m: Green/Black
#43m: Yellow/Black
#44m: Blue/Black
#45m: Purple/Black
#46m: Teal/Black
#47m: Grey/Black
#48m: White/Black
#49m: White/Black
#50m: White/Black

#51m: Nothing

#61m: Nothing

#71m: Nothing

#81m: Nothing

#91m: White/Red
#94m: White/Blue
#97m: White/Gray
