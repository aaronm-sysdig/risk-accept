# risk-accept.py
A python script to mass import/update vulnerability acceptances.  For each vuln it will first check if there is one there already.  If there is, it will delete it then add in the new one.

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

## Execution
eg:
```
python3 riskAccept.py
```

## Docker
Execution within a docker container is also possible.  a Dockerfile is provided

## Inline pipeline processsing
Also possible.  Here is an example Github Action to demonstrate how.  the `docker run` command will require a little modification depending upon your usage but the broad strokes are you need to set the required environment variables and mount in a folder that contains your csv file for processing.  Once all that lines up it will run.

```
name: risk-accept Pipeline Run Example

on:
  workflow_dispatch:

env:
  IMAGE_NAME: ghcr.io/aaronm-sysdig/risk-accept:latest # Image name
  SECURE_API_TOKEN: ${{ secrets.SECURE_API_TOKEN }} # Secure API token
  API_URL: "https://app.au1.sysdig.com" # API URL
  MAX_DAYS: "31" # Max days
  RISKS_CSV: "/risks/risks.csv" # Path to where the risks.csv file will be located
  REPO_RISKS_FOLDER: "/risks" # Houses a risks.csv example
  
jobs:
  run:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    
    - name: Log in to GitHub Container Registry
      uses: docker/login-action@v1
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    - name: Show Risk Directory
      run: |
        ls -l ${{ github.workspace }}${{ env.REPO_RISKS_FOLDER }}

    - name: Run risk-accept
      run: |
        docker run \
        -e RISKS_CSV="${{ env.RISKS_CSV }}" \
        -e SECURE_API_TOKEN="${{ env.SECURE_API_TOKEN }}" \
        -e API_URL="${{ env.API_URL }}" \
        -e MAX_DAYS="${{ env.MAX_DAYS }}" \
        -v ${{ github.workspace }}${{ env.REPO_RISKS_FOLDER }}:${{ env.REPO_RISKS_FOLDER }} ${{ env.IMAGE_NAME }}
```
## Example Github Execution rsults
As you can see it will just post its results to the STDOUT

```
Digest: sha256:7047e22e1e1748c83d3254d11b599653960bdcbf7cd474019e7e94bdd21d036d
Status: Downloaded newer image for ghcr.io/aaronm-sysdig/risk-accept:latest
Processing Input File '/risks/risks.csv'
Delete Status: 200, CVE: CVE-2018-19360
Create Status: 201, CVE: CVE-2018-19360, Expiration Date: 2023-06-30
Delete Status: 200, CVE: CVE-2018-19361
Create Status: 201, CVE: CVE-2018-19361, Expiration Date: 2023-06-30
Delete Status: 200, CVE: CVE-2018-19362
Create Status: 201, CVE: CVE-2018-19362, Expiration Date: 2023-06-30
Delete Status: 200, CVE: CVE-2018-8088
Create Status: 201, CVE: CVE-2018-8088, Expiration Date: 2023-06-30
```
