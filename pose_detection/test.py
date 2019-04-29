
import numpy as np

x = np.empty((1,9,2))
rele_dexes = [1,2,3,4,5,6,7,9,12]
right_elbow = 3
right_wrist = 4

# folders = ["High_ordered/keypoints/", "Medium_ordered/keypoints/", "Low_ordered/keypoints/"]
# threats = [0,1,2]
# y = []
# last_count = 0


file = "/home/benjamin/threat_detection/detect_threat_level/High_ordered/keypoints/high_aggressive_001168.npy"

skeletons = np.load(file)
if skeletons.size != 1:
	for skele in skeletons:
		print("\n\nskele.shape = {}").format(skele.shape)
		print("skeleton:\n{}").format(skele)

		# print("skele[rele_dexes] = {}").format(skele[rele_dexes])
		# if skele[rele_dexes].all() > .0001:
		# 	skele[:,0:2] -= skele[right_elbow,0:2]
		# 	print("skele[:,0:2] -= skele[right_elbow,0:2]")
		# 	print("skele[:,0:2] = ").format(skele[:,0:2])

