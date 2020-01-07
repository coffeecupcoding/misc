# Intro

These files are used to implement a hack to put a systemd-managed process
into its own network namespace (but not any other namespaces).  The use case
is services with their own service IP(s) when you don't want to go all the
way and use Docker or Kubernetes.  Particularly with IPv6, the Linux kernel
uses the last IP added to an interface as the 'default' address, which makes
configuring interfaces with multiple special-purpose addresses problematic.

What this does is cause systemd to create a new namespace and one or more
veth pairs the first time a service that needs the namespace is started,
and to add some basic (loopback) configuration to the namespace.  The
network configuration system in use then configures the created interfaces
and adds them to a bridge - how the bridge relates to external access is up
to you.  I have a physical or vlan interface connected to each bridge and
'host' IPs on the bridge itself.

When the namespace is no longer in use by a systemd-managed service, it and
the interfaces are removed.

This has only been tested on Debian and the paths would require some
modification for Debian 9 or prior due to the (incomplete)
/sbin->/usr/sbin transition.


# Setup

- Pick a name for the network namespace your service will use (multiple
  services can use the same namespace with the usual caveats about port
  collision).  This will be referred to as (namespace) below.
- Choose a namespace-specific interface name for each veth pair
- Create directories /etc/network/namespaces and /etc/network/services .
- Copy namespace.template into /etc/network/namespaces with the file name
  (namespace)
- Edit /etc/network/namespaces/(namespace): 
  - replace 'xxNAMESPACExx' with the namespace name
  - replace 'xxINTERFACExx' with the interface name
  - if there is more than one interface, repeat the lines modified in the
    previous step for each interface
- Add 'source /etc/network/services/* ' to /etc/network/interfaces
- Copy interface.template into /etc/network/services/(interface), once for
  each interface associated with the namespace
- Edit each new /etc/network/services/(interface) file:
  - replace 'xxMACADDRxx' with a unique mac address for the interface
  - replace 'xxNAMESPACExx' with the namespace name
  - replace 'xxINTERFACExx' with the interface name
  - replace 'xxIPADDRxx' with the IPv4 address for this interface
  - replace 'xxIP6ADDRxx' with the IPv6 address for this interface (or just
    comment out the whole inet6 stanza if not in use)
  - replace 'xxBRIDGExx' with the bridge name for this interface
  - if needed, uncomment and insert the 'ip route add' line(s) before the
    'brctl' line in each stanza, replacing 'xxROUTERxx' and 'xxV6ROUTERxx'
    with the gateway IPs.
- Install netns@.service in /etc/systemd/system if it's not already there.
- Copy the service unit file for the service that will run in the
  namespace into /etc/systemd/system; if it's already there you may want
  to save a copy somewhere else as it will be edited.
- Edit the service unit file(replacing xxNAMESPACExx with the namespace name):
    - Under [Unit] add:
      - After=netns@xxNAMESPACExx.service
      - BindsTo=netns@xxNAMESPACExx.service
      - It may also be necessary to add 'After=network.target'
    - Under [Service]:
      - change ExecStart to begin with '/usr/sbin/ip netns exec xxNAMESPACExx'
- Run 'systemctl daemon-reload' to re-read the files and look for errors
  with 'journalctl -e'
- Start the service
- you can check on things with 'ip netns list' and
  'ip netns exec (namespace) ip addr show' and
  'ip netns exec (namespace) ip route show'


# Notes
- This really is a hack, if you can think of a better approach you're probably
  right to try that instead.  It does what I needed at the time.
- I use 2000::/3 as the default IPv6 route for historical reasons, it should
  probably be changed to 'default'.
- This does not work for NFS because the kernel NFS server is not
  namespace-aware.
- If you're using NetworkManager or some other network configuration 'tool',
  you'll need to figure out where the interface configuration goes... I think
  the split between namespace and service interface configuration should still
  work though.


