### SERVER ###
def notifie_attack_incomming(packet, main):
    main.AppIndicator.notify_attack_incoming(packet.data)

def receive_hosts(packet, main):
    for row in main.AttackWindow.list_host_store:
        is_select = False
        (model, pathlist) = main.AttackWindow.list_host_view.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            if row[0] == model.get_value(tree_iter,0):
                is_select = True

        remove = True
        for host_data in packet.data:
            if row[0] == host_data["ip"] and row[1] == host_data["mac"] and row[2] == host_data["vendor"] and row[3] == host_data["os"]:
                remove = False
        if remove and not is_select:
            main.AttackWindow.list_host_store.remove(row.iter)

    for host_data in packet.data:
        append = True
        for row in main.AttackWindow.list_host_store:
            if row[0] == host_data["ip"]:
                append = False
        if append:
            main.AttackWindow.list_host_store.append([host_data["ip"], host_data["mac"], host_data["vendor"], host_data["os"]])


### DAEMON ###

def receive_selection(packet, main):
    main.HostMgr.diselect_all()
    for host in packet.data:
        main.HostMgr.select_host(host)

def receive_attack_state(packet, main):
    main.AttackProcess.is_attacking = packet.data

process = {}
process[0] = notifie_attack_incomming
process[1] = receive_hosts

process[2] = receive_selection
process[3] = receive_attack_state

def process_packet(packet, main):
    global process
    process[packet.id](packet, main)