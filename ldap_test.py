import ldap
import sys

#distinguished name for admin
LDAP_ADMIN_DN ="cn=admin,dc=example,dc=com"
#your password
LDAP_PASSWORD =""

def try_ldap_bind(ldap_host,admin_pass):
    try:
        ldap_conn = ldap.initialize(ldap_host)
    except (ldap.SERVER_DOWN):
        print("Can't contact LDAP server")
        exit(4)
    try:
        ldap_conn.simple_bind_s(LDAP_ADMIN_DN,admin_pass)
    except(ldap.INVALID_CREDENTIALS):
        print("username or password incorrect")
        sys.exit(3)
    print("Authenticated succesfully")
    return ldap_conn


def ldap_search(dn = 'ou=insat,dc=example,dc=com'):
    conn = try_ldap_bind('ldap://localhost',LDAP_PASSWORD)
    result = conn.search_s(dn, ldap.SCOPE_SUBTREE)
    print(result)

if __name__ == '__main__':
    try_ldap_bind('ldap://localhost',LDAP_PASSWORD)


