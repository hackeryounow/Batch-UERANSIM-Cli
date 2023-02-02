from resources.ip import open5gsIP,gnbIP
import os
import time 

def gnb_config_init():
    filename = "./config/gnb/open5gs-gnb.yaml"
    os.system("sed -i 's/192.168.59.134/%s/g' %s" % (gnbIP, filename))
    os.system("sed -i 's/192.168.59.130/%s/g' %s" % (open5gsIP, filename))

def gnb_monitor():
    gnb_config_init()
    while True:
        gnbId = parse_gnb_id()
        while len(gnbId) == 0:
            start_gnb()
            gnbId = parse_gnb_id()
        amf_list_str = os.popen("nr-cli -e amf-list %s" % gnbId).read()
        amf_list = amf_list_str.split("\n")
        print("gnbId:"+ gnbId +"; " + "amf-list: " + str(amf_list))
        if "id" not in amf_list_str:
            print("waiting for restart gnb.")
            time.sleep(30)
            print("restarting gnb.")
            restart_gnb()
            print("gnb restarted.")
        
        time.sleep(2)

def parse_gnb_id():
    gnb_id_str = os.popen("nr-cli -d | grep gnb").read()
    gnb_ids = gnb_id_str.split("\n")
    return gnb_ids[0]

def restart_gnb():
    stop_gnb()
    start_gnb()

def start_gnb():
    config_file = "./config/gnb/open5gs-gnb.yaml"
    log_dir = "./logs/gnb"
    os.system("nohup nr-gnb -c %s > %s/gnb.out 2>&1 &" % (config_file, log_dir))

def stop_gnb():
    processes_str = os.popen("ps -a | grep nr-gnb").read()
    processes = processes_str.split("\n")[:-1]
    for gnb_process in processes:
        process_id = gnb_process.strip().split(" ")[0]
        if len(process_id) > 0:
            os.system("kill -9 " + process_id)
    

gnb_monitor()





gnb_monitor()


