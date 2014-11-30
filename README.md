pam-keystone
============

This module allows authenticating against keystone as a
pam module. E.g. to allow nginx or other system
services to use keystone users.

It does not create an NSS module, so its for auth only.

To use, copy keystone-auth.py to /lib/security, chmod 555 it.
Then add a line like 

    auth sufficient pam_python.so owa-auth.py

usually right before:

    @include common-auth 

in a pam service. You may need to change the AUTH url
in the lib (I didn't make it an argument).


Example config. Place in /etc/pam.d/keystone:

    # PAM configuration for the Secure Shell service

    auth sufficient pam_python.so keystone-auth.py

    auth	requisite			pam_deny.so

    account sufficient pam_permit.so
    session sufficient pam_permit.so

