from django.db.models import Count, Case, When,F
from django.db.models import Sum
from datetime import  timedelta,datetime
from nilusnfs.models import TmpFat
from lancfinanceiros.models import Lancamentos
from nilusadm.models import Sequenciais
from niluscont.models import Contratos,OrdemServico
from core.utils import add_one_month
from lancfinanceiros.movto_finan import grava_movimento_financeiro_c
from nilusnfs.enotas_util import emite_nfse
from nilusnfs.models import Paramnfs


def lista_contratoeos(contratos,ordemservico):

    lista=[]


    if contratos:
        for c in contratos:



            lista.append({"pk": c.pk,"num":c.num_cont,"tipo":'c',"cliente":c.cadgeral,"servico":c.item,
                          "pfat":c.prox_faturamento,"valor":c.valor})

    if ordemservico:
        for o in ordemservico:
            lista.append({"pk": o.pk,"num":o.num_os,"tipo":'o',"cliente":o.cadgeral,"servico":o.desc_item,
                          "pfat":o.data_os,"valor":o.valor_unit})

    return(lista)




def post_save_tmpfat(contrato,os):

    if contrato:
        tmp_fat = TmpFat()

        tmp_fat.master_user = contrato.master_user
        tmp_fat.tipo = 'C'
        tmp_fat.company = contrato.company
        tmp_fat.cadgeral = contrato.cadgeral
        tmp_fat.contrato = contrato
        tmp_fat.vlr_fat = contrato.valor
        tmp_fat.data_fat = contrato.prox_faturamento
        tmp_fat.save()
    if os:
        tmp_fat = TmpFat()
        tmp_fat.master_user = os.master_user
        tmp_fat.tipo = 'O'
        tmp_fat.company = os.company
        tmp_fat.cadgeral = os.cadgeral
        tmp_fat.vlr_fat = os.valor_unit
        tmp_fat.os = os
        tmp_fat.data_fat = os.data_os
        tmp_fat.save()



def post_edit_tmpfat(contrato,os):

    if contrato:

        tmp_fat = TmpFat.objects.filter(contrato=contrato,master_user=contrato.master_user,tipo='C')

        tmp_fat.update(
            company = contrato.company,
            cadgeral=contrato.cadgeral,
            contrato = contrato,
            vlr_fat = contrato.valor

        )
    if os:
        tmp_fat = TmpFat.objects.filter(os=os,master_user=os.master_user,tipo='O')

        tmp_fat.update(
            company = os.company,
            cadgeral = os.cadgeral,
            vlr_fat = os.valor_unit,
            os = os
        )



def fat(faturar,planofinan,data_fat,contafinan):
    for f in faturar:
        if f.tipo == 'C':
            # Verifica se a OS. é referente a algum contrato e se a empresa emite notas fiscais
            if f.contrato.gera_nfs == True:
                paramnf = Paramnfs.objects.get(master_user=f.master_user, company=f.company)
                if paramnf:
                    retorno_nota = emite_nfse(f)
                    print(retorno_nota)
                    if retorno_nota.status_code == 200:
                        cria_lancamento_credito(f,planofinan,data_fat,contafinan,f.tipo)
            else:
                cria_lancamento_credito(f, planofinan, data_fat, contafinan, f.tipo)

        elif f.tipo == 'O':
            if f.os.contrato.gera_nfs == True:
                paramnf = Paramnfs.objects.get(master_user=f.master_user, company=f.company)
                if paramnf:
                    retorno_nota = emite_nfse(f)
                    if retorno_nota.status_code == 200:
                        cria_lancamento_credito(f, planofinan, data_fat, contafinan, f.tipo)
            else:
                cria_lancamento_credito(f, planofinan, data_fat, contafinan, f.tipo)


def cria_lancamento_credito(registro,planofinan,data_fat,contafinan,tipo):


        if tipo == 'C':
            # if f.contrato.proximo_faturamento < f.contrato.vigencia:
            #     f.data_fat = f.proximo_faturamento
            #     f.save()

            prox_fat = registro.contrato.prox_faturamento
            vencto_lancamento = datetime.strftime(prox_fat,'%Y')+'-'+datetime.strftime(prox_fat,'%m')+'-'+\
                                str(registro.contrato.dia_base)

            vencto_lancamento = datetime.strptime(vencto_lancamento,"%Y-%m-%d")

            lancto = Lancamentos()
            lancto.master_user = registro.master_user
            lancto.company = registro.contrato.company
            lancto.cadgeral = registro.contrato.cadgeral
            lancto.dt_lancamento = data_fat
            lancto.dt_vencimento = vencto_lancamento
            lancto.plr_financeiro = planofinan
            lancto.conta_finan = contafinan
            lancto.vlr_lancamento = registro.contrato.valor
            lancto.valor_text = registro.contrato.valor
            lancto.saldo = registro.contrato.valor
            lancto.descricao = 'Faturamento do contrato nº: '+ str(registro.contrato.num_cont) +' ' \
                               'de prestação do serviço referente: '+ str(registro.contrato.item)
            lancto.titulo = True
            lancto.indice = registro.contrato.indice
            lancto.cotacao = registro.contrato.cotacao

            seq_lanc = Sequenciais.objects.get(user=registro.master_user)
            lancto.num_lan = seq_lanc.lanc_financeiros + 1
            seq_lanc.lanc_financeiros = lancto.num_lan
            seq_lanc.save()

            lancto.tipo_lancamento = 'R'
            lancto.save()

            contrato = Contratos.objects.get(pk=registro.contrato.pk)

            if contrato.periodo_fat == 'M':
                # prox_fat = add_one_month(contrato.prox_faturamento)
                contrato.prox_faturamento = add_one_month(contrato.prox_faturamento)
            elif contrato.periodo_fat == 'S':
                # prox_fat = contrato.prox_faturamento + timedelta(days=15)
                contrato.prox_faturamento = contrato.prox_faturamento + timedelta(days=7)
            elif contrato.prox_faturamento == 'Q':
                # prox_fat = contrato.prox_faturamento + timedelta(days=15)
                contrato.prox_faturamento = contrato.prox_faturamento + timedelta(days=15)
            elif contrato.prox_faturamento == 'A':
                # prox_fat = contrato.prox_faturamento + timedelta(days=15)
                contrato.prox_faturamento = contrato.prox_faturamento + timedelta(days=15)

            contrato.save()

            grava_movimento_financeiro_c(lancto, registro.master_user)

        elif tipo == 'O':
                registro.situacao = True
                registro.save()

                os = OrdemServico.objects.get(pk=registro.os.pk)
                os.situacao_fat = 'F'
                os.save()

                lancto = Lancamentos()
                lancto.master_user = registro.master_user
                lancto.company = registro.os.company
                lancto.cadgeral = registro.os.cadgeral
                lancto.dt_lancamento = registro.os.data_os
                lancto.dt_vencimento = registro.os.data_os
                lancto.plr_financeiro = planofinan
                lancto.conta_finan = contafinan
                lancto.vlr_lancamento = registro.os.valor_unit
                lancto.valor_text = registro.os.valor_unit
                lancto.saldo = registro.os.valor_unit
                lancto.descricao = 'Faturamento da ordem de serviço nº: ' + str(registro.os.num_os) + ' ' \
                                   'realizada em : ' + str(registro.os.data_os)
                lancto.titulo = True

                seq_lanc = Sequenciais.objects.get(user=registro.master_user)
                lancto.num_lan = seq_lanc.lanc_financeiros + 1
                seq_lanc.lanc_financeiros = lancto.num_lan
                seq_lanc.save()

                lancto.tipo_lancamento = 'R'
                lancto.save()

                grava_movimento_financeiro_c(lancto, registro.master_user)


def cria_lancamento_credito_unificado(faturar,planofinan,data_fat,contafinan):

    fatuni = faturar.values('cadgeral').annotate(vlr_fatura=Sum('vlr_fat'))
    fatuni = faturar.order_by('cadgeral')


    for f in fatuni:
        print(f)

    return fatuni

