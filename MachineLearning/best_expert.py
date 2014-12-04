import random
import math

def run(f, predictors, max_iterations):
	
	models = [1.0 for i in xrange(len(predictors))]
	
	mistakes = 0
	predictor_mistakes = [0 for i in xrange(len(predictors))]
	
	for j in xrange(max_iterations):
		
		predictions = [p() for p in predictors]
		print models
		
		d = [0, 0]
		for i in xrange(len(predictions)):
			if (predictions[i] == 0):
				d[0] += models[i]
			else:
				d[1] += models[i]
		
		guess = 0
		if (d[1] > d[0] or (d[1] == d[0] and random.random() > 0.5)):
			guess = 1
		
		actual = f()
		
		if (actual != guess):
			mistakes += 1
		
		for i in xrange(len(predictions)):
			if (predictions[i] != actual):
				models[i] = (models[i] / 2.0)
				predictor_mistakes[i] += 1
				
		
		total = sum(models)
		models = map(lambda m : m / total, models)
				
		print "----------------------------------------"
		print "Running Simulation on Iteration %d" %(j)
		print "Guess: %d" %(guess)
		print "Actual: %d" %(actual)
		print "Total Mistakes: %d" %(mistakes)
		print "Best Predictor Mistakes %d" %(min(predictor_mistakes))
		
		
def test():
	f = lambda : 1
	predictors = [lambda : 1, lambda : 0]
	run (f, predictors, 100)
	
test()