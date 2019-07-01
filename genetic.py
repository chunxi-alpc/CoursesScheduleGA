import copy
import numpy as np

class Schedule:
    def __init__(self, courseId, classId, teacherId):
        self.courseId = courseId
        self.classId = classId
        self.teacherId = teacherId
        #print(courseId, classId, teacherId)
        self.roomId = 0
        self.weekDay = 0
        self.slot = 0

    def random_init(self, roomRange):
        self.roomId = np.random.randint(1, roomRange + 1, 1)[0]
        self.weekDay = np.random.randint(1, 8, 1)[0]
        self.slot = np.random.randint(1, 20, 1)[0]

def schedule_cost(population, elite):
    conflicts = []
    n = len(population[0])
    for p in population:
        conflict = 0
        for i in range(0, n - 1):
            for j in range(i + 1, n):
            # check course in same time and same room 
                if p[i].roomId == p[j].roomId and p[i].weekDay == p[j].weekDay and p[i].slot == p[j].slot:
                    conflict += 1             
                # check course for one class in the same time
                if p[i].classId == p[j].classId and p[i].weekDay == p[j].weekDay and p[i].slot == p[j].slot:
                    conflict += 1
                # check course for one teacher in the same time
                if p[i].teacherId == p[j].teacherId and p[i].weekDay == p[j].weekDay and p[i].slot == p[j].slot:
                    conflict += 1
                        
        conflicts.append(conflict)
    index = np.array(conflicts).argsort()
    return index[: elite], conflicts[index[0]]

class GeneticOptimize:
    def __init__(self, popsize=32, mutprob=0.3, elite=8, maxiter=500):
        # 种群的规模（0-100）
        self.popsize = popsize
        # 变异概率
        self.mutprob = mutprob
        # 精英个数
        self.elite = elite
        # 进化代数（100-500）
        self.maxiter = maxiter
        
    #随机初始化不同的种群
    def init_population(self, schedules, roomRange):
        self.population = []
        for i in range(self.popsize):
            entity = []
            for s in schedules:
                s.random_init(roomRange)
                entity.append(copy.deepcopy(s))
            self.population.append(entity)
            
    #变异
    def mutate(self, eiltePopulation, roomRange,slotnum):
        #选择变异的个数
        e = np.random.randint(0, self.elite, 1)[0]
        ep = copy.deepcopy(eiltePopulation[e])
        for p in ep:
            pos = np.random.randint(0, 3, 1)[0]
            if pos == 0:
                p.roomId = self.change(p.roomId,roomRange)
            elif pos == 1:
                p.weekDay = self.change(p.weekDay, 7)
            else:
                p.slot = self.change(p.slot, slotnum)
        
        return ep

    def change(self, value, valueRange):
        value = np.random.randint(1, valueRange+1, 1)[0]
        #value=(value)%valueRange+1
        return value

    def crossover(self, eiltePopulation):
        e1 = np.random.randint(0, self.elite, 1)[0]
        e2 = np.random.randint(0, self.elite, 1)[0]
        pos = np.random.randint(0, 3, 1)[0]
        ep1 = copy.deepcopy(eiltePopulation[e1])
        ep2 = eiltePopulation[e2]
        for p1, p2 in zip(ep1, ep2):
            if pos == 0:
                p1.weekDay = p2.weekDay
            if pos == 1:
                p1.roomId = p2.roomId
            if pos == 2:
                p1.slot = p2.slot
        return ep1

    def evolution(self, schedules, roomRange,slotnum):
        bestScore = 0
        bestSchedule = None
        self.init_population(schedules, roomRange)
        for i in range(self.maxiter):
            eliteIndex, bestScore = schedule_cost(self.population, self.elite)
            print('Iter: {} | conflict: {}'.format(i + 1, bestScore))
            if bestScore == 0:
                bestSchedule = self.population[eliteIndex[0]]
                break
            newPopulation = [self.population[index] for index in eliteIndex]
            while len(newPopulation) < self.popsize:
                if np.random.rand() < self.mutprob:
                    newp = self.mutate(newPopulation, roomRange, slotnum)
                else:
                    newp = self.crossover(newPopulation)
                newPopulation.append(newp)
            self.population = newPopulation
        return bestSchedule
