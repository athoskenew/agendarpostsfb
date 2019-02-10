#coding: utf-8
import facebook
from datetime import datetime
def validar_data(mes,dia_final):
    security_token = 1
    if(mes==1 and dia_final>31):
        print("data invalida")
        security_token = 0
    elif(mes==2 and dia_final>28):
        print("data invalida")
        security_token = 0
    elif(mes==3 and dia_final>31):
        print("data invalida")
        security_token = 0
    elif(mes==4 and dia_final>30):
        print("data invalida")
        security_token = 0
    elif(mes==5 and dia_final>31):
        print("data invalida")
        security_token = 0
    elif(mes==6 and dia_final>30):
        print("data invalida")
        security_token = 0
    elif(mes==7 and dia_final>31):
        print("data invalida")
        security_token = 0
    elif(mes==8 and dia_final>31):
        print("data invalida")
        security_token = 0
    elif(mes==9 and dia_final>30):
        print("data invalida")
        security_token = 0
    elif(mes==10 and dia_final>31):
        print("data invalida")
        security_token = 0
    elif(mes==11 and dia_final>30):
        print("data invalida")
        security_token = 0
    elif(mes==12 and dia_final>31):
        print("data invalida")
        security_token = 0
    return security_token
#deprecated
def varios_posts(dia,mes,dia_final,qtd_posts):
    valid_data = validar_data(mes,dia_final)
    if(valid_data==1):
        for a in range(dia,(dia_final+1)):
            print("dia:",a)
            
    for post in range((qtd_posts+1)):
        print("postagem:",post)

def pegar_imagem(nome):
    nome_img = ""
    try:
        open(nome,'rb')
    except:
        try:
            open(nome+".jpg",'rb')
            nome_img = nome+".jpg"
        except:
            try:
                open(nome+".png",'rb')
                nome_img = nome+".png"
            except:
                try:
                    open(nome+".gif",'rb')
                    nome_img = nome+".gif"
                except:
                    nome_img = "Erro!"
    
    return nome_img

#retorna uma lista com horarios predefinidos
def horarios_predefinidos(predef):
    #14 posts
    horarios_uma = [[9,0],[10,0],[11,0],[12,0],[13,0],[14,0],[15,0],[16,0],[17,0],[18,0],[19,0],[20,0],[21,0],[22,0]]
    #8 posts
    horarios_duas = [[8,0],[10,0],[12,0],[14,0],[16,0],[18,0],[20,0],[22,0]]
    #5 posts
    horarios_tres = [[9,0],[12,0],[15,0],[18,0],[21,0]]
    if(predef==1):
        return horarios_uma
    elif(predef==2):
        return horarios_duas
    elif(predef==3):
        return horarios_tres

def conversor_timestamp(dia,mes,ano,hora,minuto):
    valuedata = datetime(ano,mes,dia,hora,minuto,tzinfo=None)
    timestmp = valuedata.timestamp()
    return int(timestmp)

#função pra agendar vendo o número de imagens e o número de dias que irá precisar pra essas imagens
#agora os dias não vão ser mais escolhidos pela pessoa, apenas o dia inicial, os dias seguintes serão de acordo
#com o número de posts
#a dinamica do dia extra é que ele só será ativado caso reste posts e assim um for extra será lançado com os posts restantes
#usando o última dia que foi agendado para saber que dia será o dia extra
def dias_post(dya,mes,ano,token,predef,legenda,posts_feitos,graph):
    predefinidos = horarios_predefinidos(predef)
    finalday = 0 #será usado caso precise agendar em um dia extra
    finaldaylock = 0
    actual_post = 0
    #receber a graph api como argumentos tbm
    if (posts_feitos<=len(predefinidos)):
        #se for menor ou igual a quantidade de posts predefinidos, apenas irá liberar o padlock e ajustar o dea como sendo 1 (apenas 1 dia de posts)
        #fazer uma verificação para saber quantos posts tem pra ver se precisa diminuir do total escolhido nos predefinidos
        #como é só um dia, não precisa de laço pros dias
        for post in range(posts_feitos):
            foto_up = pegar_imagem(str(post+1)) #0
            datapost = conversor_timestamp(dya, mes, ano, predefinidos[post][0],predefinidos[post][1])
            #graph.put_photo(image=open(foto_up,'rb'),published="false",scheduled_publish_time=datapost,message=legenda)
            print("post:",post)
            print("Token:",token)
            print("imagem:",foto_up)
            print("data:",datapost)
            print("Legenda:",legenda)
        pass
    #Instrução caso a quantidade de posts seja maior que o número de posts predefinidos, irá verificar quantos dias irá precisar e qual
    #vai ser a dinâmica do dia extra
    elif(posts_feitos>len(predefinidos)):
        #se for maior que a quantidade de posts predefinidos, irá ver a quantidade de dias necessários e agendar
        posts_sobram = (posts_feitos%len(predefinidos)) #1
        print("posts que sobram",posts_sobram)
        qtd_feita = (posts_feitos-posts_sobram) #8
        print("qtdfeita",qtd_feita)
        #qtd_feita será o numero de posts que irá ditar o número de dias, os posts_sobram irão pra um dia extra com o número de posts restantes
        dias_de_agendamento = int(qtd_feita/len(predefinidos)) #1 #dias que serão agendados, de acordo com a quantidade de posts
        print("dias de agendamento",dias_de_agendamento)
        #dia extra sempre será igual 1 (por que só irá pegar os posts se sobrarem
        #verificar erro de data
        finalday += dias_de_agendamento+dya #1+8+1 = dia 10 #dia extra será o n de dias agendados+dia inicial +1
        print("dia final:",finalday)
        finaldaylock+=1 #ativa o dia extra
        #iniciando o laço para agendar os dias completos
        dia = dya
        print("Dya:",dya)
        for dhia in range(dya,(dya+dias_de_agendamento)):
            print()
            print("Dhia:",dhia)
            for post in range(len(predefinidos)):
                foto_up = pegar_imagem(str(actual_post+1)) #0
                datapost = conversor_timestamp(dia, mes, ano, predefinidos[post][0],predefinidos[post][1])
                actual_post+=1
                #graph.put_photo(image=open(foto_up,'rb'),published="false",scheduled_publish_time=datapost,message=legenda)
                print("post:",post)
                print("Token:",token)
                print("imagem:",foto_up)
                print("actual_post:",actual_post)
                print("data:",datapost)
                print("Legenda:",legenda)
            dia+=1
        if(finaldaylock==1):
            print()
            print("Dia extra")
            for post in range(posts_sobram):
                foto_up = pegar_imagem(str(actual_post+1)) #0
                datapost = conversor_timestamp(finalday, mes, ano, predefinidos[post][0],predefinidos[post][1])
                actual_post+=1
                #graph.put_photo(image=open(foto_up,'rb'),published="false",scheduled_publish_time=datapost,message=legenda)
                print("post:",post)
                print("Token:",token)
                print("imagem:",foto_up)
                print("data:",datapost)
                print("actual_post:",actual_post)
                print("Legenda:",legenda)
    pass
    
def agendamento_massivo(dia,mes,ano,token,predef,legenda,posts_feitos):
    graph = ""#facebook.GraphAPI(token)
    dias_post(dia, mes, ano, token, predef, legenda, posts_feitos, graph)
    
    
tak = "a"
agendamento_massivo(11, 2, 2019, tak, 2,"",23)