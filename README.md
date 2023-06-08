# riskAccept.py
A python script to mass import/update vulnerability acceptances

## Parameters
Set the below environment variables

1) Your Secure API Token
```
SECURE_API_TOKEN=1c708a83-e413-4c45-87fc-9df23163ca82
```
2) Max Days that the CSV file expirations are allowed into the future
```
MAX_DAYS=31
```
3) API URL
```
API_URL=https://app.au1.sysdig.com
```
4) Risks CSV file that contains your risk acceptance data
```
RISKS_CSV=./risks.csv
```

## The CSV file containing your risks needs to be in the following format
```
"Vulnerability","Expiration Date","Reason","Description","Package Name","Package Version","Image Name"
```
For Example the below file provides examples of each possibility
0) Header row that will be ignored.  If you dont have a header row, your first row will be ignored... so have one.
1) Simple Global risk acceptance
2) Package acceptance for any version
3) Package acceptance for a specific version
4) Specific image
```
"Vulnerability","Expiration Date","Reason","Description","Package Name","Package Version","Image Name"
"CVE-2018-19360","2023-07-30","RiskAvoided","Some Description","","",""
"CVE-2018-19361","2023-06-30","RiskAvoided","Some Description","com.fasterxml.jackson.core:jackson-databind","",""
"CVE-2018-19362","2023-06-30","RiskAvoided","Some Description","com.fasterxml.jackson.core:jackson-databind","2.9.7",""
"CVE-2018-8088","2023-06-30","RiskAvoided","Some Description","","","ghcr.io/aaronm-sysdig/text4shell-docker-vuln:13"
```
nb: 'Reason' needs to match the reasons (case sensitive) that are present in the UI.  These are
```
RiskOwned
RiskTransferred
RiskMitigated
RiskNotRelevant
Custom
```
