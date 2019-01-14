cd ~/threat_detection/azure



mkdir -p ~/datasets/automatic_rifle &&  python dl_query.py --api $AZURE_KEY_1 --query "automatic rifle" --output ~/datasets/automatic_rifle
mkdir -p ~/datasets/assault_rifle &&  python dl_query.py --api $AZURE_KEY_1 --query "assault rifle" --output ~/datasets/assault_rifle
mkdir -p ~/datasets/machine_gun &&  python dl_query.py --api $AZURE_KEY_1 --query "machine gun" --output ~/datasets/machine_gun
mkdir -p ~/datasets/hand_gun &&  python dl_query.py --api $AZURE_KEY_1 --query "hand gun" --output ~/datasets/hand_gun
mkdir -p ~/datasets/pistol &&  python dl_query.py --api $AZURE_KEY_1 --query "pistol" --output ~/datasets/pistol

mkdir -p ~/datasets/pistol_in_hand &&  python dl_query.py --api $AZURE_KEY_1 --query "pistol in hand" --output ~/datasets/pistol_in_hand


