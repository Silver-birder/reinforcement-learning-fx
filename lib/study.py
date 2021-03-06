import sys,os
import gym
import numpy

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

sys.path.append(os.pardir)
from etc import constant

class Study():
	def __init__(self):
		Episodes = 1

		obs = []

		ENV_NAME = 'FxEnv-v0'

		env = gym.make(ENV_NAME)
		numpy.random.seed(123)
		env.seed(123)
		nb_actions = env.action_space.n

		# Next, we build a very simple model.
		model = Sequential()
		model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
		model.add(Dense(16))
		model.add(Activation('relu'))
		model.add(Dense(16))
		model.add(Activation('relu'))
		model.add(Dense(16))
		model.add(Activation('relu'))
		model.add(Dense(nb_actions))
		model.add(Activation('linear'))
		print(model.summary())

		# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
		# even the metrics!
		memory = SequentialMemory(limit=144000, window_length=1)
		policy = BoltzmannQPolicy()
		dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=7200,
					   target_model_update=1e-2, policy=policy)
		dqn.compile(Adam(lr=1e-3), metrics=['mae'])

		# Okay, now it's time to learn something! We visualize the training here for show, but this
		# slows down training quite a lot. You can always safely abort the training prematurely using
		# Ctrl + C.
		dqn.fit(env, nb_steps=144000, visualize=True, verbose=2)

		# After training is done, we save the final weights.
		dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
