import requests
import json
from django.conf import settings
from  bs4 import BeautifulSoup
from nilusnfs.models import Paramnfs,ErrosParametrosNFS,NotasFiscais

def cad_empresa_emissora(paramnfs):

        url = settings.ENOTASURL +'/empresas'

        if paramnfs.simples_nac:
            simples = 'true'
        else:
            simples = 'false'

        if paramnfs.incent_cult:
            incentivo = 'true'
        else:
            incentivo = 'false'

        data = {
            "id": str(paramnfs.key_empresa),
            "status": "Habilitada",
            "prazo": 0,
            "dadosObrigatoriosPreenchidos": "true",
            "cnpj": paramnfs.company.cnpj_cpf,
            "inscricaoMunicipal": paramnfs.company.insc_mun,
            "inscricaoEstadual": paramnfs.company.insc_est,
            "razaoSocial": paramnfs.company.razao,
            "nomeFantasia": paramnfs.company.fantasia,
            "optanteSimplesNacional": simples,
            "email": paramnfs.company.email,
            "telefoneComercial": paramnfs.company.telefone,
            "endereco": {
                "pais": "Brasil",
                "codigoIbgeUf": paramnfs.company.ibge_uf,
                "codigoIbgeCidade": paramnfs.company.ibge_mun,
                "uf": paramnfs.company.uf,
                "cidade": paramnfs.company.cidade,
                "logradouro": paramnfs.company.endereco,
                "numero": paramnfs.company.numero,
                "complemento": paramnfs.company.complemento,
                "bairro": paramnfs.company.bairro,
                "cep": paramnfs.company.cep
            },
            "incentivadorCultural": incentivo,
            "regimeEspecialTributacao": paramnfs.regime_trib,
            "ConfiguracoesNFSeProducao": {
                "sequencialNFe": paramnfs.conf_sequenciaNFE,
                "serieNFe": paramnfs.conf_serieNFE,
                "sequencialLoteNFe": paramnfs.conf_sequencialoteNFe,
                "usuarioAcessoProvedor": paramnfs.conf_usuarioAcesso,
                "senhaAcessoProvedor": paramnfs.conf_senhaUsuarioAcesso,
            },
            "codigoServicoMunicipal": paramnfs.cd_srv_padrao,
            "itemListaServicoLC116": paramnfs.it_lista_srv,
            "cnae": paramnfs.cnae,
            "aliquotaIss": str(paramnfs.aliquota_iss),
            "descricaoServico": paramnfs.desc_srv,
            "enviarEmailCliente": "true"
        }

        resposta = requests.post(
            url,json=data,headers={"Authorization": "Basic"+settings.ENOTASKEY}
        )

        print(resposta)
        print(resposta.text)

        xml = BeautifulSoup(resposta.text,"lxml")


        if resposta.status_code == 200:
            key_emp = xml.find("empresaid").contents[0]
            paramnfs.key_empresa = key_emp
            paramnfs.save()
        if resposta.status_code == 400:
            erromsg = xml.find("mensagem").contents[0]
            erro = ErrosParametrosNFS()
            erro.master_user = paramnfs.master_user
            erro.paramnfs = paramnfs
            erro.mensagem = erromsg
            erro.save()


def edit_empresa_emissora(paramnfs):
    url = settings.ENOTASURL + '/empresas'

    if paramnfs.simples_nac:
        simples = 'true'
    else:
        simples = 'false'

    if paramnfs.incent_cult:
        incentivo = 'true'
    else:
        incentivo = 'false'

    data = {
        "id": str(paramnfs.key_empresa),
        "status": "Habilitada",
        "prazo": 0,
        "dadosObrigatoriosPreenchidos": "true",
        "cnpj": paramnfs.company.cnpj_cpf,
        "inscricaoMunicipal": paramnfs.company.insc_mun,
        "inscricaoEstadual": paramnfs.company.insc_est,
        "razaoSocial": paramnfs.company.razao,
        "nomeFantasia": paramnfs.company.fantasia,
        "optanteSimplesNacional": simples,
        "email": paramnfs.company.email,
        "telefoneComercial": paramnfs.company.telefone,
        "endereco": {
            "pais": "Brasil",
            "codigoIbgeUf": paramnfs.company.ibge_uf,
            "codigoIbgeCidade": paramnfs.company.ibge_mun,
            "uf": paramnfs.company.uf,
            "cidade": paramnfs.company.cidade,
            "logradouro": paramnfs.company.endereco,
            "numero": paramnfs.company.numero,
            "complemento": paramnfs.company.complemento,
            "bairro": paramnfs.company.bairro,
            "cep": paramnfs.company.cep
        },
        "incentivadorCultural": incentivo,
        "regimeEspecialTributacao": paramnfs.regime_trib,
        "ConfiguracoesNFSeProducao": {
            "sequencialNFe": paramnfs.conf_sequenciaNFE,
            "serieNFe": paramnfs.conf_serieNFE,
            "sequencialLoteNFe": paramnfs.conf_sequencialoteNFe,
            "usuarioAcessoProvedor": paramnfs.conf_usuarioAcesso,
            "senhaAcessoProvedor": paramnfs.conf_senhaUsuarioAcesso,
        },
        "codigoServicoMunicipal": paramnfs.cd_srv_padrao,
        "itemListaServicoLC116": paramnfs.it_lista_srv,
        "cnae": paramnfs.cnae,
        "aliquotaIss": str(paramnfs.aliquota_iss),
        "descricaoServico": paramnfs.desc_srv,
        "enviarEmailCliente": "true"
    }

    resposta = requests.post(
        url, json=data, headers={"Authorization": "Basic "+settings.ENOTASKEY}
    )

    print(resposta)
    print(resposta.text)

    xml = BeautifulSoup(resposta.text, "lxml")

    if resposta.status_code != 200:
        erromsg = xml.find("mensagem").contents[0]
        erro = ErrosParametrosNFS()
        erro.master_user = paramnfs.master_user
        erro.paramnfs = paramnfs
        erro.mensagem = erromsg
        erro.save()



def emite_nfse(servico):

        paramnfs = Paramnfs.objects.get(company=servico.company)
        url = settings.ENOTASURL + '/empresas/' + paramnfs.key_empresa + '/nfes'

        cnpj_cpf = servico.cadgeral.cnpj_cpf.replace('.', '')
        cnpj_cpf = cnpj_cpf.replace('-', '')
        cnpj_cpf = cnpj_cpf.replace('/', '')

        if len(cnpj_cpf) < 12:
            tp_pessoa = 'F'
        else:
            tp_pessoa = 'J'

        data = {'cliente':
                    {'tipoPessoa': tp_pessoa,
                     'nome': servico.cadgeral.razao,
                     'email': servico.cadgeral.email,
                     'cpfCnpj': servico.cadgeral.cnpj_cpf,
                     'inscricaoMunicipal': None,
                     'inscricaoEstadual': None,
                     'telefone': servico.cadgeral.telefone,
                     'endereco':
                         {'pais': 'Brasil',
                          'uf': servico.cadgeral.uf,
                          'cidade': servico.cadgeral.cidade,
                          'logradouro': servico.cadgeral.endereco,
                          'numero': servico.cadgeral.numero,
                          'complemento': servico.cadgeral.complemento,
                          'bairro': servico.cadgeral.bairro,
                          'cep': servico.cadgeral.cep
                          },
                     },
                'enviarPorEmail': True,
                'id': None,
                'ambienteEmissao': 'Producao',
                'tipo': 'NFS-e',
                'idExterno': str(servico.pk),
                'consumidorFinal': True,
                'indicadorPresencaConsumidor': None,
                'servico':
                    {'descricao': paramnfs.desc_srv,
                     'aliquotaIss': float(paramnfs.aliquota_iss),
                     'issRetidoFonte': True,
                     'cnae': None,
                     'codigoServicoMunicipio': paramnfs.cd_srv_padrao,
                     'descricaoServicoMunicipio': paramnfs.desc_srv,
                     'itemListaServicoLC116': paramnfs.it_lista_srv,
                     'ufPrestacaoServico': paramnfs.company.uf,
                     'municipioPrestacaoServico': paramnfs.company.uf,
                     'valorCofins': 0,
                     'valorCsll': 0,
                     'valorInss': 0,
                     'valorIr': 0,
                     'valorPis': 0,
                     'observacoes': ''
                     },
                'valorTotal': float(servico.vlr_fat),
                'idExternoSubstituir': None,
                'nfeIdSubstitituir': None
                }

        data2 = json.dumps(data)

        resposta = requests.post(
            url, json=data, headers={"Authorization": "Basic "+settings.ENOTASKEY}
        )

        print(resposta)
        print(resposta.text)

        if resposta.status_code == 200:
            xml = BeautifulSoup(resposta.text, "lxml")
            print(xml)
            key_nfs = xml.find("nfeid").contents[0]

            url = url+'/'+key_nfs

            retorno_emissao = requests.get(
                url,  headers={"Authorization": "Basic " + settings.ENOTASKEY}
            )
            print(retorno_emissao.text)


            xmlret = BeautifulSoup(retorno_emissao.text,"lxml")
            statusret = xmlret.find("status").contents[0]


            nfs = NotasFiscais()
            nfs.master_user = servico.master_user
            nfs.company = servico.company
            nfs.cadgeral = servico.cadgeral
            # nfs.data_emissao = xmlret.find("datacriacao").contents[0]
            nfs.desc_status_nfs = statusret
            if statusret == 'Autorizada':
                nfs.num_nf = xmlret.find("numero").contents[0]
                nfs.link_pdf = xmlret.find("linkdownloadpdf").contents[0]
                nfs.link_xml = xmlret.find("linkdownloadxml").contents[0]
            elif statusret == 'Negada':
                nfs.motivoStatus = xmlret.find("motivostatus").contents[0]
            nfs.save()


        return data