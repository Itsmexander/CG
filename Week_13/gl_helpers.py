from numpy import array, ndarray, zeros, dot, cross, float32, identity
from numpy.linalg import norm
from math import sqrt, sin, cos, tan, acos, pi

def Identity():
    return array(((1, 0, 0, 0),
                  (0, 1, 0, 0),
                  (0, 0, 1, 0),
                  (0, 0, 0, 1)), dtype=float32)

def normalize(v):
    l = norm(v)
    if l == 0:
        return v
    else:
        return v/l

def Translate(tx, ty, tz):
    return array(((1, 0, 0, tx),
                  (0, 1, 0, ty),
                  (0, 0, 1, tz),
                  (0, 0, 0, 1)), dtype=float32)

def Scale(sx, sy, sz):
    return array(((sx, 0, 0, 0),
                  (0, sy, 0, 0),
                  (0, 0, sz, 0),
                  (0, 0, 0, 1)), dtype=float32)

def Rotate(angle, x, y, z):
    C = cos(angle*(pi/180))
    S = sin(angle*(pi/180))
    return array((((x**2)*(1-C)+C, x*y*(1-C)-(z*S), x*z*(1-C)+(y*S), 0),
                  (y*x*(1-C)+(z*S), (y**2)*(1-C)+C, y*z*(1-C)-(x*S), 0),
                  (z*x*(1-C)-(y*S), z*y*(1-C)+(x*S), (z**2)*(1-C)+C, 0),
                  (0, 0, 0, 1)), dtype=float32)

def LookAt(eyex, eyey, eyez, atx, aty, atz, upx, upy, upz):
    ea = array((eyex-atx ,eyey-aty ,eyez-atz), dtype=float32)
    Z = normalize(ea)
    up = array((upx, upy, upz), dtype=float32)
    Y = normalize(up)
    X = normalize(cross(Y,Z))
    Y = normalize(cross(Z,X))
    eye = array((eyex, eyey ,eyez), dtype=float32)

    return array(((X[0], X[1], X[2], -dot(X,eye)),
                  (Y[0], Y[1], Y[2], -dot(Y,eye)),
                  (Z[0], Z[1], Z[2], -dot(Z,eye)),
                  (0, 0, 0, 1)), dtype=float32)

def Perspective(fovy, aspect, zNear, zFar):
    return array((( 
                  (1/tan((fovy/2)*(pi/180)))/aspect, 0, 0, 0),
                  (0, 1/tan((fovy/2)*(pi/180)), 0, 0),
                  (0, 0, -(zFar+zNear)/(zFar-zNear), (-2*zNear*zFar)/(zFar-zNear)),
                  (0, 0, -1, 0) ), dtype=float32)

def Frustum(left, right, bottom, top, near, far):
    return array((((2*near)/(right-left), 0, (right+left)/(right-left), 0),
                  (0, (2*near)/(top-bottom), (top+bottom)/(top-bottom), 0),
                  (0, 0, -(far+near)/(far-near), -(2*far*near)/(far-near)),
                  (0, 0, -1, 0)), dtype=float32)

def Ortho(left, right, bottom, top, near, far):
    return array(((2/(right-left), 0, 0, -(right+left)/(right-left)),
                  (0, 2/(top-bottom), 0, -(top+bottom)/(top-bottom)),
                  (0, 0, -2/(far-near), -(far+near)/(far-near)),
                  (0, 0, 0, 1)), dtype=float32)