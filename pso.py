import constants
from random import uniform

class Particle:
    def __init__(self, x, y, x_velocity=0, y_velocity=0, fp_list=[]):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.fp_list = fp_list

    def calculate_pb(self):
        self.pb = min(self.fp_list)

def create_particles(qtd_particles):
    # Cria um numero determinado de novas particulas
    return [
         # X e Y recebe um numero aleatorio dentro do dominio especificado
        Particle( 
            uniform(constants.X_DOMAIN[0], constants.X_DOMAIN[1]),
            uniform(constants.Y_DOMAIN[0], constants.Y_DOMAIN[1])
        ) for x in range(qtd_particles)
    ]

def check_velocity_limit(velocity, domain):
    # Para limitar a velocidade de uma particula para que nao extrapole o espaço de busca
    if velocity > (domain[0] * constants.VELOCITY_LIMIT):
        velocity = domain[0] * constants.VELOCITY_LIMIT
    elif velocity < (domain[1] * constants.VELOCITY_LIMIT):
        velocity = domain[1] * constants.VELOCITY_LIMIT

def initial_velocity(particles):
    new_velocity = 0.1 # Aqui entra a formula que eu ainda preciso compreender

    for particle in particles:
        particle.x_velocity = particle.y_velocity = new_velocity

    #for position in [particle.x_velocity, particle.x_velocity]:
        

def define_velocity(particle):
    new_x_velocity = 0.1 # Aqui entra a formula que eu ainda preciso compreender
    new_y_velocity = 3.4 # ~


def main(args):
    from math import sin, sqrt, pow
    particles = create_particles(constants.PARTICLES_NUMBER)
    initial_velocity(particles)

    for particle in particles:
        fp = 0.5 + (pow(sin(sqrt(pow(particle.x,2) + pow(particle.y,2)), 2) - 0.5) / pow(1 + 0.0001 * (pow(particle.x, 2) + pow(particle.y, 2)), 2))
        particle.fp_list.append(fp)
        particle.calculate_pb()

    

    print(particles)
    

if __name__ == "__main__":
    from sys import argv
    main(argv)