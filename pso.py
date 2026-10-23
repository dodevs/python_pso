import constants
from math import sin, sqrt
from random import uniform
from statistics import mean, pstdev

DOMAINS = [constants.X_DOMAIN, constants.Y_DOMAIN]

def schaffer_f6(position):
    # Funcao F6 de Schaffer, minimo global 0 em (0, 0)
    s = position[0] ** 2 + position[1] ** 2
    return 0.5 + (sin(sqrt(s)) ** 2 - 0.5) / (1 + 0.001 * s) ** 2

def velocity_limit(domain, profile):
    return (domain[1] - domain[0]) * profile["velocity_limit"]

class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.fp = None
        self.pb_position = list(position)
        self.pb = float('inf')

    def evaluate(self):
        self.fp = schaffer_f6(self.position)
        # Melhor posicao da particula ate o momento (pB)
        if self.fp < self.pb:
            self.pb = self.fp
            self.pb_position = list(self.position)

def create_particles(profile):
    # Posicao aleatoria dentro do dominio e velocidade inicial aleatoria limitada por velocity_limit
    particles = []
    for _ in range(profile["particles"]):
        position = [uniform(d[0], d[1]) for d in DOMAINS]
        velocity = [uniform(-velocity_limit(d, profile), velocity_limit(d, profile)) for d in DOMAINS]
        particles.append(Particle(position, velocity))
    return particles

def best_neighbor(particles, index, topology):
    # topology 0: melhor de toda a populacao (gB); k: melhor entre os k vizinhos de cada lado no anel
    if topology == 0:
        return min(particles, key=lambda p: p.pb)
    n = len(particles)
    return min((particles[(index + k) % n] for k in range(-topology, topology + 1)), key=lambda p: p.pb)

def update_particle(particle, gb_position, profile, inertia):
    for d, domain in enumerate(DOMAINS):
        velocity = (
            inertia * particle.velocity[d]
            + profile["phi1"] * uniform(0, 1) * (particle.pb_position[d] - particle.position[d])
            + profile["phi2"] * uniform(0, 1) * (gb_position[d] - particle.position[d])
        )
        vmax = velocity_limit(domain, profile)
        velocity = max(-vmax, min(vmax, velocity))
        position = particle.position[d] + velocity

        # Fora do intervalo: corrige para o limite e zera a velocidade
        if position > domain[1]:
            position, velocity = domain[1], 0
        elif position < domain[0]:
            position, velocity = domain[0], 0

        particle.velocity[d] = velocity
        particle.position[d] = position

def run(iterations, profile):
    # Retorna, por iteracao, o melhor fp global (gB) e a media dos fp da populacao
    particles = create_particles(profile)
    gb = float('inf')
    best_curve, mean_curve = [], []
    w_start, w_end = profile["w"]

    for t in range(iterations):
        for particle in particles:
            particle.evaluate()
            gb = min(gb, particle.pb)

        best_curve.append(gb)
        mean_curve.append(mean(p.fp for p in particles))

        inertia = w_start + (w_end - w_start) * t / max(iterations - 1, 1)
        leaders = [list(best_neighbor(particles, i, profile["topology"]).pb_position) for i in range(len(particles))]
        for particle, leader in zip(particles, leaders):
            update_particle(particle, leader, profile, inertia)

    return best_curve, mean_curve

def main(profile_name="spec"):
    import matplotlib.pyplot as plt
    from os import makedirs

    profile = constants.PROFILES[profile_name]
    makedirs("resultados", exist_ok=True)
    print("Perfil: {0}".format(profile_name))
    print("Iteracoes | Melhor | Media | Desvio padrao | Chegou a 0")

    for iterations in constants.ITERATIONS:
        runs = [run(iterations, profile) for _ in range(constants.EXECUTIONS)]
        finals = [best[-1] for best, _ in runs]
        hits = sum(f < constants.SUCCESS_THRESHOLD for f in finals)
        print("{0:>9} | {1:.6f} | {2:.6f} | {3:.6f} | {4}/{5}".format(
            iterations, min(finals), mean(finals), pstdev(finals), hits, constants.EXECUTIONS))

        # Curvas medias entre as execucoes: melhor resultado e media da populacao
        x = range(1, iterations + 1)
        best_line, = plt.plot(x, [mean(r[0][i] for r in runs) for i in range(iterations)], color='g')
        mean_line, = plt.plot(x, [mean(r[1][i] for r in runs) for i in range(iterations)], color='b')
        plt.title('PSO {0} - Schaffer F6 ({1} iteracoes)'.format(profile_name, iterations))
        plt.xlabel('Iteracao')
        plt.ylabel('Fitness')
        plt.legend([best_line, mean_line], ['Melhor', 'Media da populacao'])
        plt.savefig("resultados/pso_{0}_{1}.png".format(profile_name, iterations))
        plt.clf()

if __name__ == "__main__":
    from sys import argv
    main(*argv[1:2])
