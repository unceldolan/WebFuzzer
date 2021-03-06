import FindInputs
from customauth import customauth
from page_discovery import LinkAggregator
import sys
import requests
from sensitive import Sensitive

def main():
	custom_auth = False
	custom_auth_string = ""
	common_words_file = ""
	vectors =""
	sensitive =""
	random = False
	slow = 500
	argv = sys.argv
	if len(argv) < 3:
		print("Not enough information provided")
		exit()
	url = argv[2]
	if (argv[1] == "discover"):
		for arg in argv[2:]:
			a =arg.split("=")
			if(a[0] == "--custom-auth"):
				custom_auth = True
				custom_auth_string = a[1]
			if(a[0] == "--common-words"):
				common_words_file = a[1]
	elif argv[1] == "test":
		for arg in argv[2:]:
			a =arg.split("=")
			if(a[0] == "--custom-auth"):
				custom_auth = True
				custom_auth_string = a[1]
			if(a[0] == "--common-words"):
				common_words_file = a[1]
			if(a[0] == "--vectors"):
				vectors = a[1]
			if(a[0] == "--sensitive"):
				sensitive = a[1]
			if(a[0] == "--random"):
				if(a[1] == True):
					random = True
			if(a[0] == "--slow"):
				slow = int(a[1])
	else:
		print("Invalid Mode")
	
	if(common_words_file == ""):
		print("Please provide valid word file\n")
		exit()
	f = open(common_words_file)
	commonw = f.read().split('\n')
	if(custom_auth):
		customauth.getsite(custom_auth_string)
	
	res = FindInputs.getPage(url)
	cookies = FindInputs.getCookies(res)
	inputs = FindInputs.crawlForInput(res)
	
	urlargs = FindInputs.parseUrl(url)
	gather = LinkAggregator() 
	sens = Sensitive()
	urls = gather.getAllLinks(url)
	if(argv[1] == "discover"):
		print("======================================================")
		print("Guessed pages:\n")
		for w in commonw:
			guesses = gather.guessPage(url,w)
			for guess in guesses:
				print("{0}\n".format(guess))
		
		print("======================================================")
		print("linked pages:\n")
		for a in urls:
			print("{0} \n".format(a))
		print("======================================================")
		print("cookies received\n")
		for cookie in cookies:
			print("{0}\n".format(cookie))
		print("======================================================")
		print("Found inputs\n")
		for input in inputs:
			print("name {0} : type {1} \n".format(input[0], input[1]))
		print("======================================================")
		print("URL arguments\n")
		for urlarg in urlargs:
			if len(urlarg) == 2:
				print("Key {0}: Value {1}\n".format(urlarg[0], urlarg[1]))
		print("======================================================")
		for a in urls:
			urlargs = parseUrl(a)
			res = getPage(a)
			inputs = crawlForInput(a)
			cookies = getCookies(a)
			print("for url: %s", url)
		
	if(argv[1] == "test"):
		if len(inputs) != 0:
			print("Beginning Test")
			if random:
				num = random.randint(0,len(inputs)-1)
				for i in open(vectors).split('\n'):
					print("Testing vector {0}",i)
					payload = {inputs[num], i}
					r = request.post(url,data=payload)
					print(gather.siteStatus(r))
					print(gather.responseTime(r,slow))
					#UNCOMMENT ME TO TEST THE POTENTIAL BROKEN SENSITIVE BIT
					#sens.checklist(open(vectors).read().split('\n'),sensitive)
			else:
				for i in inputs:
					for j in open(vectors).read().split('\n'):
						print("Testing input {0}".format(i))
						print("Testing vector {0}".format(j))
						payload = {i:j}
						r = requests.post(url,payload)
						print(gather.siteStatus(r))
						print(gather.responseTime(r,slow))
						#UNCOMMENT ME TO TEST THE POTENTIAL BROKEN SENSITIVE BIT
						#sens.checklist(open(vectors).read().split('\n'),sensitive)
			print("Ending Test")			
		else:
			print("No inputs to test on page")
		
			
		
main()