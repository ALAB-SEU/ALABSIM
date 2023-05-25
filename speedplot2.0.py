import os
import random
import time

import carla

client=carla.Client('127.0.0.1',2000)
client.set_timeout(2.0)
print ('successfully create client！')
world=client.get_world()
print ('successfully created VR world: ',client.get_world())

#储存添加到这个世界的所有actor，便于最后销毁
actor_list = [] 
# 拿到这个世界所有物体的蓝图
blueprint_library = world.get_blueprint_library()
with open("世界物体蓝图信息.txt","w") as f:
        f.write(str(blueprint_library))

ego_vehicle_bp = blueprint_library.find('vehicle.nissan.micra')

# 或者随机找辆车
# ego_vehicle_bp = random.choice(blueprint_library.filter('vehicle'))

# 给我们的车加上特定的颜色
ego_vehicle_bp.set_attribute('color', '255, 0, 0')

# 找到所有可以作为初始点的位置并随机选择一个
# transform = random.choice(world.get_map().get_spawn_points())
transform = carla.Transform(carla.Location(x=12.500000, y=5.250000, z=4.000000), carla.Rotation(pitch=0.000000, yaw=0.000000, roll=0.000000))

# 在这个位置生成汽车
ego_vehicle = world.spawn_actor(ego_vehicle_bp, transform)
actor_list.append(ego_vehicle)

#观察者（spectator）放置，使视野转移至小车处
spectator = world.get_spectator()
transform = ego_vehicle.get_transform()
spectator.set_transform(carla.Transform(transform.location + carla.Location(z=20),
                                                    carla.Rotation(pitch=-90)))


 

from matplotlib import pyplot as plt   
from matplotlib import animation 
import matplotlib.style as ms  
import numpy as np
  
ms.use("dark_background") # use black style

# first set up the figure, the axis, and the plot element we want to animate   
fig = plt.figure() 
ax1 = fig.add_subplot(5,1,1,xlim=(0, 2), ylim=(-10, 10))
ax2 = fig.add_subplot(5,1,2,xlim=(0, 2), ylim=(-10, 10))
ax3 = fig.add_subplot(5,1,3,xlim=(0, 2), ylim=(-1, 1))
ax4 = fig.add_subplot(5,1,4,xlim=(0, 2), ylim=(-1, 1))
ax5 = fig.add_subplot(5,1,5,xlim=(0, 2), ylim=(-1, 1))
line, = ax1.plot([], [], lw=2)  
line2, = ax2.plot([], [], lw=2)  
line3, = ax3.plot([], [], lw=2)  
line4, = ax4.plot([], [], lw=2)  
line5, = ax5.plot([], [], lw=2)  

ax1.axes.xaxis.set_visible(False)
ax2.axes.xaxis.set_visible(False)
ax3.axes.xaxis.set_visible(False)
ax4.axes.xaxis.set_visible(False)
ax5.axes.xaxis.set_visible(False)


ax1.set_title('Velocity')
ax2.set_title('Acceleration')
ax3.set_title('Throttle')
ax4.set_title('Steer')
ax5.set_title('Brake')

ax1.set_ylabel('m/s')
ax2.set_ylabel('m/s2')


 
# animation function.  this is called sequentially   
def animate(i):
    # 车辆油门改变
    control = carla.VehicleControl(random.random())
    ego_vehicle.apply_control(control)   

    # 数据更新
    velocity[ :velocity.size - 1] = velocity[ 1: ]
    velocity[velocity.size - 1] = ego_vehicle.get_velocity().x

    acceleration[ :acceleration.size - 1] = acceleration[ 1: ]
    acceleration[acceleration.size - 1] = ego_vehicle.get_acceleration().x

    throttle[ :throttle.size - 1] = throttle[ 1: ]
    throttle[throttle.size - 1] = control.throttle

    steer[ :steer.size - 1] = steer[ 1: ]
    steer[steer.size - 1] = control.steer

    brake[ :brake.size - 1] = brake[ 1: ]
    brake[brake.size - 1] = control.brake

    # 数据传入图片
    x = np.linspace(0, 2, 100)   
    y = velocity
    line.set_data(x, y)      
 

    x2 = np.linspace(0, 2, 100)   
    y2 = acceleration
    line2.set_data(x2, y2)   

    x3 = np.linspace(0, 2, 100)   
    y3 = throttle
    line3.set_data(x3, y3)   

    x4 = np.linspace(0, 2, 100)   
    y4 = steer
    line4.set_data(x4, y4)  

    x5 = np.linspace(0, 2, 100)   
    y5 = brake
    line5.set_data(x5, y5) 



velocity = np.zeros(100)
acceleration = np.zeros(100)
throttle = np.zeros(100)
steer = np.zeros(100)
brake = np.zeros(100)
anim1=animation.FuncAnimation(fig, animate, interval=30)  
plt.show() 

