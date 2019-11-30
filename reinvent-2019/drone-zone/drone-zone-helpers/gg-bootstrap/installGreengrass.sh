wget https://d1onfpft10uf5o.cloudfront.net/greengrass-core/downloads/1.10.0/greengrass-linux-aarch64-1.10.0.tar.gz
sudo tar -xzvf greengrass-linux-aarch64-1.10.0.tar.gz -C /

wget https://www.amazontrust.com/repository/AmazonRootCA1.pem -O root.ca.pem

if [ -d "/lib/systemd/system" ]; then
    echo "systemd detected"

    if [ ! -f "/lib/systemd/system/greengrass.service" ]; then
        echo "Creating Greengrass systemd service"
        cp greengrass.service /lib/systemd/system/greengrass.service
        systemctl daemon-reload
        systemctl enable greengrass
    else
        echo "Greengrass service already exists, skipping installation of systemd file"
    fi
fi
