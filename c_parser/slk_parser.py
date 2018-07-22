import abc

import toolz

from c_parser.code_util import LeafParseNode, ProductionNode, Production, parse_tree_to_top_down_process, \
    ProductionVocabulary
from common import util
from c_parser.buffered_clex import BufferedCLex


class C99SLKConstants(object):
    def __init__(self):
        self.END_OF_SLK_INPUT_ = 88
        self.START_SYMBOL = 89
        self.START_STATE = 0
        self.START_CONFLICT = 320
        self.END_CONFLICT = 348
        self.START_ACTION = 227
        self.END_ACTION = 231
        self.TOTAL_CONFLICTS = 28
        self.NOT_A_SYMBOL = 0
        self.NONTERMINAL_SYMBOL = 1
        self.TERMINAL_SYMBOL = 2
        self.ACTION_SYMBOL = 3

        self._production = [0
            , 4, 89, 211, 90, 227, 3, 90, 211, 90, 1, 90, 2, 91, 1, 2, 91, 2
            , 2, 91, 3, 4, 91, 4, 124, 5, 3, 92, 91, 93, 5, 93, 6, 124, 7, 93
            , 4, 93, 4, 5, 93, 5, 93, 4, 94, 5, 93, 4, 93, 8, 1, 93
            , 4, 93, 9, 1, 93, 3, 93, 10, 93, 3, 93, 11, 93, 1, 93, 3, 94, 121, 95
            , 4, 95, 12, 121, 95, 1, 95, 2, 96, 92, 3, 96, 10, 96, 3, 96, 11, 96
            , 3, 96, 97, 98, 3, 96, 13, 96, 5, 96, 13, 4, 183, 5, 2, 97, 14
            , 2, 97, 15, 2, 97, 16, 2, 97, 17, 2, 97, 18, 2, 97, 19, 2, 98, 96
            , 5, 98, 4, 183, 5, 98, 3, 99, 98, 100, 4, 100, 15, 98, 100, 4, 100, 20, 98, 100
            , 4, 100, 21, 98, 100, 1, 100, 3, 101, 99, 102, 4, 102, 16, 99, 102
            , 4, 102, 17, 99, 102, 1, 102, 3, 103, 101, 104, 4, 104, 22, 101, 104
            , 4, 104, 23, 101, 104, 1, 104, 3, 105, 103, 106, 4, 106, 24, 103, 106
            , 4, 106, 25, 103, 106, 4, 106, 26, 103, 106, 4, 106, 27, 103, 106, 1, 106
            , 3, 107, 105, 108, 4, 108, 28, 105, 108, 4, 108, 29, 105, 108, 1, 108
            , 3, 109, 107, 110, 4, 110, 14, 107, 110, 1, 110, 3, 111, 109, 112, 4, 112, 30, 109, 112
            , 1, 112, 3, 113, 111, 114, 4, 114, 31, 111, 114, 1, 114, 3, 115, 113, 116
            , 4, 116, 32, 113, 116, 1, 116, 3, 117, 115, 118, 4, 118, 33, 115, 118
            , 1, 118, 3, 119, 117, 120, 1, 120, 5, 120, 34, 124, 35, 119, 3, 121, 96, 122
            , 16, 121, 4, 183, 5, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120
            , 12, 122, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 3, 122, 123, 121
            , 2, 123, 36, 2, 123, 37, 2, 123, 38, 2, 123, 39, 2, 123, 40, 2, 123, 41
            , 2, 123, 42, 2, 123, 43, 2, 123, 44, 2, 123, 45, 2, 123, 46, 3, 124, 121, 125
            , 4, 125, 12, 121, 125, 1, 125, 2, 126, 119, 4, 127, 128, 217, 47, 5, 127, 48, 128, 218, 47
            , 3, 128, 161, 129, 3, 128, 160, 130, 3, 128, 139, 131, 3, 128, 138, 132
            , 1, 129, 2, 129, 128, 1, 130, 2, 130, 128, 1, 131, 2, 131, 128, 1, 132
            , 2, 132, 128, 3, 133, 136, 134, 4, 134, 12, 136, 134, 1, 134, 4, 135, 136, 228, 219
            , 3, 136, 162, 137, 1, 137, 3, 137, 36, 189, 2, 138, 49, 2, 138, 50
            , 2, 138, 51, 2, 138, 52, 2, 139, 53, 2, 139, 54, 2, 139, 55, 2, 139, 56
            , 2, 139, 57, 2, 139, 58, 2, 139, 59, 2, 139, 60, 2, 139, 61, 2, 139, 62
            , 2, 139, 63, 2, 139, 64, 2, 139, 140, 2, 139, 152, 2, 139, 65, 6, 140, 141, 1, 66, 142, 67
            , 5, 140, 141, 66, 142, 67, 3, 140, 141, 1, 2, 141, 68, 2, 141, 69
            , 3, 142, 144, 143, 3, 143, 144, 143, 1, 143, 4, 144, 145, 148, 47, 3, 145, 160, 146
            , 3, 145, 139, 147, 2, 146, 145, 1, 146, 2, 147, 145, 1, 147, 3, 148, 150, 149
            , 4, 149, 12, 150, 149, 1, 149, 3, 150, 162, 151, 3, 150, 35, 126, 1, 151
            , 3, 151, 35, 126, 3, 152, 70, 153, 3, 153, 1, 154, 4, 153, 66, 157, 156
            , 4, 154, 66, 157, 155, 1, 154, 2, 155, 67, 3, 155, 12, 67, 2, 156, 67
            , 3, 156, 12, 67, 3, 157, 159, 158, 4, 158, 12, 159, 158, 1, 158, 2, 159, 1
            , 4, 159, 1, 36, 126, 2, 160, 71, 2, 160, 72, 2, 160, 73, 2, 161, 74
            , 3, 162, 168, 163, 2, 162, 163, 3, 163, 1, 164, 5, 163, 4, 162, 5, 164
            , 3, 164, 4, 165, 3, 164, 6, 166, 7, 164, 229, 4, 173, 230, 5, 164
            , 1, 164, 4, 165, 181, 5, 164, 3, 165, 5, 164, 3, 166, 171, 167, 4, 166, 121, 7, 164
            , 6, 166, 50, 171, 121, 7, 164, 4, 166, 15, 7, 164, 3, 166, 7, 164
            , 4, 167, 121, 7, 164, 3, 167, 7, 164, 5, 167, 50, 121, 7, 164, 4, 167, 15, 7, 164
            , 3, 168, 15, 169, 3, 169, 171, 170, 2, 169, 170, 1, 170, 2, 170, 168
            , 3, 171, 160, 172, 3, 172, 160, 172, 1, 172, 3, 173, 175, 174, 1, 174
            , 3, 174, 12, 75, 3, 175, 177, 176, 4, 176, 12, 177, 176, 1, 176, 3, 177, 128, 220
            , 2, 178, 179, 3, 178, 168, 221, 3, 179, 1, 180, 5, 179, 4, 178, 5, 180
            , 5, 179, 6, 222, 7, 180, 5, 179, 4, 223, 5, 180, 5, 180, 6, 224, 7, 180
            , 5, 180, 4, 173, 5, 180, 5, 180, 4, 225, 5, 180, 1, 180, 3, 181, 1, 182
            , 4, 182, 12, 1, 182, 1, 182, 3, 183, 145, 184, 1, 184, 2, 184, 185
            , 3, 185, 168, 186, 2, 185, 187, 1, 186, 2, 186, 187, 5, 187, 4, 185, 5, 188
            , 4, 187, 6, 7, 188, 5, 187, 6, 121, 7, 188, 5, 187, 6, 15, 7, 188
            , 4, 187, 4, 5, 188, 5, 187, 4, 173, 5, 188, 4, 188, 6, 7, 188
            , 5, 188, 6, 121, 7, 188, 5, 188, 6, 15, 7, 188, 4, 188, 4, 5, 188
            , 5, 188, 4, 173, 5, 188, 4, 189, 66, 191, 190, 2, 189, 121, 2, 190, 67
            , 3, 190, 12, 67, 3, 191, 189, 192, 4, 191, 193, 189, 192, 4, 192, 12, 189, 192
            , 5, 192, 12, 193, 189, 192, 1, 192, 3, 193, 194, 36, 3, 194, 196, 195
            , 3, 195, 196, 195, 1, 195, 4, 196, 6, 126, 7, 3, 196, 8, 1, 2, 197, 198
            , 2, 197, 199, 2, 197, 203, 2, 197, 204, 2, 197, 206, 2, 197, 210, 4, 198, 1, 35, 197
            , 5, 198, 76, 126, 35, 197, 4, 198, 77, 35, 197, 5, 199, 229, 66, 230, 67
            , 6, 199, 229, 66, 200, 230, 67, 3, 200, 202, 201, 3, 201, 202, 201, 1, 201
            , 2, 202, 127, 2, 202, 197, 2, 203, 47, 3, 203, 124, 47, 7, 204, 78, 4, 124, 5, 197, 205
            , 6, 204, 79, 4, 124, 5, 197, 3, 205, 80, 197, 1, 205, 4, 206, 81, 4, 207
            , 6, 206, 82, 4, 124, 5, 197, 8, 206, 83, 197, 82, 4, 124, 5, 47
            , 4, 207, 127, 203, 208, 4, 207, 203, 203, 209, 3, 208, 5, 197, 4, 208, 124, 5, 197
            , 3, 209, 5, 197, 4, 209, 124, 5, 197, 4, 210, 84, 1, 47, 3, 210, 85, 47
            , 3, 210, 86, 47, 3, 210, 87, 47, 4, 210, 87, 124, 47, 3, 211, 128, 212
            , 5, 211, 48, 128, 226, 47, 3, 212, 162, 213, 2, 212, 47, 2, 213, 214
            , 4, 213, 137, 134, 47, 3, 214, 215, 199, 2, 214, 199, 3, 215, 127, 216
            , 3, 216, 127, 216, 2, 217, 133, 1, 217, 2, 218, 135, 1, 218, 5, 219, 12, 136, 228, 219
            , 1, 219, 2, 220, 178, 1, 220, 2, 221, 179, 1, 221, 2, 222, 126, 1, 222
            , 2, 223, 173, 1, 223, 2, 224, 126, 1, 224, 2, 225, 181, 1, 225, 2, 226, 135
            , 1, 226
            , 0]
        self._production_row = [0
            , 1, 6, 10, 12, 15, 18, 21, 26, 30, 36, 41, 47, 52, 57, 61, 65
            , 67, 71, 76, 78, 81, 85, 89, 93, 97, 103, 106, 109, 112, 115, 118, 121
            , 124, 130, 134, 139, 144, 149, 151, 155, 160, 165, 167, 171, 176, 181, 183, 187
            , 192, 197, 202, 207, 209, 213, 218, 223, 225, 229, 234, 236, 240, 245, 247, 251
            , 256, 258, 262, 267, 269, 273, 278, 280, 284, 286, 292, 296, 313, 326, 330, 333
            , 336, 339, 342, 345, 348, 351, 354, 357, 360, 363, 367, 372, 374, 377, 382, 388
            , 392, 396, 400, 404, 406, 409, 411, 414, 416, 419, 421, 424, 428, 433, 435, 440
            , 444, 446, 450, 453, 456, 459, 462, 465, 468, 471, 474, 477, 480, 483, 486, 489
            , 492, 495, 498, 501, 504, 507, 514, 520, 524, 527, 530, 534, 538, 540, 545, 549
            , 553, 556, 558, 561, 563, 567, 572, 574, 578, 582, 584, 588, 592, 596, 601, 606
            , 608, 611, 615, 618, 622, 626, 631, 633, 636, 641, 644, 647, 650, 653, 657, 660
            , 664, 670, 674, 678, 686, 688, 693, 697, 701, 706, 713, 718, 722, 727, 731, 737
            , 742, 746, 750, 753, 755, 758, 762, 766, 768, 772, 774, 778, 782, 787, 789, 793
            , 796, 800, 804, 810, 816, 822, 828, 834, 840, 842, 846, 851, 853, 857, 859, 862
            , 866, 869, 871, 874, 880, 885, 891, 897, 902, 908, 913, 919, 925, 930, 936, 941
            , 944, 947, 951, 955, 960, 965, 971, 973, 977, 981, 985, 987, 992, 996, 999, 1002
            , 1005, 1008, 1011, 1014, 1019, 1025, 1030, 1036, 1043, 1047, 1051, 1053, 1056, 1059, 1062, 1066
            , 1074, 1081, 1085, 1087, 1092, 1099, 1108, 1113, 1118, 1122, 1127, 1131, 1136, 1141, 1145, 1149
            , 1153, 1158, 1162, 1168, 1172, 1175, 1178, 1183, 1187, 1190, 1194, 1198, 1201, 1203, 1206, 1208
            , 1214, 1216, 1219, 1221, 1224, 1226, 1229, 1231, 1234, 1236, 1239, 1241, 1244, 1246, 1249
            , 0]
        self._parse = [0, 0, 275, 275, 275, 275, 4, 5, 6, 7, 176, 275, 275, 177, 275, 275, 275, 275, 275
            , 275, 275, 26, 27, 28, 29, 30, 31, 19, 243, 243, 243, 243, 182, 244, 18, 244, 183, 243, 243
            , 165, 243, 243, 243, 243, 243, 243, 243, 327, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275
            , 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 275, 156, 275, 275
            , 275, 275, 274, 275, 275, 275, 275, 275, 275, 275, 266, 266, 266, 266, 243, 8, 8, 8, 8, 266
            , 266, 173, 266, 266, 266, 266, 266, 266, 266, 296, 296, 296, 296, 296, 296, 296, 296, 296, 296, 296
            , 296, 296, 296, 296, 296, 296, 296, 297, 193, 296, 296, 296, 296, 296, 296, 296, 266, 266, 266, 266
            , 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 266, 267, 266, 266, 266
            , 266, 266, 266, 266, 218, 266, 266, 266, 266, 340, 266, 266, 266, 266, 266, 266, 266, 265, 265, 265
            , 265, 115, 116, 117, 118, 0, 265, 265, 162, 265, 265, 265, 265, 265, 265, 265, 1, 1, 1, 1
            , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 325, 324, 1, 1, 1, 1
            , 1, 1, 1, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265, 265
            , 265, 265, 265, 161, 265, 265, 265, 265, 265, 265, 265, 0, 265, 265, 265, 265, 0, 265, 265, 265
            , 265, 265, 265, 265, 269, 269, 269, 269, 285, 286, 287, 342, 0, 269, 269, 0, 269, 269, 269, 269
            , 269, 269, 269, 95, 94, 94, 94, 94, 94, 94, 94, 94, 94, 94, 94, 94, 94, 94, 94, 94
            , 94, 137, 138, 94, 94, 94, 94, 94, 94, 94, 269, 268, 268, 268, 268, 268, 268, 268, 268, 268
            , 268, 268, 268, 268, 268, 268, 268, 268, 268, 269, 109, 268, 268, 268, 268, 268, 268, 268, 157, 269
            , 269, 269, 269, 0, 269, 269, 269, 269, 269, 269, 269, 320, 16, 9, 16, 12, 13, 14, 15, 16
            , 0, 16, 16, 16, 16, 110, 0, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16
            , 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 280, 280, 280, 280, 170
            , 171, 172, 0, 158, 280, 280, 164, 280, 280, 280, 280, 280, 280, 280, 16, 99, 99, 99, 99, 98
            , 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 272, 273, 98, 98, 98, 97, 97, 97
            , 96, 280, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279, 279
            , 0, 163, 279, 279, 279, 279, 279, 279, 279, 77, 326, 77, 223, 222, 223, 202, 77, 242, 77, 77
            , 77, 77, 203, 223, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77
            , 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 77, 160, 0, 316, 160, 160, 160, 317, 333
            , 217, 214, 335, 160, 334, 167, 160, 217, 198, 198, 198, 77, 241, 140, 140, 140, 140, 140, 140, 140
            , 140, 140, 140, 140, 140, 140, 160, 141, 140, 140, 140, 140, 140, 140, 210, 0, 0, 332, 160, 212
            , 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 159, 0, 160
            , 160, 160, 160, 160, 160, 160, 328, 181, 179, 282, 282, 282, 282, 281, 181, 227, 226, 227, 282, 282
            , 0, 282, 282, 282, 282, 282, 282, 282, 0, 108, 111, 100, 108, 111, 100, 100, 100, 181, 181, 250
            , 0, 250, 100, 108, 111, 100, 276, 277, 278, 181, 181, 181, 181, 181, 181, 181, 181, 181, 181, 181
            , 181, 181, 181, 181, 181, 181, 181, 181, 181, 251, 181, 181, 181, 181, 181, 181, 181, 100, 0, 101
            , 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 101, 0, 0, 101, 101
            , 101, 101, 101, 101, 101, 102, 113, 150, 102, 102, 102, 284, 284, 284, 284, 283, 102, 154, 0, 102
            , 284, 284, 0, 284, 284, 284, 284, 284, 284, 284, 114, 112, 175, 104, 112, 175, 104, 104, 104, 260
            , 155, 113, 151, 206, 104, 112, 174, 104, 0, 0, 331, 102, 154, 103, 103, 103, 103, 103, 103, 103
            , 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 0, 0, 103, 103, 103, 103, 103, 103, 103, 104
            , 0, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 0, 338
            , 105, 105, 105, 105, 105, 105, 105, 106, 0, 220, 106, 106, 106, 0, 261, 262, 219, 337, 106, 336
            , 0, 106, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 201, 0
            , 0, 201, 201, 201, 201, 201, 201, 201, 295, 248, 249, 248, 249, 106, 247, 107, 107, 107, 107, 107
            , 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 295, 0, 107, 107, 107, 107, 107, 107
            , 107, 0, 0, 295, 294, 294, 294, 294, 294, 294, 294, 294, 294, 294, 294, 294, 294, 294, 294, 294
            , 294, 294, 294, 304, 294, 294, 294, 294, 294, 294, 294, 2, 2, 2, 2, 2, 2, 2, 2, 2
            , 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 305, 0
            , 339, 256, 256, 256, 252, 0, 253, 0, 0, 256, 256, 3, 256, 256, 256, 256, 256, 256, 256, 79
            , 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 0, 0, 38, 0, 38, 0, 0, 0, 0, 38
            , 0, 38, 35, 38, 38, 0, 256, 36, 37, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38
            , 38, 38, 38, 0, 0, 255, 0, 0, 308, 0, 0, 308, 309, 308, 38, 254, 254, 257, 257, 309
            , 258, 258, 258, 259, 259, 259, 259, 146, 0, 0, 146, 146, 146, 0, 38, 240, 240, 240, 240, 0
            , 149, 146, 0, 149, 240, 240, 0, 240, 240, 240, 240, 240, 240, 240, 149, 208, 0, 0, 208, 148
            , 208, 146, 148, 148, 148, 225, 0, 225, 0, 209, 0, 0, 0, 148, 149, 0, 224, 0, 0, 145
            , 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 145, 0, 148, 145, 145, 145, 145, 145, 145
            , 239, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 147, 147, 147, 147, 147, 147, 147, 147, 147
            , 147, 147, 147, 147, 0, 0, 147, 147, 147, 147, 147, 147, 291, 290, 290, 290, 290, 290, 290, 290
            , 290, 290, 290, 290, 290, 290, 290, 290, 290, 290, 0, 0, 290, 290, 290, 290, 290, 290, 290, 298
            , 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 298, 313, 0, 298
            , 298, 298, 298, 298, 298, 298, 299, 299, 299, 299, 299, 299, 299, 299, 299, 299, 299, 299, 299, 299
            , 299, 299, 299, 299, 0, 0, 299, 299, 299, 299, 299, 299, 299, 0, 0, 0, 0, 0, 0, 0
            , 0, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 312, 0, 0
            , 312, 312, 312, 312, 312, 312, 312, 204, 204, 204, 204, 204, 204, 204, 204, 204, 204, 204, 204, 204
            , 204, 204, 204, 204, 0, 0, 204, 204, 204, 204, 204, 204, 204, 207, 207, 207, 207, 207, 207, 207
            , 207, 207, 207, 207, 207, 207, 207, 207, 207, 207, 0, 0, 207, 207, 207, 207, 207, 207, 207, 42
            , 0, 42, 0, 0, 0, 0, 42, 0, 42, 0, 40, 41, 0, 0, 0, 0, 42, 42, 42, 42
            , 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 0, 0, 0, 200, 200, 200, 200, 200, 200, 200
            , 0, 42, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 0, 196, 0, 0, 196, 196, 196, 0
            , 292, 42, 0, 292, 196, 0, 46, 197, 46, 92, 0, 92, 0, 46, 292, 46, 91, 0, 0, 0
            , 0, 0, 200, 44, 45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 0, 0, 92
            , 0, 0, 0, 199, 199, 199, 293, 0, 46, 0, 0, 92, 0, 0, 139, 139, 139, 139, 139, 139
            , 139, 139, 139, 139, 139, 139, 139, 0, 46, 139, 139, 139, 139, 139, 139, 142, 142, 142, 142, 142
            , 142, 142, 142, 142, 142, 142, 142, 142, 0, 0, 142, 142, 142, 142, 142, 142, 144, 144, 144, 144
            , 144, 144, 144, 144, 144, 144, 144, 144, 144, 0, 0, 144, 144, 144, 143, 143, 143, 221, 221, 221
            , 221, 221, 221, 221, 221, 221, 221, 221, 221, 221, 0, 0, 221, 221, 221, 221, 221, 221, 52, 306
            , 52, 0, 306, 307, 306, 52, 0, 52, 0, 0, 307, 0, 0, 306, 0, 0, 0, 48, 49, 50
            , 51, 52, 52, 52, 52, 52, 52, 52, 52, 185, 185, 185, 185, 0, 0, 188, 0, 0, 185, 185
            , 52, 185, 185, 329, 185, 185, 185, 185, 152, 300, 0, 152, 300, 0, 0, 0, 0, 0, 0, 0
            , 52, 0, 152, 300, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 133, 0, 186, 131
            , 131, 132, 153, 0, 302, 0, 0, 302, 0, 0, 0, 0, 0, 318, 0, 301, 318, 0, 302, 184
            , 184, 184, 189, 189, 189, 189, 0, 318, 190, 0, 0, 189, 189, 0, 189, 189, 330, 189, 189, 189
            , 189, 0, 0, 0, 0, 0, 0, 0, 0, 56, 303, 56, 271, 271, 271, 271, 56, 0, 56, 319
            , 0, 271, 271, 0, 271, 271, 271, 271, 271, 271, 271, 191, 54, 55, 56, 56, 56, 56, 56, 56
            , 0, 0, 0, 0, 0, 0, 0, 310, 310, 310, 310, 56, 0, 311, 0, 0, 310, 310, 270, 310
            , 310, 310, 310, 310, 310, 310, 314, 314, 314, 314, 0, 56, 315, 0, 0, 314, 314, 0, 314, 314
            , 314, 314, 314, 314, 314, 17, 17, 17, 17, 0, 0, 0, 0, 0, 17, 17, 0, 17, 17, 17
            , 17, 17, 17, 17, 20, 20, 20, 20, 0, 0, 0, 0, 0, 21, 22, 0, 321, 23, 23, 23
            , 23, 23, 23, 32, 32, 32, 322, 0, 0, 0, 0, 0, 32, 32, 0, 32, 32, 32, 32, 32
            , 32, 32, 34, 34, 34, 34, 0, 0, 0, 0, 0, 34, 34, 0, 34, 34, 34, 34, 34, 34
            , 34, 39, 39, 39, 39, 0, 0, 0, 0, 0, 39, 39, 0, 39, 39, 39, 39, 39, 39, 39
            , 43, 43, 43, 43, 0, 0, 0, 0, 0, 43, 43, 0, 43, 43, 43, 43, 43, 43, 43, 47
            , 47, 47, 47, 0, 0, 0, 0, 0, 47, 47, 0, 47, 47, 47, 47, 47, 47, 47, 53, 53
            , 53, 53, 0, 0, 0, 0, 0, 53, 53, 0, 53, 53, 53, 53, 53, 53, 53, 57, 57, 57
            , 57, 0, 0, 0, 0, 0, 57, 57, 0, 57, 57, 57, 57, 57, 57, 57, 60, 60, 60, 60
            , 0, 0, 0, 0, 0, 60, 60, 0, 60, 60, 60, 60, 60, 60, 60, 63, 63, 63, 63, 0
            , 0, 0, 0, 0, 63, 63, 0, 63, 63, 63, 63, 63, 63, 63, 66, 66, 66, 66, 0, 0
            , 0, 0, 0, 66, 66, 0, 66, 66, 66, 66, 66, 66, 66, 69, 69, 69, 69, 0, 0, 0
            , 0, 0, 69, 69, 0, 69, 69, 69, 69, 69, 69, 69, 72, 72, 72, 72, 0, 0, 0, 0
            , 0, 72, 72, 0, 72, 72, 72, 72, 72, 72, 72, 75, 75, 75, 323, 0, 0, 0, 0, 0
            , 75, 75, 0, 75, 75, 75, 75, 75, 75, 75, 90, 90, 90, 90, 0, 0, 0, 0, 0, 90
            , 90, 0, 90, 90, 90, 90, 90, 90, 90, 93, 93, 93, 93, 0, 0, 0, 0, 0, 93, 93
            , 0, 93, 93, 93, 93, 93, 93, 93, 59, 0, 59, 0, 0, 0, 62, 59, 62, 58, 0, 0
            , 0, 62, 0, 0, 0, 65, 0, 65, 0, 0, 0, 0, 65, 59, 59, 59, 59, 59, 59, 61
            , 62, 62, 62, 62, 62, 0, 0, 0, 0, 0, 59, 64, 65, 65, 65, 65, 62, 0, 0, 0
            , 0, 68, 0, 68, 71, 0, 71, 65, 68, 195, 59, 71, 195, 195, 195, 73, 62, 73, 0, 0
            , 195, 0, 73, 195, 0, 0, 0, 65, 67, 68, 68, 68, 70, 71, 71, 0, 0, 0, 0, 0
            , 0, 0, 0, 68, 74, 73, 71, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 73, 0, 0
            , 0, 0, 0, 68, 0, 0, 71, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 73, 0, 194
            , 194, 194, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self._parse_row = [0
            , 147, 842, 5, 93, 346, 1683, 22, 1702, 7, 1721, 1740, 946, 1759, 1273, 1778, 1340
            , 1797, 1472, 1816, 1603, 1835, 2002, 1854, 2008, 1873, 2019, 1892, 2055, 1911, 2058, 1930, 2069
            , 1949, 463, 902, 1968, 1343, 1987, 234, 365, 609, 683, 711, 785, 607, 317, 608, 709
            , 673, 131, 1490, 145, 232, 1340, 479, 1361, 1382, 1005, 1037, 1018, 674, 1526, 684, 6
            , 336, 510, 175, 393, 38, 457, 46, 327, 26, 710, 9, 581, 31, 1507, 1580, 112
            , 2067, 1331, 456, 1311, 752, 469, 1177, 717, 1203, 1033, 552, 514, 162, 783, 1403, 467
            , 1040, 590, 517, 792, 1013, 464, 27, 766, 822, 823, 612, 917, 918, 717, 102, 175
            , 88, 262, 1610, 353, 1, 544, 393, 587, 689, 183, 1063, 1338, 815, 60, 1090, 1117
            , 1527, 1562, 870, 1477, 986, 1645, 1151, 1664, 512, 1571
            , 0]
        self._conflict = [0, 0, 11, 11, 11, 11, 10, 344, 0, 0, 0, 11, 11, 0, 11, 11, 11, 11, 11
            , 11, 11, 24, 24, 24, 343, 166, 0, 168, 0, 0, 24, 24, 0, 24, 24, 24, 24, 24, 24
            , 24, 32, 32, 32, 32, 0, 0, 0, 0, 0, 32, 32, 169, 32, 32, 32, 32, 32, 32, 32
            , 0, 0, 75, 75, 75, 75, 0, 0, 0, 0, 0, 75, 75, 135, 75, 75, 75, 75, 75, 75
            , 75, 0, 0, 168, 0, 0, 0, 178, 0, 0, 0, 178, 167, 33, 33, 33, 33, 33, 33, 33
            , 33, 33, 33, 33, 33, 33, 345, 0, 33, 33, 33, 33, 33, 33, 76, 76, 76, 76, 76, 76
            , 76, 76, 76, 76, 76, 76, 76, 0, 0, 76, 76, 76, 76, 76, 76, 180, 180, 180, 180, 180
            , 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 0, 0, 180, 180, 180, 180, 180, 180
            , 180, 0, 0, 185, 185, 185, 185, 0, 0, 187, 0, 135, 185, 185, 0, 185, 185, 185, 185, 185
            , 185, 185, 189, 189, 189, 189, 0, 0, 192, 0, 0, 189, 189, 0, 189, 189, 189, 189, 189, 189
            , 189, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 205, 0, 0
            , 205, 205, 205, 205, 205, 205, 205, 206, 211, 0, 0, 211, 213, 211, 230, 230, 230, 230, 0, 0
            , 229, 0, 211, 230, 230, 0, 230, 230, 346, 230, 230, 230, 230, 0, 216, 0, 0, 0, 216, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 213, 213, 213, 213
            , 213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 213, 0, 0, 213, 213, 213, 213, 213
            , 213, 213, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 215, 0
            , 0, 215, 215, 215, 215, 215, 215, 215, 228, 232, 228, 235, 235, 235, 235, 0, 0, 234, 0, 228
            , 235, 235, 0, 235, 235, 347, 235, 235, 235, 235, 245, 245, 245, 245, 0, 246, 0, 246, 0, 245
            , 245, 0, 245, 245, 245, 245, 245, 245, 245, 0, 0, 0, 0, 233, 233, 233, 233, 233, 233, 233
            , 233, 233, 233, 233, 233, 233, 233, 233, 233, 233, 0, 0, 233, 233, 233, 233, 233, 233, 233, 0
            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 245, 247, 0, 256, 237
            , 256, 0, 256, 256, 256, 256, 256, 0, 256, 256, 256, 256, 0, 0, 256, 256, 256, 256, 256, 256
            , 256, 256, 256, 256, 256, 256, 256, 256, 256, 254, 256, 256, 256, 256, 256, 256, 256, 256, 256, 256
            , 256, 256, 0, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238, 238
            , 0, 0, 238, 238, 238, 238, 238, 238, 238, 264, 264, 264, 264, 0, 0, 0, 0, 0, 264, 264
            , 0, 264, 264, 264, 264, 264, 264, 264, 230, 230, 230, 230, 0, 0, 231, 0, 0, 230, 230, 0
            , 230, 230, 230, 230, 230, 230, 230, 0, 0, 0, 0, 0, 0, 0, 0, 264, 264, 264, 264, 264
            , 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 264, 263, 264, 264, 264, 264
            , 264, 264, 264, 0, 264, 264, 264, 264, 0, 264, 264, 264, 264, 264, 264, 264, 289, 289, 289, 289
            , 0, 0, 0, 0, 0, 289, 289, 0, 289, 289, 289, 289, 289, 289, 289, 24, 24, 24, 24, 0
            , 0, 0, 0, 0, 24, 24, 0, 24, 24, 24, 24, 24, 24, 24, 0, 0, 0, 0, 0, 0
            , 0, 0, 288, 0, 0, 0, 136, 0, 0, 136, 136, 136, 0, 0, 0, 0, 0, 136, 0, 0
            , 136, 0, 0, 0, 0, 0, 0, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25
            , 136, 0, 25, 25, 25, 25, 25, 25, 0, 0, 0, 0, 136, 0, 136, 136, 136, 136, 136, 136
            , 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 134, 0, 136, 136, 136, 136, 136, 136, 136
            , 235, 235, 235, 235, 0, 0, 236, 0, 0, 235, 235, 0, 235, 235, 235, 235, 235, 235, 235]
        self._conflict_row = [0
            , 1, 20, 39, 60, 6, 104, 24, 15, 85, 161, 180, 151, 226, 252, 232, 323
            , 329, 413, 348, 413, 487, 1, 574, 593, 624, 624, 506, 698
            , 0]

    @property
    def parse_table(self):
        return self._parse


    @property
    def parse_row(self):
        return self._parse_row


    @property
    def conflict_table(self):
        return self._conflict


    @property
    def conflict_row(self):
        return self._conflict_row


    @property
    def production_table(self):
        return self._production


    @property
    def production_row(self):
        return self._production_row


    def is_non_terminal(self, symbol_index):
        return self.START_SYMBOL <= symbol_index < self.START_ACTION


    def is_terminal(self, symbol_index):
        return 0 < symbol_index < self.START_SYMBOL


    def is_action(self, symbol_index):
        return self.START_ACTION <= symbol_index < self.END_ACTION


    def get_symbol_type(self, symbol_index):
        symbol_type = self.NOT_A_SYMBOL

        if self.START_ACTION <= symbol_index < self.END_ACTION:
            symbol_type = self.ACTION_SYMBOL
        elif symbol_index >= self.START_SYMBOL:
            symbol_type = self.NONTERMINAL_SYMBOL
        elif symbol_index > 0:
            symbol_type = self.TERMINAL_SYMBOL
        return symbol_type


    def get_production_array(self, production_id):
        index = self.production_row[production_id]
        array_length = self.production_table[index]
        return self.production_table[index + 1: index + 1 + array_length]


class C99LabelVocabulary(object):
    def __init__(self, slk_constants: C99SLKConstants):
        self._slk_constants = slk_constants
        self._terminal_names = ["0"
            , "IDENTIFIER"
            , "CONSTANT"
            , "STRING_LITERAL"
            , "("
            , ")"
            , "["
            , "]"
            , "."
            , "PTR_OP"
            , "INC_OP"
            , "DEC_OP"
            , ","
            , "SIZEOF"
            , "&"
            , "*"
            , "+"
            , "-"
            , "~"
            , "!"
            , "/"
            , "%"
            , "LEFT_OP"
            , "RIGHT_OP"
            , "<"
            , ">"
            , "LE_OP"
            , "GE_OP"
            , "EQ_OP"
            , "NE_OP"
            , "^"
            , "|"
            , "AND_OP"
            , "OR_OP"
            , "?"
            , ":"
            , "="
            , "MUL_ASSIGN"
            , "DIV_ASSIGN"
            , "MOD_ASSIGN"
            , "ADD_ASSIGN"
            , "SUB_ASSIGN"
            , "LEFT_ASSIGN"
            , "RIGHT_ASSIGN"
            , "AND_ASSIGN"
            , "XOR_ASSIGN"
            , "OR_ASSIGN"
            , ";"
            , "TYPEDEF"
            , "EXTERN"
            , "STATIC"
            , "AUTO"
            , "REGISTER"
            , "VOID"
            , "CHAR"
            , "SHORT"
            , "INT"
            , "LONG"
            , "FLOAT"
            , "DOUBLE"
            , "SIGNED"
            , "UNSIGNED"
            , "BOOL"
            , "COMPLEX"
            , "IMAGINARY"
            , "TYPE_NAME"
            , "{"
            , "}"
            , "STRUCT"
            , "UNION"
            , "ENUM"
            , "CONST"
            , "RESTRICT"
            , "VOLATILE"
            , "INLINE"
            , "ELLIPSIS"
            , "CASE"
            , "DEFAULT"
            , "IF"
            , "SWITCH"
            , "ELSE"
            , "FOR"
            , "WHILE"
            , "DO"
            , "GOTO"
            , "CONTINUE"
            , "BREAK"
            , "RETURN"
            , "END_OF_SLK_INPUT"]
        self._non_terminal_name = ["0"
            , "translation_unit"
            , "more_translation_unit"
            , "primary_expression"
            , "postfix_expression"
            , "more_postfix_expression"
            , "argument_expression_list"
            , "more_argument_expression_list"
            , "unary_expression"
            , "unary_operator"
            , "cast_expression"
            , "multiplicative_expression"
            , "more_multiplicative_expression"
            , "additive_expression"
            , "more_additive_expression"
            , "shift_expression"
            , "more_shift_expression"
            , "relational_expression"
            , "more_relational_expression"
            , "equality_expression"
            , "more_equality_expression"
            , "and_expression"
            , "more_and_expression"
            , "exclusive_or_expression"
            , "more_exclusive_or_expression"
            , "inclusive_or_expression"
            , "more_inclusive_or_expression"
            , "logical_and_expression"
            , "more_logical_and_expression"
            , "logical_or_expression"
            , "more_logical_or_expression"
            , "conditional_expression"
            , "conditional_expression_tail"
            , "assignment_expression"
            , "assignment_expression_tail"
            , "assignment_operator"
            , "expression"
            , "more_expression"
            , "constant_expression"
            , "declaration"
            , "declaration_specifiers"
            , "declaration_specifiers_tail_4"
            , "declaration_specifiers_tail_3"
            , "declaration_specifiers_tail_2"
            , "declaration_specifiers_tail"
            , "init_declarator_list"
            , "more_init_declarator_list"
            , "init_declarator_list2"
            , "init_declarator"
            , "init_declarator_tail"
            , "storage_class_specifier"
            , "type_specifier"
            , "struct_or_union_specifier"
            , "struct_or_union"
            , "struct_declaration_list"
            , "more_struct_declaration_list"
            , "struct_declaration"
            , "specifier_qualifier_list"
            , "specifier_qualifier_list_tail_2"
            , "specifier_qualifier_list_tail"
            , "struct_declarator_list"
            , "more_struct_declarator_list"
            , "struct_declarator"
            , "struct_declarator_tail"
            , "enum_specifier"
            , "enum_specifier_tail"
            , "enum_specifier_tail_tail_2"
            , "enum_specifier_tail_tail_2_tail"
            , "enum_specifier_tail_tail"
            , "enumerator_list"
            , "more_enumerator_list"
            , "enumerator"
            , "type_qualifier"
            , "function_specifier"
            , "declarator"
            , "direct_declarator"
            , "more_direct_declarator"
            , "more_direct_declarator_tail_2"
            , "more_direct_declarator_tail"
            , "more_direct_declarator_tail_tail"
            , "pointer"
            , "pointer_tail"
            , "pointer_tail_tail"
            , "type_qualifier_list"
            , "more_type_qualifier_list"
            , "parameter_type_list"
            , "parameter_type_list_tail"
            , "parameter_list"
            , "more_parameter_list"
            , "parameter_declaration"
            , "declarator_or_abstract_declarator"
            , "direct_declarator_or_direct_abstract_declarator"
            , "more_dd_or_dad"
            , "identifier_list"
            , "more_identifier_list"
            , "type_name"
            , "type_name_tail"
            , "abstract_declarator"
            , "abstract_declarator_tail"
            , "direct_abstract_declarator"
            , "more_direct_abstract_declarator"
            , "initializer"
            , "initializer_tail"
            , "initializer_list"
            , "more_initializer_list"
            , "designation"
            , "designator_list"
            , "more_designator_list"
            , "designator"
            , "statement"
            , "labeled_statement"
            , "compound_statement"
            , "block_item_list"
            , "more_block_item_list"
            , "block_item"
            , "expression_statement"
            , "selection_statement"
            , "selection_statement_tail"
            , "iteration_statement"
            , "iteration_statement_tail"
            , "iteration_statement_tail_tail_2"
            , "iteration_statement_tail_tail"
            , "jump_statement"
            , "external_declaration"
            , "external_declaration_tail"
            , "external_declaration_tail_tail"
            , "function_definition_tail"
            , "declaration_list"
            , "more_declaration_list"
            , "init_declarator_list_opt"
            , "init_declarator_list2_opt"
            , ",_init_declarator_*"
            , "declarator_or_abstract_declarator_opt"
            , "direct_declarator_or_direct_abstract_declarator_opt"
            , "constant_expression_opt"
            , "parameter_type_list_opt"
            , "constant_expression_2_opt"
            , "identifier_list_opt"
            , "init_declarator_list2_2_opt"
                                   ]
        self._action_name = ["0" ,"__FinishParse" ,"__SetTypedefName" ,"__NewScope" ,"__ReleaseScope"]
        self._production_name = ["0"
            , "translation_unit --> external_declaration more_translation_unit __FinishParse"
            , "more_translation_unit --> external_declaration more_translation_unit"
            , "more_translation_unit -->"
            , "primary_expression --> IDENTIFIER"
            , "primary_expression --> CONSTANT"
            , "primary_expression --> STRING_LITERAL"
            , "primary_expression --> ( expression )"
            , "postfix_expression --> primary_expression more_postfix_expression"
            , "more_postfix_expression --> [ expression ] more_postfix_expression"
            , "more_postfix_expression --> ( ) more_postfix_expression"
            , "more_postfix_expression --> ( argument_expression_list ) more_postfix_expression"
            , "more_postfix_expression --> . IDENTIFIER more_postfix_expression"
            , "more_postfix_expression --> PTR_OP IDENTIFIER more_postfix_expression"
            , "more_postfix_expression --> INC_OP more_postfix_expression"
            , "more_postfix_expression --> DEC_OP more_postfix_expression"
            , "more_postfix_expression -->"
            , "argument_expression_list --> assignment_expression more_argument_expression_list"
            , "more_argument_expression_list --> , assignment_expression more_argument_expression_list"
            , "more_argument_expression_list -->"
            , "unary_expression --> postfix_expression"
            , "unary_expression --> INC_OP unary_expression"
            , "unary_expression --> DEC_OP unary_expression"
            , "unary_expression --> unary_operator cast_expression"
            , "unary_expression --> SIZEOF unary_expression"
            , "unary_expression --> SIZEOF ( type_name )"
            , "unary_operator --> &"
            , "unary_operator --> *"
            , "unary_operator --> +"
            , "unary_operator --> -"
            , "unary_operator --> ~"
            , "unary_operator --> !"
            , "cast_expression --> unary_expression"
            , "cast_expression --> ( type_name ) cast_expression"
            , "multiplicative_expression --> cast_expression more_multiplicative_expression"
            , "more_multiplicative_expression --> * cast_expression more_multiplicative_expression"
            , "more_multiplicative_expression --> / cast_expression more_multiplicative_expression"
            , "more_multiplicative_expression --> % cast_expression more_multiplicative_expression"
            , "more_multiplicative_expression -->"
            , "additive_expression --> multiplicative_expression more_additive_expression"
            , "more_additive_expression --> + multiplicative_expression more_additive_expression"
            , "more_additive_expression --> - multiplicative_expression more_additive_expression"
            , "more_additive_expression -->"
            , "shift_expression --> additive_expression more_shift_expression"
            , "more_shift_expression --> LEFT_OP additive_expression more_shift_expression"
            , "more_shift_expression --> RIGHT_OP additive_expression more_shift_expression"
            , "more_shift_expression -->"
            , "relational_expression --> shift_expression more_relational_expression"
            , "more_relational_expression --> < shift_expression more_relational_expression"
            , "more_relational_expression --> > shift_expression more_relational_expression"
            , "more_relational_expression --> LE_OP shift_expression more_relational_expression"
            , "more_relational_expression --> GE_OP shift_expression more_relational_expression"
            , "more_relational_expression -->"
            , "equality_expression --> relational_expression more_equality_expression"
            , "more_equality_expression --> EQ_OP relational_expression more_equality_expression"
            , "more_equality_expression --> NE_OP relational_expression more_equality_expression"
            , "more_equality_expression -->"
            , "and_expression --> equality_expression more_and_expression"
            , "more_and_expression --> & equality_expression more_and_expression"
            , "more_and_expression -->"
            , "exclusive_or_expression --> and_expression more_exclusive_or_expression"
            , "more_exclusive_or_expression --> ^ and_expression more_exclusive_or_expression"
            , "more_exclusive_or_expression -->"
            , "inclusive_or_expression --> exclusive_or_expression more_inclusive_or_expression"
            , "more_inclusive_or_expression --> | exclusive_or_expression more_inclusive_or_expression"
            , "more_inclusive_or_expression -->"
            , "logical_and_expression --> inclusive_or_expression more_logical_and_expression"
            , "more_logical_and_expression --> AND_OP inclusive_or_expression more_logical_and_expression"
            , "more_logical_and_expression -->"
            , "logical_or_expression --> logical_and_expression more_logical_or_expression"
            , "more_logical_or_expression --> OR_OP logical_and_expression more_logical_or_expression"
            , "more_logical_or_expression -->"
            , "conditional_expression --> logical_or_expression conditional_expression_tail"
            , "conditional_expression_tail -->"
            , "conditional_expression_tail --> ? expression : conditional_expression"
            , "assignment_expression --> unary_expression assignment_expression_tail"
            ,
                                 "assignment_expression --> ( type_name ) cast_expression more_multiplicative_expression more_additive_expression more_shift_expression more_relational_expression more_equality_expression more_and_expression more_exclusive_or_expression more_inclusive_or_expression more_logical_and_expression more_logical_or_expression conditional_expression_tail"
            ,
                                 "assignment_expression_tail --> more_multiplicative_expression more_additive_expression more_shift_expression more_relational_expression more_equality_expression more_and_expression more_exclusive_or_expression more_inclusive_or_expression more_logical_and_expression more_logical_or_expression conditional_expression_tail"
            , "assignment_expression_tail --> assignment_operator assignment_expression"
            , "assignment_operator --> ="
            , "assignment_operator --> MUL_ASSIGN"
            , "assignment_operator --> DIV_ASSIGN"
            , "assignment_operator --> MOD_ASSIGN"
            , "assignment_operator --> ADD_ASSIGN"
            , "assignment_operator --> SUB_ASSIGN"
            , "assignment_operator --> LEFT_ASSIGN"
            , "assignment_operator --> RIGHT_ASSIGN"
            , "assignment_operator --> AND_ASSIGN"
            , "assignment_operator --> XOR_ASSIGN"
            , "assignment_operator --> OR_ASSIGN"
            , "expression --> assignment_expression more_expression"
            , "more_expression --> , assignment_expression more_expression"
            , "more_expression -->"
            , "constant_expression --> conditional_expression"
            , "declaration --> declaration_specifiers init_declarator_list_opt ;"
            , "declaration --> TYPEDEF declaration_specifiers init_declarator_list2_opt ;"
            , "declaration_specifiers --> function_specifier declaration_specifiers_tail_4"
            , "declaration_specifiers --> type_qualifier declaration_specifiers_tail_3"
            , "declaration_specifiers --> type_specifier declaration_specifiers_tail_2"
            , "declaration_specifiers --> storage_class_specifier declaration_specifiers_tail"
            , "declaration_specifiers_tail_4 -->"
            , "declaration_specifiers_tail_4 --> declaration_specifiers"
            , "declaration_specifiers_tail_3 -->"
            , "declaration_specifiers_tail_3 --> declaration_specifiers"
            , "declaration_specifiers_tail_2 -->"
            , "declaration_specifiers_tail_2 --> declaration_specifiers"
            , "declaration_specifiers_tail -->"
            , "declaration_specifiers_tail --> declaration_specifiers"
            , "init_declarator_list --> init_declarator more_init_declarator_list"
            , "more_init_declarator_list --> , init_declarator more_init_declarator_list"
            , "more_init_declarator_list -->"
            , "init_declarator_list2 --> init_declarator __SetTypedefName ,_init_declarator_*"
            , "init_declarator --> declarator init_declarator_tail"
            , "init_declarator_tail -->"
            , "init_declarator_tail --> = initializer"
            , "storage_class_specifier --> EXTERN"
            , "storage_class_specifier --> STATIC"
            , "storage_class_specifier --> AUTO"
            , "storage_class_specifier --> REGISTER"
            , "type_specifier --> VOID"
            , "type_specifier --> CHAR"
            , "type_specifier --> SHORT"
            , "type_specifier --> INT"
            , "type_specifier --> LONG"
            , "type_specifier --> FLOAT"
            , "type_specifier --> DOUBLE"
            , "type_specifier --> SIGNED"
            , "type_specifier --> UNSIGNED"
            , "type_specifier --> BOOL"
            , "type_specifier --> COMPLEX"
            , "type_specifier --> IMAGINARY"
            , "type_specifier --> struct_or_union_specifier"
            , "type_specifier --> enum_specifier"
            , "type_specifier --> TYPE_NAME"
            , "struct_or_union_specifier --> struct_or_union IDENTIFIER { struct_declaration_list }"
            , "struct_or_union_specifier --> struct_or_union { struct_declaration_list }"
            , "struct_or_union_specifier --> struct_or_union IDENTIFIER"
            , "struct_or_union --> STRUCT"
            , "struct_or_union --> UNION"
            , "struct_declaration_list --> struct_declaration more_struct_declaration_list"
            , "more_struct_declaration_list --> struct_declaration more_struct_declaration_list"
            , "more_struct_declaration_list -->"
            , "struct_declaration --> specifier_qualifier_list struct_declarator_list ;"
            , "specifier_qualifier_list --> type_qualifier specifier_qualifier_list_tail_2"
            , "specifier_qualifier_list --> type_specifier specifier_qualifier_list_tail"
            , "specifier_qualifier_list_tail_2 --> specifier_qualifier_list"
            , "specifier_qualifier_list_tail_2 -->"
            , "specifier_qualifier_list_tail --> specifier_qualifier_list"
            , "specifier_qualifier_list_tail -->"
            , "struct_declarator_list --> struct_declarator more_struct_declarator_list"
            , "more_struct_declarator_list --> , struct_declarator more_struct_declarator_list"
            , "more_struct_declarator_list -->"
            , "struct_declarator --> declarator struct_declarator_tail"
            , "struct_declarator --> : constant_expression"
            , "struct_declarator_tail -->"
            , "struct_declarator_tail --> : constant_expression"
            , "enum_specifier --> ENUM enum_specifier_tail"
            , "enum_specifier_tail --> IDENTIFIER enum_specifier_tail_tail_2"
            , "enum_specifier_tail --> { enumerator_list enum_specifier_tail_tail"
            , "enum_specifier_tail_tail_2 --> { enumerator_list enum_specifier_tail_tail_2_tail"
            , "enum_specifier_tail_tail_2 -->"
            , "enum_specifier_tail_tail_2_tail --> }"
            , "enum_specifier_tail_tail_2_tail --> , }"
            , "enum_specifier_tail_tail --> }"
            , "enum_specifier_tail_tail --> , }"
            , "enumerator_list --> enumerator more_enumerator_list"
            , "more_enumerator_list --> , enumerator more_enumerator_list"
            , "more_enumerator_list -->"
            , "enumerator --> IDENTIFIER"
            , "enumerator --> IDENTIFIER = constant_expression"
            , "type_qualifier --> CONST"
            , "type_qualifier --> RESTRICT"
            , "type_qualifier --> VOLATILE"
            , "function_specifier --> INLINE"
            , "declarator --> pointer direct_declarator"
            , "declarator --> direct_declarator"
            , "direct_declarator --> IDENTIFIER more_direct_declarator"
            , "direct_declarator --> ( declarator ) more_direct_declarator"
            , "more_direct_declarator --> ( more_direct_declarator_tail_2"
            , "more_direct_declarator --> [ more_direct_declarator_tail"
            , "more_direct_declarator --> __NewScope ( parameter_type_list __ReleaseScope ) more_direct_declarator"
            , "more_direct_declarator -->"
            , "more_direct_declarator_tail_2 --> identifier_list ) more_direct_declarator"
            , "more_direct_declarator_tail_2 --> ) more_direct_declarator"
            , "more_direct_declarator_tail --> type_qualifier_list more_direct_declarator_tail_tail"
            , "more_direct_declarator_tail --> assignment_expression ] more_direct_declarator"
            ,
                                 "more_direct_declarator_tail --> STATIC type_qualifier_list assignment_expression ] more_direct_declarator"
            , "more_direct_declarator_tail --> * ] more_direct_declarator"
            , "more_direct_declarator_tail --> ] more_direct_declarator"
            , "more_direct_declarator_tail_tail --> assignment_expression ] more_direct_declarator"
            , "more_direct_declarator_tail_tail --> ] more_direct_declarator"
            , "more_direct_declarator_tail_tail --> STATIC assignment_expression ] more_direct_declarator"
            , "more_direct_declarator_tail_tail --> * ] more_direct_declarator"
            , "pointer --> * pointer_tail"
            , "pointer_tail --> type_qualifier_list pointer_tail_tail"
            , "pointer_tail --> pointer"
            , "pointer_tail_tail -->"
            , "pointer_tail_tail --> pointer"
            , "type_qualifier_list --> type_qualifier more_type_qualifier_list"
            , "more_type_qualifier_list --> type_qualifier more_type_qualifier_list"
            , "more_type_qualifier_list -->"
            , "parameter_type_list --> parameter_list parameter_type_list_tail"
            , "parameter_type_list_tail -->"
            , "parameter_type_list_tail --> , ELLIPSIS"
            , "parameter_list --> parameter_declaration more_parameter_list"
            , "more_parameter_list --> , parameter_declaration more_parameter_list"
            , "more_parameter_list -->"
            , "parameter_declaration --> declaration_specifiers declarator_or_abstract_declarator_opt"
            , "declarator_or_abstract_declarator --> direct_declarator_or_direct_abstract_declarator"
            , "declarator_or_abstract_declarator --> pointer direct_declarator_or_direct_abstract_declarator_opt"
            , "direct_declarator_or_direct_abstract_declarator --> IDENTIFIER more_dd_or_dad"
            , "direct_declarator_or_direct_abstract_declarator --> ( declarator_or_abstract_declarator ) more_dd_or_dad"
            , "direct_declarator_or_direct_abstract_declarator --> [ constant_expression_opt ] more_dd_or_dad"
            , "direct_declarator_or_direct_abstract_declarator --> ( parameter_type_list_opt ) more_dd_or_dad"
            , "more_dd_or_dad --> [ constant_expression_2_opt ] more_dd_or_dad"
            , "more_dd_or_dad --> ( parameter_type_list ) more_dd_or_dad"
            , "more_dd_or_dad --> ( identifier_list_opt ) more_dd_or_dad"
            , "more_dd_or_dad -->"
            , "identifier_list --> IDENTIFIER more_identifier_list"
            , "more_identifier_list --> , IDENTIFIER more_identifier_list"
            , "more_identifier_list -->"
            , "type_name --> specifier_qualifier_list type_name_tail"
            , "type_name_tail -->"
            , "type_name_tail --> abstract_declarator"
            , "abstract_declarator --> pointer abstract_declarator_tail"
            , "abstract_declarator --> direct_abstract_declarator"
            , "abstract_declarator_tail -->"
            , "abstract_declarator_tail --> direct_abstract_declarator"
            , "direct_abstract_declarator --> ( abstract_declarator ) more_direct_abstract_declarator"
            , "direct_abstract_declarator --> [ ] more_direct_abstract_declarator"
            , "direct_abstract_declarator --> [ assignment_expression ] more_direct_abstract_declarator"
            , "direct_abstract_declarator --> [ * ] more_direct_abstract_declarator"
            , "direct_abstract_declarator --> ( ) more_direct_abstract_declarator"
            , "direct_abstract_declarator --> ( parameter_type_list ) more_direct_abstract_declarator"
            , "more_direct_abstract_declarator --> [ ] more_direct_abstract_declarator"
            , "more_direct_abstract_declarator --> [ assignment_expression ] more_direct_abstract_declarator"
            , "more_direct_abstract_declarator --> [ * ] more_direct_abstract_declarator"
            , "more_direct_abstract_declarator --> ( ) more_direct_abstract_declarator"
            , "more_direct_abstract_declarator --> ( parameter_type_list ) more_direct_abstract_declarator"
            , "initializer --> { initializer_list initializer_tail"
            , "initializer --> assignment_expression"
            , "initializer_tail --> }"
            , "initializer_tail --> , }"
            , "initializer_list --> initializer more_initializer_list"
            , "initializer_list --> designation initializer more_initializer_list"
            , "more_initializer_list --> , initializer more_initializer_list"
            , "more_initializer_list --> , designation initializer more_initializer_list"
            , "more_initializer_list -->"
            , "designation --> designator_list ="
            , "designator_list --> designator more_designator_list"
            , "more_designator_list --> designator more_designator_list"
            , "more_designator_list -->"
            , "designator --> [ constant_expression ]"
            , "designator --> . IDENTIFIER"
            , "statement --> labeled_statement"
            , "statement --> compound_statement"
            , "statement --> expression_statement"
            , "statement --> selection_statement"
            , "statement --> iteration_statement"
            , "statement --> jump_statement"
            , "labeled_statement --> IDENTIFIER : statement"
            , "labeled_statement --> CASE constant_expression : statement"
            , "labeled_statement --> DEFAULT : statement"
            , "compound_statement --> __NewScope { __ReleaseScope }"
            , "compound_statement --> __NewScope { block_item_list __ReleaseScope }"
            , "block_item_list --> block_item more_block_item_list"
            , "more_block_item_list --> block_item more_block_item_list"
            , "more_block_item_list -->"
            , "block_item --> declaration"
            , "block_item --> statement"
            , "expression_statement --> ;"
            , "expression_statement --> expression ;"
            , "selection_statement --> IF ( expression ) statement selection_statement_tail"
            , "selection_statement --> SWITCH ( expression ) statement"
            , "selection_statement_tail --> ELSE statement"
            , "selection_statement_tail -->"
            , "iteration_statement --> FOR ( iteration_statement_tail"
            , "iteration_statement --> WHILE ( expression ) statement"
            , "iteration_statement --> DO statement WHILE ( expression ) ;"
            , "iteration_statement_tail --> declaration expression_statement iteration_statement_tail_tail_2"
            , "iteration_statement_tail --> expression_statement expression_statement iteration_statement_tail_tail"
            , "iteration_statement_tail_tail_2 --> ) statement"
            , "iteration_statement_tail_tail_2 --> expression ) statement"
            , "iteration_statement_tail_tail --> ) statement"
            , "iteration_statement_tail_tail --> expression ) statement"
            , "jump_statement --> GOTO IDENTIFIER ;"
            , "jump_statement --> CONTINUE ;"
            , "jump_statement --> BREAK ;"
            , "jump_statement --> RETURN ;"
            , "jump_statement --> RETURN expression ;"
            , "external_declaration --> declaration_specifiers external_declaration_tail"
            , "external_declaration --> TYPEDEF declaration_specifiers init_declarator_list2_2_opt ;"
            , "external_declaration_tail --> declarator external_declaration_tail_tail"
            , "external_declaration_tail --> ;"
            , "external_declaration_tail_tail --> function_definition_tail"
            , "external_declaration_tail_tail --> init_declarator_tail more_init_declarator_list ;"
            , "function_definition_tail --> declaration_list compound_statement"
            , "function_definition_tail --> compound_statement"
            , "declaration_list --> declaration more_declaration_list"
            , "more_declaration_list --> declaration more_declaration_list"
            , "init_declarator_list_opt --> init_declarator_list"
            , "init_declarator_list_opt -->"
            , "init_declarator_list2_opt --> init_declarator_list2"
            , "init_declarator_list2_opt -->"
            , ",_init_declarator_* --> , init_declarator __SetTypedefName ,_init_declarator_*"
            , ",_init_declarator_* -->"
            , "declarator_or_abstract_declarator_opt --> declarator_or_abstract_declarator"
            , "declarator_or_abstract_declarator_opt -->"
            , "direct_declarator_or_direct_abstract_declarator_opt --> direct_declarator_or_direct_abstract_declarator"
            , "direct_declarator_or_direct_abstract_declarator_opt -->"
            , "constant_expression_opt --> constant_expression"
            , "constant_expression_opt -->"
            , "parameter_type_list_opt --> parameter_type_list"
            , "parameter_type_list_opt -->"
            , "constant_expression_2_opt --> constant_expression"
            , "constant_expression_2_opt -->"
            , "identifier_list_opt --> identifier_list"
            , "identifier_list_opt -->"
            , "init_declarator_list2_2_opt --> init_declarator_list2"
            , "init_declarator_list2_2_opt -->"]

        self._label_to_id = {"ID": 1,
                             "CONSTANT": 2, # all constants
                             "STRING_LITERAL": 3, # all string literal
                             "LPAREN": 4,
                             "RPAREN": 5,
                             "LBRACKET": 6,
                             "RBRACKET": 7,
                             "PERIOD": 8,
                             "ARROW": 9,
                             "PLUSPLUS": 10,
                             "MINUSMINUS": 11,
                             "COMMA": 12,
                             "SIZEOF": 13,
                             "AND": 14,
                             "TIMES": 15,
                             "PLUS": 16,
                             "MINUS": 17,
                             "NOT": 18,
                             "LNOT": 19,
                             "DIVIDE": 20,
                             "MOD": 21, "LSHIFT": 22, "RSHIFT": 23,
                             "LT": 24, "GT": 25, "LE": 26, "GE": 27, "EQ": 28, "NE": 29,
                             "XOR": 30, "OR": 31, "LAND": 32, "LOR": 33, "CONDOP": 34, "COLON": 35,
                             "EQUALS": 36, "TIMESEQUAL": 37, "DIVEQUAL": 38, "MODEQUAL": 39, "PLUSEQUAL": 40,
                             "MINUSEQUAL": 41, "LSHIFTEQUAL": 42, "RSHIFTEQUAL": 43, "ANDEQUAL": 44,
                             "XOREQUAL": 45, "OREQUAL": 46, "SEMI": 47, "TYPEDEF": 48, "EXTERN": 49,
                             "STATIC": 50, "AUTO": 51, "REGISTER": 52, "VOID": 53, "CHAR": 54, "SHORT": 55,
                             "INT": 56, "LONG": 57, "FLOAT": 58, "DOUBLE": 59, "SIGNED": 60, "UNSIGNED": 61,
                             "_BOOL": 62, "_COMPLEX": 63, "IMAGINARY_": 64, "TYPEID": 65, "LBRACE": 66,
                             "RBRACE": 67, "STRUCT": 68, "UNION": 69, "ENUM": 70, "CONST": 71, "RESTRICT": 72,
                             "VOLATILE": 73, "INLINE": 74, "ELLIPSIS": 75, "CASE": 76, "DEFAULT": 77, "IF": 78,
                             "SWITCH": 79, "ELSE": 80, "FOR": 81, "WHILE": 82, "DO": 83, "GOTO": 84,
                             "CONTINUE": 85, "BREAK": 86, "RETURN": 87, "END_OF_SLK_INPUT": 88,
                             }
        self._id_to_label = util.reverse_dict(self._label_to_id)
        self._id_to_symbol_name_dict = self._create_symbol_name_dict()
        # print("symbol dict:{}".format(self._id_to_symbol_name_dict))
        self._symbol_name_to_id_dict = util.reverse_dict(self._id_to_symbol_name_dict)
        self._production_list = self._create_production_list()

    def _create_symbol_name_dict(self):
        terminal_dict = {k: self._get_symbol_name(k) for k in range(1, self._slk_constants.START_SYMBOL)}
        non_terminal_dict = {k: self._get_symbol_name(k) for k in range(self._slk_constants.START_SYMBOL, self._slk_constants.START_ACTION)}
        action_dict = {k: self._get_symbol_name(k) for k in range(self._slk_constants.START_ACTION, self._slk_constants.END_ACTION)}
        return {**terminal_dict, **non_terminal_dict, **action_dict}

    def _get_symbol_name(self, symbol_index):
        if self._slk_constants.START_ACTION <= symbol_index < self._slk_constants.END_ACTION:
            return self._action_name[symbol_index - (self._slk_constants.START_ACTION - 1)]
        elif symbol_index >= self._slk_constants.START_SYMBOL:
            return self._non_terminal_name[symbol_index - (self._slk_constants.START_SYMBOL - 1)]
        elif symbol_index > 0:
            return self._terminal_names[symbol_index]
        raise ValueError("The symbol index {} is out of range".format(symbol_index))

    def get_symbol_name(self, symbol_index):
        if symbol_index in self._id_to_symbol_name_dict:
            return self._id_to_symbol_name_dict[symbol_index]
        else:
            raise ValueError("The symbol index {} is out of range".format(symbol_index))

    def get_symbol_index(self, symbol_name):
        return self._symbol_name_to_id_dict[symbol_name]

    def get_production_name(self, production_number):
        return self._production_name[production_number]

    def _create_production_list(self):
        res = []
        for index in range(1, len(self._production_name)):
            production_array = self._slk_constants.get_production_array(index)
            lhs_name = self.get_symbol_name(production_array[0])
            rhs_name = [self.get_symbol_name(t) for t in production_array[1:]]
            res.append(Production(lhs_name, rhs_name, self._symbol_name_to_id_dict))
        return res

    def get_production(self, production_id):
        return self._production_list[production_id-1]

    def get_label_id(self, label):
        if label in self._label_to_id:
            return self._label_to_id[label]
        elif label in { 'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX', 'INT_CONST_BIN'}:
            return self._label_to_id["CONSTANT"]
        elif label in {'FLOAT_CONST', 'HEX_FLOAT_CONST'}:
            return self._label_to_id["CONSTANT"]
        elif label in {'CHAR_CONST', 'WCHAR_CONST'}:
            return self._label_to_id["CONSTANT"]
        elif label in {'STRING_LITERAL', 'WSTRING_LITERAL'}:
            return self._label_to_id["STRING_LITERAL"]
        else:
            raise ValueError("no such label:{}".format(label))

    def get_label_by_id(self, index):
        return self._id_to_label[index]


class LexTokens(metaclass=abc.ABCMeta):

    def __init__(self):
        self._last_token = None
        self._typedef_lookup_fn = None

    @abc.abstractmethod
    def get(self,):
        """
        :return: the next token
        """

    @abc.abstractmethod
    def peek(self, level, ):
        """
        :param level: the lookhead level
        :return: the lookhead tokens
        """

    def last_token_value(self):
        return self._last_token

    @property
    def typedef_lookup_fn(self):
        """
        :return: The last token value by the parser
        """
        return self._typedef_lookup_fn

    @typedef_lookup_fn.setter
    def typedef_lookup_fn(self, f):
        self._typedef_lookup_fn = f


class InputLexTokens(LexTokens):
    def __init__(self, tokens, label_vocabulary: C99LabelVocabulary, slk_constants: C99SLKConstants):
        super().__init__()
        self._index = 0
        self._label_vocabulary = label_vocabulary
        self._slk_constants = slk_constants
        self._tokens = [t[0] for t in tokens]

    def _typename_to_id(self, res):
        if res.type == "ID" and self.typedef_lookup_fn(res.value):
            res.type = 'TYPEID'
        return self._label_vocabulary.get_label_id(res.type)

    def get(self):
        if self._index >= len(self._tokens):
            return self._slk_constants.END_OF_SLK_INPUT_
        res = self._tokens[self._index]
        self._index += 1
        self._last_token = res.value
        # print("The next token is:{}".format(res.value))
        return self._typename_to_id(res)

    def peek(self, level):
        res = self._tokens[self._index+level-1]
        return self._typename_to_id(res)


class Action(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self, action_id):
        """
        :param action_id: The action id
        :return: None
        """

    @abc.abstractmethod
    def predict(self, production_number):
        """
        :param production_number: The production id
        :return:
        """


class CAction(Action):
    def __init__(self,
                 slk_constants: C99SLKConstants,
                 label_vocabulary: C99LabelVocabulary,
                 lex: LexTokens,
                 verbose=False):
        self._slk_constants = slk_constants
        self._label_vocabulary = label_vocabulary
        self._verbose = verbose
        self._lex = lex
        self._root_node = ProductionNode(None, None)
        self._tree_stack = [(slk_constants.START_SYMBOL, self._root_node)]
        self._terminal_stack = []
        self._scope = []
        self._execute_route = {
            1: self._finish_parse,
            2: self._set_typedef_name,
            3: self._new_scope,
            4: self._release_scope,
        }
        self._token_value_list = []
        self._new_scope()

    def predict(self, production_number):
        production = self._label_vocabulary.get_production(production_number)
        if self._verbose:
            print(str(production))

        top, node = self._tree_stack.pop()
        assert top == production.left_id, "The top is {}, the right id of production is:{}".format(top,
                                                                                                    production.left_id)
        node.production = production
        for i, right in reversed(list(enumerate(production.right_id))):
            if self._slk_constants.is_non_terminal(right):
                node[i] = ProductionNode(None, None)
                node[i].parent_node = node
                self._tree_stack.append((right, node[i]))
            if self._slk_constants.is_terminal(right):
                node[i] = LeafParseNode(self._label_vocabulary.get_symbol_name(right), None, right)
                node[i].parent_node = node
                self._terminal_stack.append(node[i])
            if self._slk_constants.is_action(right):
                node[i] = LeafParseNode(self._label_vocabulary.get_symbol_name(right),
                                        self._label_vocabulary.get_symbol_name(right),
                                        right)
                node[i].parent_node = node


    def match_terminal_value(self, token, value):
        node = self._terminal_stack.pop()
        assert node.type_id == token, "expect_type_id:{}, true type:{}".format(node.type_id, token)
        node.value = value
        self._token_value_list.append(value)

    def _last_value(self):
        return self._token_value_list[-1]

    def type_lookup_fn(self, v):
        for scope in reversed(self._scope):
            if v in scope["typedef_name"]:
                return True

        return False

    def _finish_parse(self):
        pass

    def _set_typedef_name(self):
        self._scope[-1]["typedef_name"].add(self._last_value())

    def _new_scope(self):
        self._scope.append({"typedef_name": set()})

    def _release_scope(self):
        self._scope.pop()

    def execute(self, action_id):
        self._execute_route[action_id]()

    @property
    def parse_tree(self):
        return self._root_node


class MoniteredCAction(CAction):
    def __init__(self, slk_constants: C99SLKConstants, label_vocabulary: C99LabelVocabulary, lex: InputLexTokens,
                 predefined_identifier_set, predefined_typename, vocabulary, verbose=False):
        super().__init__(slk_constants, label_vocabulary, lex, verbose)
        self._new_scope()
        self._predefined_identifier_set= predefined_identifier_set
        self._predefined_typename = predefined_typename
        self._identifier_type_id = self._label_vocabulary.get_symbol_index("IDENTIFIER")
        self._typename_type_id = self._label_vocabulary.get_symbol_index("TYPE_NAME")
        self._token_vocabulary = vocabulary
        self._identifier_scope_index = [0]
        self._max_scope_list = [1]
        self._consistent_identifier = [self._all_defined_identifier_set()]
        self._consistent_typename = [self._all_defined_typename_set()]
        self._is_identifier = [0]

    @property
    def identifier_scope_index(self):
        return self._identifier_scope_index

    @property
    def max_scope_list(self):
        return self._max_scope_list

    @property
    def consistent_identifier(self):
        return self._consistent_identifier

    @property
    def is_identifier(self):
        return self._is_identifier

    @property
    def consistent_typename(self):
        return self._consistent_typename

    def _new_scope(self):
        self._scope.append({"typedef_name": set(), "defined_identifier": set()})

    def _all_defined_identifier_set(self):
        return self._all_defined_id("defined_identifier")

    def _all_defined_typename_set(self):
        return self._all_defined_id("typedef_name")

    def _all_defined_id(self, key):
        res = set()
        for scope in self._scope:
            res |= scope[key]
        return {self._token_vocabulary.word_to_id(t) for t in res}

    def _get_identifier_index(self, identifier_value):
        return self._get_id_index(identifier_value, "defined_identifier")

    def _get_typename_index(self, typename_value):
        return self._get_id_index(typename_value, "typedef_name")

    def _get_id_index(self, value, key):
        for i, scope in enumerate(self._scope):
            if value in scope[key]:
                return i
        if key == "typedef_name":
            if value in self._predefined_typename:
                return 0
        elif key == "defined_identifier":
            if value in self._predefined_identifier_set:
                return 0
        return -1

    def _add_new_identifier(self):
        identifier_value = self._last_value()
        identifier_index = self._get_identifier_index(identifier_value)
        if identifier_index == -1:
            self._scope[-1]["defined_identifier"].add(identifier_value)
            identifier_index = len(self._scope) - 1
        self._identifier_scope_index.append(identifier_index)

    def _set_typedef_name(self):
        super()._set_typedef_name()
        typename = self._last_value()
        self._scope[-1]["defined_identifier"].remove(typename)
        self._consistent_identifier[-1] = self._all_defined_identifier_set()
        self._consistent_typename[-1] = self._all_defined_typename_set()
        self._identifier_scope_index[-1] = len(self._scope) - 1

    def match_terminal_value(self, token, value):
        super().match_terminal_value(token, value)
        # print("token:{}. identifier_id:{}, typename_type_id:{}".format(token,
        #                                                                self._identifier_type_id,
        #                                                                self._typename_type_id))
        if token == self._identifier_type_id:
            self._add_new_identifier()
            self._is_identifier.append(1)
        elif token == self._typename_type_id:
            identifier_value = self._last_value()
            self._identifier_scope_index.append(self._get_typename_index(identifier_value))
            self._is_identifier.append(1)
        else:
            self._is_identifier.append(0)
            self._identifier_scope_index.append(0)
        self._consistent_identifier.append(self._all_defined_identifier_set())
        self._consistent_typename.append(self._all_defined_typename_set())
        self._max_scope_list.append(len(self._scope))


class SLKParser(object):
    def __init__(self,
                 skl_constants: C99SLKConstants,
                 label_vocabulary: C99LabelVocabulary):
        self._sklconstants = skl_constants
        self._label_vocabulary = label_vocabulary

    def _report_str(self, symbol, token):
        return "Now symbol is {} and now token is {}".format(self._label_vocabulary.get_symbol_name(symbol),
                                                             self._label_vocabulary.get_symbol_name(token))

    def _report_error(self, symbol, token):
        raise ValueError(self._report_str(symbol, token))

    def parse(self,
              tokens: LexTokens,
              action: CAction):
        stack = list()
        stack.append(0)
        start_symbol = self._sklconstants.START_SYMBOL
        stack.append(start_symbol)
        token = tokens.get()
        new_token = token
        START_CONFLICT = self._sklconstants.START_CONFLICT
        while stack[-1] != 0:
            symbol = stack.pop()
            # print(self._report_str(symbol, token))

            if self._sklconstants.is_action(symbol):
                action.execute(symbol - (self._sklconstants.START_ACTION - 1))
            elif self._sklconstants.is_non_terminal(symbol):
                entry = 0
                level = 1
                if entry == 0:
                    index = self._sklconstants.parse_row[symbol - (start_symbol - 1)]
                    index += token
                    entry = self._sklconstants.parse_table[index]
                while entry >= START_CONFLICT:
                    index = self._sklconstants.conflict_row[entry - (START_CONFLICT - 1)]
                    index += tokens.peek(level)
                    entry = self._sklconstants.conflict_table[index]
                    level += 1
                if entry != 0:
                    index = self._sklconstants.production_row[entry]
                    production_length = self._sklconstants.production_table[index] - 1
                    index += 1
                    lhs = self._sklconstants.production_table[index]
                    if lhs == symbol:
                        action.predict(entry)
                        index += production_length
                        for _ in range(production_length):
                            stack.append(self._sklconstants.production_table[index])
                            index -= 1
                    else:
                        self._report_error(symbol, token)
                else:
                    self._report_error(symbol, token)
            elif self._sklconstants.is_terminal(symbol):
                if symbol == token:
                    action.match_terminal_value(token, tokens.last_token_value())
                    token = tokens.get()
                    new_token = token
                else:
                    self._report_error(symbol, token)
            else:
                raise ValueError("The symbol should not in the grammar")
        if token != self._sklconstants.END_OF_SLK_INPUT_:
            raise ValueError("The input too short")


@toolz.curry
def c99_slk_parse(code, clex):
    slk_constants = C99SLKConstants()
    label_vocabulary = C99LabelVocabulary(slk_constants)
    clex.input(code)
    tokens = InputLexTokens(clex.tokens_buffer, label_vocabulary, slk_constants)
    action = CAction(slk_constants, label_vocabulary, tokens)
    tokens.typedef_lookup_fn = action.type_lookup_fn
    slk_parser = SLKParser(slk_constants, label_vocabulary)
    slk_parser.parse(tokens, action)
    tree = action.parse_tree
    # show_production_node(tree)
    def get_t(token):
        t = token.type
        if t in {'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX', 'INT_CONST_BIN'}:
            return "CONSTANT"
        elif t in {'FLOAT_CONST', 'HEX_FLOAT_CONST'}:
            return "CONSTANT"
        elif t in {'CHAR_CONST', 'WCHAR_CONST'}:
            return "CONSTANT"
        elif t in {'STRING_LITERAL', 'WSTRING_LITERAL'}:
            return "STRING_LITERAL"
        else:
            return token.value
    tokens = [get_t(t[0]) for t in clex.tokens_buffer]
    return parse_tree_to_top_down_process(tree), tokens


@toolz.curry
def monitored_slk_parse(code, clex, predefined_identifer, predefined_typename, vocabulary):
    slk_constants = C99SLKConstants()
    label_vocabulary = C99LabelVocabulary(slk_constants)
    clex.input(code)
    tokens = InputLexTokens(clex.tokens_buffer, label_vocabulary, slk_constants)
    action = MoniteredCAction(slk_constants, label_vocabulary, tokens, predefined_identifer, predefined_typename, vocabulary)
    tokens.typedef_lookup_fn = action.type_lookup_fn
    slk_parser = SLKParser(slk_constants, label_vocabulary)
    slk_parser.parse(tokens, action)
    tree = action.parse_tree

    # show_production_node(tree)
    def get_t(token):
        t = token.type
        if t in {'INT_CONST_DEC', 'INT_CONST_OCT', 'INT_CONST_HEX', 'INT_CONST_BIN'}:
            return "CONSTANT"
        elif t in {'FLOAT_CONST', 'HEX_FLOAT_CONST'}:
            return "CONSTANT"
        elif t in {'CHAR_CONST', 'WCHAR_CONST'}:
            return "CONSTANT"
        elif t in {'STRING_LITERAL', 'WSTRING_LITERAL'}:
            return "STRING_LITERAL"
        else:
            return token.value

    tokens = [get_t(t[0]) for t in clex.tokens_buffer]
    consistent_identifier = action.consistent_identifier
    identifier_scope_index = action.identifier_scope_index
    is_identifier = action.is_identifier
    max_scope_list = action.max_scope_list
    consistent_typename = action.consistent_typename
    return parse_tree_to_top_down_process(tree), \
           tokens, \
           consistent_identifier, \
           identifier_scope_index, \
           is_identifier, \
           max_scope_list, \
           consistent_typename


class SLKProductionVocabulary(ProductionVocabulary):
    def __init__(self, slk_constants):
        self._slk_constants = slk_constants
        self._non_terminal_compact_dict = self._get_all_compact_id()
        self._confilict_compact_dicct = {}

    def _get_all_compact_id(self):
        start_symbol = self._slk_constants.START_SYMBOL
        end_symbol = self._slk_constants.START_ACTION
        res = dict()
        for symbol in range(start_symbol, end_symbol):
            start_entry = self._slk_constants.parse_row[symbol-start_symbol+1]
            r_list = set()
            for i in range(1, start_symbol):
                r = self._slk_constants.parse_table[start_entry + i]
                if r == 0:
                    pass
                else:
                    r_list.add(i)
            res[symbol] = r_list
        return res

    def get_parse_entry(self, symbol, token):
        index = self._slk_constants.parse_row[symbol-self._slk_constants.START_SYMBOL+1]
        index += token
        return self._slk_constants.parse_table[index]

    def get_conflict_entry(self, entry, token):
        index = self._slk_constants.conflict_row[entry - (self._slk_constants.START_CONFLICT - 1)]
        index += token
        entry = self._slk_constants.conflict_table[index]
        return entry

    def get_conflict_matched_terminal_node(self, entry):
        if entry in self._confilict_compact_dicct:
            return self._confilict_compact_dicct[entry]
        else:
            res = set()
            assert entry - (self._slk_constants.START_CONFLICT - 1) >= 0
            index = self._slk_constants.conflict_row[entry - (self._slk_constants.START_CONFLICT - 1)]
            for i in range(1, self._slk_constants.START_SYMBOL):
                r = self._slk_constants.conflict_table[index + i]
                if r == 0:
                    pass
                else:
                    res.add(i)
            self._confilict_compact_dicct[entry] = res
            return res

    def token_num(self):
        return self._slk_constants.START_ACTION - 1

    def terminal_token_num(self):
        return self._slk_constants.START_SYMBOL - 1

    @property
    def EMPTY_id(self):
        return self._slk_constants.START_ACTION

    def get_matched_terminal_node(self, token_id):
        if self._slk_constants.is_terminal(token_id) or token_id == self.EMPTY_id:
            return [token_id]
        elif self._slk_constants.is_non_terminal(token_id):
            return self._non_terminal_compact_dict[token_id]

    def is_token(self, token_id):
        return 0 < token_id < self._slk_constants.START_ACTION

    @property
    def slk_constants(self):
        return self._slk_constants

    def need_peek(self, symbol, token, is_entry=False):
        if is_entry:
            entry = self.get_conflict_entry(symbol, token)
        else:
            entry = self.get_parse_entry(symbol, token)
        return entry >= self._slk_constants.START_CONFLICT


class DynamicLexTokens(LexTokens):
    def __init__(self,  label_vocabulary: C99LabelVocabulary, slk_constants: C99SLKConstants):
        super().__init__()
        self._tokens = []
        self._index = 0
        self._label_vocabulary = label_vocabulary
        self._slk_constants = slk_constants

    def _typename_to_id(self, res):
        if res.type == "ID" and self.typedef_lookup_fn(res.value):
            res.type = 'TYPEID'
        return self._label_vocabulary.get_label_id(res.type)

    def get(self, ):
        if self._index >= len(self._tokens):
            return None
        res = self._tokens[self._index]
        self._index += 1
        self._last_token = res.value
        return self._typename_to_id(res)

    def peek(self, level, ):
        if self._index + level - 1 >= len(self._tokens):
            return None
        res = self._tokens[self._index + level - 1]
        return self._typename_to_id(res)

    def add_token(self, token):
        self._tokens.append(token)


class DynamicSLKParser(object):
    def __init__(self,
                 skl_constants: C99SLKConstants,
                 label_vocabulary: C99LabelVocabulary):
        self._sklconstants = skl_constants
        self._label_vocabulary = label_vocabulary
        self._slk_production_vocabulary = SLKProductionVocabulary(slk_constants=skl_constants)

    def _report_str(self, symbol, token):
        return "Now symbol is {} and now token is {}".format(self._label_vocabulary.get_symbol_name(symbol),
                                                             self._label_vocabulary.get_symbol_name(token))

    def _report_error(self, symbol, token):
        raise ValueError(self._report_str(symbol, token))

    def parse(self,
              tokens: DynamicLexTokens,
              action: CAction):
        stack = list()
        stack.append(0)
        start_symbol = self._sklconstants.START_SYMBOL
        stack.append(start_symbol)
        token = tokens.get()
        if token is None:
            yield self._slk_production_vocabulary.get_matched_terminal_node(start_symbol)
            token = tokens.get()
            assert token is not None
        new_token = token
        START_CONFLICT = self._sklconstants.START_CONFLICT
        while stack[-1] != 0:
            symbol = stack.pop()
            # print("now symbol:{}".format(self._label_vocabulary.get_symbol_name(symbol)))
            # print("left stack:")
            # for i in stack[1:]:
            #     print("{}".format(self._label_vocabulary.get_symbol_name(i)))
            # print(self._report_str(symbol, token))

            if self._sklconstants.is_action(symbol):
                action.execute(symbol - (self._sklconstants.START_ACTION - 1))
            elif self._sklconstants.is_non_terminal(symbol):
                entry = 0
                level = 1
                if entry == 0:
                    index = self._sklconstants.parse_row[symbol - (start_symbol - 1)]
                    index += token
                    entry = self._sklconstants.parse_table[index]
                while entry >= START_CONFLICT:
                    index = self._sklconstants.conflict_row[entry - (START_CONFLICT - 1)]
                    t = tokens.peek(level, )
                    if t is None:
                        yield self._slk_production_vocabulary.get_conflict_matched_terminal_node(entry)
                        t = tokens.peek(level)
                        assert t is not None
                    index += t
                    entry = self._sklconstants.conflict_table[index]
                    level += 1
                if entry != 0:
                    index = self._sklconstants.production_row[entry]
                    production_length = self._sklconstants.production_table[index] - 1
                    index += 1
                    lhs = self._sklconstants.production_table[index]
                    if lhs == symbol:
                        action.predict(entry)
                        index += production_length
                        for _ in range(production_length):
                            stack.append(self._sklconstants.production_table[index])
                            index -= 1
                    else:
                        self._report_error(symbol, token)
                else:
                    self._report_error(symbol, token)
            elif self._sklconstants.is_terminal(symbol):
                if symbol == token:
                    action.match_terminal_value(token, tokens.last_token_value())
                    token = tokens.get()
                    if token is None:
                        yield self._slk_production_vocabulary.get_matched_terminal_node(stack[-1])
                        token = tokens.get()
                        assert token is not None
                    new_token = token
                else:
                    self._report_error(symbol, token)
            else:
                raise ValueError("The symbol should not in the grammar")
        if token != self._sklconstants.END_OF_SLK_INPUT_:
            raise ValueError("The input too short")


class DynamicSLKPaserTokensWrapper(object):
    def __init__(self, parser: DynamicSLKParser, tokens: DynamicLexTokens, action: CAction):
        self.parser = parser
        self.tokens = tokens
        self.action = action
        self.once = False
        self.iter_parser = self.parser.parse(self.tokens, self.action)

    def add_token(self, token):
        self.tokens.add_token(token)

    def __iter__(self):
        if self.once:
            raise Exception("This object can only be used once")
        self.once = True
        return self

    def __next__(self):
        return next(self.iter_parser)


class PackedDynamicSLKParser(object):
    def __init__(self):
        self.slk_constants = C99SLKConstants()
        self.label_vocabulary = C99LabelVocabulary(self.slk_constants)
        self._dynamic_parser = DynamicSLKParser(self.slk_constants, self.label_vocabulary)
        self._clex = BufferedCLex(error_func=lambda self, msg, line, column: None,
                                  on_lbrace_func=lambda: None,
                                  on_rbrace_func=lambda: None,
                                  type_lookup_func=lambda typ: None)
        self._clex.build()

    def new(self):
        tokens = DynamicLexTokens(self.label_vocabulary, self.slk_constants)
        c_action = CAction(self.slk_constants, self.label_vocabulary, tokens)
        tokens.typedef_lookup_fn = c_action.type_lookup_fn
        return DynamicSLKPaserTokensWrapper(self._dynamic_parser, tokens, c_action)

    def get_all_compatible_token(self, code):
        """
        :param code: str or list of LexToken
        :return: a list of list of compatible token type
        """
        if isinstance(code, str):
            self._clex.input(code)
            code = [t[0] for t in self._clex.tokens_buffer]
        code = iter(code)
        tokens = DynamicLexTokens(self.label_vocabulary, self.slk_constants)
        c_action = CAction(self.slk_constants, self.label_vocabulary, tokens)
        tokens.typedef_lookup_fn = c_action.type_lookup_fn
        res = []
        for t in self._dynamic_parser.parse(tokens, c_action):
            res.append([self.label_vocabulary.get_label_by_id(tt) for tt in t])
            try:
                tokens.add_token(next(code))
            except StopIteration:
                break
        return res


if __name__ == '__main__':
    code = '''
     int max(int a,int* b){
     if (a>b)return a;
     else return b;}
     typedef int my_type;
    int main(void) {
     int n,a,b,c, i;
     int da[n+1];
     scanf( "%d %d %d %d" ,&n,&a,&b,&c);
     for(i=1;i<=n;i++){
     int x=-1,y=-1,z=-1;
     if(i>c){
     y=da[i-c];
     }
     da[i]=max(max(x,y),z)+1;
     }
     printf( "%d" ,da[1]);
     return 0;
    }'''

    # code = """
    # int add(int a, int b)
    # {
    #     return a+b;
    # }
    # """

    label_vocabulary = C99LabelVocabulary(C99SLKConstants())

    clex = BufferedCLex(error_func=lambda self, msg, line, column: None,
                        on_lbrace_func=lambda: None,
                        on_rbrace_func=lambda: None,
                        type_lookup_func=lambda typ: None)
    clex.build()
    # c99_slk_parse(code, clex)
    clex.input(code)
    parser = PackedDynamicSLKParser()
    t_parser = parser.new()
    print([t[0] for t in clex.tokens_buffer])
    token_list = iter([t[0] for t in clex.tokens_buffer])
    for t in t_parser:
        print([label_vocabulary.get_label_by_id(tt) for tt in t])
        try:
            tt = next(token_list)
            print(tt)
            t_parser.add_token(tt)
        except StopIteration:
            break

    print()
    for t in parser.get_all_compatible_token(code):
        print(t)

    # BEGIN, END, UNK = ["<BEGIN>", "<END>", "<UNK>"]
    # from read_data.load_parsed_data import get_vocabulary_id_map_with_keyword, get_token_vocabulary
    # vocabulary = load_vocabulary(get_token_vocabulary, get_vocabulary_id_map_with_keyword, [BEGIN], [END], UNK)
    # # header_identifier_set =  extract_fake_c_header_identifier()
    # pre_identifier_set = {"printf"}
    # pre_type_set = {"size_t"}
    # tree, tokens, consistent_identifier, \
    #        identifier_scope_index, \
    #        is_identifier, \
    #        max_scope_list, \
    #        consistent_typename = monitored_slk_parse(code, clex, pre_identifier_set, pre_type_set, vocabulary)
    # # for t in tree:
    # #     print(t)
    # # print()
    #
    # for t in  [tokens, consistent_identifier, \
    #        identifier_scope_index, \
    #        is_identifier, \
    #        max_scope_list, \
    #        consistent_typename]:
    #     print(len(t))
    #
    # print(pre_identifier_set)
    # print(pre_type_set)
    #
    # print("consistent_identifier")
    # for t in consistent_identifier:
    #     print(t)
    # print()
    #
    # print("consistent_typename")
    # for t in consistent_typename:
    #     print(t)
    # print()
    #
    # print("identifier_scope_index")
    # for t in identifier_scope_index:
    #     print(t)
    # print()
    #
    # print("is_identifier")
    # for t in is_identifier:
    #     print(t)
    # print()
    #
    # print("max_scope_list")
    # for t in max_scope_list:
    #     print(t)
    # print()

