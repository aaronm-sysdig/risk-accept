# Disclaimer

Notwithstanding anything that may be contained to the contrary in your agreement(s) with Sysdig, Sysdig provides no support, no updates, and no warranty or guarantee of any kind with respect to these script(s), including as to their functionality or their ability to work in your environment(s).  Sysdig disclaims all liability and responsibility with respect to any use of these scripts. 

# Sysdig Risk Acceptance as code Example
Example python code that allows you to manage your Sysdig Vulnerability Risk Acceptance as code.

***NOTE: This script uses unsupported, undocumented API's that may change at any point.***

## CSV File format
Create a CSV file in with the following columns for your risk you want to accept

| Field | Mandatory? | Note |
|---|---|---|
| Vulnerability | Y | CVE ID of the vulnerability you want to accept the risk for |
| Expiration Date | Y | Expiration Date you want the risk to expire at in format YYYY-MM-DD |
| Reason | Y | One of the following Values `RiskOwned, RiskTransferred, RiskAvoided, RiskMitigated, RiskNotRelevant, Custom`  |
| Description | Y | Description of Who and Why Accepted the Risk |
| Package Name | N | Used if you want to scope the exception to a certain package. ie `com.fasterxml.jackson.core:jackson-databind` | 
| Package Version | N | Used if you want to scope the exception to a certain package version. ie `2.9.7` | 
| Image Name | N | Used if you want to scope the exception to a certain image (all packages in an image) ie `ghcr.io/aaronm-sysdig/text4shell-docker-vuln:13` |

### Example CSV enteries

Accept CVE-2018-19360 globally across all images & packages until 30th July 2023 with the Reason of Risk Owned

```
"Vulnerability","Expiration Date","Reason","Description","Package Name","Package Version","Image Name"
"CVE-2018-19360","2023-07-30","RiskOwned","Base Image patch due to be rolled out environment wide on 15th July","","",""
```

Accept CVE-2018-19361 for the package `com.fasterxml.jackson.core:jackson-databind` until 30th July 2023 with the Reason of Risk Owned

```
"Vulnerability","Expiration Date","Reason","Description","Package Name","Package Version","Image Name"
"CVE-2018-19361","2023-07-30","RiskOwned","Base Image patch due to be rolled out environment wide on 15th July","com.fasterxml.jackson.core:jackson-databind","",""
```

Accept CVE-2018-19362 for the package `com.fasterxml.jackson.core:jackson-databind` version `2.9.7` until 30th July 2023 with the Reason of Risk Owned

```
"Vulnerability","Expiration Date","Reason","Description","Package Name","Package Version","Image Name"
"CVE-2018-19362","2023-07-30","RiskOwned","Base Image patch due to be rolled out environment wide on 15th July","com.fasterxml.jackson.core:jackson-databind","2.9.7",""
```

Accept CVE-2018-19362 for the image `ghcr.io/aaronm-sysdig/text4shell-docker-vuln:13` until 30th July 2023 with the Reason of Risk Owned

```
"Vulnerability","Expiration Date","Reason","Description","Package Name","Package Version","Image Name"
"CVE-2018-8088","2023-07-30","RiskOwned","Base Image patch due to be rolled out environment wide on 15th July","","","ghcr.io/aaronm-sysdig/text4shell-docker-vuln:13"
```

## Parameters
Set the below environment variables

```
# Your Sysdig Secure API Token
export SECURE_API_TOKEN=1c708a83-e413-4c45-87fc-9df23163ca82 

# Max # of Days from today that the expiration in the CSV is allowed to be in the future
export MAX_DAYS=30 

# Your Sysdig Secure region URL
export API_URL=https://app.au1.sysdig.com 

# Path to your defined csv file
export RISKS_CSV=./risks/risks.csv 
```

## Usage
```
pip3 install -r requirements.txt
python3 risk-accept.py
```

## Docker
```
export RISKS_CSV=/risks/risks.csv 
docker run \                     
  -e RISKS_CSV="$RISKS_CSV" \
  -e SECURE_API_TOKEN="$SECURE_API_TOKEN" \
  -e API_URL="$API_URL" \
  -e MAX_DAYS="$MAX_DAYS" \
   -v $PWD/risks:/risks ghcr.io/aaronm-sysdig/risk-accept:latest
```

## Inline pipeline processsing
An example Github Action to demonstrate how this can be used in your Github repo, where you can store your risk acceptance with your code/pipeline

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
## Example output

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
