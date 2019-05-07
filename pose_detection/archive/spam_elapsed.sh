echo " "
echo " "
echo " "
echo " "
cat timed_image_list.txt | while read line
do
   
   # VALUE=$(rosparam get $line)
   # echo "python threat_pipeline_single_image.py --image_path $line"
   python threat_pipeline_single_image.py --image_path $line
done
