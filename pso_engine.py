import numpy as np

class Particle:
    def __init__(self, num_dimensions):
        self.position = np.random.rand(num_dimensions)
        self.velocity = np.random.uniform(-0.2, 0.2, num_dimensions)
        self.pBest_position = self.position.copy()
        self.pBest_fitness = -np.inf

class PSO:
    def __init__(self, num_particles, num_dimensions, w, c1, c2,
                 avg_scores,
                 r1_values_dict=None,
                 r2_values_dict=None,
                 initial_positions_all_particles=None,
                 initial_velocities_all_particles=None):

        self.num_particles = num_particles
        self.num_dimensions = num_dimensions
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.avg_scores = np.array(avg_scores, dtype=float)  # pastikan float
        self.r1_values_dict = r1_values_dict
        self.r2_values_dict = r2_values_dict
        self.initial_positions_all_particles = initial_positions_all_particles
        self.initial_velocities_all_particles = initial_velocities_all_particles

        self.particles = [Particle(num_dimensions) for _ in range(num_particles)]

        if self.initial_positions_all_particles is not None:
            for idx, particle in enumerate(self.particles):
                particle.position = np.array(self.initial_positions_all_particles[idx], dtype=float)

        if self.initial_velocities_all_particles is not None:
            for idx, particle in enumerate(self.particles):
                particle.velocity = np.array(self.initial_velocities_all_particles[idx], dtype=float)

        self.gBest_position = np.zeros(num_dimensions, dtype=float)
        self.gBest_fitness = -np.inf

    def calculate_fitness(self, position):
        normalized_position = position / np.sum(position)
        fitness = np.dot(normalized_position, self.avg_scores)
        return fitness

    def update_global_best(self):
        # Update global best (gBest) after each iteration
        for particle in self.particles:
            if particle.pBest_fitness > self.gBest_fitness:
                self.gBest_fitness = particle.pBest_fitness
                self.gBest_position = particle.pBest_position.copy()

    def run(self, num_iterations):
        log = []

        # Inisialisasi iterasi 0 (hasil pertama)
        for particle in self.particles:
            fitness = self.calculate_fitness(particle.position)
            particle.pBest_position = particle.position.copy()
            particle.pBest_fitness = fitness

        # Update gBest setelah evaluasi pertama
        self.update_global_best()

        # Menampilkan data untuk iterasi pertama
        for idx, particle in enumerate(self.particles):
            log.append({
                "ITERASI": 0,
                "PARTIKEL": idx + 1,
                **{f"x{i+1}": float(particle.position[i]) for i in range(self.num_dimensions)},
                **{f"v{i+1}": float(particle.velocity[i]) for i in range(self.num_dimensions)},
                **{f"r1_x{i+1}": None for i in range(self.num_dimensions)},
                **{f"r2_x{i+1}": None for i in range(self.num_dimensions)},
                "FITNESS": float(particle.pBest_fitness),
                "Status pBest": "UPDATE",
                "Status gBest": "JADI gBest" if np.allclose(particle.pBest_position, self.gBest_position) else "-",
                "∆Fitness": float(particle.pBest_fitness),
                "Performa Fitness": "Naik",
                **{f"pBest_x{i+1}": float(particle.pBest_position[i]) for i in range(self.num_dimensions)},
                **{f"gBest_x{i+1}": float(self.gBest_position[i]) for i in range(self.num_dimensions)},
                "FITNESS gbest": float(self.gBest_fitness),
            })

        for iteration in range(1, num_iterations + 1):
            # Update kecepatan dan posisi
            for idx, particle in enumerate(self.particles):
                r1_matrix = self.r1_values_dict.get(iteration, {}) if self.r1_values_dict else {}
                r2_matrix = self.r2_values_dict.get(iteration, {}) if self.r2_values_dict else {}

                r1 = np.array(r1_matrix.get(idx, np.random.rand(self.num_dimensions)), dtype=float)
                r2 = np.array(r2_matrix.get(idx, np.random.rand(self.num_dimensions)), dtype=float)

                inertia = self.w * particle.velocity
                cognitive = self.c1 * r1 * (particle.pBest_position - particle.position)
                social = self.c2 * r2 * (self.gBest_position - particle.position)

                particle.velocity = np.clip(inertia + cognitive + social, -0.2, 0.2)
                particle.position += particle.velocity
                particle.position = np.clip(particle.position, 0, 1)

            # Simpan fitness & status pbest semua partikel dulu
            fitness_list = []
            status_pbest_list = []

            for particle in self.particles:
                fitness = self.calculate_fitness(particle.position)
                fitness_list.append(fitness)

                if fitness > particle.pBest_fitness:
                    particle.pBest_position = particle.position.copy()
                    particle.pBest_fitness = fitness
                    status_pbest_list.append("UPDATE")
                else:
                    status_pbest_list.append("TETAP")

            # Sekarang update gBest
            self.update_global_best()

            # Setelah gBest ter-update, simpan ke log
            for idx, particle in enumerate(self.particles):
                r1_matrix = self.r1_values_dict.get(iteration, {}) if self.r1_values_dict else {}
                r2_matrix = self.r2_values_dict.get(iteration, {}) if self.r2_values_dict else {}

                r1 = np.array(r1_matrix.get(idx, np.random.rand(self.num_dimensions)), dtype=float)
                r2 = np.array(r2_matrix.get(idx, np.random.rand(self.num_dimensions)), dtype=float)

                log.append({
                    "ITERASI": iteration,
                    "PARTIKEL": idx + 1,
                    **{f"x{i+1}": float(particle.position[i]) for i in range(self.num_dimensions)},
                    **{f"v{i+1}": float(particle.velocity[i]) for i in range(self.num_dimensions)},
                    **{f"r1_x{i+1}": float(r1[i]) for i in range(self.num_dimensions)},
                    **{f"r2_x{i+1}": float(r2[i]) for i in range(self.num_dimensions)},
                    "FITNESS": float(fitness_list[idx]),
                    "Status pBest": status_pbest_list[idx],
                    "Status gBest": "JADI gBest" if np.allclose(particle.pBest_position, self.gBest_position) else "-",
                    "∆Fitness": float(fitness_list[idx] - particle.pBest_fitness),
                    "Performa Fitness": "Naik" if fitness_list[idx] > particle.pBest_fitness else ("Turun" if fitness_list[idx] < particle.pBest_fitness else "Tetap"),
                    **{f"pBest_x{i+1}": float(particle.pBest_position[i]) for i in range(self.num_dimensions)},
                    **{f"gBest_x{i+1}": float(self.gBest_position[i]) for i in range(self.num_dimensions)},
                    "FITNESS gbest": float(self.gBest_fitness),
                })

        return log, self.gBest_position, self.gBest_fitness
