import constants
from math import sin, sqrt
from random import uniform
from statistics import mean, pstdev

DOMAINS = [constants.X_DOMAIN, constants.Y_DOMAIN]

def schaffer_f6(position):
    # Funcao F6 de Schaffer, minimo global 0 em (0, 0)
    s = position[0] ** 2 + position[1] ** 2
    return 0.5 + (sin(sqrt(s)) ** 2 - 0.5) / (1 + 0.001 * s) ** 2

def velocity_limit(domain):
    return (domain[1] - domain[0]) * constants.VELOCITY_LIMIT

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

def create_particles(qtd_particles):
    # Posicao aleatoria dentro do dominio e velocidade inicial aleatoria limitada a 15% do espaco de busca
    particles = []
    for _ in range(qtd_particles):
        position = [uniform(d[0], d[1]) for d in DOMAINS]
        velocity = [uniform(-velocity_limit(d), velocity_limit(d)) for d in DOMAINS]
        particles.append(Particle(position, velocity))
    return particles

def update_particle(particle, gb_position):
    for d, domain in enumerate(DOMAINS):
        velocity = (
            particle.velocity[d]
            + constants.PHI1 * uniform(0, 1) * (particle.pb_position[d] - particle.position[d])
            + constants.PHI2 * uniform(0, 1) * (gb_position[d] - particle.position[d])
        )
        vmax = velocity_limit(domain)
        velocity = max(-vmax, min(vmax, velocity))
        position = particle.position[d] + velocity

        # Fora do intervalo: corrige para o limite e zera a velocidade
        if position > domain[1]:
            position, velocity = domain[1], 0
        elif position < domain[0]:
            position, velocity = domain[0], 0

        particle.velocity[d] = velocity
        particle.position[d] = position

def run(iterations):
    # Retorna, por iteracao, o melhor fp global (gB) e a media dos fp da populacao
    particles = create_particles(constants.PARTICLES_NUMBER)
    gb, gb_position = float('inf'), None
    best_curve, mean_curve = [], []

    for _ in range(iterations):
        for particle in particles:
            particle.evaluate()
            if particle.pb < gb:
                gb, gb_position = particle.pb, list(particle.pb_position)

        best_curve.append(gb)
        mean_curve.append(mean(p.fp for p in particles))

        for particle in particles:
            update_particle(particle, gb_position)

    return best_curve, mean_curve

def main():
    import matplotlib.pyplot as plt
    from os import makedirs

    makedirs("resultados", exist_ok=True)
    print("Iteracoes | Melhor | Media | Desvio padrao")

    for iterations in constants.ITERATIONS:
        runs = [run(iterations) for _ in range(constants.EXECUTIONS)]
        finals = [best[-1] for best, _ in runs]
        print("{0:>9} | {1:.6f} | {2:.6f} | {3:.6f}".format(iterations, min(finals), mean(finals), pstdev(finals)))

        # Curvas medias entre as execucoes: melhor resultado e media da populacao
        x = range(1, iterations + 1)
        best_line, = plt.plot(x, [mean(r[0][i] for r in runs) for i in range(iterations)], color='g')
        mean_line, = plt.plot(x, [mean(r[1][i] for r in runs) for i in range(iterations)], color='b')
        plt.title('PSO - Schaffer F6 ({0} iteracoes)'.format(iterations))
        plt.xlabel('Iteracao')
        plt.ylabel('Fitness')
        plt.legend([best_line, mean_line], ['Melhor', 'Media da populacao'])
        plt.savefig("resultados/pso_{0}.png".format(iterations))
        plt.clf()

if __name__ == "__main__":
    main()
