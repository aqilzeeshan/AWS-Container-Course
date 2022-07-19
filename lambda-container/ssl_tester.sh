#/bin/bash
EVENT=$1
RESULTS=""
# extract json array of domains
DOMAINS=$(echo $EVENT | jq -r '.[]')
# loop thru the array of domains
for domain in $DOMAINS; do
  echo Checking domain: $domain 1>&2;
  # openssl client connect to the domain and extract the certificate
  expires=$(echo | openssl s_client -connect "${domain}:443" -servername "$domain" 2> /dev/null | openssl x509 -enddate -noout)
  status=$?
  if [ $status -eq 1 ]; then
    # return an error if openssl fails
    expires="error accessing domain"
  fi
  # combine the results for each domain into json
  RESULTS+=$(jq -n --arg domain "$domain" --arg expires "$expires"  '{ "domain" : $domain, "valid": $expires }')
done
# return the combined json
echo $RESULTS | jq -s .
