from pybird import PyBird

pybird = PyBird(socket_file="/var/run/bird/bird.ctl")
peer_state = pybird.get_peer_status()
print(peer_state)
for peer in peer_state:
    received = pybird.get_peer_prefixes_accepted(peer_name=peer.get('name'))
    print(received)
    for prefix in received:
        print(f"Prefix {prefix.get('prefix')} via {prefix.get('next_hop')} -- {prefix.get('as_path')} -- from {prefix.get('peer')} - at {prefix.get('time')}")

status = pybird.get_bird_status()
print(status)
