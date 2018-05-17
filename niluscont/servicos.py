from niluscad.models import Cadgeral



def lista_contratoeos(contratos,ordemservico):

    lista=[]


    if contratos:
        for c in contratos:



            lista.append({"id": 'c%s' % (str(c.pk)),"num":c.num_cont,"tipo":'c',"cliente":c.cadgeral,"servico":c.item,
                          "pfat":c.prox_faturamento,"valor":c.valor})

    if ordemservico:
        for o in ordemservico:
            lista.append({"id": 'o%s' %(str(o.pk)),"num":o.num_os,"tipo":'o',"cliente":o.cadgeral,"servico":o.desc_item,
                          "pfat":o.data_os,"valor":o.valor_unit})

    return(lista)