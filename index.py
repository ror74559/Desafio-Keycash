from flask import Flask, render_template,request, make_response
import numpy as np
import os
import joblib
from category_encoders import OneHotEncoder
import locale
from datetime import datetime
from reportlab.pdfgen import canvas

app = Flask(__name__)
model = joblib.load('model/model.pkl')

@app.route('/download')
def download():
	return (url_for('static', filename='consulta.txt'))


@app.route('/')
def index():
    return render_template('index.html',escondido='hidden')
@app.route('/prever',methods=['POST'])
def prever():
	zona = request.form['zona']
	area = request.form['area']
	qualidade = request.form['qualidade']
	anoconstrucao = request.form['anoconstrucao']
	banheiros = request.form['banheiros']
	qualidadeaquecimento = request.form['qualidadeaquacimento']
	comodos = request.form['comodos']
	lareiras = request.form['lareiras']
	garagem = request.form['garagem']
	if anoconstrucao == '':
		anoconstrucao = 1960
	if area == '':
		area = 100
	teste = np.array([[zona,area,qualidade,anoconstrucao,banheiros,qualidadeaquecimento,comodos,lareiras,garagem]])
	valor = model.predict(teste)[0]
	locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
	valor = locale.currency(valor, grouping=True, symbol = False)
	valor = str(valor)
	valor = valor.split(',')
	
	if len(valor) > 1:
		valor[-1] = valor[-1].replace('.',',')
		valor = '.'.join(valor)
	else:
		valor = valor[-1].replace('.',',')
	now = datetime.now()
	consulta = ["Resultado da consulta","O preço de um imóvel com as seguintes características:",
	"Zona: " + str(zona),"Área: "+str(area),"Qualidade: "+str(qualidade),"Ano de construção: "+str(anoconstrucao),
	"Banheiros: "+str(banheiros),"Qualidade do Aquecimento: "+str(qualidadeaquecimento),"Cômodos: "+str(comodos),
	"Lareiras: "+str(lareiras),"Garagem: "+str(garagem),"Será de aproximadamente: R$ "+valor,
	"Consulta efetuada no dia " + now.strftime('%d/%m/%Y %H:%M')]

	cnv = canvas.Canvas("static/consulta.pdf")
	altura = 800
	for elemento in consulta:
		cnv.drawString(10,altura,elemento)
		altura -= 20

	cnv.save()
	
	
	return render_template('index.html', preco="Preço: R$ "+valor,zona ="Zona: " + str(zona),area="Área: "+str(area),
		qualidade="Qualidade: "+str(qualidade), anoconstrucao="Ano de construção: "+str(anoconstrucao),
		banheiros="Banheiros: "+str(banheiros),qualidadeaquecimento="Qualidade do aquecimento: "+str(qualidadeaquecimento),
		comodos="Cômodos: "+str(comodos),lareiras="Lareiras: "+str(lareiras),garagem="Garagem: "+str(garagem),
		Resultado="Resultado",borda="border: solid 1px black", baixar="Baixar consulta", escondido=' ')



if __name__ == '__main__':
	port = int(os.environ.get('PORT',5000))
	app.run(host='0.0.0.0',port=port)
