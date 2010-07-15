from ply import yacc
from lexer import tokens
__all__ = ['tokens', 'parser', 'precedence']

def p_proofst(p):
    '''proofst : subgoal hyp goal
            | subgoal goal'''
    if len(p) == 4:
        p[0] = dict(subgoal=p[1], hyp=p[2], goal=p[3])
    else:
        p[0] = dict(subgoal=p[1], goal=p[2])

def p_subgoal(p):
    '''subgoal : NUMBER SUBGOAL'''
    p[0] = ' '.join((str(p[1]), str(p[2])))

def p_hyp(p):
    '''hyp : ID COLON PROP hyp
           | ID COLON expr hyp
           | ID COLON PROP
           | ID COLON expr
           '''
    hyp = [dict(name=p[1], type=p[3])]
    if len(p) == 5:
        p[0] = hyp + [p[4]]
    else:
        p[0] = dict(name=p[1], type=p[3])

parser = yacc.yacc(debug=True)
