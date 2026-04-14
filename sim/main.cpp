#include "Vmatmul.h"
#include "verilated.h"
#include <fstream>
#include <cstdint>
#include <iostream>

int main() {
    Vmatmul* top = new Vmatmul;

    int8_t A[16];
    int8_t B[16];

    std::ifstream fa("A.txt");
    std::ifstream fb("B.txt");

    if (!fa.is_open() || !fb.is_open()) {
        std::cerr << "Could not open A.txt or B.txt\n";
        return 1;
    }

    int temp;

    for (int i = 0; i < 16; i++) {
        fa >> temp;
        A[i] = (int8_t)temp;
    }

    for (int i = 0; i < 16; i++) {
        fb >> temp;
        B[i] = (int8_t)temp;
    }

    // Pack into 4 x 32-bit words for Verilator VlWide<4>
    for (int i = 0; i < 4; i++) {
        uint32_t a_word = 0;
        uint32_t b_word = 0;

        for (int j = 0; j < 4; j++) {
            a_word |= ((uint32_t)(uint8_t)A[i * 4 + j]) << (j * 8);
            b_word |= ((uint32_t)(uint8_t)B[i * 4 + j]) << (j * 8);
        }

        top->A[i] = a_word;
        top->B[i] = b_word;
    }

    top->start = 1;
    top->eval();

    std::ofstream fout("C.txt");
    if (!fout.is_open()) {
        std::cerr << "Could not open C.txt for writing\n";
        return 1;
    }

    // CRITICAL: cast to int32_t before writing
    fout << (int32_t)top->C0 << " "
         << (int32_t)top->C1 << " "
         << (int32_t)top->C2 << " "
         << (int32_t)top->C3 << "\n";

    delete top;
    return 0;
}
