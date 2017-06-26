from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from svg.path import parse_path
import numpy as np
from scipy.misc import comb
import triangle
import triangle.plot
from stl import mesh
from math import cos, pi, sqrt


def bezier_curve(points, nTimes=1000):
    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])
    t = np.linspace(0.0, 1.0, nTimes)

    def bernstein_poly(i, n, t):
        return comb(n, i) * (t ** (n - i)) * (1 - t)**i

    polynomial_array = np.array([bernstein_poly(i, nPoints - 1, t) for i in range(0, nPoints)])
    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)
    return xvals, yvals


def triangulate_svg(svg_file, plot=False, optimize=False):
    path = []
    with open(svg_file) as f:
        soup = BeautifulSoup(f, 'lxml')
        path = parse_path(soup.select_one('path')['d'])
    xvals = []
    yvals = []
    for curve in path:
        if xvals:
            xvals = xvals[:-1]
            yvals = yvals[:-1]
        points = np.array([[curve.start.real, curve.start.imag], [curve.control1.real, curve.control1.imag],
                           [curve.control2.real, curve.control2.imag], [curve.end.real, curve.end.imag]])
        factor = max(int(curve.length() / 40) * 10, 30) if optimize else 100
        xval, yval = bezier_curve(points, nTimes=factor)
        xval = xval[::10]
        yval = yval[::10]
        xvals.extend(xval[::-1])
        yvals.extend(yval[::-1])
    mesh2d = {}
    bias = max(yvals) + min(yvals)
    vertices = [[x, bias - y] for (x, y) in zip(xvals, yvals)]
    mesh2d['vertices'] = np.array(vertices)
    segments = [[i, i + 1] for i in range(len(vertices) - 1)]
    segments.append([len(vertices) - 1, 0])
    mesh2d['segments'] = np.array(segments)
    triangles = triangle.triangulate(mesh2d, 'p')
    if plot:
        ax1 = plt.subplot(131, aspect='equal')
        ax1.axis('off')
        for curve in path:
            points = np.array([[curve.start.real, -curve.start.imag], [curve.control1.real, -curve.control1.imag],
                               [curve.control2.real, -curve.control2.imag], [curve.end.real, -curve.end.imag]])
            xvals, yvals = bezier_curve(points, nTimes=1000)
            ax1.plot(xvals, yvals, 'k')
        ax2 = plt.subplot(132, sharex=ax1, sharey=ax1)
        triangle.plot.plot(ax2, **mesh2d)
        ax3 = plt.subplot(133, sharex=ax1, sharey=ax1)
        triangle.plot.plot(ax3, **triangles)
        plt.show()
    return triangles


def svg2stl(svg_file, stl_file, dmax=30, dinterval=5, bias=-100):
    result2d = triangulate_svg(svg_file, optimize=True)
    vertices2d = result2d['vertices']
    triangles2d = result2d['triangles']
    nv = len(vertices2d)
    vertices = [[x, y, 0] for x, y in vertices2d]
    triangles = [[a, b, c] for a, b, c in triangles2d]
    for i, deg in enumerate(range(dinterval, dmax + 1, dinterval)):
        cosd = cos(deg / 180 * pi)
        sind = sqrt(1 - cosd * cosd)
        vertices.extend([[x, bias - (bias - y) * cosd, (bias - y) * sind] for (x, y) in vertices2d])
        this = i * nv
        that = this + nv
        for iv in range(nv - 1):
            a = this + iv
            b = a + 1
            c = that + iv
            d = c + 1
            triangles.append([a, d, b])
            triangles.append([a, c, d])
        a = that - 1
        b = this
        c = that + nv - 1
        d = that
        triangles.append([a, d, b])
        triangles.append([a, c, d])
    print('Generated model has %d vertices, %d faces.' % (len(vertices), len(triangles)))
    obj = mesh.Mesh(np.zeros(len(triangles), dtype=mesh.Mesh.dtype))
    for i, t in enumerate(triangles):
        for j in range(3):
            obj.vectors[i][j] = vertices[t[j]]
    obj.save(stl_file)
    print('Save to ' + stl_file)

if __name__ == '__main__':
    svg_file = 'github.svg'
    stl_file = 'github.stl'
    svg2stl(svg_file, stl_file)
