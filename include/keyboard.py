import time
import string

import numpy as np
#import pyautogui
#pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
#pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
#pyautogui.PAUSE = 0  #
#pyautogui.FAILSAFE = True  # Set to false in real world

class Keyboard:
    def __init__(self, layout, person_seed):
        self._layout = layout
        self._key_to_index = {i:k for k,i in enumerate(self._layout.keys())}
        self._index_to_key = {k:i for k,i in enumerate(self._layout.keys())}

        # Unrandomized section
        np.random.seed(person_seed)

        self._handicap = np.random.uniform()
        self._move_delay_matrix = self._generate_move_delay_matrix()
        self._hold_delay_dict = self._generate_hold_delay_dict()

        np.random.seed()

    def type_text(self, text, stress=0.3):
        shifted_keys = '~!@#$%^&*()_+{}|:"<>?' + string.ascii_uppercase
        
        keys = self.generate_keys(text, stress)

        # Press keys in that order
        #try:
        for i, k in enumerate(keys):
            print(k)
            intended_key = k[0]
            needs_shift = k[1]
            movement_delay = k[2]
            hold_delay = k[3]

            time.sleep(movement_delay)
            if needs_shift:
                self.hold_key('shift')

            self.press_key(intended_key, hold_delay)

            if i != len(keys)-1 and not keys[i+1][1]:
                self.release_key('shift')
        #except Exception as e:
        #    print(e)

    def generate_keys(self, text, stress):
        keys = []
        shifted_keys = '~!@#$%^&*()_+{}|:"<>?' + string.ascii_uppercase

        typo_posibility = stress * 0.2

        for i, c in enumerate(text):
            last_key = self.char_to_key(text[i - 1])
            this_key = self.char_to_key(c)

            if i != 0 and np.random.uniform() <= typo_posibility and this_key not in ['tab', 'return']:
                # Add typo and keys
                max_time = int(5 * stress)
                time_to_notice = 0 if max_time <= 1 else np.random.randint(1, max_time)
                time_to_notice = time_to_notice if time_to_notice < len(text) - i else len(text) - i
                key = self._generate_typo(c)

                origin_i = self._key_to_index[last_key]
                dest_i = self._key_to_index[key]

                movement_delay = self._move_delay_matrix[origin_i][dest_i] * 0.1 * self._handicap

                hold_delay = self._hold_delay_dict[key]
                needs_shift = key in shifted_keys

                # A key action has: key, wheter it needs shift, movement shift and hold delay    
                keys.append( [key, needs_shift, movement_delay, hold_delay] )

                _c = self.char_to_key(text[i])
                for j in range(time_to_notice):
                    _last_c = self.char_to_key(text[i + j - 1])
                    _c = self.char_to_key(text[i + j])
                    origin_i = self._key_to_index[_last_c]
                    dest_i = self._key_to_index[_c]

                    movement_delay = self._move_delay_matrix[origin_i][dest_i] * 0.1 * self._handicap

                    hold_delay = self._hold_delay_dict[_c]
                    needs_shift = _c in shifted_keys

                    # A key action has: key, wheter it needs shift, movement shift and hold delay    
                    keys.append( [_c, needs_shift, movement_delay, hold_delay] )

                # Backspace with delay
                origin_i = self._key_to_index[_c]
                dest_i = self._key_to_index['backspace']

                movement_delay = self._move_delay_matrix[origin_i][dest_i] * 0.1 * self._handicap
                hold_delay = self._hold_delay_dict['backspace']
                keys.append( ['backspace', False, movement_delay, hold_delay] )
                # Rest of backspaces
                for _ in range(time_to_notice):
                    keys.append( ['backspace', False, 0.05 + np.random.uniform(-0.005, 0.005), hold_delay] )

            if i == 0:
                movement_delay = 0
            else:
                origin_i = self._key_to_index[last_key]
                dest_i = self._key_to_index[this_key]

                movement_delay = self._move_delay_matrix[origin_i][dest_i] * 0.1 * self._handicap

            hold_delay = self._hold_delay_dict[this_key]
            needs_shift = c in shifted_keys

            # A key action has: key, wheter it needs shift, movement shift and hold delay    
            keys.append( [this_key, needs_shift, movement_delay, hold_delay] )

        return keys

    def press_key(self, char, delay=0.0):
        if char not in pyautogui.KEYBOARD_KEYS:
            raise Exception(f"{char} is not a valid key to press")

        #pyautogui.keyDown(char)
        time.sleep(delay)
        #pyautogui.keyUp(char)

    def hold_key(self, char):
        #if char not in pyautogui.KEYBOARD_KEYS:
        #    raise Exception(f"{char} is not a valid key to press")

        #pyautogui.keyDown(char)

    def release_key(self, char):
        #if char not in pyautogui.KEYBOARD_KEYS:
        #    raise Exception(f"{char} is not a valid key to press")

        #pyautogui.keyUp(char)

    def char_to_key(self, char):
        if char == ' ':
            intended_key = 'space'
        elif char == '\n':
            intended_key = 'return'
        elif char == '\t':
            intended_key = 'tab'
        else:
            intended_key = char.lower()
        return intended_key

    def _generate_typo(self, intended_key):
        needs_shift = '~!@#$%^&*()_+{}|:"<>?' + string.ascii_uppercase

        if intended_key == ' ':
            intended_key = 'space'
        elif intended_key == '\n':
            intended_key = 'return'
        elif intended_key == '\t':
            intended_key = 'tab'
        else:
            intended_key = intended_key.lower()

        # We generate a random displacement
        x_offset = np.random.randint(-1,2)
        y_offset = np.random.randint(-1,2)

        typo_coordinates = np.array(self._layout[intended_key]) - np.array((x_offset, y_offset))

        # Find posibilities
        typo_key = intended_key
        for k, v in self._layout.items():
            if np.all(np.array(v) == typo_coordinates) and k not in needs_shift:
                typo_key = k

        return typo_key

    def _generate_hold_delay_dict(self):
        hold_dict = {k: self._handicap * np.random.uniform(low=0.2,high=0.6) for k in self._layout.keys()}
        return hold_dict
    
    def _generate_move_delay_matrix(self):
        # First we generate a index number for each key
        key_to_index = {i:k for k,i in enumerate(self._layout.keys())}
        
        # We calculate a distance matrix for each combination of keys
        distance_matrix = np.empty((len(self._key_to_index), len(self._key_to_index)))
        for k_i, i in self._key_to_index.items():
            for k_j, j in self._key_to_index.items():
                # We calculate the distance between the two keys
                pos_i = np.array(self._layout[k_i])
                pos_j = np.array(self._layout[k_j])
                distance = np.linalg.norm(pos_i - pos_j)

                distance_matrix[i][j] = distance
        
        # Now we sum to the places where the destination is a letter, a scalar proportional to the handicap
        for k, i in self._key_to_index.items():
            if k not in string.ascii_letters:
                continue
            
            distance_matrix[:][i] += np.random.uniform(low=self._handicap, high=self._handicap+0.3) 

        # Now we sum to the places where the destination is a number, a scalar proportional to the handicap
        for k, i in self._key_to_index.items():
            if k not in string.digits:
                continue
            
            distance_matrix[:][i] += np.random.uniform(low=self._handicap+0.1, high=self._handicap+0.4) 

        # Now we sum to the places where the destination is a symbol, a scalar proportional to the handicap
        for k, i in self._key_to_index.items():
            if k not in string.punctuation.split() + ["return", "backspace", "ctrl", "shift", "capslock", "tab", "esc", "space"]:
                continue
            
            distance_matrix[:][i] += np.random.uniform(low=self._handicap+0.2, high=self._handicap+0.6) 

        return distance_matrix