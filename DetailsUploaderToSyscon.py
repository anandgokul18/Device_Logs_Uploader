#!/usr/bin/env python

import pexpect,sys, time

#Destination on Syscon (don't give a slash after location) Eg) /home/anandgokul/<directoryname>/ck381
dest='/home/anandgokul/testdir/ck381'
#Switch Name
switch = 'ck381'
#Choose whether multiagent (OR) gated for logs. 0 means Gated and 1 means multiagent
multiagent=1 

#Whether to include tech-support for ASU2 (default=0 .ie. no need)
asu2=1   

intromessage='''
=========================================================================================
NOTE:
1) Ensure reachability to the switch from the device you are running this script on
2) Please ensure that the DUT's admin password is either None (or) 'arastra'
3) Please ensure that the destination Directory is already created .aka. exists on Syscon

For anything else, please contact anandgokul@
=========================================================================================
'''

print intromessage
time.sleep(5)

def sysconValidator(ret_val):
	if ret_val == 0:
		child.sendline('yes')
		print child.before
		print child.after
    	ret_val=child.expect([ssh_newkey,"timed out","password:","#",">"])

    #Starting as new if since ret_val value has been changed	
	if ret_val==1:
	    print child.before
	    print child.after
	    print "Syscon is not reachable from the switch - Kindly fix the same. "
	    sys.exit(1)
	elif ret_val==2:
	    child.sendline("arista123")
	    child.expect("#")
	    pass
	elif ret_val==3:
	    pass
	elif ret_val==4:
	    pass
	

def bashSysconValidator(ret_val):
	if ret_val == 0:
	           child.sendline('yes')
	           ret_val=child.expect([ssh_newkey,'password:',">"])
	if ret_val==1:
	           child.sendline("arista123")
	           child.expect("#")
	elif ret_val==2:
	           pass

if __name__ == "__main__":

	ssh_newkey = 'Are you sure you want to continue connecting'

	child = pexpect.spawn("ssh admin@"+switch,timeout=120)
	print "[Script Log] Trying to login to Switch "+switch
	try:
		ret_val=child.expect([ssh_newkey,"word",">","#"])   #This o/p can be either one of the three cases
	except Exception as e:
		print e
		print "[ERROR] Exiting due to the above shown error"
		sys.exit(1)
	if ret_val == 0:
	    child.sendline('yes')
	    ret_val=child.expect([ssh_newkey,'password:',">"])
	elif ret_val==1:
	    child.sendline("arastra")
	    child.expect("#")
	elif ret_val==2:
	    pass
	elif ret_val==3:
	    pass

	child.sendline("enable")
	child.expect("#")
	child.sendline("term len 0")
	child.expect("#")
	child.sendline("conf")
	child.expect("#")
	print "[Script Log] Login Successful"

	print "\n[Informational Message] The destination given to upload the files on Syscon is: "+dest +"\n"

	#Running Config
	print "[Script Log] Getting running-config"
	cmd="show run"
	child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/running-config")
	ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
	sysconValidator(ret_val)
	print "[Script Log] Getting running-config is Successful"

	#Startup Config
	print "[Script Log] Getting startup-config"
	cmd="show start"
	child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/startup-config")
	ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
	sysconValidator(ret_val)
	print "[Script Log] Getting startup-config is Successful"

	#Version
	print "[Script Log] Getting Version"
	cmd="show version"
	child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/show-version")
	ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
	sysconValidator(ret_val)
	print "[Script Log] Getting Version is Successful"

	#Core Dump
	print "[Script Log] Getting Core Files"
	bashcmd="bash sudo scp -r /var/core/"
	child.sendline(bashcmd+" anandgokul@syscon:"+dest+"/")
	ret_val=child.expect([ssh_newkey,"word","#"])
	bashSysconValidator(ret_val)
	print "[Script Log] Getting Core Files is Successful"

	#All logs- messages, qt, agent
	print "[Script Log] Getting all logs- messages, qt, agent"
	bashcmd="bash sudo scp -r /var/log/"
	child.sendline(bashcmd+" anandgokul@syscon:"+dest+"/")
	ret_val=child.expect([ssh_newkey,"word","#"])
	bashSysconValidator(ret_val)
	print "[Script Log] Getting all logs- messages, qt, agent is Successful"

	#Tech-Support
	print "[Script Log] Getting Tech-Support (this might take a lot of time)"
	cmd="show tech"
	child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/show-tech")
	ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
	sysconValidator(ret_val)
	print "[Script Log] Getting Tech-Support is Successful"


	#Tech-Support BGP
	print "[Script Log] Getting Tech-Support for BGP"
	cmd="show tech bgp"
	child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/show-tech-bgp")
	ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
	sysconValidator(ret_val)
	print "[Script Log] Getting Tech-Support for BGP is Successful"

	if multiagent==0:  #Ribd tech-support
		print "[Script Log] Tech-Support for Ribd (since mentioned as Gated mode)"
		cmd="show tech ribd"
		child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/show-tech-ribd")
		ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
		sysconValidator(ret_val)
		print "[Script Log] Tech-Support for Ribd is Successful"
	else:
		print "[Script Log] Tech-Support for Ospf (since mentioned as Multiagent mode)"
		cmd="show tech extended ospf"
		child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/show-tech-extended-ospf")
		ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
		sysconValidator(ret_val)
		print "[Script Log] Tech-Support for Ospf is completed successfully"

	#Tech-Support for ASU2 reload (this is supported only on some platforms)
	if asu2==1:
		print "[Script Log] Tech-Support for Reload Fast Boot"
		cmd="show tech reload-fast-boot"
		child.sendline(cmd+" > scp:anandgokul@syscon"+dest+"/show-tech-reload_fast_boot")
		ret_val=child.expect([ssh_newkey,"timed out","word","#",">"])
		sysconValidator(ret_val)
		print "[Script Log] Tech-Support for Reload Fast Boot is Successful"


	#There are lots of other options in tech-support like isis, kernelFib, etc...Add as and when needed
	
	closingmessage='''
===================================================================================================
If you are uploading this for Bug filing, then, you may want to run the below command on syscon:
mkdir /export/bugs/<bug-id>/
mkdir /export/bugs/<bug-id>/'''+switch+'''
mv	'''
	print closingmessage+ dest + "/ /export/bugs/<bug-id>/"+switch+"/"
	print "==================================================================================================="

	child.close()


