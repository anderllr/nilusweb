from lancfinanceiros.models import Lancamentos,Movtos_lancamentos




def grava_movimento_financeiro_b(lancamento,situacao,valor_lancamento):
    if situacao is True:
        
        movto_lanc = Movtos_lancamentos()
        movto_lanc.lancamento = lancamento
        movto_lanc.dt_movimento = lancamento.data_baixa
        movto_lanc.vlr_movimento = valor_lancamento
        movto_lanc.conta_financeira = lancamento.conta_finan
        if lancamento.tipo_lancamento == 'R':
            movto_lanc.desc_movimento = 'Recebido'
        else:
            movto_lanc.desc_movimento = 'Pago'
        movto_lanc.tipo_movto = 'B'
        movto_lanc.save() 
    else:
    
        movto_lanc = Movtos_lancamentos()
        movto_lanc.lancamento = lancamento
        movto_lanc.dt_movimento = lancamento.data_baixa
        movto_lanc.vlr_movimento = valor_lancamento
        movto_lanc.conta_financeira = lancamento.conta_finan
        if lancamento.tipo_lancamento == 'R':
            movto_lanc.desc_movimento = 'Recebimento Parcial'
        else:
            movto_lanc.desc_movimento = 'Pagamento Parcial'
        movto_lanc.tipo_movto = 'B'
        movto_lanc.save()


