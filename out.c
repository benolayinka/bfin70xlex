

/*****************************************************************************
 * bf706ez.c
 *****************************************************************************/

#include <sys/platform.h>
#include "adi_initialize.h"
#include "bf706ez.h"
#include "test.h"

#include <string.h>
#include <cycle_count.h>
#include <stdio.h>

#define STRINGIZE_(TEST) #TEST
#define STRINGIZE(TEST) STRINGIZE_(TEST)

#define TEST_NAME_LENGTH 50

#if defined SIM
asm ("#define SIM 1");
#endif

asm ("#define COMMA ,");
asm ("#if defined SIM");
asm ("#define SECONE 1");
asm ("#define SECTWO 1");
asm ("#define SECZERO 1");
asm ("#else");
asm ("#define SECONE 50000000");
asm ("#define SECTWO 25000000");
asm ("#define SECZERO 0xFFFFFFFF");
asm ("#endif");

asm ("#define lp100(instr) P4=SECONE; LOOP LC0 = P4; instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr LOOP_END;");
asm ("#define lp200(instr) P4=SECTWO; LOOP LC0 = P4; instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr instr LOOP_END;");

/** 
 * If you want to use command program arguments, then place them in the following string. 
 */
char __argv_string[] = "";

int add (volatile int * a, volatile int * b){
			return *a+*b;
	}

int main(int argc, char *argv[]) {
	/**
	 * Initialize managed drivers and/or services that have been added to
	 * the project.
	 * @return zero on success
	 */
	// adi_initComponents(); //ben this doesnt seem to make a difference. register init?
	/* Begin adding your custom code here */

	cycle_t start_count;
	cycle_t final_count;
	START_CYCLE_COUNT(start_count);

	#if TEST == 0
		#define TESTNAME "notest"
	#elif TEST == 1
		asm ("lp200(R3.H = R1.H + R2.L (NS) ;)");
		#define TESTNAME "R3.H = R1.H + R2.L (NS) ;"
	#elif TEST == 2
		asm ("lp200(R3 = R1 +|- R2 (S) ; )");
		#define TESTNAME "R3 = R1 +|- R2 (S) ; "
	#elif TEST == 3
		asm ("lp200(R3 = R0 +|+ R1 COMMA  R2 = R0 -|- R1 (S) ;)");
		#define TESTNAME "R3 = R0 +|+ R1 COMMA  R2 = R0 -|- R1 (S) ;"
	#elif TEST == 4
		asm ("lp200(R3 = R1 + R2 (NS) ; )");
		#define TESTNAME "R3 = R1 + R2 (NS) ; "
	#elif TEST == 5
		asm ("lp200(P3 = P1 + SP ; )");
		#define TESTNAME "P3 = P1 + SP ; "
	#elif TEST == 6
		asm ("lp200(R3 = R1 + R2 COMMA  R4 = R1 - R2 (NS); )");
		#define TESTNAME "R3 = R1 + R2 COMMA  R4 = R1 - R2 (NS); "
	#elif TEST == 7
		asm ("lp200(R3 = A0 + A1 COMMA  R4 = A0 - A1 (S); )");
		#define TESTNAME "R3 = A0 + A1 COMMA  R4 = A0 - A1 (S); "
	#elif TEST == 8
		asm ("lp200(A1 = R1 (X) COMMA  A0 = R0 (X); )");
		#define TESTNAME "A1 = R1 (X) COMMA  A0 = R0 (X); "
	#elif TEST == 9
		asm ("lp200(A1 = R1 (Z) COMMA  A0 = R0 (Z); )");
		#define TESTNAME "A1 = R1 (Z) COMMA  A0 = R0 (Z); "
	#elif TEST == 10
		asm ("lp200(A1 = A0 = 0; )");
		#define TESTNAME "A1 = A0 = 0; "
	#elif TEST == 11
		asm ("lp200(A1:0 += R2 * R3 ;)");
		#define TESTNAME "A1:0 += R2 * R3 ;"
	#elif TEST == 12
		asm ("lp200(R0 = R1 * R2 (FU) ;)");
		#define TESTNAME "R0 = R1 * R2 (FU) ;"
	#elif TEST == 13
		asm ("lp200(R1 = R2 * R3 (IU COMMA  NS) ;)");
		#define TESTNAME "R1 = R2 * R3 (IU COMMA  NS) ;"
	#elif TEST == 14
		asm ("lp200(R1:0 = R1 * R2 ;)");
		#define TESTNAME "R1:0 = R1 * R2 ;"
	#elif TEST == 15
		asm ("lp200(R1 = cmul(R2 COMMA  R3) ;)");
		#define TESTNAME "R1 = cmul(R2 COMMA  R3) ;"
	#elif TEST == 16
		asm ("lp200(R1 = cmul(R2 COMMA  R3)(IS);)");
		#define TESTNAME "R1 = cmul(R2 COMMA  R3)(IS);"
	#elif TEST == 17
		asm ("lp200(R1:0 = cmul(R2 COMMA  R3) ;)");
		#define TESTNAME "R1:0 = cmul(R2 COMMA  R3) ;"
	#elif TEST == 18
		asm ("lp200(R0 *= R1 ;)");
		#define TESTNAME "R0 *= R1 ;"
	#elif TEST == 19
		asm ("lp200(A1 += R3.H * R4.H ; )");
		#define TESTNAME "A1 += R3.H * R4.H ; "
	#elif TEST == 20
		asm ("lp200(R0.L = R1.L * R2.L (FU) ;)");
		#define TESTNAME "R0.L = R1.L * R2.L (FU) ;"
	#elif TEST == 21
		asm ("lp200(R0.H = R2.H * R3.H (IU) ;)");
		#define TESTNAME "R0.H = R2.H * R3.H (IU) ;"
	#elif TEST == 22
		asm ("lp200(R0 = R1.L * R2.L ; )");
		#define TESTNAME "R0 = R1.L * R2.L ; "
	#elif TEST == 23
		asm ("lp200(A1 += R1.H * R2.L COMMA  A0 += R1.L * R2.H ; )");
		#define TESTNAME "A1 += R1.H * R2.L COMMA  A0 += R1.L * R2.H ; "
	#elif TEST == 24
		asm ("lp200(R3.H = (A1 += R1.H * R2.L) COMMA  R3.L = (A0 += R1.L * R2.L) ;)");
		#define TESTNAME "R3.H = (A1 += R1.H * R2.L) COMMA  R3.L = (A0 += R"
	#elif TEST == 25
		asm ("lp200(R3 = (A1 += R1.H * R2.L) COMMA  R2 = (A0 += R1.L * R2.L) ;)");
		#define TESTNAME "R3 = (A1 += R1.H * R2.L) COMMA  R2 = (A0 += R1.L "
	#elif TEST == 26
		asm ("lp200(R3.H = (A1 += R1.H * R2.L) COMMA  A0 += R1.L * R2.L ;)");
		#define TESTNAME "R3.H = (A1 += R1.H * R2.L) COMMA  A0 += R1.L * R2"
	#elif TEST == 27
		asm ("lp200(R0 >>= 0x04 ;)");
		#define TESTNAME "R0 >>= 0x04 ;"
	#elif TEST == 28
		asm ("lp200(R0 <<= 0x04 ;)");
		#define TESTNAME "R0 <<= 0x04 ;"
	#elif TEST == 29
		asm ("lp200(R0 <<= R2 ;)");
		#define TESTNAME "R0 <<= R2 ;"
	#elif TEST == 30
		asm ("lp200(R1.H = R0.L << 0x04 ; )");
		#define TESTNAME "R1.H = R0.L << 0x04 ; "
	#elif TEST == 31
		asm ("lp200(R1 = LSHIFT R0 by R2.L ; )");
		#define TESTNAME "R1 = LSHIFT R0 by R2.L ; "
	#elif TEST == 32
		asm ("lp200(R1 = ASHIFT R0 by R2.L ; )");
		#define TESTNAME "R1 = ASHIFT R0 by R2.L ; "
	#elif TEST == 33
		asm ("lp200(R1 = ROT R0 by R2.L ; )");
		#define TESTNAME "R1 = ROT R0 by R2.L ; "
	#elif TEST == 34
		asm ("lp200(BITCLR ( R0 COMMA  6 ) ; )");
		#define TESTNAME "BITCLR ( R0 COMMA  6 ) ; "
	#elif TEST == 35
		asm ("lp200(BITSET ( R2 COMMA  9 ) ; )");
		#define TESTNAME "BITSET ( R2 COMMA  9 ) ; "
	#elif TEST == 36
		asm ("lp200(BITTGL ( R3 COMMA  2 ) ; )");
		#define TESTNAME "BITTGL ( R3 COMMA  2 ) ; "
	#elif TEST == 37
		asm ("lp200(CC = BITTST ( R3 COMMA  0 ) ; )");
		#define TESTNAME "CC = BITTST ( R3 COMMA  0 ) ; "
	#elif TEST == 38
		asm ("lp200(R3 = EXTRACT ( R0  COMMA  R1.L ) ( Z ) ; )");
		#define TESTNAME "R3 = EXTRACT ( R0  COMMA  R1.L ) ( Z ) ; "
	#elif TEST == 39
		asm ("lp200(R3 = EXTRACT ( R0  COMMA  R1.L ) ( X ) ; )");
		#define TESTNAME "R3 = EXTRACT ( R0  COMMA  R1.L ) ( X ) ; "
	#elif TEST == 40
		asm ("lp200(R3 = DEPOSIT ( R0  COMMA  R1 ) ; )");
		#define TESTNAME "R3 = DEPOSIT ( R0  COMMA  R1 ) ; "
	#elif TEST == 41
		asm ("lp200(R3 = DEPOSIT ( R0  COMMA  R1 ) ( X ) ; )");
		#define TESTNAME "R3 = DEPOSIT ( R0  COMMA  R1 ) ( X ) ; "
	#elif TEST == 42
		asm ("lp200(R2 = PACK(R0.L COMMA  R0.H); )");
		#define TESTNAME "R2 = PACK(R0.L COMMA  R0.H); "
	#elif TEST == 43
		asm ("lp200(R3 = PACK(R1.L COMMA  R0.H); )");
		#define TESTNAME "R3 = PACK(R1.L COMMA  R0.H); "
	#elif TEST == 44
		asm ("lp200(R4 = BYTEPACK(R0 COMMA  R1); )");
		#define TESTNAME "R4 = BYTEPACK(R0 COMMA  R1); "
	#elif TEST == 45
		asm ("lp200((R6 COMMA  R7) = BYTEUNPACK R1:0;)");
		#define TESTNAME "(R6 COMMA  R7) = BYTEUNPACK R1:0;"
	#elif TEST == 46
		asm("[P0]=SP;");
		asm ("lp200(R3 = [P0];)");
		#define TESTNAME "R3 = [P0];"
	#elif TEST == 47
		asm("[P3]=SP;");
		asm ("lp200(R0 = [ P3++ ];)");
		#define TESTNAME "R0 = [ P3++ ];"
	#elif TEST == 48
		asm("[P3]=SP;");
		asm ("lp200(R0 = B [ P3++ ] (Z) ;)");
		#define TESTNAME "R0 = B [ P3++ ] (Z) ;"
	#elif TEST == 49
		asm("[P1]=SP;");
		asm ("lp200([ P1 ] = R0 ;)");
		#define TESTNAME "[ P1 ] = R0 ;"
	#elif TEST == 50
		asm("[P1]=SP;");
		asm ("lp200(B [ P1 ] = R0 ;)");
		#define TESTNAME "B [ P1 ] = R0 ;"
	#elif TEST == 51
		asm("[P1]=SP;");
		asm ("lp200(R0 = W[P1] (Z) ; )");
		#define TESTNAME "R0 = W[P1] (Z) ; "
	#elif TEST == 52
		asm("[P1]=SP;");
		asm ("lp200(R1 = W[P1] (X) ; )");
		#define TESTNAME "R1 = W[P1] (X) ; "
	#elif TEST == 53
		asm("[P1]=SP;");
		asm ("lp200(R2 = B[P1] (Z) ; )");
		#define TESTNAME "R2 = B[P1] (Z) ; "
	#elif TEST == 54
		asm("[P1]=SP;");
		asm ("lp200(R3 = B[P1] (X) ; )");
		#define TESTNAME "R3 = B[P1] (X) ; "
	#elif TEST == 55
		asm("[P1]=SP;");
		asm ("lp200(R0 = W [ P1++ ] (Z) ;)");
		#define TESTNAME "R0 = W [ P1++ ] (Z) ;"
	#elif TEST == 56
		asm ("lp200([ --SP ] = R0;)");
		#define TESTNAME "[ --SP ] = R0;"
	#elif TEST == 57
		asm ("lp200(STI R5 ;)");
		#define TESTNAME "STI R5 ;"
	#elif TEST == 58
		asm ("lp200(CLI R5 ;)");
		#define TESTNAME "CLI R5 ;"
	#elif TEST == 59
		asm ("lp200(NOP;)");
		#define TESTNAME "NOP;"
	#elif TEST == 60
		asm ("lp200(MNOP;)");
		#define TESTNAME "MNOP;"
	#elif TEST == 61
		asm ("lp200(a0 = r3.h * r2.l  COMMA  a1 = r3.l * r2.h ;)");
		#define TESTNAME "a0 = r3.h * r2.l  COMMA  a1 = r3.l * r2.h ;"
	#elif TEST >= 62
		#define TESTNAME "end"
	#else
		#define TESTNAME "undefined"
	#endif
	STOP_CYCLE_COUNT(final_count,start_count);

	char test_name[TEST_NAME_LENGTH + 1]; //MAX LENGTH!!!
	strcpy(test_name, TESTNAME);
	printf("%s ", test_name);
	PRINT_CYCLES("cycles:", final_count);
	printf("test#: %s\n", STRINGIZE(TEST));

	return 0;
}

