#calculate the sum
def grades_sum(grades):
    total = 0
    for grade in grades: 
        total += float(grade)
    return total

#Take the average by adding up each grade    
def grades_average(grades):
    sum_of_grades = grades_sum(grades)
    average = sum_of_grades / float(len(grades))
    return average

#Here we calculate the variance given the formula above 
#by subtracting each score from the average and then taking square and rolling the sum. 
def grades_variance(scores):
    average = grades_average(scores)
    variance = 0
    for score in scores:
        variance = variance + (average - float(score)) ** 2
    
    return variance/len(scores)

def grades_std_deviation(variance):
    return variance ** 0.5


f=open("elapsed_time.txt", "r")
if f.mode == 'r': 
	contents =f.read()

times = list(contents.split("\n"))



sum_times = grades_sum(times)
avg_times = grades_average(times)
var_times = grades_variance(times)
std_times = grades_std_deviation(var_times)



total = 0
num_images = len(times)-1
for time in range(0,num_images):
	total += float(times[time])

print("total processing time {}").format(total)
print("total number of images {}").format(num_images)
print("average processing time {}").format(avg_times)
print("variance of processing time {}").format(var_times)
print("std of processing time {}").format(std_times)



# print grades_variance(times)

# #And here the standard deviation comes by taking square root of the variance
# variance = grades_variance(times)
    
# print grades_std_deviation(variance)


