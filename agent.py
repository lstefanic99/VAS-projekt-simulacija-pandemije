from random import uniform, seed, randint, choice
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np
import sys


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

    def infect(self, agents):
        distances = []
        for agent in agents:
            if self != agent and self.status == 'Infected' and self.risk:
                distance = self.get_distance(agent)
                distances.append((distance, agent))
        distances.sort()
        neighbors = [agent for d, agent in distances[:num_neighbors]]
        for agent in neighbors:
            if(agent.risk >= 30):
                agent.color = self.color
                print(f"Susjedi agenta {self.name} su {agent.name}, njihov rizik: {agent.risk}. Njihove boje su: {agent.color}. Boja zaraznog agenta: {self.color}")
                agent.status = 'Infected'
                agent.type = 0
            if(agent.risk < 30):
                agent.color = 'blue'

def plot_distribution(agents, cycle_num):
    "Plot the distribution of agents after cycle_num rounds of the loop."
    x_values_0, y_values_0 = [], []
    color1 = ""
    color2 = ""
    for agent in agents:
        x, y = agent.location
        x_values_0.append(x)
        y_values_0.append(y)
        print(f"Ovo je status agenta: {agent.status}, njihova boja: {agent.color} i njihov rizik: {agent.risk}")

    fig, ax = plt.subplots(figsize=(8, 8))
    plot_args = {'markersize': 8, 'alpha': 0.6}

    scat = ax.scatter(x=[], y=[], c='black', linewidths=4)
    #ax.plot(x_values_0, y_values_0, 'o', c=(f"{[agent.color for agent in agents]}") , **plot_args)
    #ax.plot(x_values_1, y_values_1, 'o', c=(f"{[agent.color for agent in agents]}"), **plot_args)
    #ax.set_title(f'Cycle {cycle_num-1}')
    x = np.array(x_values_0).reshape(-1, 1)
    y = np.array(y_values_0).reshape(-1, 1)
    scat.set_offsets(np.concatenate((x, y), axis=1))
    scat.set_edgecolors(np.array([agent.color if agent.status=='Infected' else agent.color if agent.risk > 30 else agent.color for agent in agents]))
    plt.scatter(x,y,c=np.array(['red' if agent.status=='Infected' else 'green' for agent in agents]))
    plt.savefig('konacni_rezultat.png')
    plt.show()


num_of_type_0 = 100
num_of_type_1 = 1
num_neighbors = 10       
sex_list = ['M','Z']
job_list = ['GovtJob', 'PrivateJob', 'SelfEmployed','NoJob']

# == Create a list of agents == #
agents = [Agent(0, f"agent_{i}", randint(1,90), choice(sex_list), choice(job_list), 
color='green', status='Healthy', risk=randint(1,100)) for i in range(num_of_type_0)]

agents.extend(Agent(1, "infectious", randint(1,90),choice(sex_list), choice(job_list),
color='red', status='Infected', risk=randint(1,100)) for i in range(num_of_type_1))

count = 1
while True:
    print('Entering loop ', count)
    plot_distribution(agents, count)
    count += 1
    for agent in agents:
        agent.infect(agents)
        if all (agent.status=='Infected' for agent in agents):
            sys.exit()

         
