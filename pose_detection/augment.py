import tensorflow as tf
import numpy as np
import cv2
import time
from scipy.ndimage.interpolation import rotate

"""
This class is a generator with data augmentation techniques built in (for use 
with image data. The generator augments the data using randomized values based
on the translate, flip, roatate, and noise parameters. For each nonzero value 
in these parameters, a random value is generated using that value as a max/min
value. The dataset is then copied and augmented using the random value. The 
augmented copy is then appended to the end of the original dataset. This means 
that augmentations do not overlap (eg. a translated vector is never rotated). 
The dataset is then output in batches until there isn't enough data for a full 
batch. At this point, the used dataset is removed and a new one is generated 
using new random values.
"""

class Generator(object):
	# Initialize object with base level parameters
	def __init__(self,x,y,translate=[0,0],flip=[0,0],rotate=0,noise=0):
		# Store original dataset and parameter values
		self.x = x
		self.y = y
		self.num_samples = x.shape[0]
		self.translate = translate
		self.rotate = rotate
		self.noise = noise
		self.flip = ['none']
		if flip[0] == 1:
			self.flip.append('horizontal')
		if flip[1] == 1:
			self.flip.append('vertical')
		if flip[0] == 1 and flip[1] == 1:
			self.flip.append('both')

		# Create randomized parameters and augment data
		self.__randomize_params()
		self.__aug_data()

	# Creates random parameters to augment the original dataset with
	def __randomize_params(self):
		########## Check how to break this up in an appropriate way
		self.shift_width = np.random.randint(low=-self.translate[0],high=self.translate[0]) if self.translate[0] else 0
		self.shift_height = np.random.randint(low=-self.translate[0],high=self.translate[1]) if self.translate[1] else 0
		self.curr_flip = np.random.choice(self.flip)
		self.curr_rot = np.random.uniform(-self.rotate,self.rotate)
		self.curr_noise = np.random.uniform(0,self.noise)

	# Augment data using randomized parameters
	def __aug_data(self):

		# Copy x and y
		self.x_aug = self.x
		self.y_aug = self.y

		# Shift horizontally and vertically
		if self.shift_width != 0 or self.shift_height !=0:
			self.x_aug = np.vstack((self.x_aug,np.roll(self.x,shift=(self.shift_height,self.shift_width),axis=(1,2))))
			self.y_aug = np.hstack((self.y_aug,self.y))

		# Flip values
		if self.curr_flip != 'none':
			if self.curr_flip == 'horizontal':
				self.x_aug = np.vstack((self.x_aug,np.flip(self.x,axis=1)))
				self.y_aug = np.hstack((self.y_aug,self.y))
			elif self.curr_flip == 'vertical':
				self.x_aug = np.vstack((self.x_aug,np.flip(self.x,axis=2)))
				self.y_aug = np.hstack((self.y_aug,self.y))
			else:
				flipped = np.flip(self.x,axis=1)
				self.x_aug = np.vstack((self.x_aug,np.flip(flipped,axis=2)))
				self.y_aug = np.hstack((self.y_aug,self.y))

		# Rotate by random value
		if self.curr_rot != 0:
			self.x_aug = np.vstack((self.x_aug,rotate(self.x,self.curr_rot,axes=(1,2),reshape=False)))
			self.y_aug = np.hstack((self.y_aug,self.y))

		# Add noise to values
		if self.curr_noise != 0:
			self.x_aug = np.vstack((self.x_aug,self.x+np.random.normal(0,self.curr_noise,self.x.shape)))
			self.y_aug = np.hstack((self.y_aug,self.y))

	# Returns size of augmented data
	def aug_size(self):
		return self.x_aug.shape[0]

	# Generate batch if there is enough data, else, augment, shuffle, and return
	def gen_batch(self,batch_size,shuffle=True):
		total_poss = int(self.num_samples/batch_size) - 1
		count = 0

		while True:
			if count < total_poss:
				count += 1
				yield((self.x_aug[count*batch_size:(count+1)*batch_size],self.y_aug[count*batch_size:(count+1)*batch_size]))
			else:

				self.__randomize_params
				self.__aug_data()

				if shuffle:
					s = np.arange(self.x_aug.shape[0])
					shuff = np.random.shuffle(s)
					self.x_aug = self.x_aug[s]
					self.y_aug = self.y_aug[s]

				count = 0
