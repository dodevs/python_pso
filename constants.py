X_DOMAIN = [-100,100]
Y_DOMAIN = [-100,100]
EXECUTIONS = 10
ITERATIONS = [20, 50, 100]
SUCCESS_THRESHOLD = 1e-6 # fitness abaixo disso conta como minimo global (0)

# w: peso de inercia (inicial, final), decai linearmente ao longo das iteracoes
# topology: raio da vizinhanca em anel (0 = gB global, k = melhor entre k vizinhos de cada lado)
PROFILES = {
    # Conforme a especificacao do trabalho: sem inercia, phi = 2, vmax = 15%
    "spec": dict(particles=20, phi1=2.0, phi2=2.0, w=(1.0, 1.0), velocity_limit=0.15, topology=0),
    # Ajuste por busca aleatoria (20 particulas)
    "tuned": dict(particles=20, phi1=2.32, phi2=2.498, w=(0.968, 0.389), velocity_limit=0.5, topology=3),
    # Ajuste irrestrito: populacao maior
    "tuned200": dict(particles=200, phi1=1.708, phi2=1.808, w=(0.897, 0.568), velocity_limit=0.5, topology=1),
}
