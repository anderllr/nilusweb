from datetime import date, timedelta, datetime
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import render,get_object_or_404
from django.views.generic import UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse,Http404

from accounts.models import User
from .models import Instancia
from niluscad.models import Company,Propriety
from nilusfin.models import Indice,Cotacao
from lancfinanceiros.models import Lancamentos
# Create your views here.

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
      dt_filtro = timezone.now()
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



   # Valores dentro do mês por plano financeiro

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
   lancto_atraso_grid = Lancamentos.objects.filter(master_user=request.user.user_master,
                                                       situacao=False)
   lancto_atraso_grid = lancto_atraso_grid.filter(dt_vencimento__lt=dt_filtro).order_by('dt_vencimento').order_by('-saldo')

   # valor_receitas = Lancamentos.objects.filter(master_user=request.user, tipo_lancamento='R', pag_rec=True)
   # valor_receitas = valor_receitas.filter(dt_pagrec__year=dt_filtro.year,
   #                                        dt_pagrec__month=dt_filtro.month).aggregate(valor=Sum('valor'))
   # #
   # valor_receitas_previstas = Lancamentos.objects.filter(user=request.user, tipo_lancamento='R', pag_rec=False)
   # valor_receitas_previstas = valor_receitas_previstas.filter(dt_pagrec__year=dt_lancamentos.year,
   #                                                            dt_pagrec__month=dt_lancamentos.month).aggregate(
   #    valor=Sum('valor'))
   #


   # valor_despesas = Lancamentos.objects.filter(user=request.user, tipo_lancamento='D', pag_rec=True)
   # valor_despesas = valor_despesas.filter(dt_pagrec__year=dt_lancamentos.year,
   #                                        dt_pagrec__month=dt_lancamentos.month).aggregate(valor=Sum('valor'))
   #
   # valor_despesas_previstas = Lancamentos.objects.filter(user=request.user, tipo_lancamento='D', pag_rec=False)
   # valor_despesas_previstas = valor_despesas_previstas.filter(dt_pagrec__year=dt_lancamentos.year,
   #                                                            dt_pagrec__month=dt_lancamentos.month).aggregate(
   #    valor=Sum('valor'))
   #
   # valor_receitas_final = valor_receitas['valor'] or 0
   # valor_despesas_final = valor_despesas['valor'] or 0
   #
   # receitas_previstas_final = valor_receitas_previstas['valor'] or 0
   # despesas_previstas_final = valor_despesas_previstas['valor'] or 0
   #
   dt_lancamentos_proximo = dt_filtro + timedelta(days=31)
   dt_lancamentos_anterior = dt_filtro - timedelta(days=1)
   #

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
      'lancto_atraso_grid' : lancto_atraso_grid
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



