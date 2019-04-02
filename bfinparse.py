import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ply'))
import ply.yacc as yacc
from instructions import *


precedence = (
    ('left', 'BAR'),
    ('left', 'CARET'),
    ('left', 'AMPERSAND'),
    ('left', 'LESS_LESS', 'GREATER_GREATER'),
	('left', 'PLUS', 'MINUS'),
	('left', 'STAR', 'SLASH', 'PERCENT'),
	('right', 'ASSIGN'),
	('right', 'TILDA', 'BANG'),
 )

trans = []

def p_translation1(t):
	'''
	translation : statement
	'''
	t[0] = t[1]

def p_translation2(t):
	'''
	translation : translation statement
	'''
	t[0] = (t[1:2])


def p_statement(t):
	'''
	statement : asm
	'''
	t[0] = t[1]
	trans.append(t[1])


def p_asm(t):
	''' asm : asm_1 SEMICOLON

	| parallel_instructions SEMICOLON
	  
	| error
	
	'''
	t[0] = t[1]

# DSPMAC.

def p_asm_1(t):
	'''
	asm_1 : dspalu

	| dspmult

	| dspshift

	| jump

	| nop

	| idle

	| loadstore

	| other

	'''
	t[0] = t[1]

def p_parallel_instructions(t):
	'''
	parallel_instructions : asm_1 DOUBLE_BAR asm_1 DOUBLE_BAR asm_1

	| asm_1 DOUBLE_BAR asm_1

	'''
	t[0] = Parallel()


def p_vector_mac(t):
	'''
	vector_mac : assign_macfunc opt_mode COMMA assign_macfunc opt_mode

	| assign_macfunc opt_mode
	
	'''
	pass

def p_dspalu(t):
	'''
	dspalu : comp

	| loophardware

	| vector_mac

	| expadj

	| alu2

	| REG ASSIGN LPAREN a_plusassign REG_A RPAREN
	
	  
	| HALF_REG ASSIGN LPAREN a_plusassign REG_A RPAREN
	
	  
	| A_ZERO_DOT_H ASSIGN HALF_REG
	
	| A_ONE_DOT_H ASSIGN HALF_REG
	
	| LPAREN REG COMMA REG RPAREN ASSIGN BYTEOP16P LPAREN REG COLON expr COMMA REG COLON expr RPAREN aligndir
	
	

	| LPAREN REG COMMA REG RPAREN ASSIGN BYTEOP16M LPAREN REG COLON expr COMMA REG COLON expr RPAREN aligndir
	
	

	| LPAREN REG COMMA REG RPAREN ASSIGN BYTEUNPACK REG COLON expr aligndir
	
	
	| LPAREN REG COMMA REG RPAREN ASSIGN SEARCH REG LPAREN searchmod RPAREN
	
	  
	| REG ASSIGN A_ONE_DOT_L PLUS A_ONE_DOT_H COMMA REG ASSIGN A_ZERO_DOT_L PLUS A_ZERO_DOT_H
	
	  


	| REG ASSIGN REG_A PLUS REG_A COMMA REG ASSIGN REG_A MINUS REG_A amod1
	
	  

	| REG ASSIGN REG plus_minus REG COMMA REG ASSIGN REG plus_minus REG amod1 

	| REG ASSIGN REG op_bar_op REG COMMA REG ASSIGN REG op_bar_op REG amod2
	
	  

	| REG ASSIGN ABS REG vmod
	
	      
	  
	| a_assign ABS REG_A
	
	| A_ZERO_DOT_L ASSIGN HALF_REG
	
	  
	| A_ONE_DOT_L ASSIGN HALF_REG
	
	  

	| REG ASSIGN c_align LPAREN REG COMMA REG RPAREN
	
	  

 	| REG ASSIGN BYTEOP1P LPAREN REG COLON expr COMMA REG COLON expr RPAREN byteop_mod
	
	
 	| REG ASSIGN BYTEOP1P LPAREN REG COLON expr COMMA REG COLON expr RPAREN
	
	

	| REG ASSIGN BYTEOP2P LPAREN REG COLON expr COMMA REG COLON expr RPAREN rnd_op
	
	

	| REG ASSIGN BYTEOP3P LPAREN REG COLON expr COMMA REG COLON expr RPAREN b3_op
	
	

	| REG ASSIGN BYTEPACK LPAREN REG COMMA REG RPAREN
	
	  

	| HALF_REG ASSIGN HALF_REG ASSIGN SIGN LPAREN HALF_REG RPAREN STAR HALF_REG PLUS SIGN LPAREN HALF_REG RPAREN STAR HALF_REG
	
	  
	| REG ASSIGN REG plus_minus REG amod1
	
	      
	  
	| REG ASSIGN min_max LPAREN REG COMMA REG RPAREN vmod
	 
	  

	| a_assign MINUS REG_A
	
	| HALF_REG ASSIGN HALF_REG plus_minus HALF_REG amod1
	
	| a_assign a_assign expr 
	| a_assign REG_A LPAREN S RPAREN
	
	  

	| HALF_REG ASSIGN REG LPAREN RND RPAREN
	
	  

	| HALF_REG ASSIGN REG plus_minus REG LPAREN RND12 RPAREN
	
	  

	| HALF_REG ASSIGN REG plus_minus REG LPAREN RND20 RPAREN
	
	  

	| a_assign REG_A
	
	  

	| a_assign REG
	
	  

	| REG ASSIGN HALF_REG xpmod
	
	      
	  

	| HALF_REG ASSIGN expr
	

	| a_assign expr
	

	| REG ASSIGN expr xpmod1
	
		
			
	  

	| HALF_REG ASSIGN REG
	
	  

	| REG ASSIGN REG op_bar_op REG amod0
	
	  

	| REG ASSIGN BYTE_DREG xpmod
	
	  

	| a_assign ABS REG_A COMMA a_assign ABS REG_A
	
	  

	| a_assign MINUS REG_A COMMA a_assign MINUS REG_A
	
	  

	| a_minusassign REG_A w32_or_nothing
	
	  

	| REG _MINUS_ASSIGN expr
	
	  

	| REG _PLUS_ASSIGN REG LPAREN BREV RPAREN
	
	  

	| REG _MINUS_ASSIGN REG
	
	  

	| REG_A _PLUS_ASSIGN REG_A w32_or_nothing
	
	  

	| REG _PLUS_ASSIGN REG
	
	  

	| REG _PLUS_ASSIGN expr
	
	      
	  

 	| REG _STAR_ASSIGN REG
	
	  

	| SAA LPAREN REG COLON expr COMMA REG COLON expr RPAREN aligndir
	
	

	| a_assign REG_A LPAREN S RPAREN COMMA a_assign REG_A LPAREN S RPAREN
	
	  

	| REG ASSIGN LPAREN REG PLUS REG RPAREN LESS_LESS expr
	'''
	t[0] = Alu()

def p_comp(t):
	'''
	comp : REG ASSIGN REG BAR REG
	
	  
	| REG ASSIGN REG CARET REG
	
	  
	| REG ASSIGN REG PLUS LPAREN REG LESS_LESS expr RPAREN
	
	      
	  
	| CCREG ASSIGN REG_A _ASSIGN_ASSIGN REG_A
	
	  
	| CCREG ASSIGN REG_A LESS_THAN REG_A
	
	  
	| CCREG ASSIGN REG LESS_THAN REG iu_or_nothing
	
	  
	| CCREG ASSIGN REG LESS_THAN expr iu_or_nothing
	
	  
	| CCREG ASSIGN REG _ASSIGN_ASSIGN REG
	
	  
	| CCREG ASSIGN REG _ASSIGN_ASSIGN expr
	
	  
	| CCREG ASSIGN REG_A _LESS_THAN_ASSIGN REG_A
	
	  
	| CCREG ASSIGN REG _LESS_THAN_ASSIGN REG iu_or_nothing
	
	  
	| CCREG ASSIGN REG _LESS_THAN_ASSIGN expr iu_or_nothing
	
	  

	| REG ASSIGN REG AMPERSAND REG
	
	  

	| ccstat
	

	| REG ASSIGN REG
	
	  

	| CCREG ASSIGN REG
	
	  

	| REG ASSIGN CCREG
	
	  

	| CCREG _ASSIGN_BANG CCREG 
	'''
	pass

def p_dspmult(t):
	'''
	dspmult : HALF_REG ASSIGN multiply_halfregs opt_mode

  | REG ASSIGN multiply_regs opt_mode
  

	| REG ASSIGN multiply_halfregs opt_mode
	
	  

	| HALF_REG ASSIGN multiply_halfregs opt_mode COMMA HALF_REG ASSIGN multiply_halfregs opt_mode
	

	| REG ASSIGN multiply_halfregs opt_mode COMMA REG ASSIGN multiply_halfregs opt_mode
	

  | a_full_macfunc opt_mode
  

  | assign_full_macfunc opt_mode 

	'''
	t[0] = Mac()

#ben bitlogic done in shifter according to program reference
def p_dspshift(t):
	'''
	dspshift : a_assign ASHIFT REG_A BY HALF_REG
	
	  

	| HALF_REG ASSIGN ASHIFT HALF_REG BY HALF_REG smod
	
	  

	| a_assign REG_A LESS_LESS expr
	
	  

	| REG ASSIGN REG LESS_LESS expr vsmod
	
	      
	  
	  
	| HALF_REG ASSIGN HALF_REG LESS_LESS expr smod
	
	      
	  
	| REG ASSIGN ASHIFT REG BY HALF_REG vsmod

	| bitlogic

	| deposit
	'''
	t[0] = Shift()

def p_expadj(t):
	'''
	expadj : HALF_REG ASSIGN EXPADJ LPAREN REG COMMA HALF_REG RPAREN vmod

	| HALF_REG ASSIGN EXPADJ LPAREN HALF_REG COMMA HALF_REG RPAREN 
	'''
	pass

def p_deposit(t):
	'''
	deposit : REG ASSIGN DEPOSIT LPAREN REG COMMA REG RPAREN
	
	  

	| REG ASSIGN DEPOSIT LPAREN REG COMMA REG RPAREN LPAREN X RPAREN
	
	  

	| REG ASSIGN EXTRACT LPAREN REG COMMA HALF_REG RPAREN xpmod
	
	  

	| a_assign REG_A _GREATER_GREATER_GREATER expr
	
	  
	| a_assign LSHIFT REG_A BY HALF_REG
	
	  

	| HALF_REG ASSIGN LSHIFT HALF_REG BY HALF_REG
	
	  

	| REG ASSIGN LSHIFT REG BY HALF_REG vmod
	
	  

	| REG ASSIGN SHIFT REG BY HALF_REG
	
	  

	| a_assign REG_A GREATER_GREATER expr
	
	  

	| REG ASSIGN REG GREATER_GREATER expr vmod
	
	      
	  
	
	| HALF_REG ASSIGN HALF_REG GREATER_GREATER expr
	
	  
	| HALF_REG ASSIGN HALF_REG _GREATER_GREATER_GREATER expr smod
	
	  


	| REG ASSIGN REG _GREATER_GREATER_GREATER expr vsmod
	
	      
	  

	| HALF_REG ASSIGN ONES REG
	
	  

	| REG ASSIGN PACK LPAREN HALF_REG COMMA HALF_REG RPAREN
	
	  

	| HALF_REG ASSIGN CCREG ASSIGN BXORSHIFT LPAREN REG_A COMMA REG RPAREN
	
	  

	| HALF_REG ASSIGN CCREG ASSIGN BXOR LPAREN REG_A COMMA REG RPAREN
	
	  

	| HALF_REG ASSIGN CCREG ASSIGN BXOR LPAREN REG_A COMMA REG_A COMMA CCREG RPAREN
	
	  

	| a_assign ROT REG_A BY HALF_REG
	
	  

	| REG ASSIGN ROT REG BY HALF_REG
	
	  

	| a_assign ROT REG_A BY expr
	
	  

	| REG ASSIGN ROT REG BY expr
	
	  

	| HALF_REG ASSIGN SIGNBITS REG_A
	
	  

	| HALF_REG ASSIGN SIGNBITS REG
	
	  

	| HALF_REG ASSIGN SIGNBITS HALF_REG

	| HALF_REG ASSIGN VIT_MAX LPAREN REG RPAREN asr_asl
	
	  

	| REG ASSIGN VIT_MAX LPAREN REG COMMA REG RPAREN asr_asl
	
	  

	| BITMUX LPAREN REG COMMA REG COMMA REG_A RPAREN asr_asl

	| a_assign BXORSHIFT LPAREN REG_A COMMA REG_A COMMA CCREG RPAREN
	'''
	pass

def p_bitlogic(t):
	'''
	bitlogic :  CCREG _ASSIGN_BANG BITTST LPAREN REG COMMA expr RPAREN
	|BITCLR LPAREN REG COMMA expr RPAREN
	| BITSET LPAREN REG COMMA expr RPAREN
	| BITTGL LPAREN REG COMMA expr RPAREN
	| CCREG ASSIGN BITTST LPAREN REG COMMA expr RPAREN


	| IF BANG CCREG REG ASSIGN REG
	
	  

	| IF CCREG REG ASSIGN REG
	
	'''
	pass

def p_jump(t):
	'''
	jump : return
	  

	| IF BANG CCREG JUMP expr
	
	  

	| IF BANG CCREG JUMP expr LPAREN BP RPAREN
	
	  

	| IF CCREG JUMP expr
	
	  

	| IF CCREG JUMP expr LPAREN BP RPAREN


	| JUMP LPAREN REG RPAREN
	
	  

	| CALL LPAREN REG RPAREN
	
	  

	| CALL LPAREN PC PLUS REG RPAREN
	
	  

	| JUMP LPAREN PC PLUS REG RPAREN
	
	  

	| RAISE expr
	
	  

	| EXCPT expr
	

	| TESTSET LPAREN REG RPAREN
	
	  

	| JUMP expr
	
	  

	| JUMP_DOT_S expr
	
	  

	| JUMP_DOT_L expr
	
	  

	| JUMP_DOT_L pltpc
	
	  

	| CALL expr
	
	  
	| CALL pltpc 

	'''
	t[0] = Jump()

def p_return(t):
	'''
	return : RTS
	

	| RTI
	

	| RTX
	

	| RTN
	

	| RTE
	'''
	pass

def p_nop(t):
	'''
	nop : NOP

	| MNOP
	'''
	t[0] = Nop()

def p_idle(t):
	'''
	idle : IDLE
	'''
	t[0] = Idle()

def p_alu2(t):
	'''
	alu2 : DIVQ LPAREN REG COMMA REG RPAREN
	

	| DIVS LPAREN REG COMMA REG RPAREN
	

	| REG ASSIGN MINUS REG vsmod
	  

	| REG ASSIGN TILDA REG
	
	  

	| REG _GREATER_GREATER_ASSIGN REG
	
	  

	| REG _GREATER_GREATER_ASSIGN expr
	
	  

	| REG _GREATER_GREATER_GREATER_THAN_ASSIGN REG
	
	  

	| REG _LESS_LESS_ASSIGN REG
	
	  

	| REG _LESS_LESS_ASSIGN expr
	
	  


	| REG _GREATER_GREATER_GREATER_THAN_ASSIGN expr
	'''
	pass

def p_cache(t):
	'''
	cache : FLUSH LBRACK REG RBRACK
	

	| FLUSH reg_with_postinc
	
	  

	| FLUSHINV LBRACK REG RBRACK
	
	  

	| FLUSHINV reg_with_postinc

	| IFLUSH LBRACK REG RBRACK
	
	  

	| IFLUSH reg_with_postinc
	
	  

	| PREFETCH LBRACK REG RBRACK
	
	  

	| PREFETCH reg_with_postinc 
	'''
	pass

def p_loadstore(t):
	'''
	loadstore : pushpopmultiple

	| B LBRACK REG post_op RBRACK ASSIGN REG
 
	| B LBRACK REG plus_minus expr RBRACK ASSIGN REG
	 
	| W LBRACK REG plus_minus expr RBRACK ASSIGN REG
	
	| W LBRACK REG post_op RBRACK ASSIGN REG
	

	| W LBRACK REG post_op RBRACK ASSIGN HALF_REG
	
	| LBRACK REG plus_minus expr RBRACK ASSIGN REG

	| REG ASSIGN W LBRACK REG plus_minus expr RBRACK xpmod
	
	  

	| HALF_REG ASSIGN W LBRACK REG post_op RBRACK
	
	  


	| REG ASSIGN W LBRACK REG post_op RBRACK xpmod
	

	| REG ASSIGN W LBRACK REG _PLUS_PLUS REG RBRACK xpmod
	

	| HALF_REG ASSIGN W LBRACK REG _PLUS_PLUS REG RBRACK
	

	| LBRACK REG post_op RBRACK ASSIGN REG
	
	  

	| LBRACK REG _PLUS_PLUS REG RBRACK ASSIGN REG
	
	  

	| W LBRACK REG _PLUS_PLUS REG RBRACK ASSIGN HALF_REG
	
	  

	| REG ASSIGN B LBRACK REG plus_minus expr RBRACK xpmod
	
	  

	| REG ASSIGN B LBRACK REG post_op RBRACK xpmod
	

	| REG ASSIGN LBRACK REG _PLUS_PLUS REG RBRACK
	
	  

	| REG ASSIGN LBRACK REG plus_minus got_or_expr RBRACK
	
	  

	| REG ASSIGN LBRACK REG post_op RBRACK 
	'''
	t[0] = Move()

def p_pushpopmultiple(t):
	'''
	pushpopmultiple : reg_with_predec ASSIGN LPAREN REG COLON expr COMMA REG COLON expr RPAREN
	
	  

	| reg_with_predec ASSIGN LPAREN REG COLON expr RPAREN
	
	  

	| LPAREN REG COLON expr COMMA REG COLON expr RPAREN ASSIGN reg_with_postinc
	
	  

	| LPAREN REG COLON expr RPAREN ASSIGN reg_with_postinc
	
	  

	| reg_with_predec ASSIGN REG  
	'''
	pass

def p_linkage(t):
	'''
	linkage : LINK expr
	
	| UNLINK 
	'''
	pass

#ben added hw loop syntax loop lc0=bla
#ben added loop_end w/out expr
def p_loophardware(t):
	'''
	loophardware : LSETUP LPAREN expr COMMA expr RPAREN REG
	
	  
	| LSETUP LPAREN expr COMMA expr RPAREN REG ASSIGN REG
	
	  

	| LSETUP LPAREN expr COMMA expr RPAREN REG ASSIGN REG GREATER_GREATER expr 
	| LOOP expr REG
	
	| LOOP expr REG ASSIGN REG
	
	  
	| LOOP expr REG ASSIGN REG GREATER_GREATER expr  
	| LOOP_BEGIN NUMBER
	
	| LOOP_BEGIN expr  
	| LOOP_END NUMBER
	
	| LOOP_END expr

	| LOOP REG ASSIGN NUMBER

	| LOOP_END
	'''
	pass

def p_other(t):
	'''
	other : ABORT

	| linkage

	| cache

	| CSYNC
	

	| SSYNC
	

	| EMUEXCPT
	

	| CLI REG
	
	  

	| STI REG

	| DISALGNEXCPT
	
	| DBG
	
	| DBG REG_A
	
	| DBG REG
	

	| DBGCMPLX LPAREN REG RPAREN
	

	| DBGHALT
	

	| HLT
	

	| DBGA LPAREN HALF_REG COMMA expr RPAREN
	

	| DBGAH LPAREN REG COMMA expr RPAREN
	

	| DBGAL LPAREN REG COMMA expr RPAREN
	

	| OUTC expr
	

	| OUTC REG
	'''
	t[0] = Other()

#  AUX RULES.  

#  Register rules.  

def p_REG_A(t):
	'''	REG_A : REG_A_DOUBLE_ZERO
	
	| REG_A_DOUBLE_ONE
	
	'''
	pass


#  Modifiers. 

def p_opt_mode(t):
	'''
	
	opt_mode : empty

	| LPAREN M COMMA MMOD RPAREN
	
	| LPAREN MMOD COMMA M RPAREN
	
	| LPAREN MMOD RPAREN
	
	| LPAREN M RPAREN
	
	'''
	pass

def p_asr_asl(t):
	''' asr_asl : LPAREN ASL RPAREN
	
	| LPAREN ASR RPAREN
	
	'''
	pass

def p_sco(t):
	'''
	
	sco : empty

	| S
	
	| CO
	
	| SCO
	
	'''
	pass

def p_asr_asl_0(t):
	'''
	asr_asl_0 : ASL
	
	| ASR
	
	'''
	pass

def p_amod0(t):
	'''
	
	amod0 : empty

	| LPAREN sco RPAREN
	
	'''
	pass

def p_amod1(t):
	'''
	
	amod1 : empty

	| LPAREN NS RPAREN
	
	| LPAREN S RPAREN
	
	'''
	pass

def p_amod2(t):
	'''
	
	amod2 : empty

	| LPAREN asr_asl_0 RPAREN
	
	| LPAREN sco RPAREN
	
	| LPAREN asr_asl_0 COMMA sco RPAREN
	
	| LPAREN sco COMMA asr_asl_0 RPAREN
	
	'''
	pass

def p_xpmod(t):
	'''
	
	xpmod : empty

	| LPAREN Z RPAREN
	
	| LPAREN X RPAREN
	
	'''
	pass

def p_xpmod1(t):
	'''
	
	xpmod1 : empty

	| LPAREN X RPAREN
	
	| LPAREN Z RPAREN
	
	'''
	pass

def p_vsmod(t):
	'''
	
	vsmod : empty 

	| LPAREN NS RPAREN
	
	| LPAREN S RPAREN
	
	| LPAREN V RPAREN
	
	| LPAREN V COMMA S RPAREN
	
	| LPAREN S COMMA V RPAREN
	
	'''
	pass

def p_vmod(t):
	'''
	
	vmod : empty 
	|  LPAREN V RPAREN
	
	'''
	pass

def p_smod(t):
	'''
	
	smod : empty 
	|  LPAREN S RPAREN
	
	'''
	pass

def p_searchmod(t):
	'''
	searchmod : GE
	
	| GT
	
	| LE
	
	| LT
	
	'''
	pass

def p_aligndir(t):
	'''
	
	aligndir : empty 
	|  LPAREN R RPAREN
	
	'''
	pass

def p_byteop_mod(t):
	'''
	byteop_mod : LPAREN R RPAREN
	
	| LPAREN MMOD RPAREN
	
	| LPAREN MMOD COMMA R RPAREN
	
	| LPAREN R COMMA MMOD RPAREN
	
	'''
	pass



def p_c_align(t):
	'''
	c_align : ALIGN8
	
	| ALIGN16
	
	| ALIGN24
	
	'''
	pass

def p_w32_or_nothing(t):
	'''
	
	w32_or_nothing : empty 
	| LPAREN MMOD RPAREN
	
	'''
	pass

def p_iu_or_nothing(t):
	'''
	
	iu_or_nothing : empty 
	| LPAREN MMOD RPAREN
	
	'''
	pass

def p_reg_with_predec(t):
	''' reg_with_predec : LBRACK _MINUS_MINUS REG RBRACK
	
	'''
	pass

def p_reg_with_postinc(t):
	''' reg_with_postinc : LBRACK REG _PLUS_PLUS RBRACK
	
	'''
	pass

# Operators.  

def p_min_max(t):
	'''
	min_max : MIN
	
	| MAX
	
	'''
	pass

def p_op_bar_op(t):
	'''
	op_bar_op : _PLUS_BAR_PLUS
	
	| _PLUS_BAR_MINUS
	
	| _MINUS_BAR_PLUS
	
	| _MINUS_BAR_MINUS
	
	'''
	pass

def p_plus_minus(t):
	'''
	plus_minus : PLUS
	
	| MINUS
	
	'''
	pass

def p_rnd_op(t):
	'''
	rnd_op : LPAREN RNDH RPAREN
	

	| LPAREN TH RPAREN
	

	| LPAREN RNDL RPAREN
	

	| LPAREN TL RPAREN
	

	| LPAREN RNDH COMMA R RPAREN
	
	| LPAREN TH COMMA R RPAREN
	
	| LPAREN RNDL COMMA R RPAREN
	

	| LPAREN TL COMMA R RPAREN
	
	'''
	pass

def p_b3_op(t):
	'''
	b3_op : LPAREN LO RPAREN
	
	| LPAREN HI RPAREN
	
	| LPAREN LO COMMA R RPAREN
	
	| LPAREN HI COMMA R RPAREN
	
	'''
	pass

def p_post_op(t):
	'''
	
	post_op : empty 
	|  _PLUS_PLUS
	
	| _MINUS_MINUS
	
	'''
	pass

# Assignments, Macfuncs.  

def p_a_assign(t):
	'''
	a_assign : REG_A ASSIGN
	
	'''
	pass

def p_a_minusassign(t):
	'''
	a_minusassign : REG_A _MINUS_ASSIGN
	
	'''
	pass

def p_a_plusassign(t):
	'''
	a_plusassign : REG_A _PLUS_ASSIGN
	
	'''
	pass

def p_assign_macfunc(t):
	'''
	assign_macfunc : REG ASSIGN REG_A
	
	| a_macfunc
	
	| REG ASSIGN LPAREN a_macfunc RPAREN
	

	| HALF_REG ASSIGN LPAREN a_macfunc RPAREN
	

	| HALF_REG ASSIGN REG_A
	
	'''
	pass

def p_assign_full_macfunc(t):
	'''
  assign_full_macfunc : REG ASSIGN LPAREN A_ONE_COLON_ZERO RPAREN
  

  | LPAREN REG COLON REG RPAREN ASSIGN LPAREN A_ONE_COLON_ZERO RPAREN
  

  | LPAREN REG COLON REG RPAREN ASSIGN multiply_regs
  

  | REG ASSIGN LPAREN a_full_macfunc RPAREN
  

  | LPAREN REG COLON REG RPAREN ASSIGN LPAREN a_full_macfunc RPAREN
  
  '''
	pass

def p_a_macfunc(t):
	'''
	a_macfunc : a_assign multiply_halfregs
	
	| a_plusassign multiply_halfregs
	
	| a_minusassign multiply_halfregs
	
	'''
	pass

def p_a_full_macfunc(t):
	'''
  a_full_macfunc : LPAREN A_ONE_COLON_ZERO RPAREN ASSIGN multiply_regs
  
  | LPAREN A_ONE_COLON_ZERO RPAREN _PLUS_ASSIGN multiply_regs
  
  | LPAREN A_ONE_COLON_ZERO RPAREN _MINUS_ASSIGN multiply_regs
  
  '''
	pass

def p_multiply_regs(t):
	'''
  multiply_regs : REG STAR REG
  
    
  '''
	pass



def p_multiply_halfregs(t):
	'''
	multiply_halfregs : HALF_REG STAR HALF_REG
	
	  
	'''
	pass

def p_cc_op(t):
	'''
	cc_op : ASSIGN
	
	| _BAR_ASSIGN
	
	| _AMPERSAND_ASSIGN
	
	| _CARET_ASSIGN
	
	'''
	pass

def p_ccstat(t):
	'''
	ccstat : CCREG cc_op STATUS_REG
	
	| CCREG cc_op V
	
	| STATUS_REG cc_op CCREG
	
	| V cc_op CCREG
	
	'''
	pass

# Expressions and Symbols.  

def p_symbol(t):
	''' symbol : SYMBOL
	
	'''
	pass

def p_any_gotrel(t):
	'''
	any_gotrel : GOT
	
	| GOT17M4
	
	| FUNCDESC_GOT17M4
	
	'''
	pass

def p_got(t):
	'''	got : symbol AT any_gotrel
	
	'''
	pass

def p_got_or_expr(t):
	'''	got_or_expr : got
	
	| expr
	
	'''
	pass

def p_pltpc (t):
	'''
	pltpc : symbol AT PLTPC
	
	'''
	pass

def p_eterm(t):
	''' eterm : NUMBER
	
	| symbol
	
	| LPAREN expr_1 RPAREN
	
	| TILDA expr_1
	
	| MINUS expr_1 %prec TILDA
	
	'''
	pass

def p_expr(t):
	''' expr : expr_1
	
	'''
	pass

def p_expr_1(t):
	''' expr_1 : expr_1 STAR expr_1
	
	| expr_1 SLASH expr_1
	
	| expr_1 PERCENT expr_1
	
	| expr_1 PLUS expr_1
	
	| expr_1 MINUS expr_1
	
	| expr_1 LESS_LESS expr_1
	
	| expr_1 GREATER_GREATER expr_1
	
	| expr_1 AMPERSAND expr_1
	
	| expr_1 CARET expr_1
	
	| expr_1 BAR expr_1
	
	| eterm
	
	'''
	pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

    # Read ahead looking for a closing ';'
    while True:
        tok = parser.token()             # Get the next token
        if not tok:
        	break 
        elif tok.type == 'SEMICOLON':
        	parser.restart()
    		return tok
    

def p_empty(p):
     'empty :'
     pass

from bfinlex import *

import preprocessor
pcpp = preprocessor.Preprocessor()

import cStringIO
io = cStringIO.StringIO()

with open(sys.argv[1]) as f:
	data = f.read()

pcpp.line_directive = None
pcpp.compress = 2
pcpp.parse(data)
pcpp.write(io)

data = io.getvalue()

print(data)

# Give the lexer some input
lexer.input(data)

#Tokenize
# while True:
# 	tok = lexer.token()
#  	if not tok: 
# 		break      # No more input
# 	print(tok)

import profile

parser = yacc.yacc()

parser.parse(data, lexer=lexer, debug=True)

# while True:
#     try:
#         s = data
#     except EOFError:
#         break
#     if not s: continue
#     result = parser.parse(s)
#     print(result)

for instr in instructions:
	print(instr)
	print(instr.counter)