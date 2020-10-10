from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import axes3d
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
import math
import time

# Create a figure and axes for plotting
fig = plt.figure()
ax = plt.gca(projection='3d')

class environment():
    ''' Simulation environment with all its functions that will be used 
    '''
    def __init__(self):
        ''' Initial constant setting 
        '''
        self.w_atuador = 15
        self.max_ganho = 5.0
        self.z_joint_axes = 5.0
        self.th_l = 2.1
        self.th_e = 3.1
        self.grande = 12.856
        self.pequeno = 6.84
        self.meio = 8.5285
        self.actual_angles = np.array([0,0,0,0,0,0])
        self.plate_cords = np.array(self.base())
        self.joint_axes_cords = np.array(self.joint_axes())
        
    def showPlot(self):
        # Create an environment and call the plotting function animate
        _ = FuncAnimation(fig, self.animate)
        plt.show()

    def base(self):
        ''' Calculates the hexagon corners
        '''
        base = [(-8.5285, 3.42, 0), (2.6, 9.848, 0),\
                (8.5285, 6.428, 0), (8.5285, -6.428, 0),\
                (2.6, -9.848, 0), (-8.5285, -3.42, 0),\
                (-8.5285, 3.42, 0)]
        return base

    def joint_axes(self):
        ''' Calculates the coordinate points for the center of the servo axes.
        '''
        th_l = self.th_l
        z_joint_axes = self.z_joint_axes
        plate_cords = self.plate_cords

        joint_axes_cords = []
        joint_axes_cords.append((th_l*np.cos(math.radians(30))+plate_cords[0, 0], \
                th_l*np.sin(math.radians(30))+plate_cords[0, 1], z_joint_axes))
        joint_axes_cords.append((-th_l*np.cos(math.radians(30))+plate_cords[1, 0], \
                -th_l*np.sin(math.radians(30))+plate_cords[1, 1], z_joint_axes))
        joint_axes_cords.append((th_l*np.cos(math.radians(90))+plate_cords[2, 0], \
                -th_l*np.sin(math.radians(90))+plate_cords[2, 1], z_joint_axes))
        joint_axes_cords.append((th_l*np.cos(math.radians(90))+plate_cords[3, 0], \
                th_l*np.sin(math.radians(90))+plate_cords[3, 1], z_joint_axes))
        joint_axes_cords.append((-th_l*np.cos(math.radians(30))+plate_cords[4, 0], \
                th_l*np.sin(math.radians(30))+plate_cords[4, 1], z_joint_axes))
        joint_axes_cords.append((th_l*np.cos(math.radians(30))+plate_cords[5, 0], \
                -th_l*np.sin(math.radians(30))+plate_cords[5, 1], z_joint_axes))

        return joint_axes_cords

    def actuator(self):
        ''' Calculates the start and end coordinates of all end_actuators.
        '''
        th_e = self.th_e
        z_joint_axes = self.z_joint_axes
        actual_angles = self.actual_angles
        plate_cords = self.plate_cords
        w_atuador = self.w_atuador
        
        x, y, z = (self.joint_axes_cords[:, 0].copy(), self.joint_axes_cords[:, 1].copy(), self.joint_axes_cords[:, 2].copy())

        z[0] = z_joint_axes + 5*np.sin(math.radians(actual_angles[0])) 
        x[0] = th_e*np.cos(math.radians(actual_angles[0]))*np.cos(math.radians(30)) + x[0]
        y[0] = th_e*np.cos(math.radians(actual_angles[0]))*np.sin(math.radians(30)) + y[0]

        z[1] = z_joint_axes + 5*np.sin(math.radians(actual_angles[1])) 
        x[1] = -th_e*np.cos(math.radians(actual_angles[1]))*np.cos(math.radians(30)) + x[1]
        y[1] = -th_e*np.cos(math.radians(actual_angles[1]))*np.sin(math.radians(30)) + y[1]

        z[2] = z_joint_axes + 5*np.sin(math.radians(actual_angles[2])) 
        x[2] = th_e*np.cos(math.radians(actual_angles[2]))*np.cos(math.radians(90)) + x[2]
        y[2] = -th_e*np.cos(math.radians(actual_angles[2]))*np.sin(math.radians(90)) + y[2]

        z[3] = z_joint_axes + 5*np.sin(math.radians(actual_angles[3])) 
        x[3] = th_e*np.cos(math.radians(actual_angles[3]))*np.cos(math.radians(90)) + x[3]
        y[3] = th_e*np.cos(math.radians(actual_angles[3]))*np.sin(math.radians(90)) + y[3]

        z[4] = z_joint_axes + 5*np.sin(math.radians(actual_angles[4])) 
        x[4] = -th_e*np.cos(math.radians(actual_angles[4]))*np.cos(math.radians(30)) + x[4]
        y[4] = th_e*np.cos(math.radians(actual_angles[4]))*np.sin(math.radians(30)) + y[4]

        z[5] = z_joint_axes + 5*np.sin(math.radians(actual_angles[5])) 
        x[5] = th_e*np.cos(math.radians(actual_angles[5]))*np.cos(math.radians(30)) + x[5]
        y[5] = -th_e*np.cos(math.radians(actual_angles[5]))*np.sin(math.radians(30)) + y[5]
        
        end = []
        for i in range (6):
            b = math.sqrt(abs(x[i]-plate_cords[i,0])**2+abs(y[i]-plate_cords[i,1])**2)
            z_atuador = z[i] + math.sqrt(w_atuador**2-b**2)
            end.append([plate_cords[i,0], plate_cords[i,1], z_atuador])

        z_atuador = z[0] + math.sqrt(w_atuador**2-b**2)
        end.append([plate_cords[0,0], plate_cords[0,1], z_atuador])
        start = np.array([x, y, z])
        end = np.array(end)

        return start, end

    def step(self, action, delay, fraction):
        ''' Performs all steps to achieve the desired state of actions, 
            starting from the point of the current angles.
        '''
        actual = self.actual_angles
        target = action
        space = np.linspace(actual, target, num=fraction)

        for i in range(fraction):
            for j in range(6):
                self.actual_angles[j] = space[i,j]
            time.sleep(delay)

    def animate(self, i):
        ''' Plot animation loop
        '''
        plate_cords = self.plate_cords
        joint_axes_cords = self.joint_axes_cords

        start_actuators, end_actuators = self.actuator()

        ax.clear()
        ax.scatter3D(end_actuators[:,0], end_actuators[:,1], end_actuators[:,2], color='y',\
                linestyle='-', linewidth=3, label='Vertices')
        ax.plot3D(end_actuators[:,0], end_actuators[:,1], end_actuators[:,2], color='b',\
                linestyle='-', linewidth=3, label='Edges')
        ax.scatter3D(plate_cords[:, 0], plate_cords[:, 1], plate_cords[:, 2]+10, color='y',\
                linestyle='-', linewidth=3)
        ax.plot3D(plate_cords[:, 0], plate_cords[:, 1], plate_cords[:, 2]+10, color='b',\
                linestyle='-', linewidth=3)
        ax.scatter3D(plate_cords[:, 0], plate_cords[:, 1], plate_cords[:, 2], color='y',\
                linestyle='-', linewidth=3)
        ax.plot3D(plate_cords[:, 0], plate_cords[:, 1], plate_cords[:, 2], color='b',\
                linestyle='-', linewidth=3)

        for i in range(6):
            ax.plot3D([plate_cords[i, 0], plate_cords[i, 0]], [plate_cords[i, 1], plate_cords[i, 1]],\
                    [plate_cords[i, 2], plate_cords[i, 2]+10], color='b', linestyle='-', linewidth=3)
        
        ax.scatter3D(start_actuators[0, :], start_actuators[1, :], start_actuators[2, :], color='g', linestyle='-', linewidth=3)
        ax.scatter3D(joint_axes_cords[:, 0], joint_axes_cords[:, 1], joint_axes_cords[:, 2], color='r', linestyle='-', linewidth=3)

        for i in range (6):
            haste_x = [start_actuators[0, i], plate_cords[i,0]]
            haste_y = [start_actuators[1, i], plate_cords[i,1]]
            haste_z = [start_actuators[2, i], end_actuators[i,2]]
            ax.plot3D(haste_x, haste_y, haste_z, color='g', linestyle='-', linewidth=3)

            eixo_x = [start_actuators[0, i], joint_axes_cords[i, 0]]
            eixo_y = [start_actuators[1, i], joint_axes_cords[i, 1]]
            eixo_z = [start_actuators[2, i], joint_axes_cords[i, 2]]

            ax.plot3D(eixo_x, eixo_y, eixo_z, color='k', linestyle='-', linewidth=6)

        ax.set_title('Stewart Platform', size=20)
        ax.legend(loc=2, prop={'size':10})
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim3d([-25, 25])
        ax.set_ylim3d([-25, 25])
        ax.set_zlim3d([-3, 40])
