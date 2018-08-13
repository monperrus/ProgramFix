import copy
import math
import random
from collections import namedtuple

import numpy as np
import torch
import torch.nn.functional as F
import gym
from torch.distributions import Categorical
from tqdm import tqdm

from common.logger import info
from common.torch_util import create_sequence_length_mask
from common.util import data_loader
from error_generation.find_closest_group_data.token_level_closest_text import \
    calculate_distance_and_action_between_two_code


SavedAction = namedtuple('SavedAction', ['log_prob'])


def generate_action_between_two_code(error_tokens, ac_tokens, max_distance=None, get_value=None):
    distance, action_list = calculate_distance_and_action_between_two_code(error_tokens, ac_tokens,
                                                                      max_distance=max_distance, get_value=get_value)
    if distance > max_distance:
        distance = -1
        action_list = None
    return distance, action_list


def generate_error_code_from_ac_code_and_action_fn(inner_end_id, begin_id, end_id):
    def generate_error_code_from_ac_code_and_action(input_data, states, action, direct_output=False):
        """

        :param input_data:
        :param states:
        :param action: p1, p2, is_copy, copy_ids, sample_ids. p1 express start position of sample.
        p2 express the end position of sample
        sample position: (p1, p2).
        :return:
        """
        # output_record_list, output_record_probs = create_output_from_actions(states, action, do_sample=True, direct_output=direct_output)
        p1, p2, is_copy, copy_ids, sample_output, sample_output_ids = action

        sample_output_ids_list = sample_output_ids.tolist()
        effect_sample_output_list = []
        for sample in sample_output_ids_list:
            try:
                end_pos = sample.index(inner_end_id)
                sample = sample[:end_pos]
            except ValueError as e:
                pass
            effect_sample_output_list += [sample]
        effect_sample_output_list_length = [len(s) for s in effect_sample_output_list]

        input_seq = input_data['input_seq']
        final_output = []
        for i, one_input in enumerate(input_seq):
            effect_sample = effect_sample_output_list[i]
            one_output = one_input[1:p1[i] + 1] + effect_sample + one_input[p2[i]:-1]
            final_output += [one_output]

        next_input = [[begin_id] + one + [end_id] for one in final_output]
        # next_input = [next_inp if con else ori_inp for ori_inp, next_inp, con in
        #               zip(input_data['input_seq'], next_input, continue_list)]
        next_input_len = [len(one) for one in next_input]
        final_output = [next_inp[1:-1] for next_inp in next_input]

        input_data['input_seq'] = next_input
        input_data['input_length'] = next_input_len
        input_data['copy_length'] = next_input_len
        return input_data, final_output, effect_sample_output_list_length
    return generate_error_code_from_ac_code_and_action

def create_output_from_actions_fn(create_or_sample_fn):
    def create_output_from_actions(model_input, model_output, do_sample=False, direct_output=False,
                                   explore_p=0, p2_step_length=3):
        """

        :param model_input:
        :param model_output: p1, p2, is_copy, copy_output, sample_output, compatible_tokens
        sample position: (p1, p1 + p2 + 1).
        :param do_sample:
        :param direct_output:
        :return:
        """
        p1_o, p2_o, is_copy, copy_output, sample_output, output_compatible_tokens = model_output
        if do_sample:
            compatible_tokens = output_compatible_tokens
        else:
            compatible_tokens = model_input[8]

        p1_prob = F.softmax(p1_o, dim=-1)
        p1, p1_log_probs = create_or_sample_fn(p1_prob, explore_p)

        total_mask = create_p2_position_mask(p1_o, p1, p2_step_length)
        p2_o = p2_o.data.masked_fill_(~total_mask, -float('inf'))

        p2_prob = F.softmax(p2_o, dim=-1)
        p2, p2_log_probs = create_or_sample_fn(p2_prob, explore_p)

        if not direct_output:

            is_copy_sigmoid = torch.sigmoid(is_copy)
            not_copy_probs = 1 - is_copy_sigmoid
            is_copy_cat_probs = torch.stack([not_copy_probs, is_copy_sigmoid], dim=-1)
            is_copy, is_copy_log_probs = create_or_sample_fn(is_copy_cat_probs, explore_p)

            copy_output_prob = F.softmax(copy_output, dim=-1)
            sample_output_prob = F.softmax(sample_output, dim=-1)
            copy_output_id, copy_output_log_probs = create_or_sample_fn(copy_output_prob, explore_p)
            sample_output_id, sample_output_log_probs = create_or_sample_fn(sample_output_prob, explore_p)

            sample_output = torch.squeeze(torch.gather(compatible_tokens, dim=-1, index=torch.unsqueeze(sample_output_id, dim=-1)), dim=-1)

            input_seq = model_input[1]
            copy_output = torch.gather(input_seq, index=copy_output_id, dim=-1)
        is_copy_byte = is_copy.byte()
        sample_output_ids = torch.where(is_copy_byte, copy_output, sample_output)
        sample_output_ids_log_probs = torch.where(is_copy_byte, copy_output_log_probs, sample_output_log_probs)
        # print(torch.sum(p1_log_probs))
        # print(torch.sum(p2_log_probs))
        # print(torch.sum(is_copy_log_probs))
        # print(torch.sum(copy_output_log_probs))
        # print(torch.sum(sample_output_log_probs))
        # print(torch.sum(sample_output_ids_log_probs))

        return (p1, p2, is_copy, copy_output, sample_output, sample_output_ids), \
               (p1_log_probs, p2_log_probs, is_copy_log_probs, copy_output_log_probs, sample_output_log_probs, sample_output_ids_log_probs)
    return create_output_from_actions


def create_p2_position_mask(p1_o, p1, p2_step_length):
    max_len = p1_o.shape[1]
    batch_size = p1_o.shape[0]
    idxes = torch.arange(0, max_len, out=torch.Tensor(max_len)).to(p1.device).long().unsqueeze(0).expand(batch_size, -1)
    p2_position_max = p1 + p2_step_length + 1
    gt_mask = idxes > torch.unsqueeze(p1, dim=1)
    lt_mask = idxes < torch.unsqueeze(p2_position_max, dim=1)
    total_mask = gt_mask & lt_mask
    res = torch.eq(torch.sum(total_mask, dim=-1), 0)
    total_mask = torch.where(torch.unsqueeze(res, dim=1), torch.ones_like(total_mask).byte(), total_mask)
    return total_mask


def create_or_sample(probs, explore_p):
    if random.random() < explore_p:
        m = Categorical(probs)
        output = m.sample()
        output_log_probs = m.log_prob(output)
    else:
        output_probs, output = torch.topk(probs, dim=-1, k=1)
        output = torch.squeeze(output, dim=-1).data
        output_log_probs = torch.squeeze(torch.log(output_probs), dim=-1)
    return output, output_log_probs


def create_random_sample(probs, explore_p):
    random_probs = torch.ne(probs, 0.0).float()
    m = Categorical(random_probs)
    output = m.sample()
    output_probs = torch.squeeze(torch.gather(probs, index=torch.unsqueeze(output, dim=-1), dim=-1), dim=-1)
    output_log_probs = torch.log(output_probs)
    return output, output_log_probs


def create_reward_by_compile(result_list, states, actions, continue_list):
    """
    calculate reward by compile result and states and actions.
    :param result_list:
    :param states:
    :param actions:
    :return:
    """
    p1 = actions[0]
    p2 = actions[1]

    new_result_list = []
    for res, con in zip(result_list, continue_list):
        if con and res:
            rew = -1.0
        elif con and not res:
            rew = 1.0
        else:
            rew = 0
        new_result_list += [rew]
    done_list = [False if res else True for res in result_list]
    return new_result_list, done_list


# def deal_with_reward_fn(s_model, parse_input_batch_data_fn, g_create_next_input_batch_fn, s_create_next_input_batch_fn,
#                         compile_code_ids_fn, vocabulary, extract_includes_fn, file_path, target_file_path,
#                         create_reward_by_compile_fn):
#     def deal_with_reward(states, state_tensor, actions):
#         batch_data, output_ids, _ = g_create_next_input_batch_fn(states, state_tensor, actions)
#         model_input = parse_input_batch_data_fn(batch_data, do_sample=True)
#         model_output = s_model.forward(*model_input, do_sample=True)
#         input_data, final_output, output_records = s_create_next_input_batch_fn(states, model_input, model_output, )
#
#         batch_size = model_input.shape[0]
#         continue_list = [True for _ in range(batch_size)]
#         result_list = [False for _ in range(batch_size)]
#         _, result_list = compile_code_ids_fn(final_output, continue_list, result_list,
#                                                            vocabulary=vocabulary,
#                                                            includes_list=extract_includes_fn(input_data),
#                                                            file_path=file_path,
#                                                            target_file_path=target_file_path)
#         reward_list, done_list = create_reward_by_compile_fn(result_list, states, actions)
#         save_list = [rew > 0 for rew in reward_list]
#
#         return reward_list, done_list, save_list, output_ids
#     return deal_with_reward

count = 0
class GenerateEnvironment(gym.Env):
    def __init__(self, s_model, dataset, batch_size, preprocess_next_input_for_solver_fn,
                 parse_input_batch_data_for_solver_fn, solver_create_next_input_batch_fn, vocabulary,
                 compile_code_ids_fn, extract_includes_fn, create_reward_by_compile_fn, data_radio=1.0):
        self.s_model = s_model
        self.dataset = dataset
        self.batch_size = batch_size
        self.preprocess_next_input_for_solver_fn = preprocess_next_input_for_solver_fn
        self.parse_input_batch_data_for_solver_fn = parse_input_batch_data_for_solver_fn
        self.solver_create_next_input_batch_fn = solver_create_next_input_batch_fn
        self.vocabulary = vocabulary
        self.compile_code_ids_fn = compile_code_ids_fn
        self.extract_includes_fn = extract_includes_fn
        self.data_radio = data_radio
        self.create_reward_by_compile_fn = create_reward_by_compile_fn

        self.continue_list = [True for _ in range(batch_size)]
        self.result_list = [False for _ in range(batch_size)]

    def reset(self):
        with tqdm(total=len(self.dataset) * self.data_radio) as pbar:
            for batch_data in data_loader(self.dataset, batch_size=self.batch_size, drop_last=False,
                                          epoch_ratio=self.data_radio):
                self.continue_list = [True for _ in range(self.batch_size)]
                self.result_list = [True for _ in range(self.batch_size)]
                yield batch_data
                pbar.update(self.batch_size)

    def step(self, actions, states, states_tensor, file_path, target_file_path):
        with torch.no_grad():
            p1 = (actions[0]-1).tolist()
            p2 = (actions[1]-1).tolist()
            ac_action_pos = list(zip(p1, p2))
            ori_states = states.copy()
            batch_data, output_ids, effect_sample_output_list_length = self.preprocess_next_input_for_solver_fn(states, states_tensor, actions)
            ori_error_data = batch_data.copy()
            model_input = self.parse_input_batch_data_for_solver_fn(batch_data, do_sample=True)
            model_output = self.s_model.forward(*model_input, do_sample=True)
            input_data, final_output, output_records = self.solver_create_next_input_batch_fn(batch_data, model_input, model_output, self.continue_list)

            _, self.result_list = self.compile_code_ids_fn(final_output, self.continue_list, self.result_list,
                                                 vocabulary=self.vocabulary,
                                                 includes_list=self.extract_includes_fn(input_data),
                                                 file_path=file_path,
                                                 target_file_path=target_file_path)

            print_output = True
            global count
            count += 1
            if print_output and count % 10 == 0:
                k = 0
                for ori_code_id, ori_error_id, fin_code_id, res in zip(ori_states['input_seq'], ori_error_data['input_seq'], final_output, self.result_list):
                    if not res:
                        ori_code_id = ori_code_id[1:-1]
                        ori_error_id = ori_error_id[1:-1]

                        ori_code_list = [self.vocabulary.id_to_word(c) for c in ori_code_id]
                        ori_code = ' '.join(ori_code_list)

                        ori_error_list = [self.vocabulary.id_to_word(c) for c in ori_error_id]
                        ori_error_code = ' '.join(ori_error_list)

                        fin_code_list = [self.vocabulary.id_to_word(c) for c in fin_code_id]
                        fin_code = ' '.join(fin_code_list)

                        info('--------------------------- one ------------------------------------')
                        for a in actions:
                            info(str(a[k]))
                        info('ori_code: '+ori_code)
                        info('err_code: '+ori_error_code)
                        info('fin_code: '+fin_code)
                    k += 1


            reward_list, done_list = self.create_reward_by_compile_fn(self.result_list, states, actions, self.continue_list)
            self.continue_list = [not done for done in done_list]

            save_list = [reward > 0 for reward in reward_list]
        return ori_error_data, reward_list, done_list, {'save_list': save_list,
                                                        'ac_action_pos': ac_action_pos,
                                                        'effect_sample_output_list_length': effect_sample_output_list_length}

    def render(self, mode=''):
        return

    def seed(self, seed=None):
        if seed is not None:
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            np.random.seed(seed)
            random.seed(seed)
        return

    def close(self):
        return

    def eval(self):
        self.s_model.eval()

    def train(self):
        self.s_model.train()


def sample_generate_action_fn(create_output_from_actions_fn, calculate_encoder_sample_length_fn,
                              mask_sample_probs_with_length_fn, init_explore_p=0.1, min_explore_p=0.001,
                              decay_step=10000, decay=0.2, p2_step_length=3):
    steps = 0
    explore_p = init_explore_p

    def decay_explore():
        nonlocal explore_p
        if explore_p == min_explore_p:
            return
        explore_p_new = explore_p * decay
        if explore_p_new < min_explore_p:
            explore_p = min_explore_p
        return

    def sample_generate_action(states_tensor, model_output, do_sample=True, direct_output=False):
        nonlocal steps, explore_p
        steps += 1
        if steps % decay_step == 0:
            decay_explore()

        final_actions, final_actions_probs = create_output_from_actions_fn(states_tensor, model_output,
                                                                           do_sample=do_sample,
                                                                           direct_output=direct_output,
                                                                           explore_p=explore_p,
                                                                           p2_step_length=p2_step_length)
        sample_length = calculate_encoder_sample_length_fn(final_actions)
        final_actions_probs = mask_sample_probs_with_length_fn(final_actions_probs, sample_length)

        return final_actions, (final_actions_probs, )

    return sample_generate_action


def calculate_encoder_sample_length_fn(inner_end_id):
    def calculate_encoder_sample_length(actions):
        """

        :param actions:
        :return:
        """
        p1, p2, is_copy, copy_output, sample_output, sample_output_ids = actions

        sample_output_ids_list = sample_output_ids.tolist()
        sample_length = []
        for sample in sample_output_ids_list:
            try:
                end_pos = sample.index(inner_end_id)
                end_pos += 1
            except ValueError as e:
                end_pos = len(sample)
            sample_length += [end_pos]
        return sample_length
    return calculate_encoder_sample_length


def mask_sample_probs_with_length(action_probs, sample_length):
    """

    :param action_probs: probs with special shape like [batch, seq]
    :param sample_length:
    :return:
    """
    p1_log_probs, p2_log_probs, is_copy_log_probs, copy_output_log_probs, sample_output_log_probs, \
    sample_output_ids_log_probs = action_probs
    if not isinstance(sample_length, torch.Tensor):
        sample_length_tensor = torch.LongTensor(sample_length).to(is_copy_log_probs.device)
    else:
        sample_length_tensor = sample_length
    length_mask_float = create_sequence_length_mask(sample_length_tensor, max_len=is_copy_log_probs.shape[1]).float()

    is_copy_log_probs = is_copy_log_probs * length_mask_float
    sample_output_ids_log_probs = sample_output_ids_log_probs * length_mask_float

    sample_total_log_probs = torch.sum(is_copy_log_probs + sample_output_ids_log_probs, dim=-1) / sample_length_tensor.float()

    final_probs = p1_log_probs + p2_log_probs + sample_total_log_probs

    return final_probs


class GenerateAgent(object):
    def __init__(self, g_model, optimizer, parse_input_batch_data_fn, sample_generate_action_fn, do_sample=True,
                 do_beam_search=False, reward_discount_gamma=0.99, do_normalize=False):
        self.g_model = g_model
        self.optimizer = optimizer
        self.parse_input_batch_data_fn = parse_input_batch_data_fn
        self.do_sample = do_sample
        self.do_beam_search = do_beam_search
        self.sample_generate_action_fn = sample_generate_action_fn
        self.reward_discount_gamma = reward_discount_gamma
        self.do_normalize = do_normalize
        self.g_model.rewards, self.g_model.saved_actions, self.g_model.dones = [], [], []

    def select_action(self, states_tensor):
        # states_tensor = self.parse_input_batch_data_fn(states, do_sample=self.do_sample)
        model_output = self.g_model.forward(*states_tensor, do_sample=self.do_sample, do_beam_search=self.do_beam_search)
        actions, action_probs = self.sample_generate_action_fn(states_tensor, model_output, do_sample=self.do_sample, direct_output=self.do_beam_search)
        self.g_model.saved_actions.append(action_probs)
        return actions

    def add_step_reward(self, reward_list):
        self.g_model.rewards.append(reward_list)

    def get_rewards_sum(self):
        res = np.mean(np.sum(self.g_model.rewards, axis=-1))
        return res

    def discount_rewards(self, model_rewards):
        batch_discounted_rewards = [self.one_discount_rewards(rewards) for rewards in zip(*model_rewards)]
        return batch_discounted_rewards

    def one_discount_rewards(self, one_rewards):
        running_add = 0
        discounted_rewards = []
        for r in one_rewards[::-1]:
            running_add = r + self.reward_discount_gamma * running_add
            discounted_rewards.insert(0, running_add)
        eps = np.finfo(np.float32).eps
        if self.do_normalize:
            discounted_rewards = (discounted_rewards - np.mean(discounted_rewards)) / (np.std(discounted_rewards) + eps)
        return discounted_rewards

    def finish_episode(self):
        rewards = self.discount_rewards(self.g_model.rewards)
        rewards = torch.Tensor(rewards).to(self.g_model.saved_actions[0][0].device)
        self.optimizer.zero_grad()
        loss = self.compute_loss(rewards)
        loss.backward()
        self.optimizer.step()
        self.g_model.rewards, self.g_model.saved_actions, self.g_model.dones = [], [], []
        return loss.item()

    def compute_loss(self, rewards):
        # return torch.sum(self.g_model.saved_actions[0][0]) * torch.sum(rewards)
        policy_losses = []
        self.g_model.saved_actions = [list(zip(*s)) for s in self.g_model.saved_actions]
        for one_batch_probs, one_batch_reward in zip(zip(*self.g_model.saved_actions), rewards):
            one_loss = self.one_compute_loss(one_batch_probs, one_batch_reward)
            policy_losses += [one_loss]
        if len(policy_losses) == 1:
            return policy_losses[0]
        return torch.stack(policy_losses).mean()

    def one_compute_loss(self, action_probs, rewards):
        policy_losses = []
        for (probs, ), reward in zip(action_probs, rewards):
            policy_losses.append(- probs * reward)
        if len(policy_losses) == 1:
            return policy_losses[0]
        return torch.stack(policy_losses).sum()

    def train(self):
        self.g_model.train()

    def eval(self):
        self.g_model.eval()


def create_generate_env(s_model, dataset, env_dict):
    env = GenerateEnvironment(s_model, dataset, **env_dict)
    return env


def create_generate_agent(g_model, optimizer, agent_dict):
    agent = GenerateAgent(g_model, optimizer, **agent_dict)
    return agent


class EnvironmentStorage(object):
    def __init__(self):
        pass








