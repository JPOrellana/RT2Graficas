import numpy as np
from math import acos, asin
def reflectVector(normal,direction):
    reflect = 2* np.dot(normal, direction)
    reflect = np.multiply(reflect, normal)
    reflect = np.subtract(reflect, direction)
    reflect =reflect / np.linalg.norm(reflect)
    return reflect

def refractVector(normal, incident, n1,n2): 
    # Snell´s Law
    c1 = np.dot(normal,incident)

    if c1 < 0:
        c1 = -c1
    else:
        normal = np.array(normal) * -1
        n1, n2 = n2, n1

    n = n1 / n2

    T = n * (incident +  c1 * normal) - normal * (1 - n**2 * (1 - c1**2))** 0.5
    T = T / np.linalg.norm(T)

    return T

def totalInternalReflection(normal,incident,n1,n2):
    c1 = np.dot(normal,incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1

    if n1 < n2:
        return False
    

    return acos(c1) >= asin(n2/n1)

def fresnel(normal,incident,n1, n2):
    c1 = np.dot(normal,incident)
    if c1 < 0:
        c1 = -c1
    else:
        n1, n2 = n2, n1
        
    s2 = (n1 * (1 - c1**2)**0.5) / n2
    c2 = (1 - s2 **2) **0.5
    F1 = (( (n2 * c1) - (n1 * c2) ) / ((n2 * c1) + (n1 *c2))) **2
    F2 = (((n1 * c2) - (n2 * c1)) / ((n1 * c2) + (n2 *c1))) **2


    Kr = (F1 + F2) / 2
    Kt = 1 - Kr
    return Kr, Kt


class Light(object):
    def __init__(self, intensity = 1, color = (1,1,1), lightType = "None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType

    def getLightColor(self):
        return [self.color[0] * self.intensity,
                self.color[1] * self.intensity,
                self.color[2] * self.intensity]
    
    def getDiffuseColor(self, intercept):
        return None
    
    def getSpecularColor(self, intecept, viewPos):
        return None


class AmbientLight(Light):
    def __init__(self, intensity = 1, color = (1,1,1)):
        super().__init__(intensity, color, "Ambient")

class DirectionalLight(Light):
    def __init__(self, direction = (0,-1,0), intensity = 1, color = (1,1,1)):
        self.direction = direction / np.linalg.norm(direction)
        super().__init__(intensity, color, "Directional")

    def getDiffuseColor(self, intercept):
        dir = [(i * -1) for i in self.direction] 
        intensity = np.dot(intercept.normal, dir) * self.intensity
        intensity = max(0,min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return  [(i * intensity) for i in self.color]
    
    def getSpecularColor(self, intercept, viewPos):
        dir = [(i * -1) for i in self.direction]

        reflect = reflectVector(intercept.normal, dir)

        viewDir = np.subtract(viewPos, intercept.point)
        viewDir = viewDir / np.linalg.norm(viewDir)

        specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        return [(i * specIntensity) for i in self.color] 
    
class PointLight(Light):
    def __init__(self, point = (0,0,0),intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity,color, "Point")

    def getDiffuseColor(self, intercept):
        dir = np.subtract(self.point,intercept.point)
        dir = dir / np.linalg.norm(dir)
        intensity = np.dot(intercept.normal, dir) * self.intensity
        intensity = max(0,min(1, intensity))
        intensity *= 1 - intercept.obj.material.ks

        return  [(i * intensity) for i in self.color]

    def getSpecularColor(self, intercept, viewPos):
        dir = np.subtract(self.point,intercept.point)

        reflect = reflectVector(intercept.normal, dir)

        viewDir = np.subtract(viewPos, intercept.point)
        viewDir = viewDir / np.linalg.norm(viewDir)

        specIntensity = max(0, np.dot(viewDir, reflect)) ** intercept.obj.material.spec
        specIntensity *= intercept.obj.material.ks
        specIntensity *= self.intensity

        return [(i * specIntensity) for i in self.color] 