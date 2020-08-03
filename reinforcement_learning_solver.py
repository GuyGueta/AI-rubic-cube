from cube_utils import gen_sample, action_map, perc_solved_cube, gen_sample_2, action_map_small, flatten_1d_b
# import tensorflow.keras.backend as K
# import numpy as np
# from tensorflow.keras.layers import Dense, Input, LeakyReLU
# from tensorflow.keras.models import Model
# from tensorflow.keras.optimizers import Adam


# def acc(y_true, y_pred):
#     return K.cast(K.equal(K.max(y_true, axis=-1),
#                           K.cast(K.argmax(y_pred, axis=-1), K.floatx())),
#                   K.floatx())


# def get_model(lr=0.0001):
#     input1 = Input((324,))
#
#     d1 = Dense(1024)
#     d2 = Dense(1024)
#     d3 = Dense(1024)
#
#     d4 = Dense(50)
#
#     x1 = d1(input1)
#     x1 = LeakyReLU()(x1)
#     x1 = d2(x1)
#     x1 = LeakyReLU()(x1)
#     x1 = d3(x1)
#     x1 = LeakyReLU()(x1)
#     x1 = d4(x1)
#     x1 = LeakyReLU()(x1)
#
#     out_value = Dense(1, activation="linear", name="value")(x1)
#     out_policy = Dense(len(action_map_small), activation="softmax", name="policy")(x1)
#
#     model = Model(input1, [out_value, out_policy])
#
#     model.compile(loss={"value": "mae", "policy": "sparse_categorical_crossentropy"}, optimizer=Adam(lr),
#                   metrics={"policy": acc})
#     model.summary()
#
#     return model

#
# def solve_reinforcement_learning(action_for_scramble=None):
#     file_path = "weights.h5"
#     num_scrambles = 5
#     model = get_model()
#     model.load_weights(file_path)
#     if not action_for_scramble:
#         sample_x, sample_y, cubes = gen_sample(num_scrambles)
#     else:
#         # if we have list of action for scramble:
#         sample_x, sample_y, cubes = gen_sample_2(action_for_scramble)
#
#     cube = cubes[0]
#     cube.score = 0
#     list_sequences = [[cube]]
#     print(list_sequences)
#     existing_cubes = set()
#
#     for j in range(1000):
#         print(j)
#         X = [flatten_1d_b(x[-1]) for x in list_sequences]
#
#         value, policy = model.predict(np.array(X), batch_size=1024)
#
#         new_list_sequences = []
#
#         for x, policy in zip(list_sequences, policy):
#
#             pred = np.argsort(policy)
#             cube_1 = x[-1].copy()(list(action_map.keys())[pred[-1]])
#             cube_2 = x[-1].copy()(list(action_map.keys())[pred[-2]])
#
#             new_list_sequences.append(x + [cube_1])
#             new_list_sequences.append(x + [cube_2])
#
#         print("new_list_sequences", len(new_list_sequences))
#         last_states_flat = [flatten_1d_b(x[-1]) for x in new_list_sequences]
#         value, _ = model.predict(np.array(last_states_flat), batch_size=1024)
#         value = value.ravel().tolist()
#         for x, v in zip(new_list_sequences, value):
#             x[-1].score = v if str(x[-1]) not in existing_cubes else -1
#
#         new_list_sequences.sort(key=lambda x: x[-1].score, reverse=True)
#         new_list_sequences = new_list_sequences[:100]
#         existing_cubes.update(set([str(x[-1]) for x in new_list_sequences]))
#         list_sequences = new_list_sequences
#         list_sequences.sort(key=lambda x: perc_solved_cube(x[-1]), reverse=True)
#         prec = perc_solved_cube((list_sequences[0][-1]))
#         print(prec)
#
#         if prec == 1:
#             break
#
#     print(perc_solved_cube(list_sequences[0][-1]))
#     print(list_sequences[0][-1])
