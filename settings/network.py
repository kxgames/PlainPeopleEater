import arguments

role = arguments.option("role", default="host")

if role == "client":
    host = arguments.option("host", default='localhost')
    port = arguments.option("port", default=0, cast=int) + 11249

    print "Welcome to the PurplePeopleEater Client"
    print "======================================="
    print "Connecting to %s on port %s.\n" % (host, port)

elif role == "host":
    host = ''
    port = arguments.option("port", default=0, cast=int) + 11249

    print "Welcome to the PurplePeopleEater Host"
    print "====================================="
    print "Listening on port %s.\n" % port

elif role == "sandbox":
    host = ''
    port = 0

    print "Playing in Sandbox mode.\n"

else:
    raise AssertionError("Invalid network role: '%s'." % role)

