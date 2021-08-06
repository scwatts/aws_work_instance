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

# Install Miniconda
# Download installer and run
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh
/bin/bash Miniconda3-py39_4.9.2-Linux-x86_64.sh -b -p /data/miniconda3/
# Create alias to pull conda into PATH
echo "alias conda-init='. /data/miniconda3/etc/profile.d/conda.sh'" >> /home/ec2-user/.bashrc
# Clean up
rm Miniconda3-py39_4.9.2-Linux-x86_64.sh  Miniconda3-py39_4.9.2-Linux-x86_64.sh.sha256sum

# Change owner to ec2-user
chown -R ec2-user /data/

# Enable terminal vi mode
echo 'set -o vi' >> /home/ec2-user/.bashrc

# Flag that setup has completed
touch /home/ec2-user/ready
