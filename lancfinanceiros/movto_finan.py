from lancfinanceiros.models import Lancamentos,Movtos_lancamentos




def grava_movimento_financeiro_b(lancamento,situacao,valor_lancamento,user_master):
    if situacao is True:
        
        movto_lanc = Movtos_lancamentos()
        movto_lanc.master_user = user_master
        movto_lanc.lancamento = lancamento
        movto_lanc.dt_movimento = lancamento.data_baixa
        movto_lanc.vlr_movimento = valor_lancamento
        movto_lanc.conta_financeira = lancamento.conta_finan
        if lancamento.tipo_lancamento == 'R':
            movto_lanc.desc_movimento = 'Recebido'
            movto_lanc.sinal = 'R'
        else:
            movto_lanc.desc_movimento = 'Pago'
            movto_lanc.sinal = 'D'
        movto_lanc.tipo_movto = 'B'
        movto_lanc.save() 
    else:
    
        movto_lanc = Movtos_lancamentos()
        movto_lanc.master_user = user_master
        movto_lanc.lancamento = lancamento
        movto_lanc.dt_movimento = lancamento.data_baixa
        movto_lanc.vlr_movimento = valor_lancamento
        movto_lanc.conta_financeira = lancamento.conta_finan
        if lancamento.tipo_lancamento == 'R':
            movto_lanc.desc_movimento = 'Recebimento Parcial'
            movto_lanc.sinal = 'R'
        else:
            movto_lanc.desc_movimento = 'Pagamento Parcial'
            movto_lanc.sinal = 'D'
        movto_lanc.tipo_movto = 'B'
        movto_lanc.save()



def grava_movimento_financeiro_c(lancamento,user_master):

    movto_lanc = Movtos_lancamentos()
    movto_lanc.master_user = user_master
    movto_lanc.lancamento = lancamento
    movto_lanc.dt_movimento = lancamento.dt_lancamento
    movto_lanc.vlr_movimento = lancamento.vlr_lancamento
    if lancamento.tipo_lancamento == 'R':
        movto_lanc.desc_movimento = 'Inclusão de receita'
        movto_lanc.sinal = 'R'
    else:
        movto_lanc.desc_movimento = 'Inclusão de despesa'
        movto_lanc.sinal = 'D'
    movto_lanc.tipo_movto = 'C'
    movto_lanc.save()



    if lancamento.situacao is True:
        movto_lanc = Movtos_lancamentos()
        movto_lanc.master_user = user_master
        movto_lanc.lancamento = lancamento
        movto_lanc.dt_movimento = lancamento.dt_lancamento
        movto_lanc.vlr_movimento = lancamento.vlr_lancamento
        movto_lanc.conta_financeira = lancamento.conta_finan
        if lancamento.tipo_lancamento == 'R':
            movto_lanc.desc_movimento = 'Recebido'
            movto_lanc.sinal = 'R'
        else:
            movto_lanc.desc_movimento = 'Pago'
            movto_lanc.sinal = 'D'
        movto_lanc.tipo_movto = 'B'
        movto_lanc.save()






