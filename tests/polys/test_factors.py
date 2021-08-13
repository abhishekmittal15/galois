"""
A pytest module to test factoring polynomials over Galois fields.

Sage:
    to_coeffs = lambda poly: poly.coefficients(sparse=False)[::-1] if poly != 0 else [0]

    PARAMS = [(2,1), (2,8), (3,1), (3,5), (5,1), (5,4)]
    N = 20
    for p, m in PARAMS:
        print(f"POLY_FACTORS_{p}_{m} = [")
        R = GF(p**m, repr="int")["x"]
        for _ in range(N):
            a = R.random_element(randint(0, 40))
            polys = []
            exponents = []
            for item in factor(a):
                polys.append(to_coeffs(item[0]))
                exponents.append(item[1])
            print(f"    ({to_coeffs(a)}, {polys}, {exponents}),")
        print("]\n")
"""
import random

import pytest

import galois

PARAMS = [(2,1), (2,8), (3,1), (3,5), (5,1), (5,4)]

# LUT items are (a(x), [factors(x)], multiplicities). All coefficients in degree-descending order.

POLY_FACTORS_2_1 = [
    ([1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1], [[1, 1, 0, 1], [1, 1, 1, 0, 1, 0, 1]], [2, 1]),
    ([1, 1, 0], [[1, 0], [1, 1]], [1, 1]),
    ([1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [[1, 0], [1, 1, 0, 0, 1]], [5, 2]),
    ([1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0], [[1, 0], [1, 1], [1, 0, 1, 1], [1, 0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1]], [3, 3, 1, 1, 1]),
    ([1, 1, 0, 0, 0, 1, 0, 1], [[1, 1], [1, 0, 0, 0, 0, 1, 1]], [1, 1]),
    ([1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1], [[1, 1], [1, 1, 1], [1, 0, 0, 1, 0, 1], [1, 1, 0, 0, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1]], [1, 1, 1, 1, 1]),
    ([1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0], [[1, 0], [1, 1, 0, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1]], [1, 1, 1]),
    ([1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1], [[1, 1], [1, 1, 1], [1, 1, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1, 1]], [1, 1, 1, 1]),
    ([1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], [[1, 1], [1, 0, 0, 1, 0, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1]], [1, 1, 1, 1]),
    ([1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1], [[1, 1], [1, 0, 1, 1], [1, 1, 1, 0, 0, 1, 1], [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1]], [6, 1, 1, 1]),
    ([1, 0, 0, 0], [[1, 0]], [3]),
    ([1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0], [[1, 0], [1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1]], [1, 1, 1]),
    ([1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1], [[1, 0, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1], [1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1]], [1, 1, 1]),
    ([1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], [[1, 0], [1, 1, 0, 1], [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1]], [4, 1, 1, 1]),
    ([1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0], [[1, 0], [1, 1], [1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 0, 1, 1, 1, 1, 0, 1, 1]], [1, 1, 2, 1, 1, 1]),
    ([1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1], [[1, 1, 1], [1, 0, 1, 0, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1, 1], [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1]], [1, 1, 1, 1]),
    ([1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0], [[1, 0], [1, 1], [1, 0, 1, 1, 1, 1, 0, 1, 0, 1]], [1, 5, 1]),
    ([1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1], [[1, 1, 1], [1, 0, 0, 1, 1], [1, 0, 0, 1, 0, 1], [1, 1, 0, 1, 1, 1], [1, 1, 1, 0, 1, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1]], [1, 1, 1, 1, 1, 1]),
    ([1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1], [[1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1]], [1]),
    ([1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0], [[1, 0], [1, 1, 1], [1, 1, 0, 0, 1], [1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1]], [1, 1, 1, 1]),
]

POLY_FACTORS_2_8 = [
    ([154, 83, 12, 26, 53, 131, 93, 96, 50, 139, 246, 166, 189, 78, 120, 235, 133, 19, 171, 52, 17, 126, 46, 76, 102, 211, 83, 255, 84, 216, 103, 152, 202, 3, 167, 241, 119, 199, 24], [[1, 179, 180], [1, 10, 113, 49, 195, 162, 105, 66, 158, 248, 68, 13, 115, 204, 224, 91, 159, 223, 188, 56, 236, 164, 130, 6, 31, 238, 59, 74, 120, 150, 204, 13, 255, 238, 89, 33, 237]], [1, 1]),
    ([1, 141, 2, 187, 226, 181, 105, 45, 179, 58, 44, 213, 250, 13, 181, 39, 223, 25, 156, 121, 239, 150, 4, 55, 24, 128, 211, 218, 240, 47, 161, 43, 29, 84, 231, 175, 163, 34], [[1, 188], [1, 18, 115, 248, 131, 80, 64, 113], [1, 35, 144, 36, 67, 64, 58, 212, 73, 222, 125, 175, 208, 140, 182, 235, 176, 227, 119, 18, 54, 175, 182, 114, 245, 142, 103, 144, 130, 65]], [1, 1, 1]),
    ([114, 30, 62, 163, 197, 30, 230, 21, 189, 171], [[1, 107], [1, 136, 37, 122, 96, 221, 7, 84, 50]], [1, 1]),
    ([198, 82, 22, 23, 82, 9, 239, 250, 140, 94, 219, 166, 253, 60, 165, 133, 253, 136, 55, 163, 152, 25, 1, 223, 141, 33, 78, 252, 253, 223, 253, 56, 46], [[1, 55], [1, 80], [1, 219], [1, 228, 194], [1, 78, 98, 175, 82, 176, 74, 68, 207, 249, 33, 17, 143, 144, 26, 142, 123, 25, 4, 120, 100, 111, 217, 169, 173, 222, 163, 27]], [1, 1, 1, 1, 1]),
    ([118, 88, 240, 22, 232, 121, 183, 108, 236, 75, 161, 89, 149, 205, 79, 189, 79, 197, 229, 184, 97, 243, 17, 254, 255, 45, 77, 57, 189, 59, 59, 123], [[1, 246, 16], [1, 42, 49, 50, 60], [1, 217, 243, 115, 135, 196, 218, 205, 122, 230], [1, 62, 71, 127, 68, 30, 109, 45, 44, 192, 194, 119, 212, 57, 242, 196, 190]], [1, 1, 1, 1]),
    ([121, 151, 109, 114], [[1, 126, 227, 7]], [1]),
    ([90, 49, 25, 165, 59, 212, 66, 219, 76, 39, 48, 197, 200, 2, 184, 125], [[1, 70, 40], [1, 86, 23], [1, 175, 33, 44, 7, 217, 203, 97, 192, 57, 156, 181]], [1, 1, 1]),
    ([98, 198, 71, 120, 64, 242, 253, 192, 148, 20, 218, 251, 249], [[1, 160], [1, 145, 88], [1, 186, 67, 108, 154, 195, 235, 65, 126, 207]], [1, 1, 1]),
    ([21, 249, 112, 149, 237, 59, 191, 45, 164, 74, 21, 150, 110, 125, 174, 80, 102, 141, 235, 166, 37, 216, 136], [[1, 146], [1, 148], [1, 104, 123], [1, 101, 235, 186, 131, 157, 90], [1, 193, 195, 114, 241, 141, 48, 135, 254, 254, 131, 22, 223]], [1, 1, 1, 1, 1]),
    ([96, 7, 93, 89, 201, 128, 180, 206, 231, 197, 18, 170, 144, 215, 234, 97, 13, 249, 1, 17, 149, 21, 108, 139, 172], [[1, 58], [1, 198, 240, 104, 227, 192, 131, 229, 161, 211, 145, 135, 103, 23, 162, 14, 216, 181, 46, 28, 155, 134, 124, 49]], [1, 1]),
    ([230, 65, 196, 253, 85, 29, 184, 97, 113, 249, 218, 121, 188, 133, 57, 158, 129, 40, 159, 95, 200, 245, 145, 94, 213, 226, 132, 156, 103, 163, 213, 224, 116, 50, 121, 102], [[1, 145], [1, 176], [1, 225, 16, 141, 240, 98, 219, 152, 172, 61, 89, 145, 17, 220, 197, 220, 76, 0, 233, 246, 82, 34, 247, 170, 244, 247, 91, 205, 8, 189, 92, 36, 210, 47]], [1, 1, 1]),
    ([177, 254, 52, 227, 210, 72, 2, 126, 25, 138, 176, 206, 126, 133, 33, 75, 216, 129, 182, 247, 19, 204, 198, 183, 205, 88, 238, 161], [[1, 99], [1, 45, 22], [1, 236, 31, 189, 78, 70], [1, 166, 185, 65, 103, 125, 104, 253, 131, 159, 244, 102, 19, 146, 202, 44, 36, 39, 79, 74]], [1, 1, 1, 1]),
    ([70, 116, 17, 121, 204, 180, 214, 241, 181, 238, 127, 62, 117, 47, 192, 186, 179, 45, 123, 182, 69, 35, 114, 156, 146, 104, 189, 238, 3, 129], [[1, 28, 172, 91, 61, 202, 61], [1, 135, 74, 229, 237, 17, 224, 61, 165, 136, 149, 107, 96, 30, 22, 55, 194, 28, 120, 107, 224, 66, 81, 163]], [1, 1]),
    ([12, 200, 12, 21, 135, 245, 202, 2, 98, 23, 4, 186, 216, 39, 141, 74, 35, 39, 65, 93, 230, 111, 1], [[1, 229, 1, 62, 88, 221, 159, 122, 114, 68, 244, 96, 18, 64, 215, 116, 180, 64, 198, 48, 109, 78, 61]], [1]),
    ([174, 246, 58, 240, 69, 126, 204], [[1, 11, 137, 168, 192, 247, 130]], [1]),
    ([43, 75, 34, 136, 160, 196, 154, 115, 39, 103, 17, 172, 169, 68, 97, 222, 92, 94, 152], [[1, 95, 64, 148, 1, 128, 252], [1, 156, 231, 137, 206, 33, 118, 100, 126, 193, 146, 217, 21]], [1, 1]),
    ([82, 29, 111, 191, 186, 99, 14, 74, 94, 214, 171, 255, 168, 55, 4, 217, 162, 234, 76, 111, 117, 4, 16, 48, 71, 55, 176, 186, 34, 16, 17, 170, 99, 43, 38, 43, 184, 52, 103, 254], [[1, 110, 53, 217, 100], [1, 219, 36, 150, 198, 65, 188, 178, 1, 100], [1, 201, 131, 172, 89, 100, 156, 67, 16, 33, 89, 175, 225, 42, 193, 236, 188, 99, 69, 52, 62, 241, 155, 55, 58, 43, 185]], [1, 1, 1]),
    ([251, 111, 16, 171, 11, 252, 206, 129, 55, 228, 109, 115, 196, 115, 104, 199, 149, 54, 197, 245, 155, 97, 173, 161], [[1, 66], [1, 102, 219, 231, 75, 125, 15, 169, 16, 126, 20], [1, 247, 220, 218, 55, 249, 40, 235, 46, 22, 80, 244, 82]], [1, 1, 1]),
    ([144, 174, 11, 87, 137, 93, 180, 190, 132, 235, 181, 53, 3, 172, 78, 180, 255, 255, 239, 159, 71, 193, 162, 205, 43, 21, 208, 5, 149, 172], [[1, 217, 175], [1, 170, 88, 117, 214, 65, 192, 109, 101, 3, 173, 139, 198, 11], [1, 88, 209, 64, 4, 124, 198, 197, 198, 38, 233, 161, 141, 183, 252]], [1, 1, 1]),
    ([12, 183, 5, 134, 181, 109, 128, 121, 66, 37, 181, 165, 37, 110, 199, 239, 150, 135, 46, 175, 209, 237, 205, 138, 192, 90, 24, 224, 101, 165], [[1, 83, 14], [1, 48, 65, 140, 192, 109], [1, 255, 177, 9, 104, 144], [1, 189, 105, 53, 218, 170, 74, 157], [1, 125, 192, 234, 11, 169, 183, 152, 1, 227, 253]], [1, 1, 1, 1, 1]),
]

POLY_FACTORS_3_1 = [
    ([2, 1, 1, 0, 2, 1, 0, 1, 1, 1, 2, 2, 2, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1], [[1, 2, 2], [1, 1, 2, 1], [1, 0, 0, 2, 0, 1, 1, 0, 2], [1, 2, 2, 0, 1, 2, 0, 2, 1, 2, 1, 0, 0, 0, 0, 2, 0, 2, 2]], [1, 1, 1, 1]),
    ([1, 0, 0, 0, 2, 0, 0, 2], [[1, 1, 0, 2], [1, 2, 1, 0, 1]], [1, 1]),
    ([1, 2, 2, 1, 1, 0, 1, 0], [[1, 0], [1, 2, 2], [1, 0, 0, 1, 2]], [1, 1, 1]),
    ([2, 2, 1, 0, 1, 1, 2, 0, 0, 2, 2, 0, 2, 0, 2, 0, 0, 1, 1, 2, 0, 1, 0, 2, 1, 1, 2, 0, 0, 1, 0, 2, 0, 2, 2, 0, 2, 0, 1, 0, 0], [[1, 0], [1, 0, 1, 0, 2], [1, 2, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 2, 1, 2], [1, 2, 0, 2, 0, 1, 1, 2, 0, 0, 0, 2, 1, 0, 2, 1, 1, 0, 0, 0, 2, 2]], [2, 1, 1, 1, 1]),
    ([2, 1, 1, 1, 0, 2, 0, 0, 1, 0, 1, 0, 1, 2, 1, 1, 2, 0, 0, 2], [[1, 1], [1, 2], [1, 2, 2], [1, 0, 2, 2], [1, 1, 1, 2, 1, 2], [1, 2, 0, 2, 1, 2]], [2, 2, 1, 1, 1, 1]),
    ([1, 0, 1, 2, 1, 2, 2, 0, 0, 1, 2, 1, 2], [[1, 1], [1, 2], [1, 1, 1, 2], [1, 2, 2, 2, 1, 0, 0, 2]], [1, 1, 1, 1]),
    ([1, 2, 2, 1, 2, 2, 1], [[1, 0, 1], [1, 2, 1, 2, 1]], [1, 1]),
    ([1, 1, 2, 0, 1, 2, 2, 2, 0, 0, 2, 1, 1, 1, 0, 2, 2, 0, 1, 1, 2, 0, 2, 2, 0, 2, 0, 0, 2, 0, 1, 0], [[1, 0], [1, 2], [1, 0, 0, 1, 2], [1, 0, 0, 2, 2], [1, 0, 0, 0, 1, 0, 1, 1], [1, 2, 1, 1, 0, 0, 1, 2, 1, 0, 2, 1, 2, 0, 2]], [1, 1, 1, 1, 1, 1]),
    ([1, 2, 2, 2, 0, 2, 2, 0, 1, 1, 2, 1, 1, 0, 1, 0, 2, 1, 1, 0, 0, 0, 0, 1, 2, 2, 1, 1], [[1, 1], [1, 2, 2, 1, 1, 0, 1, 2, 1, 0, 0, 0, 1, 0, 1, 2, 2, 0, 2, 1, 0, 1, 2, 1, 1]], [3, 1]),
    ([2, 0, 0, 1, 1, 1, 2, 2, 2, 1, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 2, 2, 1, 2, 1], [[1, 1], [1, 2, 1, 2, 0, 1, 1], [1, 0, 0, 2, 0, 1, 2, 2, 2, 2, 0, 1, 1, 0, 2, 1, 2, 0, 2, 1, 1, 0, 0, 0, 2]], [1, 1, 1]),
    ([2, 0, 2, 1, 0, 2, 0, 1, 1, 1, 1, 1, 2, 2, 0, 0, 1, 1, 0, 2, 2, 2, 1, 0, 2, 1, 0], [[1, 0], [1, 1], [1, 1, 0, 0, 2], [1, 1, 1, 2, 2, 0, 0, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 0, 2, 1, 1]], [1, 1, 1, 1]),
    ([2, 1, 1, 2, 2, 0, 1, 2, 0, 2, 2, 1, 1, 1, 2, 0, 0, 1, 2, 2, 0, 1, 2, 2, 0, 2, 1, 0, 0, 0], [[1, 2], [1, 0], [1, 1, 0, 2], [1, 2, 1, 1, 2], [1, 0, 2, 0, 2, 1, 2, 2, 1], [1, 1, 1, 0, 1, 0, 2, 0, 0, 2]], [2, 3, 1, 1, 1, 1]),
    ([2, 0, 2, 2, 0, 2, 1, 0, 2, 1, 0, 0, 2, 2, 2, 2, 1, 2, 1, 1, 1, 0, 1, 0, 1, 2, 2, 2, 1, 2, 2, 0, 0, 0, 1, 2, 1, 2], [[1, 2], [1, 1, 2, 2, 2], [1, 1, 1, 2, 2, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 2, 0, 1, 0, 2, 2, 0, 1, 2, 0, 2]], [2, 1, 1]),
    ([1], [], []),
    ([2, 2, 1, 2, 0, 0, 0, 2, 2, 1, 0, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 2, 0, 1, 1, 0, 0, 2, 1, 1, 0, 2, 2, 0, 2, 0, 2, 1, 0, 0, 2], [[1, 2], [1, 1, 2, 2, 2], [1, 1, 1, 0, 2, 2, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2, 2, 1, 0, 0, 1, 2, 1, 0, 1, 2, 0, 1, 2, 0, 2, 1, 1, 0, 0, 1]], [1, 1, 1]),
    ([1, 2, 0, 2, 1, 2, 0, 0, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 0, 0, 1, 0, 0, 1, 1, 1], [[1, 1], [1, 0, 2, 1, 0, 1, 1, 0, 1, 2, 2, 2, 1, 0, 1, 0, 0, 2, 1, 2, 1, 0, 2, 2, 1]], [2, 1]),
    ([1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 2, 1, 0, 2, 2, 2, 1, 2, 0, 0, 2, 0, 2, 0, 2, 2, 0, 2, 0, 2, 1, 0, 2, 0], [[1, 0], [1, 1], [1, 2], [1, 0, 0, 2, 2, 1, 0, 1], [1, 1, 2, 0, 0, 0, 1, 0, 0, 1, 1, 2, 1, 0, 1, 0, 1, 2, 2, 2, 2, 2, 0, 1]], [1, 1, 1, 1, 1]),
    ([2, 2, 1, 2, 0, 2, 2, 1, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1, 0, 2, 1, 0, 2, 1, 0, 0, 2, 2, 0, 2, 2, 0, 0, 1, 0, 0, 1, 2, 2, 2, 0], [[1, 0], [1, 1, 2, 1, 0, 1, 1, 2, 0, 0, 1, 1, 1, 1, 0, 0, 0, 2, 0, 1, 2, 0, 1, 2, 0, 0, 1, 1, 0, 1, 1, 0, 0, 2, 0, 0, 2, 1, 1, 1]], [1, 1]),
    ([1, 2, 0, 0, 2, 2, 0, 2, 0, 1, 1, 2, 1, 2, 0, 1, 2, 1, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 1, 1, 0, 2, 2, 1], [[1, 1], [1, 2, 2], [1, 2, 2, 1, 0, 0, 1, 2, 2, 2, 2, 1, 1], [1, 0, 0, 1, 0, 0, 1, 1, 2, 1, 2, 0, 2, 2, 0, 1, 2, 1, 2]], [1, 1, 1, 1]),
    ([1, 1, 1, 1, 2, 1, 1, 0, 0, 1, 0, 0, 0, 2, 2, 2, 0, 1, 2, 0, 0, 2, 1, 0, 1, 0, 0, 0], [[1, 1], [1, 0], [1, 2, 2], [1, 1, 0, 1, 0, 0, 2, 0, 1, 0, 2, 1, 1, 0, 2, 0, 1, 0, 1, 1, 2, 2]], [1, 3, 1, 1]),
]

POLY_FACTORS_3_5 = [
    ([157, 49, 5, 220, 194, 10, 226, 5, 53, 169, 131, 58, 142, 68, 68, 185, 100, 82, 93, 11, 162, 10, 34, 69], [[1, 159], [1, 75, 148, 38, 155, 5, 37, 85], [1, 228, 18, 148, 47, 127, 214, 242, 190, 28, 84, 82, 42, 36, 236, 238]], [1, 1, 1]),
    ([141, 40, 155, 29, 129, 238, 35, 13, 143, 55, 17, 97, 82, 144, 50, 13, 226, 112, 99, 157, 155, 219, 75, 197, 84, 91, 159, 89, 93, 228, 158], [[1, 184, 11], [1, 23, 148, 79, 93, 179, 68, 30, 170, 72, 128, 147, 67, 235, 100, 159, 76, 200, 18, 18, 27, 97, 11, 52, 25, 63, 74, 43, 112]], [1, 1]),
    ([109, 232, 63, 107, 50, 18, 217, 224, 132, 49, 96, 22, 194, 80, 117, 239, 13, 207, 122, 141, 36, 216, 45, 55, 63, 142, 127], [[1, 99], [1, 235], [1, 234, 210, 111, 79], [1, 72, 39, 223, 192, 137, 37, 205, 194], [1, 240, 9, 114, 7, 59, 90, 225, 72, 166, 78, 183, 98]], [1, 1, 1, 1, 1]),
    ([47, 45, 16, 51, 72, 116, 188, 194, 215, 232, 217, 238, 144, 71, 112, 42, 95, 111, 41, 75, 34, 163, 193, 2, 164, 157, 153, 38, 234], [[1, 21, 50], [1, 68, 106], [1, 233, 150, 217, 141, 142], [1, 61, 20, 174, 14, 90, 92, 55, 100, 39, 187, 6, 200, 76, 190, 206, 69, 154, 137, 200]], [1, 1, 1, 1]),
    ([43, 4, 52, 135, 55, 2, 118, 225, 87, 168, 34, 145, 178, 95, 115, 116, 153, 238, 15, 9, 89, 221, 138, 104, 135, 235, 84, 241, 212, 94, 98, 99], [[1, 159, 155], [1, 96, 36, 181, 111], [1, 185, 231, 224, 172, 56, 69, 219, 96], [1, 188, 62, 127, 150, 10, 55, 230, 124, 112, 91, 48, 181, 152, 169, 136, 203, 14]], [1, 1, 1, 1]),
    ([204, 126, 159, 124, 143, 84, 7, 29, 166, 102, 31, 18, 132, 60, 95, 97, 219, 41], [[1, 214], [1, 232], [1, 160, 149, 190, 148, 38], [1, 130, 149, 52, 25, 228, 157, 204, 199, 37, 207]], [1, 1, 1, 1]),
    ([221, 49, 53, 195, 142, 181, 104, 152, 1, 175, 53, 105, 192, 33, 4, 170, 182, 55, 10, 113, 128, 46, 220, 187, 115, 69, 84, 199, 129, 13, 191, 85, 51, 55], [[1, 131], [1, 136, 240], [1, 100, 35, 104, 234, 62, 184, 171, 97, 20], [1, 167, 172, 69, 174, 38, 210, 145, 142, 87, 59, 178, 179, 103, 233, 74, 127, 178, 136, 226, 198, 29]], [1, 1, 1, 1]),
    ([43, 95, 26, 39, 118, 55, 17, 24, 56, 75, 197, 139, 233, 61, 28, 49, 145, 218, 87, 176, 178], [[1, 4, 180, 63], [1, 191, 166, 201], [1, 154, 39, 198, 230], [1, 83, 125, 82, 135, 131, 138, 39, 240, 117, 11]], [1, 1, 1, 1]),
    ([53, 96, 199, 236, 22, 23, 37, 182, 50, 68, 93, 208, 50, 155, 154, 188, 215, 48, 231, 234, 93, 171, 133, 192, 106, 122, 12, 238, 23, 221, 6, 31, 147, 118, 110, 185, 165, 192], [[1, 122], [1, 160], [1, 194], [1, 22, 214, 24], [1, 92, 44, 116], [1, 127, 205, 136, 191, 156, 151, 226, 30, 48, 120, 130, 147, 20, 52, 177, 180, 178, 188, 192, 201, 130, 193, 227, 199, 50, 136, 220, 45]], [1, 1, 1, 1, 1, 1]),
    ([72, 183, 240, 75, 81, 179, 73, 217, 100, 97, 18, 22, 89, 92, 169, 204, 222, 92, 149, 133, 226, 218, 161, 3], [[1, 6], [1, 66], [1, 73, 113], [1, 101, 209, 75, 108, 165, 110, 19, 19], [1, 67, 51, 242, 207, 166, 29, 68, 231, 128, 236, 198]], [1, 1, 1, 1, 1]),
    ([173, 2, 78, 183, 143, 156, 134, 157, 146, 108, 114, 191, 113, 116, 58, 95, 115, 233, 99, 191, 179, 236, 20, 123, 98, 35, 122, 77, 114, 62, 84, 98, 153, 140], [[1, 81], [1, 180], [1, 198, 44], [1, 240, 39, 151, 69, 159, 213, 50, 147, 56, 125, 182, 178, 137, 236, 58, 240, 124, 84, 44, 169, 88, 154, 0, 31, 188, 187, 60, 41, 20]], [1, 1, 1, 1]),
    ([43, 42, 12, 117, 67, 13, 34, 229, 177, 205, 113, 58, 139, 20, 163, 57, 18, 230, 168, 66, 52, 192, 189, 22, 165, 167, 207, 209, 132, 240, 142, 55, 54, 132], [[1, 119], [1, 133], [1, 195], [1, 227], [1, 33, 229], [1, 194, 156, 11, 39], [1, 208, 48, 158, 26, 173, 199, 92], [1, 138, 241, 161, 206, 160, 160, 62, 155, 178, 16, 129, 102, 23, 40, 209, 169]], [1, 1, 1, 1, 1, 1, 1, 1]),
    ([23, 134, 61, 10, 169, 109, 133, 114, 82, 200, 18, 99, 186, 8, 120, 212, 219, 74, 186, 184, 148, 14, 149, 46, 61, 18, 112, 134, 236, 7, 215, 10, 87, 90, 194], [[1, 89, 109, 120, 234, 200, 54], [1, 152, 70, 142, 136, 159, 4], [1, 176, 182, 209, 124, 122, 180, 144, 4, 38, 205], [1, 58, 24, 129, 79, 108, 93, 84, 224, 26, 69, 190, 35]], [1, 1, 1, 1]),
    ([185, 119, 79, 93, 114, 155, 38, 182, 112, 172, 223, 99, 159, 95, 140, 2, 1, 148, 201, 23], [[1, 69, 77, 24, 42], [1, 96, 184, 223, 27, 239, 239, 9, 75, 216, 169, 101, 63, 78, 169, 39]], [1, 1]),
    ([121, 76, 213, 58, 191, 159, 14, 96, 242, 180, 76, 73, 230, 23, 231, 42, 197, 170, 113, 54, 111, 71, 85, 170, 173, 77, 203, 161], [[1, 27], [1, 86], [1, 115], [1, 155, 137], [1, 192, 92, 30], [1, 104, 217, 14, 119], [1, 177, 32, 119, 21, 107], [1, 100, 165, 51, 154, 117, 137, 229, 66, 115, 74]], [1, 1, 1, 1, 1, 1, 1, 1]),
    ([20, 146, 161, 147, 63, 97, 235, 232, 158, 186, 120, 123, 227, 122, 223, 74, 139, 18, 172, 35, 37, 12, 195, 123, 127, 46, 109, 9, 216, 83, 201], [[1, 206], [1, 8, 152, 177, 40, 171, 1, 109], [1, 225, 178, 153, 72, 7, 10, 38], [1, 77, 91, 43, 230, 226, 54, 195, 76, 112, 200, 227, 149, 220, 66, 35]], [1, 1, 1, 1]),
    ([48, 143, 48, 183, 167, 189, 136, 178, 43, 195, 166, 149, 68, 242, 31, 203, 2, 42, 71, 39, 16, 85, 19, 101, 101, 54, 154, 64, 147, 79, 151, 135, 122, 221, 109, 40, 211, 176, 159, 95], [[1, 73], [1, 133], [1, 31, 103, 8, 65], [1, 109, 119, 110, 241, 90, 214, 235, 37, 202, 180, 115, 167], [1, 74, 203, 234, 102, 72, 161, 6, 175, 134, 154, 116, 166, 112, 35, 227, 64, 218, 87, 120, 192, 188]], [1, 1, 1, 1, 1]),
    ([189, 79, 65, 165, 173, 229, 139, 58, 76, 136, 51, 198, 108, 151, 103, 95, 227, 23, 195, 187, 178, 62, 108, 173, 132, 67, 152], [[1, 97, 189], [1, 84, 81, 125, 73, 169], [1, 27, 229, 187, 239, 233, 45, 32], [1, 239, 176, 185, 116, 235, 38, 85, 198, 40, 147, 162, 201]], [1, 1, 1, 1]),
    ([141, 100, 50, 80, 89, 194, 123, 113, 223, 14, 63, 85, 88, 163, 5, 214, 184, 50, 198, 230, 187, 216, 59, 112, 201, 136, 177, 214, 167, 45, 232, 173, 82], [[1, 233, 14, 204, 43], [1, 69, 38, 94, 71, 21], [1, 21, 190, 82, 39, 93, 39, 121, 75, 185, 20, 82, 127, 115, 173, 150, 212, 31, 95, 193, 179, 219, 43, 240]], [1, 1, 1]),
    ([233, 82, 133, 141, 58, 227, 43, 53, 181, 209, 171, 6, 173, 84, 111, 5, 115, 40, 100, 209, 214, 105, 57, 168, 27, 108, 61, 156, 34, 136, 66, 195, 78, 150, 79, 150, 164, 24], [[1, 22, 118, 189, 76, 139, 58], [1, 163, 65, 36, 54, 96, 125, 18], [1, 214, 125, 86, 17, 159, 59, 194, 234, 163, 199, 22, 188, 151, 232, 169, 203, 48, 40, 131, 212, 144, 76, 161, 107]], [1, 1, 1]),
]

POLY_FACTORS_5_1 = [
    ([2, 3, 2, 3, 1, 3, 4, 0, 3, 3, 1, 3, 4, 3, 1, 3, 4, 4, 4, 3, 4, 1, 0], [[1, 0], [1, 1, 4, 3], [1, 0, 3, 3, 3, 1, 3], [1, 4, 1, 0, 2, 0, 3], [1, 4, 4, 3, 0, 1, 4]], [1, 1, 1, 1, 1]),
    ([1, 3, 4, 2, 2, 4, 2, 1, 2, 0, 3, 4, 2, 4, 1, 2, 3, 4, 1, 2, 0, 3, 1, 0, 4], [[1, 4], [1, 0, 2, 1, 4, 0, 0, 3, 1, 1, 4], [1, 4, 1, 1, 2, 2, 4, 1, 0, 4, 0, 2, 3, 4]], [1, 1, 1]),
    ([4, 2, 3, 3, 4, 0, 3, 1, 4, 2, 4, 3, 4, 4], [[1, 3, 2, 2, 1, 0, 2, 4, 1, 3, 1, 2, 1, 1]], [1]),
    ([3, 0, 3, 0, 3, 4], [[1, 1], [1, 3], [1, 1, 4, 1]], [1, 1, 1]),
    ([4, 2, 3, 2, 4, 1, 0, 0, 4, 4, 2, 2, 3, 4, 2, 3, 3, 3, 1, 0], [[1, 0], [1, 1], [1, 2, 1, 4, 4, 2, 3, 0, 2], [1, 4, 0, 1, 2, 4, 2, 2, 2]], [1, 2, 1, 1]),
    ([1, 2, 4, 3, 0, 2, 1, 2, 1, 2, 0, 3, 0, 4, 1, 0, 1, 1, 4, 3, 4, 3, 4, 2, 1, 0, 1, 0, 3, 1, 3, 0, 2, 3, 3], [[1, 4], [1, 3, 4], [1, 0, 0, 0, 4, 2, 4, 3, 4], [1, 0, 1, 2, 1, 0, 4, 3, 3, 3], [1, 0, 2, 4, 3, 3, 1, 2, 4, 2, 4, 1, 3, 3, 4]], [1, 1, 1, 1, 1]),
    ([1, 3, 1], [[1, 4]], [2]),
    ([3, 4, 0, 4], [[1, 1], [1, 2, 3]], [1, 1]),
    ([4, 2, 1, 4, 2, 2, 2, 2, 3, 2, 0, 1, 1, 0, 1, 4, 1, 4, 2], [[1, 2, 3], [1, 1, 4, 0, 1, 1, 3, 4, 0, 1, 3, 0, 0, 0, 4, 3, 1]], [1, 1]),
    ([4, 1, 2, 0, 1, 3, 4, 3, 0, 4], [[1, 1], [1, 3, 0, 0, 4, 3, 3, 4, 1]], [1, 1]),
    ([4, 3, 2, 1, 4, 4, 2, 0], [[1, 0], [1, 4], [1, 3, 1, 0, 1, 2]], [1, 1, 1]),
    ([4, 1, 4, 4, 2, 2, 0, 0, 4, 1, 1, 3, 4, 4, 0, 2, 2, 3, 1, 4, 1, 4, 2, 3, 4, 1, 3, 0, 1, 0, 0, 2, 4, 3, 0, 3], [[1, 2, 2, 2], [1, 1, 4, 0, 0, 3, 2], [1, 1, 0, 3, 0, 3, 1, 4], [1, 0, 0, 3, 0, 2, 3, 4, 3, 0, 3, 1, 1, 1, 0, 4, 3, 0, 2, 2]], [1, 1, 1, 1]),
    ([2, 2, 2, 2, 2, 4, 4, 4, 3, 1, 3, 0, 3, 3, 2], [[1, 1], [1, 0, 2, 4], [1, 4, 0, 1, 2, 1, 0, 3, 1, 4]], [2, 1, 1]),
    ([1, 3, 1, 2, 0, 4, 3, 0, 0, 2, 3, 2, 3, 3, 4, 2, 2, 2, 4], [[1, 3], [1, 2, 2, 3], [1, 0, 2, 2, 4, 4], [1, 3, 1, 1, 3, 3, 1, 0, 4, 4]], [1, 1, 1, 1]),
    ([2, 3, 4, 1, 2, 4, 4, 3, 0, 1, 0, 2, 1, 4, 4, 0, 0, 2, 1, 4, 1, 1, 4], [[1, 1, 0, 2, 2, 4, 3], [1, 3, 4, 2, 1, 3, 2, 1, 1, 2, 2, 3, 4, 3, 3, 4, 4]], [1, 1]),
    ([2, 3, 4, 2, 4, 0, 2, 1, 0, 4, 3, 4, 0, 3, 4, 4, 3, 2, 1, 0, 0, 2, 1, 2, 2, 0, 4, 0, 1], [[1, 2], [1, 0, 0, 2, 4], [1, 4, 1, 2, 1, 2, 1, 4, 2], [1, 3, 0, 3, 0, 4, 2, 3, 3, 0, 0, 4, 4, 2, 1, 3]], [1, 1, 1, 1]),
    ([2, 4, 0, 3, 4, 4, 2, 0, 3, 2, 2, 4, 0, 4, 0, 4, 0, 4, 3, 1, 3, 3, 2, 3, 2, 4], [[1, 2], [1, 3], [1, 1, 1], [1, 1, 1, 4, 2], [1, 3, 3, 4, 2], [1, 4, 0, 1, 2], [1, 0, 0, 2, 1, 3, 2, 4, 3]], [1, 2, 1, 1, 1, 1, 1]),
    ([1, 1, 0, 0, 4, 2, 3, 2, 2], [[1, 1], [1, 4], [1, 1, 2, 2, 2]], [2, 2, 1]),
    ([2, 4, 3, 4, 2, 3, 1], [[1, 0, 4, 3], [1, 2, 0, 1]], [1, 1]),
    ([1, 2, 1, 4, 4, 2, 4, 1, 1, 2], [[1, 1], [1, 2, 4, 2], [1, 4, 3, 0, 0, 1]], [1, 1, 1]),
]

POLY_FACTORS_5_4 = [
    ([285, 294, 63, 570, 245, 414, 452, 613, 296, 512, 107, 71, 367, 278, 134, 557, 618, 207, 385, 25, 316, 593], [[1, 363], [1, 527], [1, 309, 93, 502], [1, 391, 116, 124, 427, 91, 71, 329, 68, 180, 223, 345, 417, 539, 159, 48, 312]], [1, 1, 1, 1]),
    ([84, 500, 618, 361, 614, 232, 239, 266, 492, 249, 215, 200, 242, 618, 375, 390, 113, 55, 579, 408, 117, 595, 250, 483, 109, 136, 564, 326, 132, 543, 62, 26, 506], [[1, 76, 254], [1, 434, 65, 484, 197], [1, 395, 287, 210, 481, 460, 308, 156, 165, 346, 194, 302, 20], [1, 109, 39, 142, 622, 363, 59, 66, 475, 537, 224, 218, 423, 28, 346]], [1, 1, 1, 1]),
    ([240, 209, 555, 395, 183, 180, 173, 167, 376, 320, 462, 305], [[1, 340], [1, 160, 51, 57, 17, 408, 445, 122, 156, 21, 391]], [1, 1]),
    ([55, 212, 308, 517, 577, 567, 423, 237, 258, 297, 287, 276, 417, 140, 371, 171, 106, 36, 468, 396, 114, 579, 54, 94, 430, 425, 154, 391, 611], [[1, 521], [1, 442, 221], [1, 267, 489, 402, 225], [1, 402, 523, 298, 330], [1, 94, 516, 404, 278, 544, 503, 132, 143, 52, 391, 113, 608, 150, 185, 229, 100, 420]], [1, 1, 1, 1, 1]),
    ([571, 128, 591, 264, 318, 585, 73, 6, 429, 107, 457, 476, 620, 44, 83, 435, 73, 19, 194, 215, 279, 586, 437, 397, 377, 433], [[1, 339], [1, 612], [1, 1, 69, 501], [1, 446, 330, 29, 588, 596], [1, 184, 221, 457, 475, 103, 534, 152], [1, 155, 493, 577, 196, 24, 79, 164, 597]], [1, 1, 1, 1, 1, 1]),
    ([46, 290, 97, 496, 621, 149, 370, 474, 324, 523, 407, 43, 544, 531, 2, 283, 563, 235, 483, 159, 442, 41, 26], [[1, 551], [1, 10, 622], [1, 600, 443, 458, 174, 146, 48, 556, 221, 422, 600, 261, 468, 240, 190, 348, 566, 516, 238, 352]], [1, 1, 1]),
    ([139, 548, 317, 299, 337, 182, 199, 420, 40, 414, 95, 61, 396, 398, 521], [[1, 401], [1, 441, 229, 532, 347, 162, 293], [1, 177, 309, 280, 193, 611, 526, 59]], [1, 1, 1]),
    ([525, 140], [[1, 124]], [1]),
    ([596, 296, 575, 381, 415, 430, 316, 459, 231, 503, 334, 1, 578, 481, 606, 150, 318, 211, 617], [[1, 494, 220, 70], [1, 275, 325, 323, 435], [1, 122, 40, 236, 70, 561, 460, 80, 423, 602, 373, 146]], [1, 1, 1]),
    ([157, 584, 108, 398], [[1, 30], [1, 187], [1, 189]], [1, 1, 1]),
    ([487, 439, 96, 482, 570, 272, 521, 216, 224, 137, 37, 104, 258, 152, 227, 541], [[1, 492, 442], [1, 350, 615, 18], [1, 544, 235, 23, 484, 2, 380, 254, 289, 403, 520]], [1, 1, 1]),
    ([317, 206, 282, 278, 467, 421, 117, 254, 335, 216, 183, 422, 521, 372, 35, 29, 391, 550, 182, 261, 172, 285, 537], [[1, 80], [1, 275, 133, 573], [1, 69, 32, 55, 18, 452], [1, 558, 50, 470, 370, 201], [1, 518, 78, 367, 262, 239, 118, 274, 198]], [1, 1, 1, 1, 1]),
    ([269, 72, 437, 606, 191, 325, 77, 463, 248, 400, 401, 531, 529, 583, 600, 293, 521], [[1, 437, 176], [1, 530, 80], [1, 47, 337, 411, 421], [1, 220, 438, 444, 288], [1, 256, 424, 313, 530]], [1, 1, 1, 1, 1]),
    ([56, 397, 41, 493, 225, 538, 299, 327, 342, 561, 474, 185, 93, 536, 76, 389, 531, 288, 403, 323, 264, 158, 436, 275, 122, 205, 458], [[1, 127], [1, 404, 294, 537], [1, 521, 202, 467, 319, 122, 51, 148, 547, 92, 442, 85, 593, 557, 585, 214, 304, 35, 519, 599, 77, 510, 264]], [1, 1, 1]),
    ([89, 141, 349, 251, 577, 323, 255, 347, 273, 367, 415, 219, 69, 575, 337, 407, 255, 210, 63, 530, 374, 444, 356, 14, 263, 513, 482, 546, 480, 326, 621, 563, 114, 348, 279, 370, 547], [[1, 422], [1, 570, 434], [1, 195, 617, 290, 602], [1, 479, 465, 528, 604, 254, 500, 449, 505, 180, 396, 187, 235, 46, 454, 240, 522, 323, 220, 468, 26, 371, 332, 269, 174, 223, 312, 256, 562, 196]], [1, 1, 1, 1]),
    ([592, 534, 350, 270, 518, 576, 611, 236, 0, 441, 15, 218, 351, 466, 433, 422, 524], [[1, 493, 375, 431, 169, 29, 383, 167], [1, 16, 582, 452, 504, 321, 324, 193, 420, 513]], [1, 1]),
    ([8, 181, 577, 410, 418, 569, 71, 431, 28, 20, 481, 617, 509, 372, 440, 585, 185, 203, 503, 373, 499, 371, 194, 145, 453, 49], [[1, 475, 400, 592, 231, 76, 53], [1, 94, 174, 436, 193, 266, 111, 148, 453, 101, 405, 300, 241, 25, 47, 331, 421, 7, 156, 280]], [1, 1]),
    ([259, 505, 258, 181, 566, 257, 356, 511, 623, 61, 324, 410, 324, 534, 136, 72, 322, 265, 377, 593, 106, 67, 218], [[1, 488, 504, 410], [1, 607, 583, 63, 441], [1, 113, 5, 213, 585, 488, 430, 436, 540, 421, 319, 129, 411, 31, 125, 107]], [1, 1, 1]),
    ([69, 84, 463, 492], [[1, 477, 544, 499]], [1]),
    ([239, 152, 78, 282, 62, 120, 260, 105, 101, 510, 317], [[1, 147], [1, 482, 209, 81], [1, 613, 193, 513, 394, 21, 592]], [1, 1, 1]),
]


def test_poly_factors_exceptions():
    GF = galois.GF(31)
    f = galois.Poly.Random(10, field=GF)

    with pytest.raises(TypeError):
        galois.poly_pow(f.coeffs)


def test_poly_factors_old():
    g0, g1, g2 = galois.conway_poly(2, 3), galois.conway_poly(2, 4), galois.conway_poly(2, 5)
    k0, k1, k2 = 2, 3, 4
    f = g0**k0 * g1**k1 * g2**k2
    factors, multiplicities = galois.poly_factors(f)
    assert factors == [g0, g1, g2]
    assert multiplicities == [k0, k1, k2]

    g0, g1, g2 = galois.conway_poly(3, 3), galois.conway_poly(3, 4), galois.conway_poly(3, 5)
    g0, g1, g2
    k0, k1, k2 = 3, 4, 6
    f = g0**k0 * g1**k1 * g2**k2
    factors, multiplicities = galois.poly_factors(f)
    assert factors == [g0, g1, g2]
    assert multiplicities == [k0, k1, k2]



# TODO: There is a bug in poly_factors() which is why this test won't pass
# @pytest.mark.parametrize("characteristic,degree", [(2,1), (2,8), (3,1), (3,5), (5,1), (5,4)])
# def test_poly_factors(characteristic, degree):
#     LUT = eval(f"POLY_FACTORS_{characteristic}_{degree}")

#     for key in LUT:
#         a = key
#         factors, multiplicities = LUT[key]

#         # Sort the Sage output to be ordered similarly to `galois`
#         factors, multiplicities = zip(*sorted(zip(factors, multiplicities), key=lambda item: item[0].integer))
#         factors, multiplicities = list(factors), list(multiplicities)

#         assert galois.poly_factors(a) == (factors, multiplicities)


def test_square_free_factorization_exceptions():
    GF = galois.GF(5)
    with pytest.raises(TypeError):
        galois.square_free_factorization([1,0,2,4])
    with pytest.raises(ValueError):
        galois.square_free_factorization(galois.Poly([2,0,2,4], field=GF))
    with pytest.raises(ValueError):
        galois.square_free_factorization(galois.Poly([2], field=GF))


def test_square_free_factorization():
    a = galois.irreducible_poly(2, 1, method="random")
    b = galois.irreducible_poly(2, 4, method="random")
    c = galois.irreducible_poly(2, 3, method="random")
    f = a * b * c**3
    assert galois.square_free_factorization(f) == ([a*b, c], [1, 3])

    a = galois.irreducible_poly(5, 1, method="random")
    b = galois.irreducible_poly(5, 4, method="random")
    c = galois.irreducible_poly(5, 3, method="random")
    f = a * b * c**3
    assert galois.square_free_factorization(f) == ([a*b, c], [1, 3])


def test_distinct_degree_factorization_exceptions():
    GF = galois.GF(5)
    with pytest.raises(TypeError):
        galois.distinct_degree_factorization([1,0,2,4])
    with pytest.raises(ValueError):
        galois.distinct_degree_factorization(galois.Poly([2,0,2,4], field=GF))
    with pytest.raises(ValueError):
        galois.distinct_degree_factorization(galois.Poly([2], field=GF))


def test_distinct_degree_factorization():
    GF = galois.GF(2)
    factors_1 = random.sample(galois.irreducible_polys(2, 1), random.randint(1, 2))
    factors_3 = random.sample(galois.irreducible_polys(2, 3), random.randint(1, 2))
    factors_4 = random.sample(galois.irreducible_polys(2, 4), random.randint(1, 3))
    f1 = galois.Poly.One(GF)
    for f in factors_1:
        f1 *= f
    f3 = galois.Poly.One(GF)
    for f in factors_3:
        f3 *= f
    f4 = galois.Poly.One(GF)
    for f in factors_4:
        f4 *= f
    f = f1 * f3 * f4
    assert galois.distinct_degree_factorization(f) == ([f1, f3, f4], [1, 3, 4])

    GF = galois.GF(5)
    factors_1 = random.sample(galois.irreducible_polys(5, 1), random.randint(1, 5))
    factors_3 = random.sample(galois.irreducible_polys(5, 3), random.randint(1, 5))
    factors_4 = random.sample(galois.irreducible_polys(5, 4), random.randint(1, 5))
    f1 = galois.Poly.One(GF)
    for f in factors_1:
        f1 *= f
    f3 = galois.Poly.One(GF)
    for f in factors_3:
        f3 *= f
    f4 = galois.Poly.One(GF)
    for f in factors_4:
        f4 *= f
    f = f1 * f3 * f4
    assert galois.distinct_degree_factorization(f) == ([f1, f3, f4], [1, 3, 4])


def test_equal_degree_factorization_exceptions():
    GF = galois.GF(5)
    a = galois.Poly([1,0,2,1], field=GF)
    b = galois.Poly([1,4,4,4], field=GF)
    f = a * b

    with pytest.raises(TypeError):
        galois.equal_degree_factorization(f.coeffs, 2)
    with pytest.raises(TypeError):
        galois.equal_degree_factorization(f, 2.0)
    with pytest.raises(ValueError):
        galois.equal_degree_factorization(galois.Poly([2], field=GF), 1)
    with pytest.raises(ValueError):
        galois.equal_degree_factorization(galois.Poly([2,0,2,4], field=GF), 2)
    with pytest.raises(ValueError):
        galois.equal_degree_factorization(f, 4)


def test_equal_degree_factorization():
    GF = galois.GF(2)
    for d in range(1, 4):
        polys = galois.irreducible_polys(2, d)
        r = random.randint(1, len(polys))
        factors = random.sample(polys, r)
        factors = sorted(factors, key=lambda item: item.integer)
    f = galois.Poly.One(GF)
    for factor in factors:
        f *= factor
    assert galois.equal_degree_factorization(f, d) == factors

    GF = galois.GF(5)
    for d in range(1, 4):
        polys = galois.irreducible_polys(5, d)
        r = random.randint(1, len(polys))
        factors = random.sample(polys, r)
        factors = sorted(factors, key=lambda item: item.integer)
    f = galois.Poly.One(GF)
    for factor in factors:
        f *= factor
    assert galois.equal_degree_factorization(f, d) == factors