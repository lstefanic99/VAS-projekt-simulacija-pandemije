#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from datetime import datetime
import os.path

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

class Agent(Agent):

	class Analyze(OneShotBehaviour):
		async def on_start(self):
			print("I start agent")
		async def run(self):	
			print("I am in analyze")		
			pd.set_option('display.max_rows', None)
			pd.set_option('display.max_columns', None)
			pd.set_option('display.width', None)
			pd.set_option('display.max_colwidth', -1)

			data = pd.read_csv("analiza_simulacije.csv")
			df = pd.DataFrame(data, columns=['agent_name', 'agent_status', 'agent_age', 'agent_job', 'agent_sex' 'Infected_from'])
			d = df[['agent_name', 'agent_status','agent_age', 'agent_job']].drop_duplicates(subset=['agent_name'])

			print(d.sort_values('agent_name'))
			d1 = d['agent_status'] == 'Infected'
			d2 = pd.DataFrame(d1, columns=['agent_status'])
			d3 = d[d1]

			#print(d2)

			count1 = d2.agent_status.groupby(d2.agent_status).value_counts()
			labels = ['Healthy', 'Infected']
			plt.pie(count1, labels = labels, autopct='%1.0f%%');
			plt.savefig('pic1.png')
			plt.close()


			#plt.show()

			count2 = d3.agent_job.groupby(d3.agent_job).value_counts()
			labels = ['Government job', 'Unemployed', 'Private job', 'Self employed']
			plt.pie(count2, labels = labels, autopct='%1.0f%%');
			plt.savefig('pic2.png')
			plt.close()
			#plt.show()


			#fin.plot(kind='hist',figsize=(20,20))

			fin = d[d1]
			print(fin)
			fig = plt.figure(figsize = (10, 10))
			plt.legend(["Number of infected in age group"])
			plt.xlabel('Agent name')
			plt.xticks(rotation=90)
			plt.ylabel('Agent age')
			plt.bar(fin['agent_name'], fin['agent_age'], color ='blue', width = 0.5)
			print(f"Medijan: {fin['agent_age'].mean()}\n")
			plt.axhline(fin['agent_age'].mean(), color='red', linestyle='solid', linewidth=1, label='median')
			plt.legend(bbox_to_anchor = (1.0, 1), loc = 'upper center')
			plt.savefig('pic3.png')
			plt.close()


			#plt.show()

			#age_groups = pd.cut(fin['agent_age'], bins=[10,20,30,40,50,60,70,80,90,100,np.inf])
			#print(age_groups)

			plt.hist(fin['agent_age'], bins = [10,20,30,40,50,60,70,80,90,100], edgecolor = 'black')
			plt.savefig('pic4.png')
			plt.close()


			#plt.show()
	
	class Report(OneShotBehaviour):
		async def run(self):
			data = pd.read_csv("analiza_simulacije.csv")
			df = pd.DataFrame(data, columns=['agent_name', 'agent_status', 'agent_age', 'agent_job', 'agent_sex' 'Infected_from'])
			d = df[['agent_name', 'agent_status','agent_age', 'agent_job']].drop_duplicates(subset=['agent_name'])
			d1 = d['agent_status'] == 'Infected'
			fin = d[d1]
			
			pdf = FPDF()
			pdf.add_page()
			pdf.set_font("Arial",size=22)
			pdf.cell(200, 10, txt = "Simulation report", ln = 1, align = 'C')
			pdf.cell(200, 10, txt = "Created on: " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), ln = 1, align = 'C') 

			pdf.add_page()
			pdf.set_font("Arial",size=12)
			pdf.cell(200, 10, txt = "Table with all agents (infected agents are colored)", ln = 1, align = 'C')
			pdf.cell(50, 10, 'Agent name', 1, 0, 'C')
			pdf.cell(40, 10, 'Agent age', 1, 0, 'C')
			pdf.cell(40, 10, 'Agent job', 1, 2, 'C')
			pdf.cell(-90)
			#fin.sort_values(by='agent_name')

			    
			for i in range(0, len(d.sort_values(by='agent_name'))):
				
				if(d['agent_status'].iloc[i] == 'Infected'):
					pdf.set_fill_color(255, 95, 95)
					pdf.cell(50, 10, '%s' % (d['agent_name'].iloc[i]), 1, 0, 'C',fill=True)
					pdf.cell(40, 10, '%s' % (str(d['agent_age'].iloc[i])), 1, 0, 'C',fill=True)
					pdf.cell(40, 10, '%s' % (str(d['agent_job'].iloc[i])), 1, 2, 'C',fill=True)
					pdf.cell(-90)
				else:
					pdf.cell(50, 10, '%s' % (d['agent_name'].iloc[i]), 1, 0, 'C')
					pdf.cell(40, 10, '%s' % (str(d['agent_age'].iloc[i])), 1, 0, 'C')
					pdf.cell(40, 10, '%s' % (str(d['agent_job'].iloc[i])), 1, 2, 'C')
					pdf.cell(-90)
			    
			    
			    #pdf.cell(40, 10, '%s' % (str(d['agent_status'].iloc[i])), 1, 3, 'C')
			    #pdf.cell(-90)
			    
			pdf.add_page()
			pdf.set_font("Arial",size=12)
			pdf.cell(40, 10, '------------------------------------------ ', ln=1, align='L')
			pdf.cell(40, 10, 'Total number of agents: ' + str(len(d)), ln = 1, align= 'L')
			pdf.cell(40, 10, 'Number of infected agents: ' + str(len(fin)), ln = 1, align= 'L')
			pdf.cell(40, 10, 'Oldest infected agent: ' + str(fin['agent_age'].max()), ln=1, align= 'L')
			pdf.cell(40, 10, 'Youngest infected agent: ' + str(fin['agent_age'].min()), ln = 1, align ='L')
			pdf.cell(40, 10, '----------------------------------------- ', ln=1, align='L')

			if(os.path.exists('pic1.png')):
				pdf.image('pic1.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
				pdf.cell(200, 10, txt = "1. Percentage of infected people", ln = 1, align = 'C')


			if(os.path.exists('pic2.png')):
				pdf.add_page()
				pdf.image('pic2.png', x = None, y = None, w = 0, h = 0, type = '', link = '')
				pdf.cell(200, 10, txt = "2. Percentage infected people in job sectors", ln = 1, align = 'C')


			if(os.path.exists('pic3.png')):
				pdf.add_page("landscape")
				pdf.image('pic3.png', x = 0, y = 0, w = 270, h = 200, type = '', link = '')
				pdf.cell(200, 10, txt = "3. Agent names and ages", ln = 1, align = 'C')

			if(os.path.exists('pic4.png')):
				pdf.add_page("landscape")
				pdf.image('pic4.png', x = 10, y = 10, w = 0, h = 0, type = '', link = '')
				pdf.cell(200, 10, txt = "4. Age groups", ln = 1, align = 'C')
				pdf.output('test.pdf','F')
	
	async def setup(self):
		analiziraj = self.Analyze()
		izvjesti = self.Report()
		self.add_behaviour(analiziraj)
		self.add_behaviour(izvjesti)




