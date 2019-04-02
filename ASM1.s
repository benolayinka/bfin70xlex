/*
Program ASM 1 tests various simple assembly language statements:
1. 16 and 32-bit arithmetic
2. Parallel instructions
3. Constants
4. Numbering formats
5. Store and retrieve from memory
6. Loops and conditionals
7. Bit set/clear/toggle
8. Arithmetic shifts
Author: Patrick Gaydecki
Date : 24.09.2016
*/
/*
.section program;
.align 4;
.global _main;
.extern _adi_initComponents;
*/
#define bb1 0.5r // Define a constant
//_main:
// call _adi_initComponents;
// 16-bit add and multiply.
r0=0;r1=0;r2=0;r3=0;
 r0.l=8192;
 r1.l=8192;
 r2.l=r0.l+r1.l;
 r3=r0*r1;
 r3=r0.l*r1.l;
 a0=r0.l*r1.l;
// 32-bit add and multiply.
r0=0;r1=0;r2=0;r3=0;
 r0.h=8192;
 r1.h=8192;
 r2=r0+r1;
 r3=r0*r1;
 a0=r0.h*r1.h;
// 16-bit add, multiply, increment and parallel move.
r0=0;r1=0;r2=0;r3=0;
p0=9;
 r0.l=8192;
 r1.l=b#101; // The #b indicates a bianry value.
 r1.l=0.125r; // The r suffix indicates fractional value.
 r1.l=bb1;
 r1=0;
 r1=bb1; // This is the same as r1.l=bb1;
 r1.h=bb1;
 r2.l=r0.l+r1.l;
 A0=r0.l*r1.l;
 A0+=r0.l*r1.l||r2 = [i0++]; // Parallel multiply and move.
// Now test multiplier instruction options
r0=0;r1=0;r2=0;r3=0;
r0=0x100;
r0=0.2r;
r1=0.3r;
r2=r0.l*r1.l; // This gives r2=0.06
r2=r0.l*r1.l(FU); // This gives r2=0.03
r0=100;r1=250;
r2=r0+r1; // This gives r2=15e
// Memory move operations.
r0=0;r1=0;r2=0;r3=0;
 p0=0x11800000;
 r0=0.34719r;
 [p0]=r0; // Load to memory
 r1=[p0]; // Retrieve data from memory
 [p0++]=r0; // This increments by 4, since it is a 32-bit word
// Now test loop structures.
 r0=0;
 loop lc0=10;
 r0+=1;
 loop_end;
// Now test condition code bit cc.
 a0=0;a1=0;
 r0=0.2r;
 r1=0.3r;
 cc=r0<r1; // If r0<r1, set cc to true, (i.e. 1)
 if cc jump lq1; // Jump to lq1 if cc=1
nop; // Jump instruction
lq1:
 r0=0.67r;
 cc=r1<r0; // If r0<r1, set cc to true, (i.e. 1)
 if cc jump lq2; // Jump to lq1 if cc=1
nop; // Jump instruction
lq2:
// Now test a bit set/clear/toggle operations.
 r0=0;
 bitset (r0,7);
 bitclr(r0,7);
 bittgl (r0, 24);
 bittgl (r0, 24);
 nop;
// Now test arithmetic shift operations.
 r0=0;r1=0;r2=0;
 r0.l=b#110000;
 r0.l=r0.l>>>3; // Arithmetic right shift
 r0.l=r0.l<<2; // Arithmetic left shift
 r2.l=b#10;
// Now place in r1.l contents of r0.l A-shifted by contents of r2.l.
 r1.l=ashift r0.l by r2.l;
 rts;
._main.end: