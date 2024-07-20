

import numpy as np
import matplotlib.pyplot as plt

phi, theta = np.mgrid[0.0:2.0 * np.pi:100j, 0.0:np.pi:50j]
x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

x_proj = x
z_proj = z

fig = plt.figure(figsize=(12, 6))

ax1 = fig.add_subplot(121, projection='3d')
ax1.plot_surface(x, y, z, color='b', alpha=0.6)
ax1.set_title('Original 3D Mesh')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')

ax2 = fig.add_subplot(122)
ax2.scatter(x_proj, z_proj, color='r', s=0.1)
ax2.set_title('Projection on X-Z Plane')
ax2.set_xlabel('X')
ax2.set_ylabel('Z')

plt.tight_layout()
plt.show()
