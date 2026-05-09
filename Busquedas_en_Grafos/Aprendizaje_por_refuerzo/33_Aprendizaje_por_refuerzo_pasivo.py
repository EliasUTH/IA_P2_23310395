import random

class MDP:
    """
    Clase simple para representar un MDP.
    """

    def __init__(self, states, actions, transitions, rewards, gamma=0.9):
        self.states = states
        self.actions = actions
        self.transitions = transitions
        self.rewards = rewards
        self.gamma = gamma

    def get_reward(self, state, action, next_state):
        return self.rewards.get((state, action, next_state), 0)

    def get_transition_prob(self, state, action, next_state):
        return self.transitions.get((state, action), {}).get(next_state, 0)

    def sample_next_state(self, state, action):
        """Muestrea el siguiente estado dado el estado y acción actuales."""
        probs = self.transitions.get((state, action), {})
        next_states = list(probs.keys())
        probabilities = list(probs.values())
        return random.choices(next_states, probabilities)[0]

class PassiveReinforcementLearning:
    """
    Clase para aprendizaje por refuerzo pasivo: evaluación de política fija.
    """

    def __init__(self, mdp, policy, alpha=0.1, gamma=0.9):
        """
        Inicializa el agente de RL pasivo.

        Parámetros:
        - mdp: instancia de MDP
        - policy: dict de estado -> acción (política fija)
        - alpha: tasa de aprendizaje
        - gamma: factor de descuento
        """
        self.mdp = mdp
        self.policy = policy
        self.alpha = alpha
        self.gamma = gamma
        self.V = {s: 0 for s in mdp.states}  # Valores estimados

    def td_learning(self, episodes=1000):
        """
        Aprendizaje por diferencia temporal (TD(0)) para evaluación de política.

        Parámetros:
        - episodes: número de episodios de experiencia
        """
        for episode in range(episodes):
            state = random.choice(self.mdp.states)  # Estado inicial aleatorio

            while True:  # Hasta estado terminal (asumiendo que hay estados terminales)
                if state not in self.policy:
                    break  # Estado terminal

                action = self.policy[state]
                next_state = self.mdp.sample_next_state(state, action)
                reward = self.mdp.get_reward(state, action, next_state)

                # Actualización TD(0)
                td_target = reward + self.gamma * self.V.get(next_state, 0)
                td_error = td_target - self.V[state]
                self.V[state] += self.alpha * td_error

                state = next_state

                # Detener si es estado terminal (simplificado)
                if state not in self.policy:
                    break

    def get_value_function(self):
        """Retorna la función de valor estimada."""
        return self.V

    def direct_evaluation(self, episodes=1000):
        """
        Evaluación directa de la política (método alternativo).

        Parámetros:
        - episodes: número de episodios
        """
        returns = {s: [] for s in self.mdp.states}

        for episode in range(episodes):
            state = random.choice(self.mdp.states)
            episode_return = 0
            discount = 1
            visited = set()

            while state in self.policy and state not in visited:
                visited.add(state)
                action = self.policy[state]
                next_state = self.mdp.sample_next_state(state, action)
                reward = self.mdp.get_reward(state, action, next_state)

                episode_return += discount * reward
                discount *= self.gamma

                state = next_state

            # Asignar retorno a estados visitados
            for s in visited:
                returns[s].append(episode_return)

        # Promediar retornos
        for s in self.mdp.states:
            if returns[s]:
                self.V[s] = sum(returns[s]) / len(returns[s])

# Ejemplo: MDP simple con política fija
print("=== Aprendizaje por Refuerzo Pasivo ===")

# Definir MDP
states = ['A', 'B', 'C', 'D']  # D es terminal
actions = ['izquierda', 'derecha']

transitions = {
    ('A', 'izquierda'): {'A': 0.9, 'B': 0.1},
    ('A', 'derecha'): {'A': 0.1, 'C': 0.9},
    ('B', 'izquierda'): {'A': 0.8, 'B': 0.2},
    ('B', 'derecha'): {'B': 0.7, 'C': 0.3},
    ('C', 'izquierda'): {'B': 0.6, 'C': 0.4},
    ('C', 'derecha'): {'C': 0.5, 'D': 0.5}  # D es terminal
}

rewards = {
    ('A', 'izquierda', 'A'): -1,
    ('A', 'izquierda', 'B'): 5,
    ('A', 'derecha', 'A'): -1,
    ('A', 'derecha', 'C'): 10,
    ('B', 'izquierda', 'A'): 2,
    ('B', 'izquierda', 'B'): -2,
    ('B', 'derecha', 'B'): -2,
    ('B', 'derecha', 'C'): 1,
    ('C', 'izquierda', 'B'): 3,
    ('C', 'izquierda', 'C'): -3,
    ('C', 'derecha', 'C'): -3,
    ('C', 'derecha', 'D'): 4
}

mdp = MDP(states, actions, transitions, rewards, gamma=0.9)

# Política fija: siempre 'derecha'
policy = {
    'A': 'derecha',
    'B': 'derecha',
    'C': 'derecha'
}

# Agente RL pasivo
rl_agent = PassiveReinforcementLearning(mdp, policy, alpha=0.1, gamma=0.9)

# Aprender con TD(0)
rl_agent.td_learning(episodes=10000)

print("Función de valor estimada con TD(0):")
for state in states:
    if state in rl_agent.V:
        print(f"  V({state}) = {rl_agent.V[state]:.2f}")

# Resetear y usar evaluación directa
rl_agent.V = {s: 0 for s in mdp.states}
rl_agent.direct_evaluation(episodes=10000)


print("\nFunción de valor estimada con Evaluación Directa:")
for state in states:
    if state in rl_agent.V:
        print(f"  V({state}) = {rl_agent.V[state]:.2f}")