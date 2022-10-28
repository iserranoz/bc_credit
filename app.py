import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def pivot_table_level1(data, index, columns = 'CLIENT_TYPE', aggfunc = 'count'):
    data = data.pivot_table(index = index, columns = columns, values = 'ID', aggfunc = aggfunc)
    data = pd.DataFrame(data)
    data.columns = data.columns.to_flat_index()
    data = data.reset_index()
    data = data.rename_axis(None, axis=1)
    return data

st.set_page_config(page_title='Business case')


nav = st.sidebar.selectbox("Menu",['Introducción','Tratamiento de los datos y KPIs', 'Análisis descriptivo'])

if nav == 'Introducción':

	
	
	
	st.subheader('Caso Práctico: Solicitudes de Tarjetas de Crédito')
	col1 , col2, col3 = st.columns([3,1,1])
	col1.markdown('Iván Serrano Zapata')
	col2.image('images/python.png',width = 50, use_column_width = False)
	col3.image('images/st.png',width = 80, use_column_width = False)
	col1.subheader('')
	
	

	with st.expander("Estructura"):
	    	st.write("""
        	La estructura del dashboard se compone de las siguientes secciones:

        	1. Introducción

        	   Presentar la estructura de la aplicación, los requerimientos del caso y una breve descripción de los datos

        	2. Tratamiento de los datos y KPIs

        	   Mostrar las transformaciones que se generaron para obtener la información requerida y plantear los KPIs, esto solo será una breve explicacion, el notebook conmpleto se deja en el [repositorio](https://github.com/iserranoz/bc_credit)

        	3. Análisis descriptivo

        	   En esta sección exploramos a nivel gráfico y estadístico el comportamiento de las variables application_record para generar algunas recomendaciones.

        	""")


    
	with st.expander("Requerimientos"):
	    	st.write("""
        	

        	1. Definir y calcular KPIs de número de créditos "buenos" y "malos" justificando la importancia de uso

        	   

        	2. Calcular el KPI por mes para los meses que sea posible calcularlos

        	  

        	3. Explicar las características de los clientes “buenos” y “malos”

        	   

        	4. Recomendaciones sobre a qué clientes buscar atraer más

        	
        	""")


	with st.expander('Descripción de los datos'):

		st.markdown('Los datasets contienen, por un lado, información de clientes que solicitan créditos y por otro el historial de pagos')
		st.info('Dataset application record')
		st.table(pd.read_csv('data/variables_application_record.csv'))
		st.info('Dataset credit record')
		st.table(pd.read_csv('data/variables_credit_record.csv'))

    
if nav == 'Tratamiento de los datos y KPIs':

	credit_record = pd.read_csv('data/credit_record.csv')
	tabla_1 = pd.read_csv('data/tabla_1.csv',index_col=0)
	tabla_2 = pd.read_csv('data/tabla_2.csv',index_col=0)
	tabla_3 = pd.read_csv('data/tabla_3.csv',index_col=0)
	tabla_1.COUNT_MONTHS = tabla_1.COUNT_MONTHS.astype(int)

	st.subheader('Tratamiento de los datos y KPIs')
	st.subheader('')
	st.info('Clasificación de créditos a nivel ID (CLIENTE)')
	st.subheader('')
	st.markdown('Dentro del dataset **credit_record** se encontraban los registros de pagos por mes de los clientes, decidimos agrupar por cliente para observar como había sido su comportamiento a lo largo de la vida del crédito.')
	st.write(tabla_1.iloc[:,:12].head(10))
	st.markdown('Esta tabla nos permite tener la información de cuantos estatus diferentes ha tenido un cliente en los meses en los que ha tenido el crédito activo, cual es el último estatus del que se tiene registro, el último mes del que se tiene registro y también cuantos meses estuvo activo el crédito, no se tomaron en cuenta los estatus X para el último cálculo y se descartaron clientes que solo tuvieron registros en X, ya que nunca tuvieron un crédito.')
	st.markdown('Generamos un describe de los datos para cuando el last_status (último registro activo) es C (liquidado ese mes) y observamos lo siguiente.')
	st.write(tabla_1.loc[tabla_1.LAST_STATUS=='C', ['0','1','2','3','4','5','C']].describe())
	st.markdown('Como se observa, de los ID en el que su último estatus está como C, tenemos registro de varios retardos en meses anteriores, en su mayoría retrasos menores a 30 días, en promedio, los clientes que pagaron su último mes se han atrasado en 8 ocasiones en sus pagos. En menor proporción hay casos donde los clientes tienen demoras más grandes. Esto nos permite saber que, aunque el cliente haya pagado en el mes mas reciente, puede tener atrasos de otros meses, incluso meses marcados como deuda incobrable, por ejemplo el ID 5079166 que muestro a continuación el cual tiene varios pagos pero igual varios meses de atraso y deuda incobrable.')
	st.write(credit_record.loc[credit_record.ID==5079166,: ])
	st.subheader('')
	st.write("""
        	Habiendo explorado los datos pasamos a generar una clasificación con base en los siguientes criterios:

        	1. **AA**: Aquellos que tengan todos sus pagos en C

        	   

        	2. **BB**: Aquellos que presenten más del 20% de sus pagos(C) versus algun tipo de mora (0,1,2,3,4) y que no tengan status de deuda incobrable (5)

        	  

        	3. **CC**: Aquellos que presenten menos o 20% de sus pagos (C) versus algun tipo de mora (0,1,2,3,4) y que no tengan status de deuda incobrable (5)

        	   

        	4. **DD**: Aquellos que presenten menos del 50% de sus pagos en deuda incobrable (5) versus pagados (C)

        	
        	5. **EE**: Aquellos que presenten más o  50% de sus pagos en deuda incobrable (5) versus pagados (C) """)

	st.write(tabla_1.loc[:, ['0','1','2','3','4','5','C', 'C_RATING']].head(10))
	st.markdown('La distribución de la clasificación queda de la siguiente forma')
	perc = pd.DataFrame(100*(tabla_1['C_RATING'].value_counts()/tabla_1.shape[0]))
	values = pd.DataFrame(tabla_1.C_RATING.value_counts())
	merge_1 = values.merge(perc, left_index=True, right_index=True, how = 'left', suffixes=('_values', '_%'))
	st.write(merge_1)
	st.write('Como podemos observar la mayor parte de los clientes se concentra en clasificaciones **BB** y **CC** que son clientes con retrasos, un pequeño porcentaje nunca ha presentado atrasos en sus pagos y un menor porcentaje presenta deuda incobrables.')
	st.write('Como conclusión de esta parte, observamos que en general no tenemos muchos clientes que presentan deuudas incobrables, pero, tenemos un porcentaje muy grande de clientes que tienen pagos demorados, por lo que habría que prestar especial atención a esto')
	st.subheader('')
	st.info('Cálculo de KPI por mes')
	st.subheader('')
	st.write('Para esta parte igual generamos una clasificación en base a algunos criterios que nos permitan reducir la dimensión de etiquetas y agrupar de mejor manera los datos, a diferencia del anterior, el nivel de agrupación es sobre el mes.')
	st.write("""
        	Criterios (Se escluyen estatus en X ya que ese mes no hubo préstamo):

        	1. **PAID**: Si el estatus está C

        	   

        	2. **LOW_DELAY**: Si el estatus está en (0,1)

        	  

        	3. **HIGH_DELAY**: Si el estatus está en (2,3,4)

        	   

        	4. **OVERDUE**: Si el estatus está en 5 """)

	
	perc_2 = pd.DataFrame(100*(tabla_2['C_RATING_MONTH'].value_counts()/tabla_2.shape[0]))
	values_2 = pd.DataFrame(tabla_2.C_RATING_MONTH.value_counts())
	merge_2 = values_2.merge(perc_2, left_index=True, right_index=True, how = 'left', suffixes=('_values', '_%'))
	st.subheader('')
	st.markdown('Aquí observamos que la mayoría de los estatus se encuentran en C, lo que significa fueron pagados, otro gran porcentaje se encuentra en LOW_DELAY, en menor grado vemos a HIGH_DELAY y OVERDUE. Como observación, existen algunos casos en donde el estatus es 0 y el MONTHS_BALANCE era -3 por lo que en teoría ya tendría más de 30 días de retraso')
	st.write(merge_2)
	st.markdown('Agrupando por MONTHS_BALANCE tenemos lo siguiente para los últimos 12 meses:')
	st.table(tabla_3.tail(12))
	st.write('De esta información se puede ver que en los últimos meses ha aumentado el procentaje de estatus PAID (C) en casi un 7%, esto tiene su contraparte en la disminución del estatus LOW_DELAY lo cual indica que se están presentando menos casos de mora leve')


if nav == 'Análisis descriptivo':

	st.subheader('Análisis descriptivo')

	st.markdown('En esta parte nos centraremos en atender el punto **"Explicar las características de los clientes buenos y malos"** y posterior **dar recomendaciones sobre a qué clientes buscar atraer más**. En mi opinión, sobre todo en estos modelos de negocio, raras veces puedes generar una clasificación con una dicotomía tan marcada, en la mayoría de los casos se operan sobre áreas, cuando menos grises. ')
	st.markdown('Mencionado lo anterior, en pro de atender el requerimiento, tomaremos dos grupos de la clasificación que generamos anteriormente, el grupo AA que serán los "buenos", y los grupos DD y EE que serán los "malos". Esto nos permitira apreciar diferencias, seguramente mas marcadas, recordemos que el grupo AA son clientes que tienen todos sus pagos al corriente, y el DD y EE son grupos que tienen deudas incobrables.')
	st.markdown('Si tuvieramos más datos, como, monto del crédito, monto de los pagos, saldo del crédito o interes cubiertos, podríamos generar una clasificación más precisa en cuanto a clientes que tienen comportamientos mezclados entre pagos demorados y no demorados, al final, que un cliente se demore en un pago o dos, no creo sea criterio suficiente para etiquetarlo. ')

	df_rating = pd.read_csv('data/rating_f.csv', index_col = 0)
	df_rating_all = pd.read_csv('data/rating_all.csv', index_col = 0)
	data_occup = pivot_table_level1(df_rating_all,'OCCUPATION_TYPE')
	data_occup = data_occup.rename(columns={'UNDEFINED':'OTHER'})
	data_occup.fillna(value=0, inplace = True)
	data_occup['TOTAL'] = data_occup.BAD + data_occup.GOOD + data_occup['OTHER']
	data_occup['BAD-TOTAL_%'] = np.round(100*data_occup['BAD']/np.sum(data_occup['BAD']),2)
	data_occup['GOOD-TOTAL_%'] = np.round(100*data_occup['GOOD']/np.sum(data_occup['GOOD']),2)
	data_occup['TOTAL_%'] = np.round(100*data_occup['TOTAL']/np.sum(data_occup['TOTAL']),2)
	

	data_group_1 = pivot_table_level1(df_rating,'NAME_FAMILY_STATUS')

	fig,ax = plt.subplots()
	ax.bar(data_group_1.NAME_FAMILY_STATUS, data_group_1.BAD, width = 0.35, label = 'BAD', color = 'blue')
	ax.bar(data_group_1.NAME_FAMILY_STATUS, data_group_1.GOOD, bottom = data_group_1.BAD, label = 'GOOD',width = 0.35 , color = 'skyblue')
	ax.set_ylabel('Número de clientes')
	ax.set_title('NAME_FAMILY_STATUS')
	ax.legend()

	fig1,ax1 = plt.subplots()
	sns.boxplot(data=df_rating,  x='AMT_INCOME_TOTAL', y='CLIENT_TYPE')
	ax1.set_ylabel('Tipo de cliente')
	ax1.set_title('Monto total de ingresos')

	fig2,ax2 = plt.subplots()
	sns.boxplot(data=df_rating,  x='AGE', y='CLIENT_TYPE')
	ax2.set_ylabel('Tipo de cliente')
	ax2.set_title('Monto total de ingresos')


	st.subheader('')

	st.info('AMT_INCOME_TOTAL')
	
	st.pyplot(fig1)
	st.markdown('Explorando la distribución de ingresos totales no notamos diferencia en los dos grupos, de hecho ambas distribuciones luce casi idéntica, por lo que no podemos tomar ningún tipo de conjetura a partir de esta variable. La distribución de los otros grupos también se comporta muy similiar.')
	st.subheader('')
	st.info('NAME_FAMILY_STATUS')
	st.pyplot(fig)
	st.markdown(f'Est variables considero si nos aporta un buen punto de información, observamos que predomina married para la clase de buenos la cual representa sin embargo, esto se debe a que la clase married predomina en general en todas las aplicaciones. Esto puede deberse a dos cosas, la primera, la edad de la población en cuestión, la cual tiene un promedio {np.round(np.mean(df_rating_all.AGE),2)} esto nos indica que es común estar casado, y como segunda razón, podría ser, que se asocia con un patron de estabilidad en la vida de la persona, lo cual es más propenso a ser aprobado.')
	st.subheader('')
	st.info('AGE')
	st.markdown('Para esta parte usamos la variable de DAYS_BIRTH para sacar la edad de las personas')
	st.pyplot(fig2)
	st.markdown('Se observan distribuciones similares entre ambos grupos,  de igual manera se comporta la distribución de todas las aplicaciones en donde el grueso se ubica entre 35 y 50 años, lo que nos hace pensar en que la estrategia es de tipo conservadora, buscando a personas que se encuentren en edades laboralmente activas.')

	st.markdown('De esto surge un posible diferenciador que podría ser interesante, por que no buscar atacar segmentos de edades más jóvenes, sabemos que es común que la industría de préstamos siga este patrón, colocar créditos a personas en una etapa de madures mediana, por lo que existe un posible nicho de mercado desatendido.')
	st.subheader('')
	st.info('OCCUPATION_TYPE')
	st.markdown('En esta tabla agrupamos por tipo de ocupación para observar algun tipo de patrón')
	st.table(data_occup)
	st.markdown('De esto podemos observar que sí existen algunos tipos de trabajo que pueden presentar un riesgo más alto, Private service staff, Realty agents y HR staff, ya que casi no participan dentro del grupo de clientes "BUENOS". También se observa claramente que el porcentaje de aplicaciones está altamente cargado en Laborers, Core staff, Managers y Sales Staff. Esto podría confirmar que la estrategia de asignación sigue un patrón tradicional, conservador y de bajo riesgo.')

	st.subheader('Conclusiones')
	st.markdown('En el notebook se hizo una exploración más extensa de los datos, pero en su mayoría pueden ser un poco redundantes para esta pequeña presentación, es por eso que decidi tomar los que consideré más importantes.')
	st.write("""
        	Me gustaría resltar algunos puntos importantes que se derivaron del análisis:

        	1. Existe una gran cantidad de clientes que demoran sus pagos, considero que esto debería atenderse y encontrar las causas. ¿Es un problema operativo? ¿Es un problema con el equipo de cobranzas? ¿Son errores en la captura de los datos?  Sin embargo, con los datos que contamos, es imposible profundizar en esto.

        	   

        	2. Con base en la clasificación que planteamos no se encontraron patrones o evidencias consistentes que nos apoyen a diferenciar y poder explicar comportamientos significativos entre los grupos de clientes, esto se pude deber a algún sesgo al momento de plantear la clasificación, falta de datos para profundizar o que los comportamientos son muy similares y no contamos con las variables explicativas necesarias.

        	  

        	3. **HIGH_DELAY**: Si el estatus está en (2,3,4)

        	   

        	4. **OVERDUE**: Si el estatus está en 5 """)











