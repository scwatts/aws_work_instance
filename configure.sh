#!/bin/bash
# Set up attached block device
sudo mkfs -t xfs /dev/sdb
sudo mkdir /data/
sudo mount /dev/sdb /data/
sudo chown ec2-user /data/

# Install software through yum
sudo yum install -y docker htop git

# Configure docker
# Set docker storage base directory to external device
mkdir -p /data/docker/
sudo sed -i 's#^\(OPTIONS=["'\'']\)#\1-g /data/docker/ #' /etc/sysconfig/docker
# Enable and start service, add user to docker group
sudo systemctl enable --now docker.service
sudo usermod -aG docker ec2-user

# Install Mambaforge
# Download installer and run
wget 'https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh'
/bin/bash Mambaforge-Linux-x86_64.sh -b -p /data/mambaforge/
# Create alias to pull conda into PATH
cat << EOF >> /home/ec2-user/.bashrc
alias conda-init='eval "\$(/data/mambaforge/bin/conda shell.bash hook)"'
EOF
# Clean up
rm Mambaforge-Linux-x86_64.sh

# Change owner to ec2-user
chown -R ec2-user /data/

# Enable terminal vi mode
echo 'set -o vi' >> /home/ec2-user/.bashrc

# Flag that setup has completed
touch /home/ec2-user/ready
