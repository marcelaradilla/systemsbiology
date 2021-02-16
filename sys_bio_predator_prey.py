# -*- coding: utf-8 -*-
"""Sys Bio Predator Prey.ipynb

Revised code with resource (grass) added.
Rabbits eat the grass and they need it for their survival.
Grass moves and grows randomly around the environment if rabbits don't eat it

"""

import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import copy as cp

nr = 500 # carrying capacity of rabbits
r_init = 100 # initial rabbit population
mr = 0.03 # magnitude of movement of rabbits
dr = 1.0 # death rate of rabbits when it faces foxes
rr = 0.1 # reproduction rate of rabbits
f_init = 80 # initial fox population
mf = 0.05 # magnitude of movement of foxes
df = 0.1 # death rate of foxes when there is no food
rf = 0.6 # reproduction rate of foxes
g_init=200 #initial amount of grass
rg=0.8 #spread/reproduction rate of grass
mg=0.03 #magnitude of movement of grass
dg=0.9 #death rate of grass to
cd = 0.02 # radius for collision detection
cdsq = cd ** 2

class agent:
    pass

def initialize():
    global agents, rdata, fdata, gdata
    agents = []
    for i in range(r_init + f_init+g_init):
        ag = agent()
        if i <r_init:
            ag.type = 'r'
        elif i < f_init+r_init:
            ag.type='f'
        else:
            ag.type='g'
        ag.x = random()
        ag.y = random()
        agents.append(ag)
    rdata = []
    fdata = []
    gdata=[]

def observe():

    global agents, rdata, fdata, gdata
    subplot(2, 1, 1)
    cla()
    rabbits = [ag for ag in agents if ag.type == 'r']
    rdata.append(len(rabbits))
    if len(rabbits) > 0:
        x = [ag.x for ag in rabbits]
        y = [ag.y for ag in rabbits]
        plot(x, y, 'b.')
    foxes = [ag for ag in agents if ag.type == 'f']
    fdata.append(len(foxes))
    if len(foxes) > 0:
        x = [ag.x for ag in foxes]
        y = [ag.y for ag in foxes]
        plot(x, y, 'ro')
    grass=[ag for ag in agents if ag.type == 'g']
    gdata.append(len(grass))
    if len(grass)>0:
        x = [ag.x for ag in grass]
        y = [ag.y for ag in grass]
        plot(x, y, 'xg')

    axis('image')
    axis([0, 1, 0, 1])
    subplot(2, 1, 2)
    cla()
    plot(rdata, label = 'prey')
    plot(fdata, label = 'predator')
    plot(gdata,label='grass')
    legend()


def update():
    global agents
    if agents == []:
        return
    ag = agents[randint(len(agents))]

    # simulating random movement
    if ag.type=='r':
        m=mr
    elif ag.type=='f':
        m=mf
    else:
        m=mg
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating death or birth
    #neighbors = [nb for nb in agents if nb.type != ag.type
    #           and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    #second list of grass neighbors, will only be used  with the rabbits
    grass_neighbors=[nb for nb in agents if nb.type =='g'
               and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
    #list of rabbit neighbors to simulate that they eat the grass and to check if foxes have food
    rabbit_neighbors=[nb for nb in agents if nb.type =='r'
               and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
    #list of fox neighbots to check if rabbits die
    fox_neighbors=[nb for nb in agents if nb.type =='f'
               and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    if ag.type == 'r':
        if len(fox_neighbors) > 0: # if there are foxes nearby
            if random() < dr:
                agents.remove(ag)
                return
        if random() < rr*(1-sum(1 for x in agents if x.type == 'r')/nr) and len(grass_neighbors)>0: #reproduction and checking if they have grass around
            agents.append(cp.copy(ag)) #reproduction
            agents.remove(grass_neighbors[randint(len(grass_neighbors))]) #removal of the grass neighbor
    elif ag.type=='f': #elif the agent is a fox
        if len(rabbit_neighbors) == 0: # if there are no rabbits nearby
            if random() < df:
                agents.remove(ag)
                return
        else: # if there are rabbits nearby
            if random() < rf:
                agents.append(cp.copy(ag))
            if random()< dr: #if we have rabbits nearby,
            #we pick a random neighbor and kill it with probability dr
                agents.remove(rabbit_neighbors[randint(len(rabbit_neighbors))])
    else: #if the agent is grass
        if len(rabbit_neighbors)>0: #if there are rabbits nearby
            if random()<dg:
                agents.remove(ag)
                return
            if random()<rg:
                agents.append(cp.copy(ag)) #grass reproduction if there are no rabbits that eat it

def update_one_unit_time():
    global agents
    t = 0
    while t < 1.:
        t += 1 / len(agents)
        update()

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update_one_unit_time])
