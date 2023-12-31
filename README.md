# Deploy Wazuh Docker in single node configuration

This deployment is defined in the `docker-compose.yml` file with one Wazuh manager containers, one Wazuh indexer containers, and one Wazuh dashboard container. It can be deployed by following these steps: 

1) Increase max_map_count on your host (Linux). This command must be run with root permissions:
```
$ sysctl -w vm.max_map_count=262144
```
2) Run the certificate creation script:
```
$ docker-compose -f generate-indexer-certs.yml run --rm generator
```
3) Start the environment with docker-compose:

- In the foregroud:
```
$ docker-compose up
```
- In the background:
```
$ docker-compose up -d
```

The environment takes about 1 minute to get up (depending on your Docker host) for the first time since Wazuh Indexer must be started for the first time and the indexes and index patterns must be generated.


# Remove thread found on Virus Total
Place this remove-threat.sh script in /var/ossec/active-response/bin/
```
#!/bin/bash

# Checking user arguments
if [ "x$1" == "xdelete" ]; then
    exit 0;
fi

LOCAL=`dirname $0`;
cd $LOCAL
cd ../

PWD=`pwd`

# Removing file
rm -f $3
if [ $? -eq 0 ]; then
    echo "`date` $0 Removed positive threat located in $3" >> ${PWD}/../logs/active-responses.log
else
    echo "`date` $0 Error removing positive threat located in $3" >> ${PWD}/../logs/active-responses.log
fi

exit 0;
```
And also change this section of /var/ossec/etc/ossec.conf to
```
<!-- Directories to check  (perform all possible verifications) -->
    <directories>/etc,/usr/bin,/usr/sbin</directories>
    <directories check_all="yes" whodata="yes" realtime="yes">/bin,/sbin,/boot</directories>
```
make sure realtime="yes"

Set permissions to the remove-threat.sh
```
chown root:wazuh /var/ossec/active-response/bin/remove-threat.sh
chmod 750 /var/ossec/active-response/bin/remove-threat.sh
```
Then restart the Wazuh Agent
```
systemctl restart wazuh-agent
```
# final-p-wazuh
