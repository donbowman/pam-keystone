# 
# Authenticate against OpenStack Keystone
#

import syslog, os, traceback
from keystoneclient.v2_0 import client

def pam_sm_authenticate(pamh, flags, argv):
    try:
	pamh.user
	pamh.authtok
	if pamh.authtok == None:
	    passmsg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Keystone password")
	    rsp = pamh.conversation(passmsg)
	    pamh.authtok = rsp.resp

	try:
	    client.Client(username=pamh.user, password=pamh.authtok, auth_url="https://nubo.sandvine.rocks:5000/v2.0")
	    syslog.syslog("pam keystone success for %s" % pamh.user)
	    return pamh.PAM_SUCCESS
	except:
	    syslog.syslog("pam keystone fail for %s" % pamh.user)
	    pass
    except:
	syslog.syslog("Unhandled exception %s " % traceback.format_exc())
    return pamh.PAM_AUTH_ERR

def pam_sm_setcred(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
  return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
  return pamh.PAM_SUCCESS
