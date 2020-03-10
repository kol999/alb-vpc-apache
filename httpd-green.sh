#!/bin/sh

#install httpd
yum install httpd -y

#enable and start httpd
systemctl enable httpd
systemctl start httpd

/bin/cat >/var/www/html/index.html <<EOL
<html>
    <body bgcolor="skyblue">
        <div align="center">
            <h1>Welcome to AWS!</h1>
            <h4>Hostname: $(hostname -f)</h4>
        </div>
    </body>
</html>
EOL

cd /tmp
yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
systemctl enable amazon-ssm-agent
systemctl start amazon-ssm-agent

amazon-linux-extras install epel -y 
yum -y update 

