def p_expression_plus(p):
    '''expression : expression PLUS term'''
    p[0] = p[1] + p[3]

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]
