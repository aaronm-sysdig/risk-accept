import copy
import csv
import datetime
import json
import os
import requests
import time

SLEEP_429_SECONDS = 30

auth_header = {
    "Authorization": f"Bearer {os.environ.get('SECURE_API_TOKEN', None)}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "riskAcceptanceDefinitions": [
        {
            "entityType": "vulnerability",
            "entityValue": "",
            "expirationDate": "",
            "context": [],
            "reason": "",
            "description": ""
        }
    ]
}


def sysdig_request(method, url, headers, _json={}) -> requests.Response:
    objResult = requests.request(method=method, url=url, headers=headers, json=_json)
    while objResult.status_code == 429:
        console_log(f"Got status 429, Sleeping for {SLEEP_429_SECONDS} seconds before trying again")
        time.sleep(SLEEP_429_SECONDS)
        objResult = requests.request(method=method, url=url, headers=headers, json=_json)
    return objResult


def console_log(log_entry):
    with open('TataDigitalImport-v2.log', 'a') as file_object:
        file_object.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {log_entry}\n")
        print(f"{log_entry}")


def main() -> None:
    console_log(f"Processing Input File '{risks_csv}'")
    with open(risks_csv) as csvfile:
        arrRisks = list(csv.reader(csvfile, delimiter=','))

    # Ignore header row
    arrRisks.pop(0)

    arrPayload = []

    for row in arrRisks:
        # Checking if expiration is no greater than the max_days
        expirationDate = datetime.datetime.strptime(row[1], '%Y-%m-%d').date()
        maxExpirationDate = datetime.date.today() + datetime.timedelta(days=int(max_days))
        if expirationDate > maxExpirationDate:
            print(f"ERROR: Expiration Date for {row[0]} of {expirationDate} exceeds the maximum ({max_days}) days, I.E {maxExpirationDate}")
            exit(1)
        # Global
        objRisk = copy.deepcopy(payload)
        objRisk['riskAcceptanceDefinitions'][0]['entityValue'] = row[0]
        objRisk['riskAcceptanceDefinitions'][0]['expirationDate'] = row[1]
        objRisk['riskAcceptanceDefinitions'][0]['reason'] = row[2]
        objRisk['riskAcceptanceDefinitions'][0]['description'] = row[3]

        # Package - No Version
        if row[4] != '':
            objRisk['riskAcceptanceDefinitions'][0]['context'].append(
                {
                    "contextType": "packageName",
                    "contextValue": str(row[4])
                })

        # Package - Version
        if row[5] != '':
            objRisk['riskAcceptanceDefinitions'][0]['context'].append(
                {
                    "contextType": "packageVersion",
                    "contextValue": str(row[5])
                })

        # Image
        if row[6] != '':
            objRisk['riskAcceptanceDefinitions'][0]['context'].append(
                {
                    "contextType": "imageName",
                    "contextValue": str(row[6])
                })

        arrPayload.append(objRisk)

    strAddRiskURL = f"{api_url}/api/scanning/riskmanager/v2/definitions"
    for row in arrPayload:
        # Check for existing Risk
        strCheckRiskURL = f"{api_url}/api/scanning/riskmanager/v2/definitions?cursor=&filter=freeText+in+%28%22"\
                          f"{row['riskAcceptanceDefinitions'][0]['entityValue']}"\
                          f"%22%29&limit=100&sort=acceptanceDate&order=desc"
        objResult = sysdig_request(method='GET', url=strCheckRiskURL, headers=auth_header)
        if objResult.status_code == 200:
            objJsonResult = json.loads(objResult.text)
            if objJsonResult['page']['matched'] > 0:
                # I.E we found one
                strDeleteRiskURL = f"https://app.au1.sysdig.com/api/scanning/riskmanager/v2/definitions/"\
                                   f"{objJsonResult['data'][0]['riskAcceptanceDefinitionID']}"
                # Now we delete it
                objResult = sysdig_request(method='DELETE', url=strDeleteRiskURL, headers=auth_header)
                console_log(f"Delete Status: {objResult.status_code}, CVE: {json.loads(objResult.text)['entityValue']}")
                time.sleep(2)  # gives backend to sync
        objResult = sysdig_request(method='POST', url=strAddRiskURL, headers=auth_header, _json=row)
        if objResult.status_code == 201:
            console_log(f"Create Status: {objResult.status_code}, "
                        f"CVE: {json.loads(objResult.text)['riskAcceptanceDefinitions'][0]['entityValue']}, "
                        f"Expiration Date: {json.loads(objResult.text)['riskAcceptanceDefinitions'][0]['expirationDate']}")
        else:
            console_log(f"Status: {objResult.status_code}, Error Reason: {objResult.text}")


if __name__ == "__main__":
    secure_api_token = os.environ.get('SECURE_API_TOKEN', None)
    max_days = os.environ.get('MAX_DAYS', None)
    api_url = os.environ.get('API_URL', None)
    risks_csv = os.environ.get('RISKS_CSV', None)
    if secure_api_token is not None and max_days is not None and api_url is not None and risks_csv is not None:
        main()
    else:
        if secure_api_token is None:
            print(f"Error: API Token not set. Hint: Set 'SECURE_API_TOKEN' environment variable)")
        if max_days is None:
            print(f"Error: Max Days not set. Hint: Set 'MAX_DAYS' environment variable")
        if api_url is None:
            print(f"Error: API Url not set. Hint: Set 'API_URL' environment variable")
        if risks_csv is None:
            print(f"Error: Risks CSV not set. Hint: Set 'RISKS_CSV' environment variable")
        exit(1)

