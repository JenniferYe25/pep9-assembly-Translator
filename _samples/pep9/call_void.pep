         BR      program
_UNIV:   .WORD 42
value:   .BLOCK 2
result:  .EQUATE 0
my_func: SUBSP 4,i
         DECI value, d
         LDWA _UNIV, d
         ADDA value, d
         STWA result, d
         DECO result, d
         ADDSP 4, i
         RET
program: CALL my_func
         .END      
