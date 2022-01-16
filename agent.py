from random import uniform, seed, randint, choice
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
import sys
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
import csv
import analiza
import time



class Agent:

	def __init__(self, type, name, age, sex, job, color, status, risk):
		self.type = type
		self.name = name
		self.age = age
		self.sex = sex
		self.job = job
		self.color = color
		self.status = status
		self.risk = risk
		self.draw_location()

	def draw_location(self):
		self.location = uniform(0, 1), uniform(0, 1)
    
	def get_distance(self, other):
		a = (self.location[0] - other.location[0])**2
		b = (self.location[1] - other.location[1])**2
		return sqrt(a + b)

	def infect(self, agents, cycle_num, risk):
		distances = []
		for agent in agents:
			if self != agent and self.status == 'Infected':
				distance = self.get_distance(agent)
				distances.append((distance, agent))
		distances.sort()
		neighbors = [agent for d, agent in distances[:num_neighbors]]

		for agent in neighbors:
			agent.color = 'red'
			agent.status = 'Infected'
			agent.type = 0
			if(agent.risk < 40 and risk=='True'):
				agent.color = 'blue'
				agent.status = 'Healthy'
			list = [agent.name, agent.status, agent.age, agent.job, agent.sex, self.name]
			with open('analiza_simulacije.csv', 'a', ) as myfile:
				wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
				wr.writerow(list)
				
	    

		
			           
          
def plot_distribution(agents, cycle_num, risk):
	x_values_0, y_values_0 = [], []
	for agent in agents:
		x, y = agent.location
		x_values_0.append(x)
		y_values_0.append(y)
		print(f"Ovo je status agenta {agent.name}: {agent.status}, njihova boja: {agent.color} i njihov rizik: {agent.risk}")

	fig, ax = plt.subplots(figsize=(8, 8))
	plot_args = {'markersize': 8, 'alpha': 0.6}

	scat = ax.scatter(x=[], y=[], c='black', linewidths=4)
	ax.set_title(f'Cycle {cycle_num}')
	x = np.array(x_values_0).reshape(-1, 1)
	y = np.array(y_values_0).reshape(-1, 1)
	scat.set_offsets(np.concatenate((x, y), axis=1))
	if risk == 'False':
		scat.set_edgecolors(np.array([agent.color if agent.status=='Infected' else agent.color for agent in agents]))
		
	if risk == 'True':
		scat.set_edgecolors(np.array([agent.color if agent.status=='Infected' else agent.color if agent.risk > 30 else agent.color for agent in agents]))
		
	plt.scatter(x,y,c=np.array([agent.color if agent.status=='Infected' else agent.color for agent in agents]))	
	plt.savefig(f'konacni_rezultat_{cycle_num}.png')
	plt.show(block=False)
	plt.pause(3)
	plt.close()
  
def assign_job(age):
	job_list = ['GovtJob', 'PrivateJob', 'SelfEmployed','NoJob']   
	if(age < 18):
		return 'NoJob'
	else:
		return choice(job_list)

   
if __name__ == '__main__':
	
			
	print("Unesite opće podatke!")
	num_of_type_0 = int(input("Broj agenata u simulaciji: "))
	num_neighbors = int(input("Broj susjednih agenata koji se mogu zaraziti: "))
	
	num_of_type_1 = 1
    
	sex_list = ['M','Z']
	job_list = ['GovtJob', 'PrivateJob', 'SelfEmployed','NoJob'] 
		
	print("Izaberite između sljedećih scenarija: ")
	print("1. Jednostavni scenarij ")
	print("2. Scenarij s uključenim rizikom ")
	odabir = input("Vaš odabir: ")
	
	if odabir == '1':


		agents = [Agent(0, f"agent_{i}", randint(1,90), choice(sex_list), choice(job_list), 
		color='green', status='Healthy', risk=randint(1,100)) for i in range(num_of_type_0)]

		agents.extend(Agent(1, "infectious", randint(1,90),choice(sex_list), choice(job_list),
		color='red', status='Infected', risk=randint(1,100)) for i in range(num_of_type_1))

		header = ['agent_name', 'agent_status', 'agent_age', 'agent_job', 'agent_sex', 'infected_from']
		with open('analiza_simulacije.csv', 'a', ) as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow(header)
			
		iteration = 0
		
		while True:
			if any (agent.status!='Infected' for agent in agents):
				print('Entering loop ', iteration)
				plot_distribution(agents, iteration, risk='False')
				iteration += 1
				for agent in agents:
					agent.infect(agents,iteration, risk='False')

			if all (agent.status=='Infected' for agent in agents):
				plot_distribution(agents,iteration,risk='False')
				break
				
	if odabir == '2':
	
		faktor1 = 0
		faktor2 = 0
				
		agents = [Agent(0, f"agent_{i}", randint(1,90), choice(sex_list), job=None, 
		color='green', status='Healthy', risk=None) for i in range(num_of_type_0)]

		agents.extend(Agent(1, "infectious", randint(1,90),choice(sex_list), job=None,
		color='red', status='Infected', risk=None) for i in range(num_of_type_1))
		
		for agent in agents:
			agent.job = assign_job(agent.age)
			
			if agent.age <= 20:
				faktor1 = 20
			if agent.age >= 21 and agent.age <= 40:
				faktor1 = 35 
			if agent.age >= 41 and agent.age <= 60:
				faktor1 = 50
			if agent.age >= 61:
				faktor1 = 70 
		
			if agent.job == 'GovtJob':
				faktor2 = 80
			if agent.job == 'PrivateJob' or agent.job == 'SelfEmployed':
				faktor2 = 40
			if agent.job == 'NoJob':
				faktor2 = 20
			
			
			agent.risk = int((faktor1 + faktor2)/2)

			

		header = ['agent_name', 'agent_status', 'agent_age', 'agent_job', 'agent_sex', 'infected_from']
		with open('analiza_simulacije.csv', 'a', ) as myfile:
			wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
			wr.writerow(header)
			
		iteration = 0
		
		while True:
			if any (agent.status!='Infected' for agent in agents):
				print('Entering loop ', iteration)
				plot_distribution(agents, iteration, risk='True')
				iteration += 1
				for agent in agents:
					agent.infect(agents,iteration, risk='True')

			if all (agent.color=='red' or agent.color=='blue' for agent in agents):
				plot_distribution(agents,iteration,risk='True')
				agent = analiza.Agent("agent@rec.foi.hr","tajna")
				agent.start()
				print("Analyzing and generating report ......")
				time.sleep(10)
				agent.stop()
				break
	



