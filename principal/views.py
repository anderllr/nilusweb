from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from django.db import models
from django.shortcuts import render,get_object_or_404
from django.views.generic import UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse,Http404
from django.db.models import Func

from accounts.models import User
from .models import Instancia
from niluscad.models import Company,Propriety
from nilusfin.models import Indice,Cotacao
from lancfinanceiros.models import Lancamentos
# Create your views here.


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


@login_required
def principal(request,ano=None, mes=None):


   # 1º Posição de todos os lançamentos em aberto e seus valores de saldos até o momento.
   # lancfin_rec = Lancamentos.objects.filter(master_user=request.user.user_master, situacao=False, tipo_lancamento='R')
   # lancfin_des = Lancamentos.objects.filter(master_user=request.user.user_master, situacao=False, tipo_lancamento='D')
   # lancfin_rec_val = lancfin_rec.aggregate(vlr_saldo=Sum('saldo'))
   # lancfin_des_val = lancfin_des.aggregate(vlr_saldo=Sum('saldo'))
   # lancfin_rec_qtd = lancfin_rec.count()
   # lancfin_des_qtd = lancfin_des.count()


   # 2º Inicia-se o processo de verificar mês a mês

   data_hoje = datetime.today()
   listaanos = [i for i in range(data_hoje.year - 10, data_hoje.year + 11)]
   listames = [i for i in range(1, 13)]

   if ano is None:
      dt_filtro = datetime.now()
      print(dt_filtro)
      ano = dt_filtro.year
      mes = dt_filtro.month

   try:
      dt_filtro = date(int(ano), int(mes), 1)
   except:
      raise Http404

   # receitas
   lancto_receitas = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R',situacao=False)
   lancto_receitas = lancto_receitas.filter(dt_vencimento__year=dt_filtro.year, dt_vencimento__month=dt_filtro.month)

   lancto_receitas_atraso = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R',situacao=False)
   lancto_receitas_atraso = lancto_receitas_atraso.filter(dt_vencimento__lt=dt_filtro)

   # somas e quantidades no período.
   lancfin_rec_val = lancto_receitas.aggregate(vlr_saldo=Sum('saldo'))
   lancfin_rec_qtd = lancto_receitas.count()
   lancfin_rec_atr = lancto_receitas_atraso.aggregate(vlr_saldo=Sum('saldo'))

   # despesas
   lancto_despesas = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D', situacao=False)
   lancto_despesas = lancto_despesas.filter(dt_vencimento__year=dt_filtro.year, dt_vencimento__month=dt_filtro.month)

   lancto_despesas_atraso = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D', situacao=False)
   lancto_despesas_atraso = lancto_despesas_atraso.filter(dt_vencimento__lt=dt_filtro)

   # somas e quantidades no período.
   lancfin_des_val = lancto_despesas.aggregate(vlr_saldo=Sum('saldo'))
   lancfin_des_qtd = lancto_despesas.count()
   lancfin_des_atr = lancto_despesas_atraso.aggregate(vlr_saldo=Sum('saldo'))



   # Valores dentro do mês por plano financeiro (gráfico pie)
   planofinan_desp = Lancamentos.objects.filter(master_user=request.user.user_master, dt_vencimento__year=dt_filtro.year,
                                                        dt_vencimento__month=dt_filtro.month,
                                                        tipo_lancamento='D').values('plr_financeiro__descricao')
   planofinan_desp = planofinan_desp.annotate(valor_plano=Sum('vlr_lancamento'))
   planofinan_desp = planofinan_desp.order_by('-valor_plano')


   planofinan_rec = Lancamentos.objects.filter(master_user=request.user.user_master, dt_vencimento__year=dt_filtro.year,
                                                dt_vencimento__month=dt_filtro.month,
                                                        tipo_lancamento='R').values('plr_financeiro__descricao')
   planofinan_rec = planofinan_rec.annotate(valor_plano=Sum('vlr_lancamento'))
   planofinan_rec = planofinan_rec.order_by('-valor_plano')


   # Grid com os lançamentos em atraso
   lancto_atraso_grid = Lancamentos.objects.filter(master_user=request.user.user_master,situacao=False)
   lancto_atraso_grid = lancto_atraso_grid.filter(dt_vencimento__lt=dt_filtro).order_by('dt_vencimento').order_by('-saldo')

   dt_lancamentos_proximo = dt_filtro + timedelta(days=31)
   dt_lancamentos_anterior = dt_filtro - timedelta(days=1)



   # # Valores nos ultimos 6 meses (CHART BAR)
   # 1º Mês
   mes1_range = dt_filtro - relativedelta(months=6)
   bars_receitas1 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R')
   bars_receitas1 = bars_receitas1.filter(dt_vencimento__year=mes1_range.year, dt_vencimento__month=mes1_range.month)
   bars_receitas1 = bars_receitas1.aggregate(vlr_mes=Sum('vlr_lancamento'))

   bars_despesas1 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D')
   bars_despesas1 = bars_despesas1.filter(dt_vencimento__year=mes1_range.year, dt_vencimento__month=mes1_range.month)
   bars_despesas1 = bars_despesas1.aggregate(vlr_mes=Sum('vlr_lancamento'))

   # 2º mês
   mes2_range = dt_filtro - relativedelta(months=5)
   bars_receitas2 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R')
   bars_receitas2 = bars_receitas2.filter(dt_vencimento__year=mes2_range.year, dt_vencimento__month=mes2_range.month)
   bars_receitas2 = bars_receitas2.aggregate(vlr_mes=Sum('vlr_lancamento'))

   bars_despesas2 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D')
   bars_despesas2 = bars_despesas2.filter(dt_vencimento__year=mes2_range.year, dt_vencimento__month=mes2_range.month)
   bars_despesas2 = bars_despesas2.aggregate(vlr_mes=Sum('vlr_lancamento'))

   # 3º mês
   mes3_range = dt_filtro - relativedelta(months=4)
   bars_receitas3 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R')
   bars_receitas3 = bars_receitas3.filter(dt_lancamento__year=mes3_range.year, dt_lancamento__month=mes3_range.month)
   bars_receitas3 = bars_receitas3.aggregate(vlr_mes=Sum('vlr_lancamento'))

   bars_despesas3 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D')
   bars_despesas3 = bars_despesas3.filter(dt_lancamento__year=mes3_range.year, dt_lancamento__month=mes3_range.month)
   bars_despesas3 = bars_despesas3.aggregate(vlr_mes=Sum('vlr_lancamento'))

   # 4º mês
   mes4_range = dt_filtro - relativedelta(months=3)
   bars_receitas4 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R')
   bars_receitas4 = bars_receitas4.filter(dt_vencimento__year=mes4_range.year, dt_vencimento__month=mes4_range.month)
   bars_receitas4 = bars_receitas4.aggregate(vlr_saldo=Sum('vlr_lancamento'))

   bars_despesas4 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D')
   bars_despesas4 = bars_despesas4.filter(dt_lancamento__year=mes4_range.year, dt_lancamento__month=mes4_range.month)
   bars_despesas4 = bars_despesas4.aggregate(vlr_mes=Sum('vlr_lancamento'))

   # 5º mês
   mes5_range = dt_filtro - relativedelta(months=2)
   bars_receitas5 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R')
   bars_receitas5 = bars_receitas5.filter(dt_lancamento__year=mes5_range.year, dt_lancamento__month=mes5_range.month)
   bars_receitas5 = bars_receitas5.aggregate(vlr_mes=Sum('vlr_lancamento'))

   bars_despesas5 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D')
   bars_despesas5 = bars_despesas5.filter(dt_lancamento__year=mes5_range.year, dt_lancamento__month=mes5_range.month)
   bars_despesas5 = bars_despesas5.aggregate(vlr_mes=Sum('vlr_lancamento'))

   # 6º mês
   mes6_range = dt_filtro - relativedelta(months=1)
   bars_receitas6 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='R')
   bars_receitas6 = bars_receitas6.filter(dt_lancamento__year=mes6_range.year, dt_lancamento__month=mes6_range.month)
   bars_receitas6 = bars_receitas6.aggregate(vlr_mes=Sum('vlr_lancamento'))

   bars_despesas6 = Lancamentos.objects.filter(master_user=request.user.user_master, tipo_lancamento='D')
   bars_despesas6 = bars_despesas6.filter(dt_lancamento__year=mes6_range.year, dt_lancamento__month=mes6_range.month)
   bars_despesas6 = bars_despesas6.aggregate(vlr_mes=Sum('vlr_lancamento'))



    # DRE

   soma_grupodre = Lancamentos.objects.filter(master_user=request.user.user_master)
   soma_grupodre = soma_grupodre.filter(dt_lancamento__year=dt_filtro.year,
                                                        dt_lancamento__month=dt_filtro.month)
   debitos = soma_grupodre.filter(master_user=request.user.user_master,
                                  tipo_lancamento='D').aggregate(vlr_debitos=Sum('vlr_lancamento'))
   creditos = soma_grupodre.filter(master_user=request.user.user_master,
                                   tipo_lancamento='R').aggregate(vlr_creditos=Sum('vlr_lancamento'))

   soma_grupodre = soma_grupodre.values('plr_financeiro__grupodre__descricao', 'plr_financeiro__descricao',
                                        'plr_financeiro__grupodre__sinal').annotate(
      vlr_lancamentos=Sum('vlr_lancamento'))
   soma_grupodre = soma_grupodre.order_by('plr_financeiro__grupodre__ordem')



   # SALDO FINAL DO RESULTADO (CREDITOS - DÉBITOS)
   if creditos['vlr_creditos'] is None:
      creditos['vlr_creditos'] = 0

   if debitos['vlr_debitos'] is None:
      debitos['vlr_debitos'] = 0



   saldo_atual = Decimal(creditos['vlr_creditos']) - Decimal(debitos['vlr_debitos'])

   context = {
      'dt_lancamentos_proximo': dt_lancamentos_proximo,
      'dt_lancamentos_anterior': dt_lancamentos_anterior,
      'dt_filtro' : dt_filtro,
      'receita_val' : lancfin_rec_val,
      'despesa_val' : lancfin_des_val,
      'receita_qtd' : lancfin_rec_qtd,
      'despesa_qtd' : lancfin_des_qtd,
      'lancto_receitas_atraso' : lancto_receitas_atraso,
      'lancto_despesas_atraso' : lancto_despesas_atraso,
      'valor_receitas_atraso' : lancfin_rec_atr,
      'valor_despesas_atraso' : lancfin_des_atr,
      'listaanos': listaanos,
      'listames': listames,
      'planofinan_rec' : planofinan_rec,
      'planofinan_desp': planofinan_desp,
      'lancto_atraso_grid' : lancto_atraso_grid,
      'mes1_range' : mes1_range,
      'mes2_range': mes2_range,
      'mes3_range': mes3_range,
      'mes4_range': mes4_range,
      'mes5_range': mes5_range,
      'mes6_range': mes6_range,
      'bars_receitas1' : bars_receitas1,
      'bars_receitas2': bars_receitas2,
      'bars_receitas3': bars_receitas3,
      'bars_receitas4': bars_receitas4,
      'bars_receitas5': bars_receitas5,
      'bars_receitas6': bars_receitas6,

      'bars_despesas1': bars_despesas1,
      'bars_despesas2': bars_despesas2,
      'bars_despesas3': bars_despesas3,
      'bars_despesas4': bars_despesas4,
      'bars_despesas5': bars_despesas5,
      'bars_despesas6': bars_despesas6,

      'soma_grupodre' :soma_grupodre,
      'saldo_atual': saldo_atual,
   }
   return render(request,'principal.html',context)


class UpdateUserView(LoginRequiredMixin, UpdateView):
   model = User
   template_name = 'profile.html'
   fields = ['name', 'email', 'tel_user', 'img_user']

   def get_success_url(self):
      messages.success(self.request, 'Cadastro Atualizado com sucesso')
      return reverse_lazy('profile')

   def get_object(self):
      return self.request.user


class UpdatePasswordView(LoginRequiredMixin, FormView):

   def get_template_names(self):
      if self.request.is_ajax():
         return ["_altera_senha.html"]
      else:
         raise Http404

   form_class = PasswordChangeForm

   def get_success_url(self):
      messages.success(self.request, 'Senha Atualizada com sucesso')

      return reverse_lazy('profile')

   def get_form_kwargs(self):
      kwargs = super(UpdatePasswordView, self).get_form_kwargs()
      kwargs['user'] = self.request.user
      return kwargs

   def form_valid(self, form):
      form.save()
      update_session_auth_hash(self.request, form.user)
      if self.request.is_ajax():
         context = self.get_context_data(form=form, success=True)
         return self.render_to_response(context)
      else:
         return super(UpdatePasswordView, self).form_valid(form)


@login_required
def company_propriety(request):

    company_id = request.GET.get('company_id',None)
    if company_id:
        company = get_object_or_404(Company, pk=company_id)
        propriety = Propriety.objects.filter(company = company)
        context = {'company' : company, 'propriety': propriety}
        return render(request,'_select_propriety.html',context)
    raise Http404



@login_required
def indice_cotacao(request):

   indice_id = request.GET.get('indice_id',None)
   if indice_id:
      indice = get_object_or_404(Indice,pk=indice_id)
      cotacao = Cotacao.objects.filter(indice=indice).order_by('-data_indice')
      context = {'indice' : indice, 'cotacao' : cotacao}
      return render(request,'_select_cotacao.html',context)
   raise Http404



# def dashboard_financeiro(request):
#    if request.is_ajax():
#       template_name = '_dashboard_financeiro.html'
#    else:
#       template_name = 'dashboard_financeiro.html'
#
#    filtrou = 'nao'



profile = UpdateUserView.as_view()
update_password = UpdatePasswordView.as_view()



