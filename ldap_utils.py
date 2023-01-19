from ldap3 import Server, Connection, ALL, SUBTREE, BASE
from ldap3.core.exceptions import LDAPException, LDAPBindError


def connect_ldap_server(pseudo, pwd):
    try:
        # Provide the hostname and port number of the openLDAP
        server_uri = f"ldap://localhost"
        server = Server(server_uri, get_info=ALL)
        user_dn = "cn =" +pseudo+", ou = gl, ou = insat, dc = example, dc = com"
        print(user_dn)
        # username and password can be configured during openldap setup
        # TODO : provide your distinguished name and password
        connection = Connection(server,
                                user=user_dn,
                                password=pwd)
        bind_response = connection.bind()  # Returns True or False
    except LDAPBindError as e:
        connection = e
        exit(1)
    if(not bind_response):
        print("Error Authentification" , connection.result['description'])
    return bind_response


# For groups provide a groupid number instead of a uidNumber
def get_ldap_users():
    # Provide a search base to search for.
    search_base = 'dc=example,dc=com'
    # provide a uidNumber to search for. '*" to fetch all users/groups
    search_filter = '(ou=*)'

    # Establish connection to the server
    ldap_conn = connect_ldap_server()
    try:
        # only the attributes specified will be returned
        ldap_conn.search(search_base=search_base,
                         search_filter=search_filter,
                         search_scope=SUBTREE,
                         )
        # search will not return any values.
        # the entries method in connection object returns the results
        results = ldap_conn.entries
    except LDAPException as e:
        results = e
    print(results)


""" add method takes a user_dn, objectclass and attributes as    dictionary  """
def add_new_user(name,group):
    # Bind connection to LDAP server
    ldap_conn = connect_ldap_server()

    # this will create testuser inside group1
    user_dn = "cn=etudiant,ou="+group+",dc=example,dc=com"
    print(user_dn)
    # user_dn = "cn="+name+",dc=example,dc=com"

    try:
        # object class for a user is inetOrgPerson
        response = ldap_conn.add(user_dn,'inetOrgPerson', {'sn': name})
    except LDAPException as e:
        response = e
    print(ldap_conn.result)
    return response

""" add method takes a user_dn, objectclass and attributes as    dictionary  """
def add_new_organisation(group):

    # Bind connection to LDAP server
    ldap_conn = connect_ldap_server()

    # this will create testuser inside group1
    # user_dn = "cn="+name+",ou=+"+group+",dc=example,dc=com"
    user_dn = "ou="+group+",dc=example,dc=com"

    try:
        # object class for a user is inetOrgPerson
        response = ldap_conn.add('ou=isi,dc=example,dc=com', 'organizationalUnit')
    except LDAPException as e:
        exit(1)
    print(response)

if __name__ == "__main__":
    # print(connect_ldap_server())
    get_ldap_users()
    # add_new_user("salah","insat")
    # add_new_organisation("isi")