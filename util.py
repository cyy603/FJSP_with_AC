import numpy as np
from numpy import random

class CaseGenerator():
    def __init__(self, rou, mu, J, M):
        self.processTime = np.zeros((J))
        self.capacity = 0
        self.jobSize = np.zeros((J))
        self.travelMatrix = np.zeros((J + 1, J + 1))
        # self.ub = np.zeros(1, J)
        # self.lb = np.zeros(1, J)
        self.rou = rou;  self.mu = mu
        # self.Lambda = Lambda
        # self.delta1 = delta1; self.delta2 = delta2
        self.J = J; self.M = M
        self.customer = []

    def construct_case(self):
        data = {
            'jobSize': [],
            'processTime' : [],
            'capacity' : 0,
            'customer' : [],
            'travelMatrix' : []
        }

        # Generate the job size and process time for each job
        for i in range(len(self.jobSize)):
            self.jobSize[i] = self.generate_job_size(self.rou)
            self.processTime[i] = self.generate_proc_time(self.jobSize[i], self.mu)
        data['jobSize'] = self.jobSize
        data['processTime'] = self.processTime

        # Generate the vehicle capacity
        self.capacity = self.generate_vehicle_cap(self.jobSize)
        data['capacity'] = self.capacity

        # Generate the travel time matrix
        self.travelMatrix, self.customer = self.generate_travelMatrix(self.J, self.M, self.rou)
        data['customer'] = self.customer
        data['travelMatrix'] = self.travelMatrix

        return data
        # # Generate the service time
        # for i in range(0, self.J):
        #     self.serviceTime[i] = self.generate_service_time(self.Lambda, self.rou)
        # # Generate the machine ready time
        # for i in range(1, self.M - 1):
        #     self.MreadyTime[i] = self.generate_ready_time(self.rou)
        # # Generate the vehicle ready time
        # self.VreadyTime[0] = self.generate_vehi_ready_time1(self.MreadyTime, self.serviceTime[0], self.rou, self.Lambda,
        #                                                     self.V, self.M)
        # for i in range(1, self.V - 1):
        #     self.VreadyTime[i] = self.generate_vehi_ready_time2(self.MreadyTime, self.serviceTime[0], self.rou, self.Lambda,
        #                                                         self.V, self.M)
        # # Generate the lower time window bounds
        # for i in range(0, self.J - 1):
        #     self.lb[i] = self.generate_lower_bound(self.processTime[i], self.serviceTime[0], self.travelMatrix[0][i + 1],
        #                                            self.delta1, self.rou, self.J, self.M, self.V)
        # for i in range(0, self.J - 1):
        #     self.ub[i] = self.generate_upper_bound(self.lb[i], self.delta2, self.rou)


    def generate_proc_time(self, d, mu):
        """
        Generate the process time for each job
        d: the job size of job i
        mu: pre-defined parameter to control the process time of each job on each machine
        """
        unit_proc_time = np.round(random.uniform(1 - mu, 1 + mu))
        proc_time = d * unit_proc_time
        return proc_time

    def generate_job_size(self, rou):
        """
        Generate the job size (related to the vehicle capacity) for each job
        rou: parameter to control the job size
        """
        return np.round(random.uniform(rou / 2, rou))

    def generate_vehicle_cap(self, U):
        """
        Generate the vehicle capacity of each vehicle
        U: the size of all jobs
        """
        max_cap = np.max(U)
        total_demand = np.sum(U)
        return np.round(random.uniform(max_cap, total_demand / 2))

    def generate_travelMatrix(self, n, m, rou):
        """
        Generate the travel time
        n: The number of  customers
        m: The number of machines
        rou: parameter to control the job size
        """
        travel_time = np.zeros((n + 1, n + 1))
        customer = []
        alpha = np.round(((3 * rou) * (m + n - 1)) / (2 * (n + 1)))
        alpha = int(alpha)
        counter = 1
        while len(customer) < n:
            temp_x = np.round(random.uniform(0, alpha))
            temp_y = np.round(random.uniform(0, alpha))
            temp_point = np.array([temp_x, temp_y])
            insert = True
            if len(customer) == 0:
                customer.append(temp_point)
            else:
                for i in range(len(customer)):
                    dist = np.linalg.norm(temp_point - customer[i])
                    if dist < alpha:
                        travel_time[counter][i] = dist
                    else:
                        insert = False
                        break
                if insert:
                    customer.append(temp_point)
                    counter += 1
        depot_x = np.sqrt(np.max(travel_time) ** 2 / 2)
        depot_y = np.sqrt(np.max(travel_time) ** 2 / 2)
        customer.append(np.array([depot_x, depot_y]))
        for i in range(len(customer)):
            dist = np.linalg.norm(customer[n] - customer[i])
            travel_time[n][i] = dist
        travel_time = travel_time + travel_time.T
        return travel_time, customer

    # def generate_service_time(self, Lambda, rou):
    #     """
    #     Generate the service time for each job (i.e. time required for each job to loading/unloading, registering)
    #     Lambda: control parameter
    #     rou: control parameter
    #     """
    #     limit = np.floor(Lambda * rou)
    #     return np.round(random.uniform(1, limit))
    #
    # def generate_ready_time(self, rou):
    #     """
    #     Generate the machine ready time. The machine that is the first ready to proces is labeled as 1 and scaled to r_1 = 0
    #     Following code aims to generate the ready time of the rest machines
    #     rou: control parameter
    #     """
    #     return np.round(random.uniform(1, rou))
    #
    # def generate_vehi_ready_time1(self, R, s_0, rou, Lambda, V, M):
    #     """
    #     Generate the ready time of the vehicle that deliver the last job of the previous set can start to be delivered
    #     R: the ready time of machines
    #     s_0: the service time at the depot
    #     rou: the maximum process time
    #     Lambda: control parameter used when generating the service time
    #     V: number of vehicles
    #     M: number of machines
    #     """
    #     max_time = np.max(R)
    #     a = np.floor(rou * (V / M))
    #     b = np.floor(Lambda * rou)
    #     gamma = np.round(random.uniform(3, a + b))
    #
    #     return max_time + s_0 + gamma
    #
    # def generate_vehi_ready_time2(self, R, s_0, rou, Lambda, V, M):
    #     """
    #     Generate the ready time of the rest vehicles
    #     """
    #     max_time = np.max(R)
    #     a = np.floor(rou * (V / M))
    #     b = np.floor(Lambda * rou)
    #
    #     return np.round(random.uniform(0, max_time + s_0 + a + b))