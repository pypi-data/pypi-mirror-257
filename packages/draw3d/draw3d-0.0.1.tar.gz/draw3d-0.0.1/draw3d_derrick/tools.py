# -*- coding: utf-8 -*-
# @Time     : 2024/2/21 15:43
# @Author   : Long-Long Qiu
# @FileName : tools.py
# @Product  : PyCharm
# import packages
from matplotlib.patches import Rectangle, Circle
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import numpy as np


class MatplotPainter:

    @staticmethod
    def drawCube(ax, x, y, z, width, height, depth, color='red', mode=2, linewidth=1, text="", fontsize=15, alpha=0.5):
        """
        绘制长方体
        :param ax:
        :param x: 左下顶点的x坐标
        :param y: 左下顶点的y坐标
        :param z: 左下顶点的z坐标
        :param width: 长
        :param height: 宽
        :param depth: 高
        :param color: 颜色
        :param mode: 1：填充； 2：不填充
        :param linewidth: 线宽
        :param text: 文字
        :param fontsize: 文字大小
        :param alpha: 透明度
        :return:
        """
        xx = [x, x, x + width, x + width, x]
        yy = [y, y + height, y + height, y, y]

        kwargs = {'alpha': 1, 'color': color, 'linewidth': linewidth}
        if mode == 1:
            ax.plot3D(xx, yy, [z] * 5, **kwargs)
            ax.plot3D(xx, yy, [z + depth] * 5, **kwargs)
            ax.plot3D([x, x], [y, y], [z, z + depth], **kwargs)
            ax.plot3D([x, x], [y + height, y + height], [z, z + depth], **kwargs)
            ax.plot3D([x + width, x + width], [y + height, y + height], [z, z + depth], **kwargs)
            ax.plot3D([x + width, x + width], [y, y], [z, z + depth], **kwargs)
        else:
            p = Rectangle((x, y), width, height, fc=color, ec='black', alpha=alpha)
            p2 = Rectangle((x, y), width, height, fc=color, ec='black', alpha=alpha)
            p3 = Rectangle((y, z), height, depth, fc=color, ec='black', alpha=alpha)
            p4 = Rectangle((y, z), height, depth, fc=color, ec='black', alpha=alpha)
            p5 = Rectangle((x, z), width, depth, fc=color, ec='black', alpha=alpha)
            p6 = Rectangle((x, z), width, depth, fc=color, ec='black', alpha=alpha)
            ax.add_patch(p)
            ax.add_patch(p2)
            ax.add_patch(p3)
            ax.add_patch(p4)
            ax.add_patch(p5)
            ax.add_patch(p6)

            if text != "":
                ax.text((x + width / 2), (y + height / 2), (z + depth / 2), str(text), color='black', fontsize=fontsize,
                        ha='center', va='center')

            art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
            art3d.pathpatch_2d_to_3d(p2, z=z + depth, zdir="z")
            art3d.pathpatch_2d_to_3d(p3, z=x, zdir="x")
            art3d.pathpatch_2d_to_3d(p4, z=x + width, zdir="x")
            art3d.pathpatch_2d_to_3d(p5, z=y, zdir="y")
            art3d.pathpatch_2d_to_3d(p6, z=y + height, zdir="y")

    @staticmethod
    def drawCylinder(ax, x, y, z, width, height, depth, color='red', text="",fontsize=10, alpha=0.2, main_axis='y'):
        """
        绘制圆柱体
        :param ax:
        :param x: 圆柱体外切长方体的左下顶点x坐标
        :param y: 圆柱体外切长方体的左下顶点y坐标
        :param z: 圆柱体外切长方体的左下顶点z坐标
        :param width: 圆柱体外切长方体的长
        :param height: 圆柱体外切长方体的宽
        :param depth: 圆柱体外切长方体的高
        :param color: 颜色
        :param text: 文字
        :param fontsize: 文字大小
        :param alpha: 透明度
        :param main_axis: 主轴：即圆柱体高所在的轴
        :return:
        """
        if main_axis == 'y':
            p = Circle((x + width / 2, z + depth / 2), radius=width / 2)
            p2 = Circle((x + width / 2, z + depth / 2), radius=width / 2)
            p.set_edgecolor('black')
            p.set_alpha(0.2)
            p.set_facecolor(color)
            p.set_alpha(0.2)
            p2.set_edgecolor('black')
            p2.set_alpha(0.2)
            p2.set_facecolor(color)
            p2.set_alpha(0.2)

            ax.add_patch(p)
            ax.add_patch(p2)
            art3d.pathpatch_2d_to_3d(p, z=y, zdir="y")
            art3d.pathpatch_2d_to_3d(p2, z=y + height, zdir="y")

            center_z = np.linspace(0, height, 100)
            theta = np.linspace(0, 2 * np.pi, 100)
            theta_grid, y_grid = np.meshgrid(theta, center_z)
            x_grid = width / 2 * np.cos(theta_grid) + x + width / 2
            z_grid = depth / 2 * np.sin(theta_grid) + z + depth / 2
            y_grid = y_grid + y

        elif main_axis == 'z':
            p = Circle((x + width / 2, y + height / 2), radius=width / 2)
            p2 = Circle((x + width / 2, y + height / 2), radius=width / 2)
            p.set_edgecolor('black')
            p.set_alpha(0.2)
            p.set_facecolor(color)
            p.set_alpha(0.2)
            p2.set_edgecolor('black')
            p2.set_alpha(0.2)
            p2.set_facecolor(color)
            p2.set_alpha(0.2)

            ax.add_patch(p)
            ax.add_patch(p2)
            art3d.pathpatch_2d_to_3d(p, z=z, zdir="z")
            art3d.pathpatch_2d_to_3d(p2, z=z + depth, zdir="z")

            center_z = np.linspace(0, depth, 100)
            theta = np.linspace(0, 2 * np.pi, 100)
            theta_grid, z_grid = np.meshgrid(theta, center_z)
            x_grid = width / 2 * np.cos(theta_grid) + x + width / 2
            y_grid = height / 2 * np.sin(theta_grid) + y + height / 2
            z_grid = z_grid + z

        elif main_axis == 'x':
            p = Circle((y + height / 2, z + depth / 2), radius=height / 2)
            p2 = Circle((y + height / 2, z + depth / 2), radius=height / 2)
            p.set_edgecolor('black')
            p.set_alpha(0.2)
            p.set_facecolor(color)
            p.set_alpha(0.2)
            p2.set_edgecolor('black')
            p2.set_alpha(0.2)
            p2.set_facecolor(color)
            p2.set_alpha(0.2)

            ax.add_patch(p)
            ax.add_patch(p2)
            art3d.pathpatch_2d_to_3d(p, z=x, zdir="x")
            art3d.pathpatch_2d_to_3d(p2, z=x + width, zdir="x")

            center_z = np.linspace(0, width, 100)
            theta = np.linspace(0, 2 * np.pi, 100)
            theta_grid, x_grid = np.meshgrid(theta, center_z)
            y_grid = height / 2 * np.cos(theta_grid) + y + height / 2
            z_grid = depth / 2 * np.sin(theta_grid) + z + depth / 2
            x_grid = x_grid + x

        ax.plot_surface(x_grid, y_grid, z_grid, shade=False, fc=color, alpha=alpha, color=color)
        if text != "":
            ax.text((x + width/2), (y + height/2), (z + depth/2), str(text), color='black',
                     fontsize=fontsize, ha='center', va='center')

    @staticmethod
    def setAxisLimits(ax, max_x, max_y, max_z, min_x=0, min_y=0, min_z=0):
        """
        设置各坐标轴的范围
        :param ax:
        :param max_x: x轴的最大值
        :param max_y: y轴的最大值
        :param max_z: z轴的最大值
        :param min_x: x轴的最小值
        :param min_y: y轴的最小值
        :param min_z: z轴的最小值
        :return:
        """
        ax.set_xlim3d([min_x, max_x])
        ax.set_ylim3d([min_y, max_y])
        ax.set_zlim3d([min_z, max_z])

    @staticmethod
    def setInitView(ax, elev, azim):
        """
        设置初始角度
        :param ax:
        :param elev: 仰角
        :param azim: 方位角
        :return:
        """
        ax.view_init(elev=elev, azim=azim)


if __name__ == '__main__':
    axGlob = plt.axes(projection='3d')
    MatplotPainter.drawCube(axGlob, 0, 0, 0, 0.5, 0.5, 0.5)
    MatplotPainter.drawCylinder(axGlob, 0.5, 0.5, 0, 0.5, 0.5, 1, alpha=0.8, main_axis='z')

    MatplotPainter.setAxisLimits(axGlob, 2, 2, 2)
    MatplotPainter.setInitView(axGlob, 50, 50)
    plt.show()
