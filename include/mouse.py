import numpy as np
#import pyautogui
import time
#pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
#pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
#pyautogui.PAUSE = 0  #
#pyautogui.FAILSAFE = True  # Set to false in real world


class Mouse:
    def __init__(self, screen_size):
        self._nervousness = 0.5
        self._control = 0.5
        self._s_width, self._s_height = screen_size

    #def left_click(self):
    #    pyautogui.click()

    #def right_click(self):
    #    pyautogui.click(pyautogui.RIGHT)

    def move_to(self, p_destination, velocity=1, max_deviation=0.05):
        '''
        p_destination : where to go in the screen
        velocity : pixels per second
        '''
        t_d = 0.001
        #p_origin = pyautogui.position()

        # Normalize values to [0:1)
        x_o = p_origin[0]/self._s_width
        y_o = p_origin[1]/self._s_height
        x_d = p_destination[0]/self._s_width
        y_d = p_destination[1]/self._s_height

        # Generate Bezier curve
        p_0 = np.array([x_o, y_o])
        p_3 = np.array([x_d, y_d])
        points = self.generate_cubic_bezier(p_0, p_3, max_deviation=max_deviation, velocity=velocity)

        # Add noise
        #points = self._add_noise(points, 0.005, 0.01)

        # Bring points back to pixels
        points[:, 0] *= self._s_width
        points[:, 1] *= self._s_height

        # Move
        for p in points:
            time.sleep(t_d)
            #pyautogui.moveTo(p[0], p[1])

    def chain_clicks(self, destinations, randomize=False):
        if randomize:
            np.random.shuffle(destinations)

        for d in destinations:
            self.move_to(d, max_deviation=0.01)
            self.left_click()

    def generate_cubic_bezier(self, p_0, p_3, 
                                max_deviation=0.05, 
                                velocity=0.5, 
                                n_steps=None, 
                                linear_progression=False):
        # Calculamos los puntos de anclaje de la curva con la formula
        rand = max_deviation - np.random.uniform() * max_deviation * 2
        rand2 = max_deviation - np.random.uniform() * max_deviation * 2
        p_1 = p_0 + np.array([rand, rand2])

        rand = max_deviation - np.random.uniform() * max_deviation * 2
        rand2 = max_deviation - np.random.uniform() * max_deviation * 2
        p_2 = p_3 + np.array([rand, rand2])

        points = []

        # Calculamos los tiempos en los que movernos
        # el numero de puntos intermedios sera proporcional a la distancia
        steps = np.random.randint(800, 1000) if n_steps is None else n_steps
        if linear_progression:
            T = np.array(range(0, n_steps)) / n_steps
        else:
            T = np.sort(np.random.triangular(0.0, np.random.uniform(0.9,1.), 1.0, steps))
            T = np.insert(T, 0, 0, axis=0)
            T = np.insert(T, len(T), 1, axis=0)

        for t_i in T:
            t = t_i
            s_0 = p_0*(1-t)**3
            s_1 = 3 * p_1 * t * (1 - t)**2
            s_2 = 3 * p_2 * (1-t) * t**2
            s_3 = p_3 * t**3

            p = s_0 + s_1 + s_2 + s_3

            points.append(p)

        return np.array(points)
    
    def add_noise(self, points, noisiness, max_deviation):
        '''
        `points` - Puntos a los que anadir ruido \n
        `noisiness` - Valor [0-1) que determina a que porcentaje de puntos anadir ruido \n
        `max_deviation` - Desviacion maxima 
        '''
        assert 1 > noisiness and noisiness >= 0
        assert len(points) != 0

        if noisiness == 0:
            return points

        # Calculate N points that we will create
        n_noisy_points = int(len(points) * noisiness)
        
        # Make it a pair number
        n_noisy_points = n_noisy_points if n_noisy_points % 2 == 0 else n_noisy_points - 1

        # Get a random set of points that we will add noise to
        i_noisy_points = []
        for _ in range(n_noisy_points):
            i = np.random.randint(1, len(points))

            # If we already took that index repeat
            while i in i_noisy_points:
                i = np.random.randint(1, len(points))

            i_noisy_points.append(i)

        # Calculate the vectors leading to those points
        vectors = []
        for i in i_noisy_points:
            vectors.append(points[i] - points[i - 1])
        vectors = np.array(vectors)

        # Choose pairs of vectors
        vs_1, vs_2 = np.split(vectors, 2)
        is_1, is_2 = np.split(np.array(i_noisy_points), 2)
        noise = np.zeros((len(points), 2))
        for i_1, i_2, v_1, v_2 in zip(is_1, is_2, vs_1, vs_2):
            # Calculate max deviations
            max_x_deviation = abs(min(v_1[0], v_2[0]))
            max_y_deviation = abs(min(v_1[1], v_2[1]))

            max_x_deviation *= max_deviation
            max_y_deviation *= max_deviation

            # Calculate noise
            n = np.empty(2)
            n[0] = np.random.uniform(-max_x_deviation, max_x_deviation)
            n[1] = np.random.uniform(-max_y_deviation, max_y_deviation)

            # Add opposite noise to each
            noise[i_1] += n
            noise[i_2] -= n

        new_points = []
        noise_sum = np.zeros(2)
        # delete the first point 
        new_points.append(points[0])

        # Recalculate points
        for og_p, n in zip(points[1:], noise[1:]):
            noise_sum += n
            new_p = og_p + noise_sum
            new_points.append(new_p)

        return np.array(new_points)