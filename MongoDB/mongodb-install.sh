#!/usr/bin/env bash

# Import the public key used by the package management system
curl -fsSL https://pgp.mongodb.com/server-6.0.pub | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg

if [ -f /usr/share/keyrings/mongodb-server-6.0.gpg ]; then
   echo "MongoDB public key successfully imported"
else
   echo "MongoDB public key import failed"
   # If gnupg is not installed, install it
   sudo apt-get install gnupg
   # Import the public key used by the package management system
   curl -fsSL https://pgp.mongodb.com/server-6.0.pub | \
      sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg
fi

# Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 signed=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | \
sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Reload local package database
sudo apt-get update

# Install the MongoDB packages
sudo apt-get install -y mongodb-org

# Install the MongoDB
sudo apt install mongodb-server-core

# Start MongoDB
sudo service mongod start

# Verify that MongoDB has started successfully
sudo service mongod status