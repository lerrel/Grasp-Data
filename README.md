Instructions to download and display the Patch dataset used in training grasping network in
https://arxiv.org/pdf/1609.09025v1.pdf

**Download the dataset**
```
cd Grasp-Data
wget https://www.dropbox.com/s/652sken7f5hqi68/Patch_Dataset.tar.gz
tar -xvzf Patch_Dataset.tar.gz
mv Patch_Dataset data
```
The dataset contains 3 folders: Train, Validation and Test.
Each of these folders contains folders for positive (successful grasps) and negative (unsuccessful) data. Each of these folders contain a folder Images that contains the patches and a text file dataInfo.txt that contains names of patch and corresponding grasp angle attempted.

**Read the dataset with python visualization code**
```
python display_data.py --dat 'Train' --pos 1 --ran 0 --msec 1000
```

Contact Lerrel Pinto lerrelpATcsDOTcmuDOTedu for more information.
