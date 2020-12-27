import numpy as np
import pyautogui
import time
pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
pyautogui.PAUSE = 0  #
pyautogui.FAILSAFE = True  # Set to false in real world


class Mouse:
    def __init__(self, screen_size=None):
        self._nervousness = 0.5
        self._control = 0.5
        self._s_width, self._s_height = pyautogui.size() if screen_size is None else screen_size

    def left_click(self):
        pyautogui.click()

    def right_click(self):
        pyautogui.click(pyautogui.RIGHT)

    def move_to(self, p_destination, velocity=1, max_deviation=0.05):
        '''
        p_destination : where to go in the screen
        velocity : pixels per second
        '''
        t_d = 0.001
        p_origin = pyautogui.position()

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
            pyautogui.moveTo(p[0], p[1])

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
            T = np.sort(np.random.triangular(0.0, np.random.uniform(0.7,1.), 1.0, steps))
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

    def _add_noise(self, points, ammount, max_deviation):
        N = len(points)
        n_points = int(N * ammount)
        if n_points % 2 == 1:
            n_points -= 1
        if n_points == 0:
            return points

        # Calculamos a que puntos queremos anadir ruido
        i_noise = np.random.choice(range(N), n_points)

        # Calculamos el ruido
        noise_inc_x = np.random.uniform(size=n_points//2)
        noise_inc_y = np.random.uniform(size=n_points//2)
        noise_dec_x = np.random.uniform(size=n_points//2)
        noise_dec_y = np.random.uniform(size=n_points//2)

        # Lo normalizamos
        noise_inc_x /= np.sum(noise_inc_x)
        noise_inc_y /= np.sum(noise_inc_y)
        noise_dec_x /= np.sum(noise_dec_x)
        noise_dec_y /= np.sum(noise_dec_y)

        # Convertimos el mayor valor a 1
        noise_inc_x /= np.max(noise_inc_x)
        noise_inc_y /= np.max(noise_inc_y)
        noise_dec_x /= np.max(noise_dec_x)
        noise_dec_y /= np.max(noise_dec_y)

        # Multiplicamos por la maxima desviacion
        noise_inc_x *= max_deviation
        noise_inc_y *= max_deviation
        noise_dec_x *= max_deviation
        noise_dec_y *= max_deviation

        # Creamos los vectores de ruido
        noise_x = np.concatenate((noise_inc_x, -noise_dec_x))
        noise_y = np.concatenate((noise_inc_y, -noise_dec_y))
        np.random.shuffle(noise_x)
        np.random.shuffle(noise_y)

        noise_points = np.column_stack((noise_x, noise_y))

        assert len(noise_points) == n_points

        noise_count = 0
        noise_sum = np.array((0., 0.))
        for i in range(N):
            if i in i_noise:
                noise_sum += noise_points[noise_count]
                noise_count += 1
            points[i] += noise_sum

        # A algunos puntos incrementamos y otros decrementamos
        #i = np.random.choice(range(N), n_points)
        #points[i] += noise_inc_x

        return points
