import os
import random

import torch.nn as nn
import torch
import math
import torch.nn.functional as F
import pandas as pd
from torch.utils.data import Dataset
import more_itertools

from common.graph_embedding import GGNNLayer, MultiIterationGraph
from common import torch_util, util
from common.problem_util import to_cuda
from common.torch_util import create_sequence_length_mask, Update, MaskOutput, expand_tensor_sequence_list_to_same, \
    SequenceMaskOutput
from common.util import PaddedList
from seq2seq.models import EncoderRNN, DecoderRNN

"""
The batch_data dict should has the following keys:
'p1_target': , 
'p2_target', 'is_copy_target', 'copy_target', 'sample_target', 'adj', 'input_seq', 'input_length', 
'copy_length', 'target', 
'compatible_tokens',
'compatible_tokens_length'
"""


class SliceEncoder(nn.Module):
    def __init__(self, rnn_type, hidden_size, n_layer, dropout_p, inner=False):
        """
        This module extract a slice from a sequence and encode the slice into a state vector
        """
        super().__init__()
        if rnn_type == 'lstm':
            self.rnn = nn.LSTM(input_size=2*hidden_size, hidden_size=hidden_size, num_layers=n_layer,
                               batch_first=True, bidirectional=True, dropout=dropout_p)
        elif rnn_type == 'gru':
            self.rnn = nn.GRU(input_size=2*hidden_size, hidden_size=hidden_size, num_layers=n_layer,
                              batch_first=True, bidirectional=True, dropout=dropout_p)
        self.inner = inner
        if not inner:
            self.transform = nn.Linear(2*hidden_size, hidden_size)

    def forward(self, p1, p2, seq):
        """
        :param p1: The slice begin position, shape [batch, ]
        :param p2: The slice end position, shape [batch, ]
        :param seq: The sequence shape [batch, seq, dim]
        :return: The encoded slice vector, shape [batch, ]
        """
        seq = torch.unbind(seq, dim=0)
        if self.inner:
            seq = [s[a:b+1] for a, b, s in zip(p1, p2, seq)]
            return self._encode(seq)
        else:
            seq_before = [s[:a+1] for a, s in zip(p1, seq)]
            before_encoder = self._encode(seq_before)
            seq_after = [s[a:] for a, s in zip(p2, seq)]
            after_encoder = self._encode(seq_after)
            encoder = torch.cat((before_encoder, after_encoder), dim=-1)
            return self.transform(encoder)

    def _encode(self, seq):
        packed_seq, idx_unsort = torch_util.pack_sequence(seq)
        _, encoded_state = self.rnn(packed_seq)
        return torch.index_select(encoded_state, 1, idx_unsort.to(seq[0].device))


class PointerNetwork(nn.Module):
    def __init__(self, hidden_size, use_query_vector=False):
        super().__init__()
        self.transform = nn.Linear(hidden_size, hidden_size)
        if use_query_vector:
            self.query_transform = nn.Linear(hidden_size, hidden_size)
        self.query_vector = nn.Parameter(torch.randn(1, hidden_size, 1))

    def forward(self, x, query=None, mask=None):
        """
        :param x: shape [batch, seq, dim]
        :param query: shape [dim]
        :param mask: shape [batch, seq]
        :return: shape [batch, seq]
        """
        batch_size = x.shape[0]
        x = self.transform(x)
        if query is not None:
            x = x + self.query_transform(query)
        x = F.tanh(x)
        x = torch.bmm(x, self.query_vector.expand(batch_size, -1, -1))
        x = x.squeeze(-1)
        if mask is None:
            x.data.masked_fill_(~mask, -float('inf'))
        return x


class RNNGraphWrapper(nn.Module):
    def __init__(self, hidden_size, parameter):
        super().__init__()
        self.encoder = EncoderRNN(hidden_size=hidden_size, **parameter)
        self.bi = 2 if parameter['bidirectional'] else 1
        self.transform_size = nn.Linear(self.bi * hidden_size, hidden_size)

    def forward(self, x, adj):
        o, _ = self.encoder(x)
        o = self.transform_size(o)
        return o


class GraphEncoder(nn.Module):
    def __init__(self,
                 hidden_size=300,
                 graph_embedding='ggnn',
                 graph_parameter={},
                 pointer_type='itr',
                 embedding=None, embedding_size=400,
                 ):
        """
        :param hidden_size: The hidden state size in the model
        :param graph_embedding: The graph propagate method, option:["ggnn", "graph_attention", "rnn"]
        :param pointer_type: The method to point out the begin and the end, option:["itr", "query"]
        """
        super().__init__()
        self.pointer_type = pointer_type
        self.embedding = embedding
        self.size_transform = nn.Linear(embedding_size, hidden_size)
        if self.pointer_type == 'itr':
            self.pointer_transform = nn.Linear(2 * hidden_size, 1)
        elif self.pointer_type == 'query':
            self.query_tensor = nn.Parameter(torch.randn(hidden_size))
            self.up_data_cell = nn.GRUCell(hidden_size, hidden_size, bias=True)
            self.p1_pointer_network = PointerNetwork(hidden_size, use_query_vector=True)
            self.p2_pointer_network = PointerNetwork(hidden_size, use_query_vector=True)
        self.graph_embedding = graph_embedding
        if graph_embedding == 'ggnn':
            self.graph = MultiIterationGraph(GGNNLayer(hidden_state_size=hidden_size), **graph_parameter)
        elif graph_embedding == 'rnn':
            self.graph = RNNGraphWrapper(hidden_size=hidden_size, parameter=graph_parameter)

    def forward(self,
                adjacent_matrix,
                input_seq,
                copy_length,
                ):
        input_seq = self.embedding(input_seq)
        input_seq = self.size_transform(input_seq)
        input_seq = self.graph(input_seq, adjacent_matrix)
        batch_size = input_seq.shape[0]
        pointer_mask = torch_util.create_sequence_length_mask(copy_length, max_len=input_seq.shape[1])
        if self.pointer_type == 'itr':
            input_seq0 = input_seq
            input_seq1 = self.graph(input_seq)
            input_seq2 = self.graph(input_seq1)
            p1 = self.pointer_transform(torch.cat((input_seq0, input_seq1), dim=-1), ).squeeze(-1)
            p1.data.masked_fill_(~pointer_mask, -float("inf"))
            p2 = self.pointer_transform(torch.cat((input_seq0, input_seq2), dim=-1), ).squeeze(-1)
            p2.data.masked_fill_(~pointer_mask, -float("inf"))
            input_seq = self.graph(input_seq2)
        elif self.pointer_type == 'query':
            p1 = self.p1_pointer_network(input_seq, query=self.query_tensor, mask=pointer_mask)
            p1_state = torch.sum(F.softmax(p1, dim=-1).unsqueeze(-1) * input_seq, dim=1)
            p2_query = self.up_data_cell(p1_state, self.query_tensor.unsqueeze(0).expand(batch_size, -1))
            p2 = self.p2_pointer_network(input_seq, query=torch.unsqueeze(p2_query, dim=1), mask=pointer_mask)
        else:
            raise ValueError("No point type is:{}".format(self.pointer_type))

        return p1, p2, input_seq


class Output(nn.Module):
    def __init__(self, hidden_size, vocabulary_size):
        super().__init__()
        self.is_copy_output = nn.Linear(hidden_size, 1)
        self.copy_embedding = nn.Embedding(2, hidden_size)
        self.update = Update(hidden_size)
        self.sample_output = SequenceMaskOutput(hidden_size, vocabulary_size)

    def forward(self, decoder_output, encoder_output, copy_mask, sample_mask, sample_length, is_sample=False,
                copy_target=None):
        is_copy = self.is_copy_output(decoder_output).squeeze(-1)
        if is_sample:
            copy_target = (is_copy > 0.5).long()
        else:
            copy_target = (copy_target == 1).long()

        copy_state = self.copy_embedding(copy_target)
        decoder_output = self.update(decoder_output, copy_state)
        copy_output = torch.bmm(decoder_output, encoder_output.permute(0, 2, 1))
        copy_output.data.masked_fill_(~torch.unsqueeze(copy_mask, dim=1), -float('inf'))
        sample_length_shape = sample_length.shape
        sample_length_mask = create_sequence_length_mask(sample_length.view(-1, )).view(*list(sample_length_shape), -1)
        sample_output = self.sample_output(decoder_output, sample_mask, sample_length_mask)
        return is_copy, copy_output, sample_output


class EncoderSampleModel(nn.Module):
    def __init__(self,
                 start_label,
                 end_label,
                 vocabulary_size,
                 embedding_size=300,
                 hidden_size=300,
                 max_sample_length=10,
                 graph_parameter={},
                 graph_embedding='ggnn',
                 pointer_type='itr',
                 rnn_type='gru',
                 rnn_layer_number=3,
                 max_length=500,
                 dropout_p=0.1,
                 ):
        """
        :param vocabulary_size: The size of token vocabulary
        :param embedding_size: The embedding size
        :param hidden_size: The hidden state size in the model
        :param max_sample_length: The max length to sample
        :param graph_embedding: The graph propagate method, option:["ggnn", "graph_attention", "rnn"]
        :param pointer_type: The method to point out the begin and the end, option:["itr", "query"]
        :param rnn_type: The rnn type used in the model, option:["lstm", "gru"]
        :param rnn_layer_number: The number of layer in this model
        :param dropout_p: The dropout p in this model
        """
        super().__init__()
        self.max_sample_length = max_sample_length
        self.embedding = nn.Embedding(vocabulary_size, embedding_size)
        self.graph_encoder = GraphEncoder(hidden_size=hidden_size, graph_embedding=graph_embedding,
                                          pointer_type=pointer_type, graph_parameter=graph_parameter,
                                          embedding=self.embedding, embedding_size=embedding_size)
        self.slice_encoder = SliceEncoder(rnn_type=rnn_type, hidden_size=hidden_size // 2, n_layer=rnn_layer_number,
                                          dropout_p=dropout_p)
        # self.slice_encoder = SliceEncoder(rnn_type=rnn_type, hidden_size=hidden_size, n_layer=rnn_layer_number,
        #                                   dropout_p=dropout_p)
        self.decoder = DecoderRNN(vocab_size=vocabulary_size, max_len=max_length, hidden_size=hidden_size,
                                  sos_id=start_label, eos_id=end_label, n_layers=rnn_layer_number, rnn_cell=rnn_type,
                                  bidirectional=False, input_dropout_p=dropout_p, dropout_p=dropout_p,
                                  use_attention=True)
        self.output = Output(hidden_size, vocabulary_size)
        self.layer_number = rnn_layer_number
        self.hidden_size = hidden_size

    def _train_forward(self,
                       adjacent_matrix,
                       input_seq,
                       input_length,
                       copy_length,
                       p1_target,
                       p2_target,
                       target,
                       compatible_tokens,
                       compatible_tokens_length,
                       is_copy_target,
                       ):
        batch_size = input_seq.shape[0]
        p1_o, p2_o, input_seq = self.graph_encoder(adjacent_matrix, input_seq, copy_length)
        slice_state = self.slice_encoder(p1_target, p2_target, input_seq)\
            .permute(1, 0, 2)\
            .contiguous()\
            .view(batch_size, self.layer_number, -1)\
            .permute(1, 0, 2)\
            .contiguous()
        encoder_mask = create_sequence_length_mask(input_length, )
        decoder_output, _, _ = self.decoder(inputs=self.embedding(target), encoder_hidden=slice_state,
                                            encoder_outputs=input_seq, encoder_mask=~encoder_mask,
                                            teacher_forcing_ratio=1)
        decoder_output = torch.stack(decoder_output, dim=1)
        copy_mask = create_sequence_length_mask(copy_length)
        is_copy, copy_output, sample_output = self.output(decoder_output, input_seq, copy_mask, compatible_tokens,
                                                          compatible_tokens_length, is_sample=False,
                                                          copy_target=is_copy_target)
        return p1_o, p2_o, is_copy, copy_output, sample_output

    def _sample_forward(self,
                        adjacent_matrix,
                        input_seq,
                        input_length,
                        copy_length,
                        ):
        pass

    def forward(self,
                adjacent_matrix,
                input_seq,
                input_length,
                copy_length,
                do_sample,
                p1_target=None,
                p2_target=None,
                target=None,
                is_copy_target=None,
                compatible_tokens=None,
                compatible_tokens_length=None,
                ):
        if do_sample:
            return self._sample_forward(adjacent_matrix,
                                        input_seq,
                                        input_length,
                                        copy_length)
        else:
            return self._train_forward(adjacent_matrix,
                                       input_seq,
                                       input_length,
                                       copy_length,
                                       p1_target,
                                       p2_target,
                                       target,
                                       compatible_tokens,
                                       compatible_tokens_length, is_copy_target)


def create_loss_fn(ignore_id):
    bce_loss = nn.BCEWithLogitsLoss(reduce=False)
    cross_loss = nn.CrossEntropyLoss(ignore_index=ignore_id)

    def loss_fn(p1_o, p2_o, is_copy, copy_output, sample_output,
                p1_target, p2_target, is_copy_target, copy_target, sample_target, sample_small_target):
        try:
            is_copy_loss = torch.mean(bce_loss(is_copy, is_copy_target) * torch.ne(is_copy_target, ignore_id).float())
        except Exception as e:
            print('')
            raise Exception(e)
        p1_loss = cross_loss(p1_o, p1_target)
        p2_loss = cross_loss(p2_o, p2_target)
        copy_loss = cross_loss(copy_output.permute(0, 2, 1), copy_target)
        sample_loss = cross_loss(sample_output.permute(0, 2, 1), sample_small_target)
        return is_copy_loss + sample_loss + p1_loss + p2_loss + copy_loss
    return loss_fn


def create_parse_target_batch_data(ignore_token):
    def parse_target_batch_data(batch_data):
        p1 = to_cuda(torch.LongTensor(batch_data['p1_target']))
        p2 = to_cuda(torch.LongTensor(batch_data['p2_target']))
        is_copy = to_cuda(torch.FloatTensor(PaddedList(batch_data['is_copy_target'], fill_value=ignore_token)))
        copy_target = to_cuda(torch.LongTensor(PaddedList(batch_data['copy_target'], fill_value=ignore_token)))
        sample_target = to_cuda(torch.LongTensor(PaddedList(batch_data['sample_target'], fill_value=ignore_token)))
        sample_small_target = to_cuda(torch.LongTensor(PaddedList(batch_data['sample_small_target'])))
        return p1, p2, is_copy, copy_target, sample_target, sample_small_target

    return parse_target_batch_data


def parse_input_batch_data_fn(batch_data, do_sample):
    def to_long(x):
        return to_cuda(torch.LongTensor(x))

    adjacent_matrix = to_long(batch_data['adj'])
    input_seq = to_long(PaddedList(batch_data['input_seq']))
    input_length = to_long(batch_data['input_length'])
    copy_length = to_long(batch_data['copy_length'])
    if not do_sample:
        p1_target = to_long(batch_data['p1_target'])
        p2_target = to_long(batch_data['p2_target'])
        target = to_long(PaddedList(batch_data['target']))
        is_copy_target = to_long(PaddedList(batch_data['is_copy_target']))
        batch_size = len(batch_data['is_copy_target'])
        seq_len = is_copy_target.shape[1]
        max_mask_len = max(max(batch_data['compatible_tokens_length']))
        compatible_tokens = to_long(PaddedList(batch_data['compatible_tokens'], shape=[batch_size, seq_len, max_mask_len]))
        compatible_tokens_length = to_long(PaddedList(batch_data['compatible_tokens_length']))
        return adjacent_matrix, input_seq, input_length, copy_length, do_sample, p1_target, p2_target, target, \
               is_copy_target, \
               compatible_tokens, \
               compatible_tokens_length
    else:
        return adjacent_matrix, input_seq, input_length, copy_length, do_sample


def create_output_ids_fn(end_id):
    def create_output_ids(model_output, model_input, do_sample=False):
        p1_o, p2_o, is_copy, copy_output, sample_output = model_output
        p1 = torch.squeeze(torch.topk(F.softmax(p1_o, dim=-1), dim=-1, k=1)[1], dim=-1)
        p2 = torch.squeeze(torch.topk(F.softmax(p2_o, dim=-1), dim=-1, k=1)[1], dim=-1)
        is_copy = torch.squeeze(is_copy, dim=-1) > 0.5
        copy_output_id = torch.squeeze(torch.topk(F.softmax(copy_output, dim=-1), dim=-1, k=1)[1], dim=-1)
        sample_output_id = torch.topk(F.softmax(sample_output, dim=-1), dim=-1, k=1)[1]
        compatible_tokens= model_input[9]
        sample_output = torch.squeeze(torch.gather(compatible_tokens, dim=-1, index=sample_output_id), dim=-1)

        adjacent_matrix, input_seq, input_length, copy_length, do_sample, p1_target, p2_target, target, is_copy_target, \
        compatible_tokens, compatible_tokens_length = model_input
        copy_ids = torch.gather(input_seq, index=copy_output_id, dim=-1)
        sample_output_ids = torch.where(is_copy, copy_ids, sample_output)

        sample_output_ids_list = sample_output_ids.tolist()
        effect_sample_output_list = []
        for sample in sample_output_ids_list:
            try:
                end_pos = sample.index(end_id)
                sample = sample[:end_pos]
            except ValueError as e:
                pass
            effect_sample_output_list += [sample]

        input_seq_list = torch.unbind(input_seq, dim=0)
        final_output = []
        for i, one_input in enumerate(input_seq_list):
            effect_sample = effect_sample_output_list[i]
            one_output = torch.cat([one_input[1:p1[i]+1], torch.LongTensor(effect_sample).to(one_input.device), one_input[p2[i]:-1]], dim=-1)
            final_output += [one_output]
        # pad output tensor in python list final output
        final_output = expand_tensor_sequence_list_to_same(final_output, dim=0, fill_value=0)
        outputs = torch.stack(final_output, dim=0)
        return outputs, sample_output_ids
    return create_output_ids