from __future__ import generators
import sys, re
import wikipedia, pagegenerators, catlib, config
import urllib, time, random, string
 
site=wikipedia.getSite()
while 1:
 
	salida=u"{| style='background-color: #white; font-family:Verdana, Arial, Helvetica, sans-serif; font-size: 100%; border: 0px solid #DCDCDC; text-align: left; padding-left: 7px; -moz-border-radius:10px' \n|- \n| valign='top' align='right' |\n===[[Special:Newpages|Páginas nuevas]]===\n"
	 
	time.sleep(1) # <---- PARA CONTROLAR LA VELOCIDAD
	######################### NUEVAS PÁGINAS ##################################
	wikipedia.output(u"Recibiendo nuevas páginas...")
	 
	gen=pagegenerators.NewpagesPageGenerator(50)
	numpage=0
	for page in gen:
		if numpage >= 12:
		        break
		if not(page.isRedirectPage() or page.isDisambig() or page.namespace()!=0):
		        try:
		                textpage =page.get(force = True)
		        except:
		                textpage =""
		        if (re.search(ur"\=\=*", textpage) and re.search(ur"\*", textpage)):
		                salida+=u"[[%s]] \n" %page.title()
		                numpage+=1
		        else:
		                print (('[[%s]] es un esbozo.' %page.title()).encode('utf-8'))
	 
	salida+=u"[[%s]] \n" %page.title()
	 
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	########################### PERSONAS #######################################
	cat=catlib.Category(wikipedia.Site("es", "wikiquote"), u"Category:Personas")
	 
	l2=[]
	l=cat.articles()
	 
	for j in l:
		l2.append(j.title())
	length=len(l2)
	 
	salida+=u'|- \n| valign="top" align="right" | \n\n===[[:Categoría:Personas|Gente]]=== \n\n'
	j=0
	pag=random.sample(l2,22)
	pag.sort()
	while j<= 20:
		salida+=u"[[%s]] —\n" %(pag[j])
		j+=1
	 
	salida+=u'[[%s]]\n|- \n| valign="top" align="right" | \n\n===[[:Categoría:Obras literarias|Obras literarias]]===\n\n' %(pag[j])
	 
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	############################### Obras literarias ###################################
	 
	cat=catlib.Category(wikipedia.Site("es", "wikiquote"), u"Category:Obras literarias")
	 
	l2=[]
	l=cat.articles()
	 
	for j in l:
		l2.append(j.title())
	length=len(l2)
	 
	j = 0
	pag=random.sample(l2,12)
	pag.sort()
	while j<= 10:
		jpage=wikipedia.Page(site,pag[j])
		if not(jpage.isRedirectPage() or jpage.isDisambig() or jpage.namespace()!=0):
		        salida+=u"''[[%s]]'' —\n" %pag[j]
		j+=1
	 
	salida+=u"''[[%s]]''" %(pag[j])
	salida+=u'\n|- \n| valign="top" align="right" | \n\n===[[:Categoría:Historietas|Historietas (cómic)]]===\n\n'
	 
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	############################### HISTORIETAS ###################################
	 
	cat=catlib.Category(wikipedia.Site("es", "wikiquote"), u"Category:Historietas")
	 
	l2=[]
	l=cat.articles()
	 
	for j in l:
		l2.append(j.title())
	length=len(l2)
	 
	j = 0
	pag=random.sample(l2,12)
	pag.sort()
	while j<= 10:
		jpage=wikipedia.Page(site,pag[j])
		if not(jpage.isRedirectPage() or jpage.isDisambig() or jpage.namespace()!=0):
		        salida+=u"''[[%s]]'' —\n" %pag[j]
		j+=1
	 
	 
	salida+=u"''[[%s]]''" %(pag[j])
	salida+=u'\n|- \n| valign="top" align="right" | \n\n===[[:Categoría:Ocupaciones|Ocupaciones]]===\n\n'
	 
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	############################### OCUPACIONES ###################################
	 
	cat=catlib.Category(wikipedia.Site("es", "wikiquote"), u"Category:Ocupaciones")
	l=cat.subcategories()
	l2=[]
	 
	for j in l:
		l2.append(j.title())
	length=len(l2)
	 
	j = 0
	pag=random.sample(l2,12)
	pag.sort()
	while j<= 10:
		nombre=re.sub(ur"Categoría\:(.*?)", ur"\1", pag[j])
		salida+=u"[[:%s|%s]] —\n" %(pag[j], nombre)
		j+=1
	 
	nombre=re.sub(ur"Categoría\:(.*?)", ur"\1", pag[j])
	salida+=u"[[:%s|%s]] " %(pag[j], nombre)
	salida+=u'\n|- \n| valign="top" align="right" | \n\n===[[:Categoría:Proverbios|Proverbios]]===\n\n'
	 
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	############################### PROvERbIOS ###################################
	 
	cat=catlib.Category(wikipedia.Site("es", "wikiquote"), u"Category:Proverbios")
	 
	l2=[]
	l=cat.articles()
	 
	for j in l:
		jtitule=j.title()
		if (re.search(ur"Proverbios",jtitule)):
		        l2.append(jtitule)
	length=len(l2)
	 
	j = 0
	pag=random.sample(l2,11)
	pag.append(u"Proverbios españoles")
	pag.sort()
	while j<= 10:
		nombre=re.sub(ur"Proverbios (.*?)", ur"\1", pag[j])
		salida+=u"[[%s|%s]] —\n" %(pag[j], string.capitalize(nombre))
		j+=1
	 
	nombre=re.sub(ur"Proverbios (.*?)", ur"\1", pag[j])
	salida+=ur"[[%s|%s]] " %(pag[j], string.capitalize(nombre))
	salida+=u'\n|- \n| valign="top" align="right" | \n\n===[[:Categoría:Películas|Películas]]===\n\n'
	 
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	############################### PELÏCULAS ###################################
	 
	cat=catlib.Category(wikipedia.Site("es", "wikiquote"), u"Category:Películas")
	 
	l2=[]
	l=cat.articles()
	 
	for j in l:
		l2.append(j.title())
	length=len(l2)
	 
	j = 0
	pag=random.sample(l2,12)
	pag.sort()
	while j<= 10:
		jpage=wikipedia.Page(site,pag[j])
		if not(jpage.isRedirectPage() or jpage.isDisambig() or jpage.namespace()!=0):
		        salida+=u"''[[%s]]'' —\n" %pag[j]
		j+=1
	 
	salida+=u"''[[%s]]''" %pag[j]
	salida+=u'\n|- \n| valign="top" align="right" | \n\n===[[:Categoría:Programas de televisión|Programas de televisión]]===\n\n'
	pag.sort()
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	############################### TV  ###################################
	 
	cat=catlib.Category(wikipedia.Site("es", "wikiquote"), u"Category:Programas de televisión")
	 
	l2=[]
	l=cat.articles()
	 
	for j in l:
		l2.append(j.title())
	length=len(l2)
	 
	j = 0
	pag=random.sample(l2,12)
	pag.sort()
	while j<= 10:
		jpage=wikipedia.Page(site,pag[j])
		if not(jpage.isRedirectPage() or jpage.isDisambig() or jpage.namespace()!=0):
		        salida+=u"''[[%s]]'' —\n" %pag[j]
		j+=1
	 
	 
	salida+=u"''[[%s]]''" %pag[j]
	salida+=u'\n|- \n| valign="top" align="right" | \n\n===[[:Categoría:Temas|Temas]]===\n\n'
	 
	time.sleep(20) # <---- PARA CONTROLAR LA VELOCIDAD
	############################### TEMAS ###################################
	 
	l2=[]
	categorias= catlib.Category(wikipedia.getSite(), 'Category:Temas')
	l=categorias.articles()
	for j in l:
		l2.append(j.title())      
	 
	categorias=categorias.subcategories()
	for cat in categorias:
		l=cat.articles()
		for j in l:
		        l2.append(j.title())      
	length=len(l2)
	 
	j = 0
	pag=random.sample(l2,20)
	pag.sort()
	while j<= 18:
		jpage=wikipedia.Page(site,pag[j])
		if not(jpage.isRedirectPage() or jpage.isDisambig() or jpage.namespace()!=0):
		        salida+=u"[[%s]] — \n" %pag[j]
		j+=1
	 
	salida+=u"[[%s]] \n" %pag[j]
	 
	salida+=u'|- \n| valign="top" align="right" |\n\n===[[:Categoría:Géneros|Géneros]]===\n\n[[Aforismo]]s —\n[[Epitafios]] —\n[[Eslóganes]] —\n[[Eslóganes institucionales]] —\n[[Eslóganes políticos]] —\n[[Lipogramas]] —\n[[Hipérbole]]s —\n[[Greguerías]] —\n[[Kenningar]] —\n[[Lemas de España]] —\n[[Mnemónicos]] —\n[[Oráculos]] —\n[[Palíndromos]] —\n[[Pangramas]] —\n[[Trabalenguas]]\n|- \n| valign="top" align="right" |\n\n===[[:Categoría:Miscelánea|Miscelánea]]===\n\n<!-- [[Favoritos]] -->\n[[Anónimo]] — \n[[Citas incorrectas]] —\n[[Flickr|Citas de portada de Flickr]] —\n[[Mnemónicos]] —\n[[Murphy]] —\n[[Pregunta del millón]] —\n[[Regla de Oro]] —\n[[Últimas palabras famosas|Últimas palabras]] —\n[[Citas de usuarios]] —\n[[Special:Newpages|<i>Más...</i>]]\n|}\n'
	 
	wikipedia.output(u"Escribiendo: %s" %salida)            
	wiii = wikipedia.Page(wikipedia.Site("es", "wikiquote"), u"Plantilla:PortadaPáginas")
	wiii.put(u"%s" % salida, u"BOT: Actualización automatica de plantilla ")
	wikipedia.output(u"Escrita aculizacion")
	time.sleep(86300) # <---- 1 dia

