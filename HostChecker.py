import requests
import csv


def requestToken():
    session = requests.session()
    session.headers = {'content-type':'application/x-www-form-urlencoded','accept': 'application/json'}
    data = {'client_id':'--add your client id here--','client_secret':'--add your client secret here--'}
    response = session.post("https://api.crowdstrike.com/oauth2/token",data=data).json()
    token = response['access_token']
    #print(token)
    return token

def hostCheck(token,hostname):
    session = requests.session()
    session.headers = {'accept': 'application/json','authorization': 'Bearer '+token}
    response = session.get("https://api.crowdstrike.com/devices/queries/devices/v1?filter=hostname:"+"'"+hostname+"'").json()
    return response

def hostCheckByIP(token,IP):
    session = requests.session()
    session.headers = {'accept': 'application/json', 'authorization': 'Bearer ' + token}
    response = session.get("https://api.crowdstrike.com/devices/queries/devices/v1?filter=local_ip:" + "'" + IP + "'").json()
    if response['meta']['pagination']['total'] == 1:
        agentID = response['resources']
        response = session.get("https://api.crowdstrike.com/devices/entities/devices/v1?ids=" +agentID[0]).json()
        #print(response)
        hostname = response['resources'][0]['hostname']
        #print(hostname)
        result = ['Reporting to CS Console.', str(IP + " address found and displaying hostname for this IP is - "+hostname)]
        return result
    else:
        result = ['Not Reporting to CS Console.', str(IP + " address not found.")]
        return result

with open('--set output file location here, ex:- C:\\Users\\Result.csv--','w',newline='') as out_server:
    with open('--set input file location here, ex:-C:\\Users\\host_list.csv') as in_server:
        server_in = csv.reader(in_server,delimiter=',')
        server_out = csv.writer(out_server,delimiter=',')
        line_count = 0
        token = requestToken()

        for row in in_server:
            row = list(row.split(","))
            if line_count == 0:
                row.append('cs_report_status')
                #print(row)
                server_out.writerow(row)
                line_count += 1
                cs_report_status = ''
            else:
                line_count += 1
                #hostname and IP values need to be changed according to input files coloumn numbers
                hostname = row[1]
                IP = row[3]
                hostname = hostname.upper()
                response = hostCheck(token,hostname)
                #print(response)
                #Identifying hostname format
                if "WILEY.COM" in hostname:
                    withDomain = True
                else:
                    withDomain = False

                if response['meta']['pagination']['total'] == 1:
                    print(str(line_count-1)+". "+hostname+" Reporting to CS Console.")
                    cs_report_status = 'Reporting to CS Console.'
                    row.append(cs_report_status)
                    #print(row)
                    server_out.writerow(row)
                elif (response['meta']['pagination']['total'] == 0) and (withDomain == True):
                    new_host_name = hostname.split('.',-1)
                    #print(new_host_name)
                    response = hostCheck(token,new_host_name[0])
                    if response['meta']['pagination']['total'] == 1:
                        print(str(line_count - 1) + ". " + hostname + " Reporting to CS Console.")
                        cs_report_status = 'Reporting to CS Console.'
                        row.append(cs_report_status)
                        #print(row)
                        server_out.writerow(row)
                    elif response['meta']['pagination']['total'] == 0:
                        cs_report_status = hostCheckByIP(token, IP)
                        print(str(line_count - 1)+". " +hostname+ " hostname not found. Switching to IP search. " +IP+" is "+ cs_report_status[0]+cs_report_status[1])
                        row.append(cs_report_status[0])
                        row.append(cs_report_status[1])
                        server_out.writerow(row)
                    else:
                        print(str(line_count - 1) + ". " + hostname + " Not Reporting to CS Console.")
                        cs_report_status = 'Not Reporting to CS Console.'
                        row.append(cs_report_status)
                        server_out.writerow(row)
                elif (response['meta']['pagination']['total'] == 0) and (withDomain == False):
                    new_hostname = hostname + "--add your domain here--"
                    #print(hostname)
                    response = hostCheck(token, new_hostname)
                    if response['meta']['pagination']['total'] == 1:
                        print(str(line_count - 1) + ". " + hostname + " Reporting to CS Console.")
                        cs_report_status = 'Reporting to CS Console.'
                        row.append(cs_report_status)
                        # print(row)
                        server_out.writerow(row)
                    elif response['meta']['pagination']['total'] == 0:
                        cs_report_status = hostCheckByIP(token, IP)
                        print(str(line_count - 1)+". " + hostname + " hostname not found. Switching to IP search.  " + IP+" is "+ cs_report_status[0]+cs_report_status[1])
                        row.append(cs_report_status[0])
                        row.append(cs_report_status[1])
                        server_out.writerow(row)
                    else:
                        print(str(line_count - 1) + ". " + hostname + " Not Reporting to CS Console.")
                        cs_report_status = 'Not Reporting to CS Console.'
                        row.append(cs_report_status)
                        server_out.writerow(row)
                elif (response['meta']['pagination']['total'] > 0):
                    cs_report_status = 'Error...! '+str(response['meta']['pagination']['total'])+' records showing up for given hostname. check these Agend IDs-> '+str(response['resources'])
                    row.append(cs_report_status)
                    server_out.writerow(row)
                    print(str(line_count - 1) +". Error...!!! " + str(response))
