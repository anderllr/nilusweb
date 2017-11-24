from datetime import date, timedelta

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,TemplateView,UpdateView,FormView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from core.utils import add_one_month
from django.http import HttpResponse,Http404
from .forms import FormCreateTitRec,FormEditTitRec,FiltroRecebimentosForm
from accounts.models import User
from nilusadm.models import Sequenciais
from principal.models import Instancia
from recebiveis.models import Recebiveis
from niluscad.models import Company,Propriety,Cadgeral,PlanoFinan,Ccusto
# Create your views here.



@login_required
def titrec_list(request):

    if request.is_ajax():
        template_name = '_table_titrec.html'
    else:
        template_name = 'titrec_list.html'

    if request.user.is_masteruser is True:
        titrec = Recebiveis.objects.filter(master_user=request.user.pk)
        empresa = Company.objects.filter(master_user=request.user.pk)
        propriedade = Propriety.objects.filter(master_user=request.user.pk)
        cliente = Cadgeral.objects.filter(master_user=request.user.pk,cliente=True)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.pk,sinal='R')
        c_custo = Ccusto.objects.filter(master_user=request.user.pk)
        empresa_init = Company.objects.filter(master_user=request.user.pk)
        propriedade_init = Propriety.objects.filter(master_user=request.user.pk)

    else:
        titrec = Recebiveis.objects.filet(master_user=request.user.user_master)
        empresa = Company.objects.filter(master_user=request.user.user_master)
        propriedade = Propriety.objects.filter(master_user=request.user.user_master)
        cliente = Cadgeral.objects.filter(master_user=request.user.user_master, cliente=True)
        plano_finan = PlanoFinan.objects.filter(master_user=request.user.user_master, sinal='R')
        c_custo = Ccusto.objects.filter(master_user=request.user.user_master)
        empresa_init = Company.objects.filter(master_user=request.user.user_master)
        propriedade_init = Propriety.objects.filter(master_user=request.user.user_master)

    form = FiltroRecebimentosForm(empresa,propriedade,cliente,plano_finan,c_custo, request.GET or None)


    if form.is_valid():
        data_venc_ini = form.cleaned_data.get('data_venc_ini', '')
        data_venc_fim = form.cleaned_data.get('data_venc_fim', '')
        data_lanc_ini = form.cleaned_data.get('data_lanc_ini', '')
        data_lanc_fim = form.cleaned_data.get('data_venc_fim', '')
        empresa = form.cleaned_data.get('empresa', '')
        propriedade = form.cleaned_data.get('propriedade', '')
        cliente = form.cleaned_data.get('cliente', '')
        plano_finan = form.cleaned_data.get('plano_finan', '')
        c_custo = form.cleaned_data.get('c_custo', '')

        if data_venc_ini:
            titrec = titrec.filter(dt_vencimento__gte=data_venc_ini)

        if data_venc_fim:
            titrec = titrec.filter(dt_vencimento__lt=data_venc_fim+timedelta(days=1))

        if data_lanc_ini:
            titrec = titrec.filter(dt_lancamento__gte=data_lanc_ini)

        if data_lanc_fim:
            titrec = titrec.filter(dt_lancamento__lt=data_lanc_fim + timedelta(days=1))

        if empresa:
            titrec = titrec.filter(company=empresa)

        if propriedade:
            titrec = titrec.filter(propriety=propriedade)

        if cliente:
            titrec = titrec.filter(client=cliente)

        if plano_finan:
            titrec = titrec.filter(plr_financeiro=plano_finan)

        if c_custo:
            titrec = titrec.filter(c_custo=c_custo)



    context = {
        'titrec': titrec,
        'form': form,
        'empresa_init' : empresa_init,
        'propriedade_init' : propriedade_init


    }

    return render(request, template_name, context)



@login_required
def company_propriety(request):

    company_id = request.GET.get('company_id',None)
    if company_id:
        company = get_object_or_404(Company, pk=company_id)
        propriety = Propriety.objects.filter(company = company)
        context = {'company' : company, 'propriety': propriety}
        return render(request,'_select_propriety.html',context)
    raise Http404




class CreateTitRec(LoginRequiredMixin,CreateView):


    def get_template_names(self):
        if self.request.is_ajax():
            return ["_create_titrec.html"]
        else:
            return ["create_titrec.html"]

    def get_form_kwargs(self):
        kwargs = super(CreateTitRec, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    model = Recebiveis
    form_class = FormCreateTitRec

    def get_initial(self):
        initial = super(CreateTitRec,self).get_initial()
        initial['company'] = self.request.user.company_p
        initial['propriety'] = self.request.user.propriety_p
        return initial

    def get_success_url(self):
        return reverse_lazy('titrec_list')


    def form_valid(self,form):
        titrec = form.save(commit=False)
        if self.request.user.is_masteruser is True:
            titrec.master_user = self.request.user
            seq_rec = Sequenciais.objects.get(user=self.request.user)
        else:
            titrec.master_user = self.request.user.user_master
            seq_rec = Sequenciais.objects.get(user=self.request.user.user_master)
        titrec.situacao = 'A'
        titrec.vlr_lancamento = titrec.valor_text.replace('R$','').replace('.','').replace(',','.')
        titrec.num_rec = seq_rec.recebiveis + 1
        seq_rec.recebiveis = titrec.num_rec
        seq_rec.save()
        titrec.save()

        id_titrec = titrec.pk

        if form.cleaned_data.get('parcela',False):
            qtd = form.cleaned_data['qtd']
            print(qtd)
            tipo_rept = form.cleaned_data['tipo_rept']
            print(tipo_rept)
            if tipo_rept == 'M':
                for i in range(qtd-1):
                    titrec.pk = None
                    titrec.num_rec = seq_rec.recebiveis + 1
                    seq_rec.recebiveis = titrec.num_rec
                    titrec.dt_vencimento = add_one_month(titrec.dt_vencimento)
                    titrec.lancamento_pai_id = id_titrec
                    titrec.save()
                    seq_rec.save()
            if tipo_rept == 'W':
                for i in range(qtd-1):
                    titrec.pk = None
                    titrec.dt_vencto = titrec.dt_vencto + timedelta(days=7)
                    titrec.lancamento_pai_id = id_titrec
                    titrec.save()
            if tipo_rept == 'D':
                for i in range(qtd-1):
                    titrec.pk = None
                    titrec.dt_vencto = titrec.dt_vencto + timedelta(days=1)
                    titrec.lancamento_pai_id = id_titrec
                    titrec.save()

        if self.request.is_ajax():
            context = self.get_context_data(form=form, success=True)
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())



class EditTitRec(LoginRequiredMixin,UpdateView):

    def get_template_names(self):
        if self.request.is_ajax():
            return ["_edit_titrec.html"]
        else:
            return ["edit_titrec.html"]

    def get_context_data(self, **kwargs):
        context = super(EditTitRec, self).get_context_data(**kwargs)
        context['tem_parcela'] = self.object.verifica_parcela()
        context['dados_titulo'] = Recebiveis.objects.get(pk=self.kwargs['pk'])

        return context

    def get_form_kwargs(self):
        kwargs = super(EditTitRec, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):

        return reverse_lazy('titrec_list')


    model = Recebiveis
    form_class = FormEditTitRec




    def form_valid(self, form):
        titrec = form.save(commit=False)
        titrec.vlr_lancamento = titrec.valor_text.replace('R$','').replace('.','').replace(',','.')
        titrec.save()
        confirma_parcela = self.request.POST.get('confirma_parcela','N')
        if confirma_parcela == 'S':
            titrec = form.instance
            titrec.altera_parcelas()

        if self.request.is_ajax():
            context = self.get_context_data(form=form,success=True,ok='ok')
            return self.render_to_response(context)
        else:
            return redirect(self.get_success_url())




def delete_titrec(request, pk):
    if request.user.is_masteruser is True:
        titrecdel = get_object_or_404(Recebiveis,master_user=request.user,pk=pk)
        titrecdel.delete()
    else:
        titrecdel = get_object_or_404(Recebiveis,master_user=request.user.user_master,pk=pk)
        titrecdel.delete()




    # messages.success(request, 'Grupo removido com sucesso !!')
    return redirect('titrec_list')




edit_titrec = EditTitRec.as_view()
create_titrec = CreateTitRec.as_view()
