# protonne

Python bindings for proton vpn's linux cli.

## Installation

Install with:

<pre>
pip install protonne
</pre>

### **NOTE**: This package requires that you have a Proton VPN account and that you've installed and set up the [Proton VPN Linux CLI](https://protonvpn.com/support/linux-vpn-tool/).

## Usage

<pre>
from protonne import Proton
proton = Proton()
proton.connect_fastest()
proton.enable_permanent_killswitch()

# If you want to execute the commands "silently", you can set 'capture_output' to True in the class constructor or after creation through the 'capture_output' property
proton.capture_output = True
proton.capture_output = False
# Almost every function returns an 'Output' object that contains 3 fields: 'return_code', 'stdout', and 'stderr'.
# When 'capture_output' is True, 'stdout' and 'stderr' can be accessed through the 'Output' object, otherwise they are empty strings.
# The 'capturing_output()' context manager can also be used.
with proton.capturing_output():
    output = proton.connect_random()
    print(output.stdout)

# Once you're connected, info about the connection is available through the 'connection' property.
# Accessing this property invokes the cli's 'status' command and parses the output into a 'Connection' object.
# For performance, it's best to store this property in a local variable for repeated access until you need an updated 'Connection' object.
ip_history = []
connection = proton.connection
ip_history.append((connection.IP, connection.server.name))
proton.connect_random()
connection = proton.connection
ip_history.append((connection.IP, connection.server.name))
proton.connect(server=ip_history[0][1])

# Full 'Connection' annotation:
connection.IP: str
connection.killswitch.active: bool
connection.killswitch.on: bool
connection.killswitch.permanent: bool
connection.raw: str # The raw output string of the 'status' cli command
connection.server.name: str
connection.server.country: str
connection.server.protocol: str
connection.server.load: str
connection.server.plan: str
connection.server.features: str | None
connection.time: str
</pre>
