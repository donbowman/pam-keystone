# 
# Authenticate against OpenStack Keystone
#

import syslog, os, traceback, sys
import urllib2, json,hashlib
import memcache

def pam_sm_authenticate(pamh, flags, argv):
    try:
	pamh.user
	pamh.authtok
	if pamh.authtok == None:
	    passmsg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Keystone password")
	    rsp = pamh.conversation(passmsg)
	    pamh.authtok = rsp.resp
	try:
            mu = hashlib.sha1()
            mu.update(pamh.user)
            mp = hashlib.sha1()
            mp.update(pamh.authtok)
            mc = memcache.Client([('127.0.0.1',11211)])
            v = mc.get("%s-%s" % (mu.hexdigest(),mp.hexdigest()))
            if v != None:
                return pamh.PAM_SUCCESS

            import json, urllib2
            val = {
                "auth": {
                    "passwordCredentials": {
                        "password": pamh.authtok,
                        "username": pamh.user
                    }
                }
            }
            req = urllib2.Request('https://keystone.sandvine.rocks/v2.0/tokens')
            req.add_header('Content-Type', 'application/json')
            try:
                response = urllib2.urlopen(req, json.dumps(val))

                if (response.getcode() == 200):
                    mc.set("%s-%s" % (mu.hexdigest(),mp.hexdigest()),"true", 900)
                    syslog.syslog("pam-keystone: user %s login" % pamh.user)
                    return pamh.PAM_SUCCESS
            except:
                # Don't want this error, its the 401
                pass
	except:
	    syslog.syslog("pam keystone fail for %s (%s)" % (pamh.user, traceback.format_exc()))
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
