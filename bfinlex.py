import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import ply.lex as lex

# Tokens.  
tokens = (
#comment
'COMMENT1', 'COMMENT2',
# Vector Specific.  
'BYTEOP16P', 'BYTEOP16M',
'BYTEOP1P', 'BYTEOP2P', 'BYTEOP3P',
'BYTEUNPACK', 'BYTEPACK',
'PACK',
'SAA',
'ALIGN8', 'ALIGN16', 'ALIGN24',
'VIT_MAX',
'EXTRACT', 'DEPOSIT', 'EXPADJ', 'SEARCH',
'ONES', 'SIGN', 'SIGNBITS',

#'', 'Stack',.'', '', '',
'LINK', 'UNLINK',

# Registers.  
'REG',
'PC',
'CCREG', 'BYTE_DREG',
'A_ONE_COLON_ZERO',
'REG_A_DOUBLE_ZERO', 'REG_A_DOUBLE_ONE',
'A_ZERO_DOT_L', 'A_ZERO_DOT_H', 'A_ONE_DOT_L', 'A_ONE_DOT_H',
'HALF_REG',

# Progctrl.  
'NOP',
'RTI', 'RTS', 'RTX', 'RTN', 'RTE',
'HLT', 'IDLE',
'STI', 'CLI',
'CSYNC', 'SSYNC',
'EMUEXCPT',
'RAISE', 'EXCPT',
'LSETUP',
'LOOP',
'LOOP_BEGIN',
'LOOP_END',
'DISALGNEXCPT',
'JUMP', 'JUMP_DOT_S', 'JUMP_DOT_L',
'CALL',

#'', 'Emulator', 'only',.'', '', '',
'ABORT',

# Operators.  
'NOT', 'TILDA', 'BANG',
'AMPERSAND', 'BAR',
'PERCENT',
'CARET',
'BXOR',

'MINUS', 'PLUS', 'STAR', 'SLASH',
'NEG',
'MIN', 'MAX', 'ABS',
'DOUBLE_BAR',
'_PLUS_BAR_PLUS', '_PLUS_BAR_MINUS', '_MINUS_BAR_PLUS', '_MINUS_BAR_MINUS',
'_MINUS_MINUS', '_PLUS_PLUS',

#'', 'Shift',/'rotate', 'ops',.'', '', '',
'SHIFT', 'LSHIFT', 'ASHIFT', 'BXORSHIFT',
'_GREATER_GREATER_GREATER_THAN_ASSIGN',
'ROT',
'LESS_LESS', 'GREATER_GREATER',
'_GREATER_GREATER_GREATER',
'_LESS_LESS_ASSIGN', '_GREATER_GREATER_ASSIGN',
'DIVS', 'DIVQ',

#'', 'In', 'place', 'operators',.'', '', '',
'ASSIGN', '_STAR_ASSIGN',
'_BAR_ASSIGN', '_CARET_ASSIGN', '_AMPERSAND_ASSIGN',
'_MINUS_ASSIGN', '_PLUS_ASSIGN',

#'', 'Assignments',,'', 'comparisons',.'', '', '',
'_ASSIGN_BANG', '_LESS_THAN_ASSIGN', '_ASSIGN_ASSIGN',
'GE', 'LT', 'LE', 'GT',
'LESS_THAN',

#'', 'Cache',.'', '', '',
'FLUSHINV', 'FLUSH',
'IFLUSH', 'PREFETCH',

#'', 'Misc',.'', '', '',
'PRNT',
'OUTC',
'WHATREG',
'TESTSET',

#'', 'Modifiers',.'', '', '',
'ASL', 'ASR',
'B', 'W',
'NS', 'S', 'CO', 'SCO',
'TH', 'TL',
'BP',
'BREV',
'X', 'Z',
'M', 'MMOD',
'R', 'RND', 'RNDL', 'RNDH', 'RND12', 'RND20',
'V',
'LO', 'HI',

#'', 'Bit', 'ops',.'', '', '',
'BITTGL', 'BITCLR', 'BITSET', 'BITTST', 'BITMUX',

#'', 'Debug',.'', '', '',
'DBGAL', 'DBGAH', 'DBGHALT', 'DBG', 'DBGA', 'DBGCMPLX',

#'', 'Semantic', 'auxiliaries',.'', '', '',

'IF', 'COMMA', 'BY',
'COLON', 'SEMICOLON',
'RPAREN', 'LPAREN', 'LBRACK', 'RBRACK',
'STATUS_REG',
'MNOP',

'LABEL',

'SYMBOL', 'NUMBER',
'GOT', 'GOT17M4', 'FUNCDESC_GOT17M4',
'AT', 'PLTPC',
)

# Comment
def t_COMMENT1(t):
    r'(/\*(.|\n)*?\*/)'
    ncr = t.value.count("\n")
    t.lexer.lineno += ncr
    return t

# Line comment
def t_COMMENT2(t):
    r'(//[^\n]*)'
    return t

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#HALF_REG #BEN MUST GO BEFORE FULLREG SO .L GETS LEXED
HALF_REG = r'[sS][pP]\.[lL]'
HALF_REG += r'|' + r'[sS][pP]\.[hH]'
HALF_REG += r'|' + r'[rR][0-7]\.[lLhHbB]'
HALF_REG += r'|' + r'[pP][0-5]\.[lLhH]'
HALF_REG += r'|' + r'[mM][0-3]\.[lLhH]'
HALF_REG += r'|' + r'[lL][0-3]\.[lLhH]'
HALF_REG += r'|' + r'[iI][0-3]\.[lLhH]'
HALF_REG += r'|' + r'[fF][pP]\.[lL]'
HALF_REG += r'|' + r'[fF][pP]\.[hH]'
HALF_REG += r'|' + r'[bB][0-3]\.[lLhH]'

@lex.TOKEN(HALF_REG)
def t_HALF_REG(t):
	return t


REG = r'[sS][fF][tT][rR][eE][sS][eE][tT]'

REG += r'|' + r'[oO][mM][oO][dD][eE]'
REG += r'|' + r'[iI][dD][lL][eE]_[rR][eE][qQ]'
REG += r'|' + r'[hH][wW][eE][rR][rR][cC][aA][uU][sS][eE]'
REG += r'|' + r'[eE][xX][cC][aA][uU][sS][eE]'
REG += r'|' + r'[eE][mM][uU][cC][aA][uU][sS][eE]'

REG += r'|' + r'[uU][sS][pP]'

REG += r'|' + r'[sS][yY][sS][cC][fF][gG]'

REG += r'|' + r'[sS][pP]'

REG += r'|' + r'[sS][eE][qQ][sS][tT][aA][tT]'

REG += r'|' + r'[rR][eE][tT][sS]'
REG += r'|' + r'[rR][eE][tT][iI]'
REG += r'|' + r'[rR][eE][tT][xX]'
REG += r'|' + r'[rR][eE][tT][nN]'
REG += r'|' + r'[rR][eE][tT][eE]'
REG += r'|' + r'[eE][mM][uU][dD][aA][tT]'

REG += r'|' + r'[rR][0-7]'

REG += r'|' + r'[pP][0-5]'

REG += r'|' + r'[mM][0-3]'

REG += r'|' + r'[lL][cC]0'
REG += r'|' + r'[lL][tT]0'
REG += r'|' + r'[lL][bB]0'
REG += r'|' + r'[lL][cC]1'
REG += r'|' + r'[lL][tT]1'
REG += r'|' + r'[lL][bB]1'

REG += r'|' + r'[lL][0-3]'

REG += r'|' + r'[iI][0-3]'

REG += r'|' + r'[fF][pP]'

REG += r'|' + r'[bB][0-3]'

REG += r'|' + r'[aA][sS][tT][aA][tT]'

REG += r'|' + r'[aA]1\.[xX]'
REG += r'|' + r'[aA]1\.[wW]'

REG += r'|' + r'[aA]0\.[xX]'
REG += r'|' + r'[aA]0\.[wW]'

REG += r'|' + r'[cC][yY][cC][lL][eE][sS]2'
REG += r'|' + r'[cC][yY][cC][lL][eE][sS]'

@lex.TOKEN(REG)
def t_REG(t):
	return t

#MMOD
MMOD = r'[wW]32'
MMOD += r'|' + r'[tT][fF][uU]'
MMOD += r'|' + r'[tT]'
MMOD += r'|' + r'[sS]2[rR][nN][dD]'
MMOD += r'|' + r'[iI][uU]'
MMOD += r'|' + r'[iI][sS][sS]2'
MMOD += r'|' + r'[iI][sS]'
MMOD += r'|' + r'[iI][hH]'
MMOD += r'|' + r'[fF][uU]'

@lex.TOKEN(MMOD)
def t_MMOD(t):
	return t

#STATUS
STATUS_REG = r'[aA][zZ]'
STATUS_REG += r'|' + r'[aA][nN]'
STATUS_REG += r'|' + r'[aA][cC]0_[cC][oO][pP][yY]'
STATUS_REG += r'|' + r'[vV]_[cC][oO][pP][yY]'
STATUS_REG += r'|' + r'[aA][qQ]'
STATUS_REG += r'|' + r'[aA][cC]0'
STATUS_REG += r'|' + r'[aA][cC]1'
STATUS_REG += r'|' + r'[aA][vV]0'
STATUS_REG += r'|' + r'[aA][vV]0[sS]'
STATUS_REG += r'|' + r'[aA][vV]1'
STATUS_REG += r'|' + r'[aA][vV]1[sS]'
STATUS_REG += r'|' + r'[vV][sS]'
STATUS_REG += r'|' + r'[rR][nN][dD]_[mM][oO][dD]'

@lex.TOKEN(STATUS_REG)
def t_STATUS_REG(t):
	return t

#CALL
CALL = r'[cC][aA][lL][lL]\.[xX]'
CALL += r'|' + r'[cC][aA][lL][lL]'

@lex.TOKEN(CALL)
def t_CALL(t):
	return t

#JUMP DOT L
JUMP_DOT_L = r'[jJ][uU][mM][pP]\.[lL]'
JUMP_DOT_L += r'|' + r'[jJ][uU][mM][pP]\.[xX]'

@lex.TOKEN(JUMP_DOT_L)
def t_JUMP_DOT_L(t):
	return t

#


Z = r'[zZ]'
@lex.TOKEN(Z)
def t_Z(t):
	return t

X = r'[xX]'
@lex.TOKEN(X)
def t_X(t):
	return t


W = r'[wW]'
@lex.TOKEN(W)
def t_W(t):
	return t

VIT_MAX = r'[vV][iI][tT]_[mM][aA][xX]'
@lex.TOKEN(VIT_MAX)
def t_VIT_MAX(t):
	return t

V = r'[vV]'
@lex.TOKEN(V)
def t_V(t):
	return t


TL = r'[tT][lL]'
@lex.TOKEN(TL)
def t_TL(t):
	return t

TH = r'[tT][hH]'
@lex.TOKEN(TH)
def t_TH(t):
	return t



TESTSET = r'[tT][eE][sS][tT][sS][eE][tT]'
@lex.TOKEN(TESTSET)
def t_TESTSET(t):
	return t



S = r'[sS]'
@lex.TOKEN(S)
def t_S(t):
	return t


STI = r'[sS][tT][iI]'
@lex.TOKEN(STI)
def t_STI(t):
	return t

SSYNC = r'[sS][sS][yY][nN][cC]'
@lex.TOKEN(SSYNC)
def t_SSYNC(t):
	return t



SIGNBITS = r'[sS][iI][gG][nN][bB][iI][tT][sS]'
@lex.TOKEN(SIGNBITS)
def t_SIGNBITS(t):
	return t

SIGN = r'[sS][iI][gG][nN]'
@lex.TOKEN(SIGN)
def t_SIGN(t):
	return t


SEARCH = r'[sS][eE][aA][rR][cC][hH]'
@lex.TOKEN(SEARCH)
def t_SEARCH(t):
	return t

SHIFT = r'[sS][hH][iI][fF][tT]'
@lex.TOKEN(SHIFT)
def t_SHIFT(t):
	return t

SCO = r'[sS][cC][oO]'
@lex.TOKEN(SCO)
def t_SCO(t):
	return t


SAA = r'[sS][aA][aA]'
@lex.TOKEN(SAA)
def t_SAA(t):
	return t



RTX = r'[rR][tT][xX]'
@lex.TOKEN(RTX)
def t_RTX(t):
	return t

RTS = r'[rR][tT][sS]'
@lex.TOKEN(RTS)
def t_RTS(t):
	return t

RTN = r'[rR][tT][nN]'
@lex.TOKEN(RTN)
def t_RTN(t):
	return t

RTI = r'[rR][tT][iI]'
@lex.TOKEN(RTI)
def t_RTI(t):
	return t

RTE = r'[rR][tT][eE]'
@lex.TOKEN(RTE)
def t_RTE(t):
	return t

ROT = r'[rR][oO][tT]'
@lex.TOKEN(ROT)
def t_ROT(t):
	return t

RND20 = r'[rR][nN][dD]20'
@lex.TOKEN(RND20)
def t_RND20(t):
	return t

RND12 = r'[rR][nN][dD]12'
@lex.TOKEN(RND12)
def t_RND12(t):
	return t

RNDL = r'[rR][nN][dD][lL]'
@lex.TOKEN(RNDL)
def t_RNDL(t):
	return t

RNDH = r'[rR][nN][dD][hH]'
@lex.TOKEN(RNDH)
def t_RNDH(t):
	return t

RND = r'[rR][nN][dD]'
@lex.TOKEN(RND)
def t_RND(t):
	return t





RAISE = r'[rR][aA][iI][sS][eE]'
@lex.TOKEN(RAISE)
def t_RAISE(t):
	return t




R = r'[rR]'
@lex.TOKEN(R)
def t_R(t):
	return t

PRNT = r'[pP][rR][nN][tT]'
@lex.TOKEN(PRNT)
def t_PRNT(t):
	return t

PC = r'[pP][cC]'
@lex.TOKEN(PC)
def t_PC(t):
	return t

PACK = r'[pP][aA][cC][kK]'
@lex.TOKEN(PACK)
def t_PACK(t):
	return t



OUTC = r'[oO][uU][tT][cC]'
@lex.TOKEN(OUTC)
def t_OUTC(t):
	return t

ONES = r'[oO][nN][eE][sS]'
@lex.TOKEN(ONES)
def t_ONES(t):
	return t


NOT = r'[nN][oO][tT]'
@lex.TOKEN(NOT)
def t_NOT(t):
	return t

NOP = r'[nN][oO][pP]'
@lex.TOKEN(NOP)
def t_NOP(t):
	return t

MNOP = r'[mM][nN][oO][pP]'
@lex.TOKEN(MNOP)
def t_MNOP(t):
	return t

NS = r'[nN][sS]'
@lex.TOKEN(NS)
def t_NS(t):
	return t



MIN = r'[mM][iI][nN]'
@lex.TOKEN(MIN)
def t_MIN(t):
	return t

MAX = r'[mM][aA][xX]'
@lex.TOKEN(MAX)
def t_MAX(t):
	return t



M = r'[mM]'
@lex.TOKEN(M)
def t_M(t):
	return t


LT = r'[lL][tT]'
@lex.TOKEN(LT)
def t_LT(t):
	return t

LSHIFT = r'[lL][sS][hH][iI][fF][tT]'
@lex.TOKEN(LSHIFT)
def t_LSHIFT(t):
	return t

LSETUP = r'[lL][sS][eE][tT][uU][pP]'
@lex.TOKEN(LSETUP)
def t_LSETUP(t):
	return t

#ben moved loop down

LOOP_BEGIN = r'[lL][oO][oO][pP]_[bB][eE][gG][iI][nN]'
@lex.TOKEN(LOOP_BEGIN)
def t_LOOP_BEGIN(t):
	return t

LOOP_END = r'[lL][oO][oO][pP]_[eE][nN][dD]'
@lex.TOKEN(LOOP_END)
def t_LOOP_END(t):
	return t

LOOP = r'[lL][oO][oO][pP]'
@lex.TOKEN(LOOP)
def t_LOOP(t):
	return t


LE = r'[lL][eE]'
@lex.TOKEN(LE)
def t_LE(t):
	return t




LO = r'[lL][oO]'
@lex.TOKEN(LO)
def t_LO(t):
	return t

JUMP_DOT_S = r'[jJ][uU][mM][pP]\.[sS]'
@lex.TOKEN(JUMP_DOT_S)
def t_JUMP_DOT_S(t):
	return t


JUMP = r'[jJ][uU][mM][pP]'
@lex.TOKEN(JUMP)
def t_JUMP(t):
	return t



IF = r'[iI][fF]'
@lex.TOKEN(IF)
def t_IF(t):
	return t




HLT = r'[hH][lL][tT]'
@lex.TOKEN(HLT)
def t_HLT(t):
	return t

HI = r'[hH][iI]'
@lex.TOKEN(HI)
def t_HI(t):
	return t

GT = r'[gG][tT]'
@lex.TOKEN(GT)
def t_GT(t):
	return t

GE = r'[gG][eE]'
@lex.TOKEN(GE)
def t_GE(t):
	return t




EXTRACT = r'[eE][xX][tT][rR][aA][cC][tT]'
@lex.TOKEN(EXTRACT)
def t_EXTRACT(t):
	return t

EXPADJ = r'[eE][xX][pP][aA][dD][jJ]'
@lex.TOKEN(EXPADJ)
def t_EXPADJ(t):
	return t

EXCPT = r'[eE][xX][cC][pP][tT]'
@lex.TOKEN(EXCPT)
def t_EXCPT(t):
	return t

EMUEXCPT = r'[eE][mM][uU][eE][xX][cC][pP][tT]'
@lex.TOKEN(EMUEXCPT)
def t_EMUEXCPT(t):
	return t

DIVS = r'[dD][iI][vV][sS]'
@lex.TOKEN(DIVS)
def t_DIVS(t):
	return t

DIVQ = r'[dD][iI][vV][qQ]'
@lex.TOKEN(DIVQ)
def t_DIVQ(t):
	return t

DISALGNEXCPT = r'[dD][iI][sS][aA][lL][gG][nN][eE][xX][cC][pP][tT]'
@lex.TOKEN(DISALGNEXCPT)
def t_DISALGNEXCPT(t):
	return t

DEPOSIT = r'[dD][eE][pP][oO][sS][iI][tT]'
@lex.TOKEN(DEPOSIT)
def t_DEPOSIT(t):
	return t

DBGHALT = r'[dD][bB][gG][hH][aA][lL][tT]'
@lex.TOKEN(DBGHALT)
def t_DBGHALT(t):
	return t

DBGCMPLX = r'[dD][bB][gG][cC][mM][pP][lL][xX]'
@lex.TOKEN(DBGCMPLX)
def t_DBGCMPLX(t):
	return t

DBGAL = r'[dD][bB][gG][aA][lL]'
@lex.TOKEN(DBGAL)
def t_DBGAL(t):
	return t

DBGAH = r'[dD][bB][gG][aA][hH]'
@lex.TOKEN(DBGAH)
def t_DBGAH(t):
	return t

DBGA = r'[dD][bB][gG][aA]'
@lex.TOKEN(DBGA)
def t_DBGA(t):
	return t

DBG = r'[dD][bB][gG]'
@lex.TOKEN(DBG)
def t_DBG(t):
	return t


CSYNC = r'[cC][sS][yY][nN][cC]'
@lex.TOKEN(CSYNC)
def t_CSYNC(t):
	return t

CO = r'[cC][oO]'
@lex.TOKEN(CO)
def t_CO(t):
	return t

CLI = r'[cC][lL][iI]'
@lex.TOKEN(CLI)
def t_CLI(t):
	return t


CCREG = r'[cC][cC]'
@lex.TOKEN(CCREG)
def t_CCREG(t):
	return t


BYTEUNPACK = r'[bB][yY][tT][eE][uU][nN][pP][aA][cC][kK]'
@lex.TOKEN(BYTEUNPACK)
def t_BYTEUNPACK(t):
	return t

BYTEPACK = r'[bB][yY][tT][eE][pP][aA][cC][kK]'
@lex.TOKEN(BYTEPACK)
def t_BYTEPACK(t):
	return t

BYTEOP16M = r'[bB][yY][tT][eE][oO][pP]16[mM]'
@lex.TOKEN(BYTEOP16M)
def t_BYTEOP16M(t):
	return t

BYTEOP16P = r'[bB][yY][tT][eE][oO][pP]16[pP]'
@lex.TOKEN(BYTEOP16P)
def t_BYTEOP16P(t):
	return t

BYTEOP3P = r'[bB][yY][tT][eE][oO][pP]3[pP]'
@lex.TOKEN(BYTEOP3P)
def t_BYTEOP3P(t):
	return t

BYTEOP2P = r'[bB][yY][tT][eE][oO][pP]2[pP]'
@lex.TOKEN(BYTEOP2P)
def t_BYTEOP2P(t):
	return t

BYTEOP1P = r'[bB][yY][tT][eE][oO][pP]1[pP]'
@lex.TOKEN(BYTEOP1P)
def t_BYTEOP1P(t):
	return t

BY = r'[bB][yY]'
@lex.TOKEN(BY)
def t_BY(t):
	return t

BXORSHIFT = r'[bB][xX][oO][rR][sS][hH][iI][fF][tT]'
@lex.TOKEN(BXORSHIFT)
def t_BXORSHIFT(t):
	return t

BXOR = r'[bB][xX][oO][rR]'
@lex.TOKEN(BXOR)
def t_BXOR(t):
	return t


BREV = r'[bB][rR][eE][vV]'
@lex.TOKEN(BREV)
def t_BREV(t):
	return t

BP = r'[bB][pP]'
@lex.TOKEN(BP)
def t_BP(t):
	return t

BITTST = r'[bB][iI][tT][tT][sS][tT]'
@lex.TOKEN(BITTST)
def t_BITTST(t):
	return t

BITTGL = r'[bB][iI][tT][tT][gG][lL]'
@lex.TOKEN(BITTGL)
def t_BITTGL(t):
	return t

BITSET = r'[bB][iI][tT][sS][eE][tT]'
@lex.TOKEN(BITSET)
def t_BITSET(t):
	return t

BITMUX = r'[bB][iI][tT][mM][uU][xX]'
@lex.TOKEN(BITMUX)
def t_BITMUX(t):
	return t

BITCLR = r'[bB][iI][tT][cC][lL][rR]'
@lex.TOKEN(BITCLR)
def t_BITCLR(t):
	return t



#Ben how to resolve conflict with binary b#xx?
# B = r'[bB]'
# @lex.TOKEN(B)
# def t_B(t):
# 	return t



ASHIFT = r'[aA][sS][hH][iI][fF][tT]'
@lex.TOKEN(ASHIFT)
def t_ASHIFT(t):
	return t

ASL = r'[aA][sS][lL]'
@lex.TOKEN(ASL)
def t_ASL(t):
	return t

ASR = r'[aA][sS][rR]'
@lex.TOKEN(ASR)
def t_ASR(t):
	return t

ALIGN8 = r'[aA][lL][iI][gG][nN]8'
@lex.TOKEN(ALIGN8)
def t_ALIGN8(t):
	return t

ALIGN16 = r'[aA][lL][iI][gG][nN]16'
@lex.TOKEN(ALIGN16)
def t_ALIGN16(t):
	return t

ALIGN24 = r'[aA][lL][iI][gG][nN]24'
@lex.TOKEN(ALIGN24)
def t_ALIGN24(t):
	return t

A_ONE_DOT_L = r'[aA]1\.[lL]'
@lex.TOKEN(A_ONE_DOT_L)
def t_A_ONE_DOT_L(t):
	return t

A_ZERO_DOT_L = r'[aA]0\.[lL]'
@lex.TOKEN(A_ZERO_DOT_L)
def t_A_ZERO_DOT_L(t):
	return t

A_ONE_DOT_H = r'[aA]1\.[hH]'
@lex.TOKEN(A_ONE_DOT_H)
def t_A_ONE_DOT_H(t):
	return t

A_ZERO_DOT_H = r'[aA]0\.[hH]'
@lex.TOKEN(A_ZERO_DOT_H)
def t_A_ZERO_DOT_H(t):
	return t

A_ONE_COLON_ZERO = r'[aA]1:0'
@lex.TOKEN(A_ONE_COLON_ZERO)
def t_A_ONE_COLON_ZERO(t):
	return t

ABS = r'[aA][bB][sS]'
@lex.TOKEN(ABS)
def t_ABS(t):
	return t

ABORT = r'[aA][bB][oO][rR][tT]'
@lex.TOKEN(ABORT)
def t_ABORT(t):
	return t


REG_A_DOUBLE_ONE = r'[aA]1'
@lex.TOKEN(REG_A_DOUBLE_ONE)
def t_REG_A_DOUBLE_ONE(t):
	return t


REG_A_DOUBLE_ZERO = r'[aA]0'
@lex.TOKEN(REG_A_DOUBLE_ZERO)
def t_REG_A_DOUBLE_ZERO(t):
	return t

GOT = r'[Gg][Oo][Tt]'
@lex.TOKEN(GOT)
def t_GOT(t):
	return t

GOT17M4 = r'[Gg][Oo][Tt]17[Mm]4'
@lex.TOKEN(GOT17M4)
def t_GOT17M4(t):
	return t

FUNCDESC_GOT17M4 = r'[Ff][Uu][Nn][Cc][Dd][Ee][Ss][Cc]_[Gg][Oo][Tt]17[Mm]4'
@lex.TOKEN(FUNCDESC_GOT17M4)
def t_FUNCDESC_GOT17M4(t):
	return t

PLTPC = r'[Pp][Ll][Tt][Pp][Cc]'
@lex.TOKEN(PLTPC)
def t_PLTPC(t):
	return t



TILDA = r"~"
@lex.TOKEN(TILDA)
def t_TILDA(t):
	return t

_BAR_ASSIGN = r"\|="
@lex.TOKEN(_BAR_ASSIGN)
def t__BAR_ASSIGN(t):
	return t

#BEN BAR WAS HERE

_CARET_ASSIGN = r"\^="
@lex.TOKEN(_CARET_ASSIGN)
def t__CARET_ASSIGN(t):
	return t

CARET = r"\^"
@lex.TOKEN(CARET)
def t_CARET(t):
	return t

RBRACK = r"]"
@lex.TOKEN(RBRACK)
def t_RBRACK(t):
	return t

LBRACK = r"\["
@lex.TOKEN(LBRACK)
def t_LBRACK(t):
	return t

_GREATER_GREATER_GREATER_THAN_ASSIGN = r">>>="
@lex.TOKEN(_GREATER_GREATER_GREATER_THAN_ASSIGN)
def t__GREATER_GREATER_GREATER_THAN_ASSIGN(t):
	return t

_GREATER_GREATER_ASSIGN = r">>="
@lex.TOKEN(_GREATER_GREATER_ASSIGN)
def t__GREATER_GREATER_ASSIGN(t):
	return t

_GREATER_GREATER_GREATER = r">>>"
@lex.TOKEN(_GREATER_GREATER_GREATER)
def t__GREATER_GREATER_GREATER(t):
	return t

GREATER_GREATER = r">>"
@lex.TOKEN(GREATER_GREATER)
def t_GREATER_GREATER(t):
	return t

_ASSIGN_ASSIGN = r"=="
@lex.TOKEN(_ASSIGN_ASSIGN)
def t__ASSIGN_ASSIGN(t):
	return t

ASSIGN = r"="
@lex.TOKEN(ASSIGN)
def t_ASSIGN(t):
	return t

_LESS_THAN_ASSIGN = r"<="
@lex.TOKEN(_LESS_THAN_ASSIGN)
def t__LESS_THAN_ASSIGN(t):
	return t

_LESS_LESS_ASSIGN = r"<<="
@lex.TOKEN(_LESS_LESS_ASSIGN)
def t__LESS_LESS_ASSIGN(t):
	return t

LESS_LESS = r"<<"
@lex.TOKEN(LESS_LESS)
def t_LESS_LESS(t):
	return t

LESS_THAN = r"<"
@lex.TOKEN(LESS_THAN)
def t_LESS_THAN(t):
	return t

LPAREN = r"\("
@lex.TOKEN(LPAREN)
def t_LPAREN(t):
	return t

RPAREN = r'\)'
@lex.TOKEN(RPAREN)
def t_RPAREN(t):
	return t

COLON = r":"
@lex.TOKEN(COLON)
def t_COLON(t):
	return t

SLASH = r"/"
@lex.TOKEN(SLASH)
def t_SLASH(t):
	return t

_MINUS_ASSIGN = r"-="
@lex.TOKEN(_MINUS_ASSIGN)
def t__MINUS_ASSIGN(t):
	return t

_PLUS_BAR_PLUS = r"\+\|+"
@lex.TOKEN(_PLUS_BAR_PLUS)
def t__PLUS_BAR_PLUS(t):
	return t

_MINUS_BAR_PLUS = r"-\|+"
@lex.TOKEN(_MINUS_BAR_PLUS)
def t__MINUS_BAR_PLUS(t):
	return t

_PLUS_BAR_MINUS = r"\+\|-"
@lex.TOKEN(_PLUS_BAR_MINUS)
def t__PLUS_BAR_MINUS(t):
	return t

_MINUS_BAR_MINUS = r"-\|-"
@lex.TOKEN(_MINUS_BAR_MINUS)
def t__MINUS_BAR_MINUS(t):
	return t

_MINUS_MINUS = r"--"
@lex.TOKEN(_MINUS_MINUS)
def t__MINUS_MINUS(t):
	return t

MINUS = r"-"
@lex.TOKEN(MINUS)
def t_MINUS(t):
	return t

COMMA = r","
@lex.TOKEN(COMMA)
def t_COMMA(t):
	return t

_PLUS_ASSIGN = r"\+="
@lex.TOKEN(_PLUS_ASSIGN)
def t__PLUS_ASSIGN(t):
	return t

_PLUS_PLUS = r"\+\+"
@lex.TOKEN(_PLUS_PLUS)
def t__PLUS_PLUS(t):
	return t

PLUS = r"\+"
@lex.TOKEN(PLUS)
def t_PLUS(t):
	return t

_STAR_ASSIGN = r"\*="
@lex.TOKEN(_STAR_ASSIGN)
def t__STAR_ASSIGN(t):
	return t

STAR = r"\*"
@lex.TOKEN(STAR)
def t_STAR(t):
	return t

_AMPERSAND_ASSIGN = r"&="
@lex.TOKEN(_AMPERSAND_ASSIGN)
def t__AMPERSAND_ASSIGN(t):
	return t

AMPERSAND = r"&"
@lex.TOKEN(AMPERSAND)
def t_AMPERSAND(t):
	return t

PERCENT = r"%"
@lex.TOKEN(PERCENT)
def t_PERCENT(t):
	return t

BANG = r"!"
@lex.TOKEN(BANG)
def t_BANG(t):
	return t

SEMICOLON = r";"
@lex.TOKEN(SEMICOLON)
def t_SEMICOLON(t):
	return t

_ASSIGN_BANG = r"=!"
@lex.TOKEN(_ASSIGN_BANG)
def t__ASSIGN_BANG(t):
	return t

DOUBLE_BAR = r"\|\|"
@lex.TOKEN(DOUBLE_BAR)
def t_DOUBLE_BAR(t):
	return t

#BEN MOVED DOUBLE BAR PRECEDENCE
BAR = r"\|"
@lex.TOKEN(BAR)
def t_BAR(t):
	return t

AT = r"@"
@lex.TOKEN(AT)
def t_AT(t):
	return t

PREFETCH = r'[pP][rR][eE][fF][eE][tT][cC][hH]'
@lex.TOKEN(PREFETCH)
def t_PREFETCH(t):
	return t

UNLINK = r'[uU][nN][lL][iI][nN][kK]'
@lex.TOKEN(UNLINK)
def t_UNLINK(t):
	return t

LINK = r'[lL][iI][nN][kK]'
@lex.TOKEN(LINK)
def t_LINK(t):
	return t

IDLE = r'[iI][dD][lL][eE]'
@lex.TOKEN(IDLE)
def t_IDLE(t):
	return t

IFLUSH = r'[iI][fF][lL][uU][sS][hH]'
@lex.TOKEN(IFLUSH)
def t_IFLUSH(t):
	return t

FLUSHINV = r'[fF][lL][uU][sS][hH][iI][nN][vV]'
@lex.TOKEN(FLUSHINV)
def t_FLUSHINV(t):
	return t

FLUSH = r'[fF][lL][uU][sS][hH]'
@lex.TOKEN(FLUSH)
def t_FLUSH(t):
	return t


#ben had to rearrange this regex to see decimals, first case was matching, i guess flex vs python regex issue
NUMBER = r'(0\.[0-9]+[rR]?)|([bhfodBHOFD]\#[0-9a-fA-F]+)|(0[xX][0-9a-fA-F]+)|([0-9]+)'
@lex.TOKEN(NUMBER)
def t_NUMBER(t):
	return t


ignore_NEWLINE = r'[\s\\t]'
@lex.TOKEN(ignore_NEWLINE)
def t_NEWLINE(t):
	pass

#SYMBOL - ben gonna drop em
SYMBOL = r'([a-zA-Z\x80-\xff_$.][a-zA-Z0-9\x80-\xff_$.]*'
SYMBOL += r'|' + r'[0-9][bfBF])'

LABEL = SYMBOL + r'[:]'

@lex.TOKEN(LABEL)
def t_LABEL(t):
	pass

@lex.TOKEN(SYMBOL)
def t_SYMBOL(t):
	return t

lexer = lex.lex()