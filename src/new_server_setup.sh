#################################
##
##  New Debian Server Setup
##
#################################

#####
## Useful commands
#####
# get hostname detail
# hostnamectl


########################
# initial root env
su -

# create new user
adduser gsm_admin
adduesr webserver_admin

# add user to sudeors
usermod -aG sudo gsm_admin
usermod -aG sudo webserver_admin


# update apt-get
sudo apt-get update

# verify openssh is installed
sudo apt install openssh-server

# install and configure git
sudo apt install git
git config --global user.name "gsm_admin"
git config --global user.email "gsm_admin@homelabs.com"

# Go to directory for git repo save locations
cd /home/gsm_admin/

# generate key pair for git. add pub ssh key to github
ssh-keygen

# clone the repo 
git clone git@github.com:benvneal88/homelabs.git


# clone webserver files
cd /home/webserver_admin/
# generate key pair for git. add pub ssh key to github
ssh-keygen
git clone git@github.com:benvneal88/ncaa-bb-fantasy-manager.git


# To prevent your Linux system from suspending or going into hibernation, disable the following systemd targets:
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# install docker 
# https://docs.docker.com/engine/install/debian/

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# add user to docker group for permissions
sudo usermod -a -G docker gsm_admin

# test
sudo docker run hello-world 

#copy file from docker
docker exec pzserver cp

# Python setup
apt-get install python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip


#ssh gsm_admin@192.168.86.240


# from src.linuxgsm import api
# api.copy_file_to_container(api.get_docker_client().containers.get('pzserver'), "/home/gsm_admin/homelabs/src/linuxgsm/api.py", "/home/linuxgsm/")
# api.patch_game_server('pzserver')
