if [ ! -d "data/Source/OctoberGPS" ] 
then
    # 1. Download OctoberGPS.zip -> ./data/OctoberGPS.zip
    wget https://waste-labs-repo-data-adil.s3-ap-southeast-1.amazonaws.com/OctoberGPS.zip -P ./data/Source/

    # 2. Unzip ./data/OctoberGPS.zip -> ./data/OctoberGPS/
    unzip ./data/Source/OctoberGPS.zip -d ./data/Source/

    rm -rf ./data/Source/OctoberGPS.zip
else
    echo "WARNING: data/source/OctoberGPS already exists!"
fi